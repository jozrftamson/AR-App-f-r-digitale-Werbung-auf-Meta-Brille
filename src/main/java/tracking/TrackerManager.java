package tracking;

import model.BrandDetection;
import org.bytedeco.opencv.opencv_core.Rect2d;
import org.bytedeco.opencv.opencv_core.Mat;
import org.bytedeco.opencv.opencv_tracking.TrackerCSRT;

import java.util.*;

/**
 * Manages multiple OpenCV trackers, one per detected object.
 *
 * Matching strategy:
 *  - For every new detection, compute IoU against existing tracker bboxes.
 *  - If IoU > threshold (e.g. 0.3) and label matches, assign detection to that tracker.
 *  - Otherwise create a new tracker.
 *
 * Tracker lifecycle:
 *  - If a tracker fails to update or has no matching detection for N frames, increment miss counter.
 *  - Remove trackers with missCount > maxMisses.
 */
public class TrackerManager {

    private static class TrackedObject {
        TrackerCSRT tracker;
        BrandDetection lastDetection;
        int missCount = 0;
    }

    private final Map<String, TrackedObject> trackers = new LinkedHashMap<>();
    private int nextId = 1;
    private final double iouThreshold = 0.3;
    private final int maxMisses = 5;

    public synchronized void update(List<BrandDetection> detections, Mat frame) {
        // First, update existing trackers with current frame
        List<String> toRemove = new ArrayList<>();
        for (Map.Entry<String, TrackedObject> e : trackers.entrySet()) {
            TrackedObject t = e.getValue();
            Rect2d rect = new Rect2d();
            boolean ok = t.tracker.update(frame, rect);
            if (ok) {
                // update last detection bbox
                t.lastDetection = new BrandDetection(t.lastDetection.getLabel(), t.lastDetection.getConfidence(), rect.x(), rect.y(), rect.width(), rect.height());
                t.lastDetection.setId(e.getKey());
                t.missCount = 0;
            } else {
                t.missCount++;
                if (t.missCount > maxMisses) toRemove.add(e.getKey());
            }
        }

        // Remove dead trackers
        for (String id : toRemove) trackers.remove(id);

        // Now match detections to existing trackers
        Set<BrandDetection> unmatchedDetections = new HashSet<>(detections);

        for (BrandDetection det : new ArrayList<>(detections)) {
            String bestId = null;
            double bestIou = iouThreshold;
            for (Map.Entry<String, TrackedObject> e : trackers.entrySet()) {
                BrandDetection ld = e.getValue().lastDetection;
                if (!ld.getLabel().equals(det.getLabel())) continue; // require same label for matching
                double iou = computeIoU(ld, det);
                if (iou > bestIou) {
                    bestIou = iou;
                    bestId = e.getKey();
                }
            }
            if (bestId != null) {
                // assign detection to tracker: re-init tracker for new bbox (optional)
                TrackedObject t = trackers.get(bestId);
                // re-init tracker for robustness
                t.tracker = createTrackerAndInit(frame, det);
                det.setId(bestId);
                t.lastDetection = det;
                t.missCount = 0;
                unmatchedDetections.remove(det);
            }
        }

        // Create trackers for unmatched detections
        for (BrandDetection det : unmatchedDetections) {
            String id = "Brand-" + (nextId++);
            TrackerCSRT tr = createTrackerAndInit(frame, det);
            TrackedObject to = new TrackedObject();
            to.tracker = tr;
            det.setId(id);
            to.lastDetection = det;
            trackers.put(id, to);
        }
    }

    private TrackerCSRT createTrackerAndInit(Mat frame, BrandDetection det) {
        TrackerCSRT tracker = TrackerCSRT.create();
        Rect2d r = det.toRect2d();
        tracker.init(frame, r);
        return tracker;
    }

    private double computeIoU(BrandDetection a, BrandDetection b) {
        double x1 = Math.max(a.getX(), b.getX());
        double y1 = Math.max(a.getY(), b.getY());
        double x2 = Math.min(a.getX() + a.getWidth(), b.getX() + b.getWidth());
        double y2 = Math.min(a.getY() + a.getHeight(), b.getY() + b.getHeight());
        double w = Math.max(0, x2 - x1);
        double h = Math.max(0, y2 - y1);
        double inter = w * h;
        double union = a.getWidth() * a.getHeight() + b.getWidth() * b.getHeight() - inter;
        return union <= 0 ? 0 : inter / union;
    }

    public synchronized Collection<BrandDetection> getTrackedObjects() {
        List<BrandDetection> out = new ArrayList<>();
        for (Map.Entry<String, TrackedObject> e : trackers.entrySet()) {
            BrandDetection bd = e.getValue().lastDetection;
            bd.setId(e.getKey());
            out.add(bd);
        }
        return out;
    }
}

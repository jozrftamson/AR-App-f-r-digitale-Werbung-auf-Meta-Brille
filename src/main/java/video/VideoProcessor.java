package video;

import detection.LogoDetector;
import model.BrandDetection;
import org.bytedeco.opencv.opencv_core.Mat;
import org.bytedeco.opencv.global.opencv_imgproc;
import org.bytedeco.opencv.global.opencv_highgui;
import org.bytedeco.opencv.global.opencv_core;
import org.bytedeco.opencv.opencv_core.Scalar;
import org.bytedeco.opencv.opencv_videoio.VideoCapture;
import tracking.TrackerManager;

import java.util.List;

/**
 * Video processing loop: open VideoCapture, detect logos, update trackers and draw results.
 */
public class VideoProcessor {

    private final LogoDetector detector = new LogoDetector();
    private final TrackerManager trackerManager = new TrackerManager();

    /**
     * Process input which can be a file path or an integer camera index (e.g. "0").
     */
    public void run(String input) {
        VideoCapture cap;
        try {
            int camId = Integer.parseInt(input);
            cap = new VideoCapture(camId);
        } catch (NumberFormatException ex) {
            cap = new VideoCapture(input);
        }

        if (!cap.isOpened()) {
            System.err.println("Failed to open video source: " + input);
            return;
        }

        Mat frame = new Mat();
        int frameIdx = 0;
        String windowName = "Logo Tracker";

        while (true) {
            boolean ok = cap.read(frame);
            if (!ok || frame.empty()) break;
            frameIdx++;

            // detect
            List<BrandDetection> detections = detector.detectLogos(frame);

            // optional console logging
            for (BrandDetection d : detections) {
                System.out.printf("Frame %d: %s at (%.1f,%.1f,%.1f,%.1f)\n", frameIdx, d.getLabel(), d.getX(), d.getY(), d.getWidth(), d.getHeight());
            }

            // update trackers with detections
            trackerManager.update(detections, frame);

            // draw tracked boxes and labels
            for (BrandDetection t : trackerManager.getTrackedObjects()) {
                int x = (int) Math.round(t.getX());
                int y = (int) Math.round(t.getY());
                int w = (int) Math.round(t.getWidth());
                int h = (int) Math.round(t.getHeight());
                opencv_imgproc.rectangle(
                    frame,
                    new org.bytedeco.opencv.opencv_core.Point(x, y),
                    new org.bytedeco.opencv.opencv_core.Point(x + w, y + h),
                    new Scalar(0, 0, 255, 0),
                    2,
                    opencv_imgproc.LINE_8,
                    0);
                String label = String.format("%s %s", t.getLabel(), t.getId() != null ? t.getId() : "");
                opencv_imgproc.putText(
                    frame,
                    label,
                    new org.bytedeco.opencv.opencv_core.Point(x, Math.max(10, y - 6)),
                    opencv_imgproc.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    new Scalar(0, 255, 0, 0));
            }

            // show
            opencv_highgui.imshow(windowName, frame);
            int key = opencv_highgui.waitKey(1);
            // ESC to quit
            if (key == 27) break;
        }

        cap.release();
        opencv_highgui.destroyAllWindows();
    }
}

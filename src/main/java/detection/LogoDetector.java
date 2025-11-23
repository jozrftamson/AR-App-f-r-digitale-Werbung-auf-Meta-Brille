package detection;

import model.BrandDetection;
import org.bytedeco.opencv.opencv_core.*;
import org.bytedeco.opencv.global.opencv_imgproc;
import org.bytedeco.opencv.global.opencv_core;
import org.bytedeco.opencv.opencv_core.Scalar;

import java.util.ArrayList;
import java.util.List;

/**
 * Logo detection module.
 *
 * This example implements a simple color-based detector for demonstration:
 *  - Red-ish contours -> "Coca-Cola"
 *  - Blue-ish contours -> "Pepsi"
 *
 * Replace `detectLogos` body with a real model inference call (ONNX/TensorFlow) using OpenCV DNN
 * or any cloud API. See comments below where to plug your model.
 */
public class LogoDetector {

    /**
     * Detect logos in a frame.
     *
     * Replace this with model inference. Example steps when using a DNN:
     *  - Load model once (e.g. Net net = Dnn.readNetFromONNX("path/to/model.onnx");)
     *  - Preprocess frame: resize to model input, convert BGR->RGB if needed, scale/normalize
     *  - Run forward pass and parse outputs into BrandDetection entries
     */
    public List<BrandDetection> detectLogos(Mat frame) {
        List<BrandDetection> out = new ArrayList<>();

        Mat hsv = new Mat();
        opencv_imgproc.cvtColor(frame, hsv, opencv_imgproc.COLOR_BGR2HSV);

        // Red mask
        Mat lowerRed = new Mat();
        Mat upperRed = new Mat();
        scalarInRange(hsv, lowerRed, new Scalar(0, 120, 70, 0), new Scalar(10, 255, 255, 0));
        scalarInRange(hsv, upperRed, new Scalar(170, 120, 70, 0), new Scalar(180, 255, 255, 0));
        Mat redMask = new Mat();
        opencv_core.bitwise_or(lowerRed, upperRed, redMask);

        // Blue mask
        Mat blueMask = new Mat();
        scalarInRange(hsv, blueMask, new Scalar(100, 120, 70, 0), new Scalar(140, 255, 255, 0));

        // Find contours for red and blue masks
        findContoursAndAdd(redMask, frame, "Coca-Cola", out);
        findContoursAndAdd(blueMask, frame, "Pepsi", out);

        // Cleanup
        hsv.release(); lowerRed.release(); upperRed.release(); redMask.release(); blueMask.release();

        return out;
    }

    private void scalarInRange(Mat src, Mat dst, Scalar lower, Scalar upper) {
        Mat lowerMat = new Mat(1, 1, opencv_core.CV_8UC3, lower);
        Mat upperMat = new Mat(1, 1, opencv_core.CV_8UC3, upper);
        opencv_core.inRange(src, lowerMat, upperMat, dst);
        lowerMat.release();
        upperMat.release();
    }

    private void findContoursAndAdd(Mat mask, Mat frame, String label, List<BrandDetection> out) {
        MatVector contours = new MatVector();
        Mat hierarchy = new Mat();
        opencv_imgproc.findContours(mask, contours, hierarchy, opencv_imgproc.RETR_EXTERNAL, opencv_imgproc.CHAIN_APPROX_SIMPLE);

        for (long i = 0; i < contours.size(); i++) {
            Mat cnt = contours.get(i);
            double area = opencv_imgproc.contourArea(cnt);
            if (area < 800) continue; // filter small blobs
            Rect r = opencv_imgproc.boundingRect(cnt);
            // clamp to frame
            int x = Math.max(0, r.x());
            int y = Math.max(0, r.y());
            int w = Math.min(frame.cols() - x, r.width());
            int h = Math.min(frame.rows() - y, r.height());

            // Confidence mock: area-based
            double conf = Math.min(0.99, 0.3 + Math.log(area) / 10.0);
            out.add(new BrandDetection(label, conf, x, y, w, h));
            cnt.release();
        }
        contours.deallocate();
        hierarchy.release();
    }
}

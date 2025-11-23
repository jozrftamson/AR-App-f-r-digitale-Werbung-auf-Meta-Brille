import video.VideoProcessor;

/**
 * Entry point. Usage:
 *  - Run on video file: java -jar logo-tracker.jar /path/to/video.mp4
 *  - Run on webcam: java -jar logo-tracker.jar 0
 */
public class Main {
    public static void main(String[] args) {
        String source = "0"; // default to webcam
        if (args.length > 0) {
            source = args[0];
        } else {
            System.out.println("No argument given — defaulting to webcam '0'. To use a file, pass its path as first argument.");
        }

        // Note: with Bytedeco OpenCV the native libraries are loaded automatically when the classes are used.

        VideoProcessor processor = new VideoProcessor();
        processor.run(source);
    }
}

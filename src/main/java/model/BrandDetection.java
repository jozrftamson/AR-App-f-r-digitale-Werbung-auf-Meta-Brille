package model;

import org.bytedeco.opencv.opencv_core.Rect;

/**
 * POJO representing a detected brand/logo in a frame.
 */
public class BrandDetection {
    private String label;
    private double confidence;
    private double x;
    private double y;
    private double width;
    private double height;
    private String id; // Assigned by tracker manager (e.g., "Brand-1")

    public BrandDetection(String label, double confidence, double x, double y, double width, double height) {
        this.label = label;
        this.confidence = confidence;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }

    public String getLabel() { return label; }
    public double getConfidence() { return confidence; }
    public double getX() { return x; }
    public double getY() { return y; }
    public double getWidth() { return width; }
    public double getHeight() { return height; }
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public Rect toRect() {
        return new Rect((int) Math.round(x), (int) Math.round(y), (int) Math.round(width), (int) Math.round(height));
    }

    @Override
    public String toString() {
        return String.format("%s(%.2f) @ [%.1f,%.1f,%.1f,%.1f] id=%s", label, confidence, x, y, width, height, id);
    }
}

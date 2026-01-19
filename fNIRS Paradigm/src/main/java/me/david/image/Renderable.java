package me.david.image;

import lombok.Setter;
import me.david.paradgim.Event;

import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;

public class Renderable extends JPanel {
    @Setter private BufferedImage currentImage;

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (currentImage == null) return;

        Graphics2D g2D = (Graphics2D) g;
        g2D.setRenderingHints(new RenderingHints(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BICUBIC));

        int w = getWidth();
        int h = getHeight();

        int imageWidth = currentImage.getWidth();
        int imageHeight = currentImage.getHeight();

        double scaleX = (double) (w-250) / imageWidth;
        double scaleY = (double) (h-250) / imageHeight;
        double scale = Math.min(scaleX, scaleY);

        int x = (int) ((w - (imageWidth * scale)) / 2);
        int y = (int) ((h - (imageHeight * scale)) / 2);

        g2D.drawImage(currentImage, x, y, (int) (imageWidth * scale), (int) (imageHeight * scale), this);
    }

    public void drawImage(Event currentEvent) {
        this.currentImage = currentEvent.getToDisplay();
        repaint();
    }
}

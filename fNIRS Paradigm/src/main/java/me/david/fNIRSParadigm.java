package me.david;

import me.david.image.Renderable;
import me.david.paradgim.Event;
import me.david.util.Context;

import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.WindowEvent;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class fNIRSParadigm {
    private final Context currentContext;

    private boolean isRunning = true;
    private boolean hasStarted = false;
    private boolean displayTimer = true;

    private final List<Event> taskEvents = new ArrayList<Event>();
    private Event currentEvent;

    public fNIRSParadigm(Context currentContext) {
        this.currentContext = currentContext;

        // Window Display Setup
        final JFrame frame = new JFrame("fNIRS Basic Block Paradigm");

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setExtendedState(JFrame.MAXIMIZED_BOTH);
        frame.setUndecorated(true);
        frame.setVisible(false);

        frame.addKeyListener(new KeyListener() {
            @Override public void keyTyped(KeyEvent e) {}
            @Override public void keyReleased(KeyEvent e) {}

            @Override
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_ESCAPE) frame.dispatchEvent(new WindowEvent(frame, WindowEvent.WINDOW_CLOSING));
                if (e.getKeyCode() == KeyEvent.VK_T) displayTimer = !displayTimer;
            }
        });

        // Process Folders to Create Event Blocks
        fillEvents();

        // Set Initial Event
        currentEvent = taskEvents.get(0);

        // Image Rendering
        Renderable imageRenderer = new Renderable();
        imageRenderer.setCurrentImage(null);

        // Timer Label
        JLabel text = new JLabel("");
        text.setSize(50, 20);
        text.setLocation(0, 0);
        frame.add(text);

        imageRenderer.add(text);

        frame.add(imageRenderer);

        long initialTime = System.currentTimeMillis();

        while (isRunning) {
            frame.setVisible(true);

            int currentTimeInSeconds = (int) ((System.currentTimeMillis() - initialTime)/1000);
            String result = String.format("%02d:%02d", (currentTimeInSeconds / 60) % 60, currentTimeInSeconds % 60);

            if (!hasStarted) {
                if (currentTimeInSeconds >= 5) { // Initial delay before recording
                    hasStarted = true;
                    initialTime = System.currentTimeMillis();
                }

                continue;
            }

            if (!currentEvent.isActive() && currentEvent.getEventTime() <= currentTimeInSeconds)
                currentEvent.setActive(true);


            if (currentEvent.isActive()) {
                // RENDER IMAGE
                imageRenderer.drawImage(currentEvent);

                if (currentTimeInSeconds >= (currentEvent.getEventTime() + currentEvent.getEventDuration())) {
                    imageRenderer.setCurrentImage(null);

                    taskEvents.remove(0);

                    if (taskEvents.isEmpty()) {
                        frame.dispatchEvent(new WindowEvent(frame, WindowEvent.WINDOW_CLOSING));
                        isRunning = false;

                        return;
                    }

                    currentEvent = taskEvents.get(0);
                }
            }

            if (displayTimer) text.setText(result); else text.setText("");
        }

        frame.dispatchEvent(new WindowEvent(frame, WindowEvent.WINDOW_CLOSING));

        // Save any relevant data about block time if using context, n/a rn
    }

    private void fillEvents() {
        int lastEventTime = -15; // Weird initialization for sake of proper event timing

        // Indicator event, flashes black when the paradigm begins.
        taskEvents.add(new Event(0, 1, new File("images/clear.png")));

        for (String currentPath : currentContext.getTaskBlockFolders()) {
            File dir = new File(currentPath);
            File[] directoryListing = dir.listFiles();

            if (directoryListing == null) {
                System.out.println("UNABLE TO READ GIVEN DIRECTORY: " + currentPath);
                isRunning = false;
                return;
            }

            for (File image : directoryListing) {
                lastEventTime += 30;
                taskEvents.add(new Event(lastEventTime, 10, image));
            }
        }

        taskEvents.add(new Event(lastEventTime + 35, 1, new File("images/clear.png"))); // Just adding a last control
    }
}

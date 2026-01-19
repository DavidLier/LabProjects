package me.david;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class EventServer {
    private final ServerSocket serverSocket;
    private final Socket clientSocket;

    private final PrintWriter out;
    private final BufferedReader in;

    Robot keySimulator;

    public EventServer(int port) throws IOException, AWTException {
        serverSocket = new ServerSocket(port);

        System.out.println("Waiting for Client!");
        clientSocket = serverSocket.accept();
        System.out.println("Client Detected! Successfully Initialized. ");

        out = new PrintWriter(clientSocket.getOutputStream(), true);
        in = new BufferedReader((new InputStreamReader((clientSocket.getInputStream()))));

        keySimulator = new Robot();

        while (true) {
            String ping = in.readLine();
            switch (ping) {
                case "F1":
                    System.out.println("Marking Start Event.");
                    out.println("Marking Start Event.");
                    simulateButtonPress(KeyEvent.VK_F1);
                    break;
                case "F2":
                    System.out.println("Marking Taken Breath.");
                    out.println("Marking Taken Breath.");
                    simulateButtonPress(KeyEvent.VK_F2);
                    break;
                case "F3":
                    System.out.println("Marking 14 Breaths Reached.");
                    out.println("Marking 14 Breaths Reached.");
                    simulateButtonPress(KeyEvent.VK_F3);
                    break;
                case "F4":
                    System.out.println("Marking Manually Marked Miscount.");
                    out.println("Marking Manually Marked Miscount.");
                    simulateButtonPress(KeyEvent.VK_F4);
                    break;
                default:
                    out.println("ERR.");
                    System.out.println("Different ping received, " + ping);
                    break;
            }
        }
    }

    private void simulateButtonPress(int key) {
        keySimulator.keyPress(key);
        keySimulator.keyRelease(key);
    }

}
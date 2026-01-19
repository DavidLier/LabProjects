package me.david.util;

import me.david.StimuliSender;

import java.io.IOException;

public class Launcher {
    public static void main(String[] args) throws IOException {
        if (args.length < 2) {
            System.out.println("Please define in the Arguments the receiving IP and Port.");
            return;
        }

        String ip = args[0];
        int port = parsePort(args, 1);
        if (port == -1) return;

        System.out.println("Tool Started with Focus on " + ip + " on port " + port);
        new StimuliSender(ip, port);
    }


    private static int parsePort(String[] args, int index) {
        int port = -1;
        try {
            port = Integer.parseInt(args[index]);
        } catch (Exception e) {
            System.out.println("Error attempting to parse port, are your arguments like the following? Client 127.0.0.1 3333");
        }

        return port;
    }
}
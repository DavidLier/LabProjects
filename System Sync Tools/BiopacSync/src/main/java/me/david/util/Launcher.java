package me.david.util;

import com.github.kwhat.jnativehook.NativeHookException;
import me.david.EventClient;
import me.david.EventServer;

import java.awt.*;
import java.io.IOException;


public class Launcher {
    public static void main(String[] args) throws IOException, AWTException, NativeHookException {
        if (args.length < 1) {
            System.out.println("Please define in the Arguments whether this is the client or server.");
            return;
        }

        boolean isServer = false;
        switch (args[0].toLowerCase()) {
            case "server":
                isServer = true;
                break;
            case "client":
                break;
            default:
                System.out.println("Option one should either be Client or Server");
                return;
        }

        if (isServer) {
            int port = parsePort(args, 1, "Server 3333");
            if (port == -1) return;

            System.out.println("Attempting to initialize server on port " + port + "...");
            new EventServer(port);

            return;
        }

        String ip = args[1];
        int port = parsePort(args, 2, "Client 127.0.0.1 3333");
        if (port == -1) return;

        System.out.println("Attempting to create client and connect to " + ip + " on port " + port);
        new EventClient(ip, port);
    }


    private static int parsePort(String[] args, int index, String desiredArgs) {
        int port = -1;
        try {
            port = Integer.parseInt(args[index]);
        } catch (Exception e) {
            System.out.println("Error attempting to parse port, are your arguments like the following? " + desiredArgs);
        }

        return port;
    }
}
package me.david;

import java.io.*;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.Socket;

public class EventClient {
    private final Socket clientSocket;
    private final PrintWriter out;
    private final BufferedReader in;

    public EventClient(String ip, int port) throws IOException {
        clientSocket = new Socket(ip, port);
        out = new PrintWriter(clientSocket.getOutputStream(), true);
        in = new BufferedReader((new InputStreamReader((clientSocket.getInputStream()))));

        System.out.println("Client Created!");

        DatagramSocket socket = new DatagramSocket(9876);
        byte[] buffer = new byte[1024];

        while (true) {
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
            socket.receive(packet);
            String message = new String(packet.getData(), 0, packet.getLength());
            sendMessage(message);
        }
    }

    public String sendMessage(String msg) throws IOException {
        out.println(msg);
        return in.readLine();
    }
}

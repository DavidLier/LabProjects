package me.david;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.net.*;

public class StimuliSender extends JFrame implements ActionListener {
    private final DatagramSocket socket;

    private final String ip;
    private final int port;

    public StimuliSender(String ip, int port) throws SocketException, UnknownHostException {
        socket = new DatagramSocket();

        this.ip = ip;
        this.port = port;

        JButton sendSignalButton = new JButton("Press");
        sendSignalButton.addActionListener(this);

        add(sendSignalButton);

        setTitle("Stimulus Sender");
        setPreferredSize(new Dimension(250, 250));
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        pack();

        setVisible(true);
    }

    private void sendPacket() throws IOException {
        byte[] buffer = "Stimuli".getBytes();

        DatagramPacket packet = new DatagramPacket(buffer, buffer.length, InetAddress.getByName(ip), port);;

        long sendTime = System.currentTimeMillis();
        socket.send(packet);
        System.out.println("Packet Sent.");

        packet = new DatagramPacket(buffer, buffer.length);
        socket.receive(packet);
        System.out.println(new String(packet.getData(), 0, packet.getLength()));

        long receiveTime = (System.currentTimeMillis() - sendTime);

        System.out.println("Response Received. Time Taken: " + receiveTime + " ms.");
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        try {
            sendPacket();
        } catch (Exception ex) {
            System.out.println("Error Sending Packet.");
            ex.printStackTrace();
        }
    }

}

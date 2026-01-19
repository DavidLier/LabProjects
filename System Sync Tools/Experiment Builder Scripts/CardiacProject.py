import sreb
import socket

class StimuliSync(sreb.EBObject):
    def __init__(self):
        sreb.EBObject.__init__(self);

    def awaitSignal(self, condition):
        ip = "0.0.0.0";
        port = 5005;

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        sock.bind((ip, port));

        while True:
            data, address = sock.recvfrom(1024);
            msg = data.decode('utf-8');

            if msg != condition:
                continue;

            localSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
     
            if condition == "Systolic":
                localSocket.sendto(b'F1', ("127.0.0.1", 9876));
            elif condition == "Diastolic":
                localSocket.sendto(b'F2', ("127.0.0.1", 9876));

            localSocket.close();

            break;

        sock.close();
        return condition;

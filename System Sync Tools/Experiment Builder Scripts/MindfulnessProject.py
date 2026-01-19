import sreb
import socket

class BiopacSync(sreb.EBObject):
	def __init__(self):
		sreb.EBObject.__init__(self)
		
	def syncStart(self):
		sendMessage(b"F1");
		return

	def onBreath(self):
		sendMessage(b"F2");
		return

	def onReachFourteen(self):
		sendMessage(b"F3");
		return 

	def onMiscount(self):
		sendMessage(b"F4");
		return

	def sendMessage(txt):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
		sock.sendto(txt, ("127.0.0.1", 9876));
		return "Sending Signal";


# This script is placed in Experiment Builder whenever receiving and recieving one in response is necessary. (Mindfulness Project) 
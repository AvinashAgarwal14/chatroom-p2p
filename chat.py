#!/usr/bin/python
import socket
import threading
import sys
from random import randint 
import time

class Server: 
	connections = []
	peers = []
	def __init__(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind(("0.0.0.0", 10004))
		sock.listen(100)
		print("Server Running ...")
		while True:
			client_socket, client_addr = sock.accept()
			cThread = threading.Thread(target = self.handler, args=(client_socket, client_addr))
			cThread.daemon = True
			cThread.start()
			self.connections.append(client_socket)
			self.peers.append(client_addr[0])
			self.sendPeers()
			print(str(client_addr[0]) + ":" + str(client_addr[1]), "Connected!")


	def handler(self, client_socket, client_addr):
		while True:
			data = client_socket.recv(1024)
			updatedData = str(client_addr[0]) + ":" + str(client_addr[1]) + " - " + str(data, "utf-8")
			for connection in self.connections:
				if connection != client_socket:
					connection.send(bytes(updatedData, "utf-8"))
			if not data:
				print(str(client_addr[0]) + ":" + str(client_addr[1]), "Disconnected!")
				self.connections.remove(client_socket)
				self.peers.remove(client_addr[0])
				client_socket.close()
				self.sendPeers()
				break
			
	def sendPeers(self):
		p = ""
		for peer in self.peers:
			p = p + peer + ","
		for connection in self.connections:
			connection.send(b'\x11' + bytes(p, "utf-8"))
		
class Client:
	def __init__(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)		
		sock.connect(("0.0.0.0", 10004))
		iThread = threading.Thread(target = self.sendMsg, args=(sock, ))
		iThread.daemon = True
		iThread.start()
		print("Server: " + "Connected as Client.")

		while True:
			data = sock.recv(1024)
			if not data:
				break
			if data[0:1] == b'\x11':
				print("Server: Someone Connected/Disconnected")
				self.peersUpdated(data[1:])
			else:
				print((str(data, "utf-8")))
	
	def peersUpdated(self, peerData):
			p2p.peers = str(peerData, "utf-8").split(",")[:-1]

	def sendMsg(self, sock):
		while True:
			sock.send(bytes(input(""), "utf-8"))

class p2p:
	peers = ["127.0.0.1"]

while True:
	try:
		print("Trying to connect ...")
		time.sleep(randint(1, 5))
		for peer in p2p.peers:
			try:
				client = Client()
			except KeyboardInterrupt:
				sys.exit(0)
			except:
				pass
			try:
				server = Server()
			except KeyboardInterrupt:
				sys.exit(0)
			except:
				print("Couldn't start the server.")
	except KeyboardInterrupt:
		sys.exit(0)
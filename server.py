import time, socket, sys

print("Welcome")
print("Initializing...")
time.sleep(1)

s = socket.socket()
host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 3000
s.bind(('', port))

s.listen()
print("Waiting for incoming connections...")

c, addr = s.accept()
print("Received connection from", addr[0], "(", addr[1], ")")
c.send(host.encode())
s_name = c.recv(1024)
s_name = s_name.decode()
print(s_name, "has connected to the chat room")
print("Enter 'exit' to exit the chat room")

while True:
	message = input(str("Me: "))
	if message == "exit":
		message = "Left chat room!"
		c.send(message.encode())
		print()
		break
	c.send(message.encode())
	message = c.recv(1024)
	message = message.decode()
	print(s_name, ":", message)
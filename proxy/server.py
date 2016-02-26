import socket
import ssl
import threading

class Client(threading.Thread):#represents an ssl connection to a client
    def __init__(self,sock):#initializes the client thread using a socket
        threading.Thread.__init__(self)
        self.sock=sock
    def run(self):#starts the thread fro communicating with the client
        data = self.sock.recv(1024)
        print data
        self.sock.send("HTTP/1.1 200 OK\r\n\r\nThis is a test message")
        self.sock.close()
        return
    
class Server(object):
    def __init__(self): #sets up the socket for use
        sock = socket.socket()#creates simple tcp socket
        self.ssl_sock = ssl.wrap_socket(sock,keyfile="C:\\Users\\YuvalArad\\Documents\\proxy\\proxy\\server.key",certfile="C:\\Users\\YuvalArad\\Documents\\proxy\\proxy\\server.crt",server_side=True)#wraps the socket in ssl context using the self-signed ssl private key and certificate

    def start(self,port):#starts the server
        self.ssl_sock.bind(("",port))
        self.ssl_sock.listen(10)
        while True:
            client_sock, addr = self.ssl_sock.accept()
            client = Client(client_sock)
            client.start()


s = Server()
s.start(1234)

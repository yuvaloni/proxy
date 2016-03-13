
#import libraries

import zlib
import socket
import ssl
import threading

#defining constants:
port=1234
server_url="https://52.37.162.165:1234"


class compression:#takes care of compressed response bodies
    @staticmethod
    def gzip_compress(text):#compresses text in gzip
        gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
        return gzip_compress.compress(text)+gzip_compress.flush()
    @staticmethod
    def gzip_decompress(text):#decompresses to gzip
        return zlib.decompress(text,zlib.MAX_WBITS|16)

    
class Request(object):#represents the request sent to the website and the connection to the website
    def __init__(self,text):
        self.init_text=text
        
    def process_request(self):#replacing parameters in request before sending to website
        #get url
        self.url = self.init_text[self.init_text.find("url=")+len("url="):self.init_text.find(" HTTP/")]
        #get request parameter
        request_param = self.url[self.url.find("://")+len("://"):]
        request_param = request_param[request_param.find("/"):]
        #get host header
        host = self.url[self.url.find("/")+2:]
        self.host = host[:host.find("/")]
        #get referer header
        if self.init_text.find("Referer:")>-1:
            referer = self.init_text[self.init_text.find("Referer:")+len("Referer:"):]
            referer = referer[referer.find("url=")+len("url="):]
            referer = referer[:referer.find("\r\n")]
        else:
            referer=""
        #replace request parameter
        self.processed_request = self.init_text[:self.init_text.find(" ")+1]+request_param+self.init_text[self.init_text.find(" HTTP/"):]
        #replace host header
        request_host_split = self.processed_request.partition("Host:")
        self.processed_request = request_host_split[0]+request_host_split[1]+" "+self.host+request_host_split[2][request_host_split[2].find("\r\n"):]
        #replace referer header
        if referer!="":
            request_referer_split = self.processed_request.partition("Referer:")
            self.processed_request = request_referer_split[0]+request_referer_split[1]+" "+referer+request_referer_split[2][request_referer_split[2].find("\r\n"):]
    

    def send_request(self):#sends the processed request
        sock = socket.socket()
        sock.settimeout(1)
        if self.url.find("https://")>-1:
            sock=ssl.wrap_socket(sock)
            sock.connect((self.host,443))
        else:
            sock.connect((self.host,80))
        sock.send(self.processed_request)
        self.init_response=""
        try:
            result = sock.recv(1024)
        except:
            result=""
        while len(result)>0:
            self.init_response+=result
            try:
                result = sock.recv(1024)
            except:
                result=""
        sock.close()
        
    def process_response(self):#replaces parameters in response before
        response_split=self.init_response.partition("\r\n\r\n")
        response_header = response_split[0]
        response_body=response_split[2]
        if response_split[0].find("gzip")>-1:
            try:
                response_body_temp=compression.gzip_decompress(response_split[2])
            except:
                response_body=response_body=response_split[2]
        self.processed_response=self.init_response

    def get_response(self):
        return self.processed_response
    
class Client(threading.Thread):#represents an ssl connection to a client
    def __init__(self,sock):#initializes the client thread using a socket
        threading.Thread.__init__(self)
        self.sock=sock
        
    def run(self):#starts the thread for communicating with the client
        self.sock.settimeout(1)
        data=""
        try:
            result = self.sock.recv(1024)
        except:
            result=""
        while len(result)>0:
            data+=result
            try:
                result = self.sock.recv(1024)
            except:
                result=""
        if len(data)>0:
            request = Request(data)
            request.process_request()
            request.send_request()
            request.process_response()
            response = request.get_response()
            self.sock.send(response)
        self.sock.close()
        return
    
class Server(object):
    def __init__(self): #sets up the socket for use
        sock = socket.socket()#creates simple tcp socket
        self.ssl_sock = ssl.wrap_socket(sock,keyfile="server.key",certfile="server.crt",server_side=True)#wraps the socket in ssl context using the self-signed ssl private key and certificate

    def start(self,port):#starts the server
        self.ssl_sock.bind(("",port))
        self.ssl_sock.listen(100)
        while True:
            client_sock, addr = self.ssl_sock.accept()
            client = Client(client_sock)
            client.start()


s = Server()
s.start(1234)

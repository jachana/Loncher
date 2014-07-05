import socket
import sys
from thread import *

class AbortServer:
        """Objeto que modela el servidor de aborto de juego en curso
        """

        def __init__(self,gHandle):
                self.KillFlag = False
                self.gHandle = gHandle                   # Creamos campo para Handle del proceso en curso.
                self.s = socket.socket()         # Create a socket object
                self.host = socket.gethostname() # Get local machine name
                self.port = 12345                # Reserve a port for your service.
                try:
                        self.s.bind((host, port))        # Bind to the port
                except:
                        pass
                start_new_thread(sv_main,(gHandle,))

        def sv_main(self,gHandle):
                """Metodo principal del servidor.
                """
                s.listen(1)
                while not KillFlag:
                        #wait to accept a connection - blocking call
                        conn, addr = s.accept()
                        print 'Connected with ' + addr[0] + ':' + str(addr[1])
                        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
                        start_new_thread(clientthread ,(conn,))

        def kill(self):
                """Metodo que aborta el servidor.
                """

                self.KillFlag = True
                self.s.close()

        def clientthread(self,conn):
        #Sending message to connected client
                conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
                #infinite loop so that function do not terminate and thread do not end.
                while True:
                        #Receiving from client
                        data = conn.recv(1024)
                        reply = 'OK...' + data
                        if data == "abort":
                                self.gHandle.abort()
                        if not data:
                                break
                        conn.sendall(reply)
                #came out of loop
                conn.close()

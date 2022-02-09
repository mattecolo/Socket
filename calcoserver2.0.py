import socket
from threading import Thread
import json

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224

def ricevi_comandi(sock_service,addr_client):#codice programma calcolatrice precedente
    print("avviato")
    while True:
        data=sock_service.recv(1024)
        if not data: #se data è un vettore vuoto risulta false; sennò true/if len(data)==0/se è vuoto esce, sennò continua
                break
        data=data.decode()
        data=json.loads(data)
        primoNumero=data['primoNumero']
        operazione=data['operazione']
        secondoNumero=data['secondoNumero']
        ris=""
        if operazione=="+":
            ris=primoNumero+secondoNumero
        elif operazione=="-":
            ris=primoNumero-secondoNumero
        elif operazione=="*":
            ris=primoNumero*secondoNumero
        elif operazione=="/":
            if secondoNumero==0:
                ris="Non puoi dividere per 0"
            else:
                ris=primoNumero/secondoNumero
        elif operazione=="%":
            ris=primoNumero%secondoNumero
        else:
            ris="Operazione non riuscita"
        ris=str(ris)#Casting a stringa
        sock_service.sendall(ris.encode("UTF-8"))
    sock_service.close()

def ricevi_connessioni(sock_listen):#funzione che accetta la connessione del client, al suo interno crea dei thread per eseguire le richieste che arrivano dal client
    while True:
        sock_service, addr_client = sock_listen.accept()
        print("\nConnessione ricevuta da " + str(addr_client))
        print("\nCreo un thread per servire le richieste ")
        try:
            Thread(target=ricevi_comandi,args=(sock_service,addr_client)).start()
        except:
            print("il thread non si avvia")
            sock_listen.close()
        
def avvia_server(INDIRIZZO,PORTA):#funzione che avvia il server
    sock_listen=socket.socket()
    sock_listen.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock_listen.bind((INDIRIZZO,PORTA))
    sock_listen.listen(5)
    print("Server in ascolto su %s." %str((INDIRIZZO,PORTA)))
    ricevi_connessioni(sock_listen)

if __name__=='__main__':
    avvia_server(SERVER_ADDRESS,SERVER_PORT)
#nome del file : pagellaServerMulti.py

import socket
from statistics import median
from threading import Thread
import json


SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22225

#Versione 1 
def ricevi_comandi1(sock_service,addr_client):
    while True:
        data=sock_service.recv(1024)
        if not data: 
                break
        data=data.decode()
        data=json.loads(data)        
        #1. recuperare dal json studente, materia, voto e assenze
        studente=data['studente']
        materia=data['materia']
        voto=data['voto']
        assenze=data['assenze']
        valutazioneTestuale=""
        messaggio=""
        #2. restituire un messaggio in json contenente studente, materia e una valutazione testuale :
        # voto < 4 Gravemente insufficiente
        if voto<4:
            valutazioneTestuale="Gravemente insufficiente"
        # voto [4..5] Insufficiente
        elif voto<=5:
            valutazioneTestuale="Insufficiente"
        # voto = 6 Sufficiente
        elif voto==6:
            valutazioneTestuale="Sufficiente"
        # voto = 7 Discreto 
        elif voto==7:
            valutazioneTestuale="Discreto"
        # voto [8..9] Buono
        elif voto<=9 and voto>=8:
            valutazioneTestuale="Buono"
        # voto = 10 Ottimo
        elif voto==10:
            valutazioneTestuale="Ottimo"
        messaggio={"studente":studente, "materia":materia, "voto":valutazioneTestuale,"assenze":assenze}
        messaggio=json.dumps(messaggio)
        sock_service.sendall(messaggio.encode("UTF-8"))

    sock_service.close()

#Versione 2 
def ricevi_comandi2(sock_service,addr_client):
    while True:
        data=sock_service.recv(1024)
        if not data: 
                break
        data=data.decode()
        data=json.loads(data)
  #1.recuperare dal json studente e pagella
        studente=data['studente']
        pagella=data['pagella']
        media=0
        totvoti=0
        assenzetot=0
        cont=0
        print(pagella)
        for voto in pagella[studente]:
            totvoti+=voto[1]
            cont=cont+1
        for assenze in pagella[studente]:
            assenzetot+=assenze[1]
        media=totvoti/cont
        messaggio={"studente":studente, "media voti":media, "somma assenze":assenzetot}
        messaggio=json.dumps(messaggio)
        sock_service.sendall(messaggio.encode("UTF-8"))
    sock_service.close()

#Versione 3
def ricevi_comandi3(sock_service,addr_client):
   while True:
        data=sock_service.recv(1024)
        if not data: 
                break
        data=data.decode()
        data=json.loads(data)
        pagella=data['pagella']
  #1.recuperare dal json il tabellone
  #2. restituire per ogni studente la media dei voti e somma delle assenze :
  #manca


def ricevi_connessioni(sock_listen):
    while True:    
        sock_service, addr_client = sock_listen.accept()
        print("\nConnessione ricevuta da " + str(addr_client))
        print("\nCreo un thread per servire le richieste ")
        try:
            Thread(target=ricevi_comandi2,args=(sock_service,addr_client)).start()
        except:
            print("il thread non si avvia")
            sock_listen.close()
        
def avvia_server(SERVER_ADDRESS,SERVER_PORT):
    sock_listen=socket.socket()
    sock_listen.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock_listen.bind((SERVER_ADDRESS,SERVER_PORT))
    sock_listen.listen(5)
    print("Server in ascolto su %s." %str((SERVER_ADDRESS,SERVER_PORT)))
    ricevi_connessioni(sock_listen)

if __name__=='__main__':
    avvia_server(SERVER_ADDRESS,SERVER_PORT)
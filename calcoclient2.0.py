import socket
import json

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224

def invia_comandi(sock_service):#codice del programma vecchio
    while True:
        primoNumero=input("Inserisci il primo numero. exit() per uscire ")
        if primoNumero=="exit()":
            break
        primoNumero=float(primoNumero)
        operazione=input("Inserisci l'operazione (+,-,*,/,%)")
        secondoNumero=float(input("Inserisci il secondo numero "))
        messaggio={'primoNumero':primoNumero, 'operazione':operazione, 'secondoNumero':secondoNumero}
        messaggio=json.dumps(messaggio)#Trasforma l'oggetto in stringa
        sock_service.sendall(messaggio.encode("UTF-8"))
        #UTF-8 è la famiglia dei caratteri, utilizzato anche in HTML
        data=sock_service.recv(1024)
        print("Risultato: ",data.decode())#Decode trasforma da un vettore di byte ad un vettore di stringa

def connessione_server(address,port):#funzione che si connette al server e chiama la funzione che permette di inserire i numeri
    sock_service=socket.socket()
    sock_service.connect((SERVER_ADDRESS,SERVER_PORT))
    print("Connesso a " + str((SERVER_ADDRESS,SERVER_PORT)))
    invia_comandi(sock_service)

if __name__=='main':
    connessione_server(SERVER_ADDRESS,SERVER_PORT)

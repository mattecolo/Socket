import socket
import json

HOST="127.0.0.1"
PORT=65432

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    #AF_INEF: tipo indirizzo/protocollo usato; la famiglia dell'indirizzo
    #STREAM: TCP. Indica la connessione, per l'appunto
    s.connect((HOST, PORT))
    while True:
        primoNumero=input("Inserisci il primo numero. exit() per uscire ")
        if primoNumero=="exit()":
            break
        primoNumero=float(primoNumero)
        operazione=input("Inserisci l'operazione (+,-,*,/,%)")
        secondoNumero=float(input("Inserisci il secondo numero "))
        messaggio={'primoNumero':primoNumero, 'operazione':operazione, 'secondoNumero':secondoNumero}
        messaggio=json.dumps(messaggio)#Trasforma l'oggetto in stringa
        s.sendall(messaggio.encode("UTF-8"))
        #UTF-8 è la famiglia dei caratteri, utilizzato anche in HTML
        data=s.recv(1024)
        print("Risultato: ",data.decode())#Decode trasforma da un vettore di byte ad un vettore di stringa
        #Fine parte client
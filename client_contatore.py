import socket
import json

HOST="127.0.0.1"
PORT=65432

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    #AF_INEF: tipo indirizzo/protocollo usato; la famiglia dell'indirizzo
    #STREAM: TCP. Indica la connessione, per l'appunto
    s.connect((HOST, PORT))
    while True:
        stringa=input("Inserisci la stringa, 'KO' per uscire : ")
        messaggio={
            'stringa' : stringa
        }
        messaggio=json.dumps(messaggio)#Trasforma l'oggetto in stringa
        s.sendall(messaggio.encode("UTF-8"))
        #UTF-8 è la famiglia dei caratteri, utilizzato anche in HTML
        data=s.recv(1024)
        if stringa=="KO":
            print(data.decode())
            break
        else:
            print("Stringa modificata", data.decode())
        #Fine parte client
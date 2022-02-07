import socket
import json

HOST="127.0.0.1"
PORT=65432

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    #AF_INEF: tipo indirizzo/protocollo usato; la famiglia dell'indirizzo
    #STREAM: TCP. Indica la connessione, per l'appunto
    s.connect((HOST, PORT))
    while True:
        operazione=input("Comandi disponibili: \n#list : per vedere i voti inseriti \n #set /nomestudente : per inserire uno studente \n #put /nomestudente/materia/voto/ore \n #get /nomestudente : per richiedere i voti di uno studente \n #close: per chiudere la connessione con il server e per spegnerlo\n")
        messaggio={
            'operazione' : operazione
        }
        messaggio=json.dumps(messaggio)
        s.sendall(messaggio.encode("UTF-8"))
        #UTF-8 è la famiglia dei caratteri, utilizzato anche in HTML
        data=s.recv(1024)
        data=data.decode()
        print(data)
        if operazione=='#list':
            deserialized_dict=json.loads(data)#decodifica dopo aver ricevuto
            print(deserialized_dict)
        elif operazione.find('#set') != -1:
            print(data)
        elif operazione=='#close':
            print("Connessione chuisa")
            break
        elif operazione.find('#put') != -1:
            print(data)
        print("\n")
        #Fine parte client
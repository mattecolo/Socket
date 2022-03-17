#nome del file : pagellaClientMulti.py
import socket
import sys
import random
import os
import time
import threading
import multiprocessing
import json
import pprint

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22225
NUM_WORKERS=4

#Versione 1 
def genera_richieste1(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()

    #1. Generazione casuale:
    #   di uno studente (valori ammessi: 5 cognomi a caso tra cui il tuo cognome)
    listaCognomi=["Colombo","Rossi","Bianchi","Verdi","Neri"]
    cognome=listaCognomi[random.randint(0,4)]
    #   di una materia (valori ammessi: Matematica, Italiano, inglese, Storia e Geografia)
    listaMaterie=["Matematica","Italiano","Inglese","Storia","Geografia"]
    materia=listaMaterie[random.randint(0,4)]
    #   di un voto (valori ammessi 1 ..10)
    voto=random.randint(1,10)
    #   delle assenze (valori ammessi 1..5) 
    assenze=random.randint(1,5)
    #2. comporre il messaggio, inviarlo come json
    #   esempio: {'studente': 'Studente4', 'materia': 'Italiano', 'voto': 2, 'assenze': 3}
    messaggio={'studente':cognome, 'materia':materia, 'voto':voto,'assenze':assenze}
    messaggio=json.dumps(messaggio)#Trasforma l'oggetto in stringa
    print("Invio dati ",messaggio)#mostra l'operazione
    s.sendall(messaggio.encode("UTF-8"))
    #3. ricevere il risultato come json: {'studente':'Studente4','materia':'italiano','valutazione':'Gravemente insufficiente'}
    data=s.recv(1024)

    if not data:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        data=data.decode()  
        data=json.loads(data)     
        #1. recuperare dal json studente, materia, voto e assenze
        studente=data['studente']
        materia=data['materia']
        valutazione=data['voto']
        assenze=data['assenze']
        print(f"{threading.current_thread().name}: La valutazione di: {studente} in {materia} è {valutazione}")
    s.close()

#Versione 2 
def genera_richieste2(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()
  #   1. Generazione casuale di uno studente(valori ammessi: 5 cognomi a caso scelti da una lista)
    pagella={}
    listaCognomi=["Colombo","Rossi","Bianchi","Verdi","Neri"]
    cognome=listaCognomi[random.randint(0,4)]
  #   Per ognuna delle materie ammesse: Matematica, Italiano, inglese, Storia e Geografia)
    listaMaterie=["Matematica","Italiano","Inglese","Storia","Geografia"]
    for materia in listaMaterie:
        voto=random.randint(1,10)
        assenze=random.randint(1,5)
        pagella[cognome].append((materia,voto,assenze))
  #   esempio: pagella={"Cognome1":[("Matematica",8,1), ("Italiano",6,1), ("Inglese",9.5,3), ("Storia",8,2), ("Geografia",8,1)]}
  #2. comporre il messaggio, inviarlo come json
    messaggio={
        "studente" : cognome,
        "pagella" : pagella[cognome]
    }
    messaggio=json.dumps(messaggio)#Trasforma l'oggetto in stringa
    print("Invio dati ",messaggio)#mostra l'operazione
    s.sendall(messaggio.encode("UTF-8"))
  #3  ricevere il risultato come json {'studente': 'Cognome1', 'media': 8.0, 'assenze': 8}
    data=s.recv(1024)
    if not data:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        data=data.decode()  
        data=json.loads(data)  
        print("Ricevo dati ",data)   
        #1. recuperare dal json studente, materia, voto e assenze
        studente=data['studente']
        media=data['media']
        assenzetot=data['assenzetot']
        print(f"{threading.current_thread().name}: Lo studente {studente} ha una media di: {media} e un totale di assenze {assenzetot}")
    s.close()

#Versione 3
def genera_richieste3(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()
  #   1. Per ognuno degli studenti ammessi: 5 cognomi a caso scelti da una lista
    pagella={}
    listaCognomi=["Colombo","Rossi","Bianchi","Verdi","Neri"]
  #   Per ognuna delle materie ammesse: Matematica, Italiano, inglese, Storia e Geografia)
    listaMaterie=["Matematica","Italiano","Inglese","Storia","Geografia"]
    for studente in listaCognomi:
        oggetto=[]
        for materia in listaMaterie:
            voto=random.randint(1,10)
            assenze=random.randint(1,5)
            oggetto.append((materia,voto,assenze))
        pagella[studente]=oggetto
  #   Per ognuna delle materie ammesse: Matematica, Italiano, inglese, Storia e Geografia)
  #   generazione di un voto (valori ammessi 1 ..10)
  #   e delle assenze (valori ammessi 1..5) 
  #   esempio: tabellone={"Cognome1":[("Matematica",8,1), ("Italiano",6,1), ("Inglese",9,3), ("Storia",8,2), ("Geografia",8,1)],
  #                       "Cognome2":[("Matematica",7,2), ("Italiano",5,3), ("Inglese",4,12), ("Storia",5,2), ("Geografia",4,1)],
  #                        .....}
  #2. comporre il messaggio, inviarlo come json
    messaggio=json.dumps(pagella)#Trasforma l'oggetto in stringa
    print("Invio dati ",messaggio)#mostra l'operazione
    s.sendall(messaggio.encode("UTF-8"))
  #3  ricevere il risultato come json e stampare l'output come indicato in CONSOLE CLIENT V.3
    #manca

if __name__ == '__main__':
    start_time=time.time()
    for cont in range(0,NUM_WORKERS):
        genera_richieste1(cont,SERVER_ADDRESS,SERVER_PORT)
        genera_richieste2(cont,SERVER_ADDRESS,SERVER_PORT)
        genera_richieste3(cont,SERVER_ADDRESS,SERVER_PORT)
    end_time=time.time()
    print("Total SERIAL time=", end_time - start_time)
     
    start_time=time.time()
    threads=[]
    # 4 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un thread al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    for num in range(NUM_WORKERS):
        thread=threading.Thread(target=genera_richieste1 ,args=(num,SERVER_ADDRESS, SERVER_PORT,))
        threads.append(thread)
        thread=threading.Thread(target=genera_richieste2 ,args=(num,SERVER_ADDRESS, SERVER_PORT,))
        threads.append(thread)
        thread=threading.Thread(target=genera_richieste3 ,args=(num,SERVER_ADDRESS, SERVER_PORT,))
        threads.append(thread)
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    end_time=time.time()
    print("Total THREADS time= ", end_time - start_time)

    start_time=time.time()
    process=[]
    # 7 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un processo al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    for num in range(NUM_WORKERS):
        processo=multiprocessing.Process(target=genera_richieste1 , args=(num,SERVER_ADDRESS, SERVER_PORT))
        process.append(processo)
        processo=multiprocessing.Process(target=genera_richieste2 , args=(num,SERVER_ADDRESS, SERVER_PORT))
        process.append(processo)
        processo=multiprocessing.Process(target=genera_richieste3 , args=(num,SERVER_ADDRESS, SERVER_PORT))
        process.append(processo)
    [processo.start() for processo in process]
    [processo.join() for processo in process]
    end_time=time.time()
    print("Total PROCESS time= ", end_time - start_time)
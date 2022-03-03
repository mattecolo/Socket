#Colombo Matteo
#calcolatrice client per calcoServer.py versione multithread
import socket
import sys
import random
import os
import time
import threading
import multiprocessing
import json

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22001
NUM_WORKERS=2

def genera_richieste(num,address,port):
    start_time_thread= time.time()
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()
    #1. rimpiazzare questa parte con la generazione di operazioni e numeri random, non vogliamo inviare sempre 3+5 
    primoNumero=random.randint(0,100)#assegno ai due numeri un valore casuale tra 0 e 100
    secondoNumero=random.randint(0,100)
    listaoperazioni=["+","-","*","/","%"]#lista con le operazioni
    operazione=listaoperazioni[random.randint(0,4)]#pesca un operazione dalla lista
    '''
    Soluzione alternativa
    Numoperazione=random.randint(0,4)
    if(Numoperazione==0):
        operazione="+"
    elif(Numoperazione==1):
        operazione="-"
    elif(Numoperazione==2):
        operazione="*"
    elif(Numoperazione==3):
        operazione="/"
    elif(Numoperazione==4):
        operazione="%"'''
    #print(primoNumero)
    #print(secondoNumero)
    #print(operazione)
    messaggio={'primoNumero':primoNumero, 'operazione':operazione, 'secondoNumero':secondoNumero}#mostra i due numeri e l'operazione
    messaggio=json.dumps(messaggio)#Trasforma l'oggetto in stringa
    print("Invio richesta ",messaggio)#mostra l'operazione
    s.sendall(messaggio.encode("UTF-8"))
    data=s.recv(1024)
    
    if not data:#se il server non manda una risposta
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:#se il server manda una risposta
        print(f"{threading.current_thread().name}: Risultato: {data.decode()}") # trasforma il vettore di byte in stringa
    s.close()
    end_time_thread=time.time()
    print(f"{threading.current_thread().name} tempo di esecuzione time=", end_time_thread-start_time_thread)

if __name__ == '__main__':
    start_time=time.time()#prende il tempo all'inizio dell'esecuzione
    # 3 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste alla quale passo i parametri (num,SERVER_ADDRESS, SERVER_PORT)
    for cont in range(NUM_WORKERS):
        genera_richieste(cont,SERVER_ADDRESS,SERVER_PORT)#chiamata alla funzione
    end_time=time.time()#prende il tempo all'inizio dell'esecuzione
    print("Total SERIAL time=", end_time - start_time)#mostra il tempo di esecuzione facendo la sottrazione tra il tempo finale e iniziale
     
    start_time=time.time()#prende il tempo all'inizio dell'esecuzione
    threads=[]#lista dei thread
    # 4 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un thread al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    for num in range(NUM_WORKERS):#per ogni "lavoratore"
        thread=threading.Thread(target=genera_richieste ,args=(num,SERVER_ADDRESS, SERVER_PORT))#creazione dei thread con target e parametri
    # ad ogni iterazione appendo il thread creato alla lista threads
        threads.append(thread)#lo aggiungo alla lista
    # 5 avvio tutti i thread
    [thread.start() for thread in threads]#partono tutti i thread
    # 6 aspetto la fine di tutti i thread 
    [thread.join() for thread in threads]#con join il programma attende la fine dei thread prima di terminare 
    end_time=time.time()#prende il tempo alla fine dell'esecuzione
    print("Total THREADS time= ", end_time - start_time)#mostra il tempo di esecuzione facendo la sottrazione tra il tempo finale e iniziale

    start_time=time.time()#prende il tempo all'inizio dell'esecuzione
    process=[]#lista dei processi
    # 7 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un processo al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    for num in range(NUM_WORKERS):
        processo=multiprocessing.Process(target=genera_richieste , args=(num,SERVER_ADDRESS, SERVER_PORT))#creazione dei processi con target e parametri
    # ad ogni iterazione appendo il processo creato alla lista process
        process.append(processo)#lo aggiungo alla lista
    # 8 avvio tutti i processi
    [processo.start() for processo in process]#partono tutti i processi
    # 9 aspetto la fine di tutti i processi 
    [processo.join() for processo in process]#con join il programma attende la fine dei processi prima di terminare 
    end_time=time.time()#prende il tempo alla fine dell'esecuzione
    print("Total PROCESS time= ", end_time - start_time)#mostra il tempo di esecuzione facendo la sottrazione tra il tempo finale e iniziale

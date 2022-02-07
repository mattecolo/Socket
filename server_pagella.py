import socket
import json

HOST='127.0.0.1'
PORT=65432

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))#tupla: array non modificabile
    s.listen()
    print("[*] In ascolto su %s:%d "%(HOST, PORT))
    #conversione del client
    clientsocket, address=s.accept()#accetta la conversione
    students = { 
                'Giuseppe Gullo':[("Matematica",9,0),("Italiano",7,3),("Inglese",7.5,4),("Storia",7.5,4),("Geografia",5,7)],
                'Antonio Barbera':[("Matematica",8,1),("Italiano",6,1),("Inglese",9.5,0),("Storia",8,2),("Geografia",8,1)],
                'Nicola Spina':[("Matematica",7.5,2),("Italiano",6,2),("Inglese",4,3),("Storia",8.5,2),("Geografia",8,2)]
                }
    with clientsocket as cs:
        while True:
            print("Connessione da ", address)
            while True:
                data=cs.recv(1024)
                if not data: #se data è un vettore vuoto risulta false; sennò true/if len(data)==0/se è vuoto esce, sennò continua
                    break
                data=data.decode()
                data=data.strip()
                data=json.loads(data)
                comando=data['operazione']
                print ("[*] Recived: %s" % comando)
                if comando == '#list':
                    serialized_stud = json.dumps(students)
                    cs.sendall(serialized_stud.encode("UTF-8"))
                elif comando.find('#set') != -1:
                    inserimento=data.split(delim='/')
                    controllo_pres=inserimento[1]
                    if(controllo_pres in students):
                        cs.sendall("Studente già inserito".encode("UTF-8"))
                    else:
                        students[inserimento[1]]=[]
                        cs.sendall(students.encode("UTF-8"))
                elif comando.find('#get') != -1:
                    inserimento=data.split(delim='/')
                    controllo_pres=inserimento[1]
                    if(controllo_pres in students):
                        serialized_stud = json.dumps(students[controllo_pres])
                        cs.sendall(students.encode("UTF-8"))
                    else:
                        cs.sendall("Studente non presente".encode("UTF-8"))
                elif comando.find('#put') != -1:
                    inserimento=data.split(delim='/')
                    controllo_pres=inserimento[1]
                    controllo_materia=inserimento[2]
                    if(controllo_pres in students):
                        for alunno,materie in students.items():
                            if(alunno==controllo_pres):
                                for i in materie:
                                    if(controllo_materia == i[0]):
                                         cs.sendall("Materia già presente".encode("UTF-8"))
                                    else:
                                        students[inserimento[1]].append((students[inserimento[2]],students[inserimento[3]],students[inserimento[4]]))
                                        cs.sendall("Inserimento avvenuto".encode("UTF-8"))
                    else:
                        cs.sendall("Studente non presente".encode("UTF-8"))
                    
                elif data.find('#exit') != -1:
                    break
                    #no
                elif data.find('#close') != -1:
                    break
                    #no
                print(cs.getpeername())
                #pp=pprint.PrettyPrinter(indent=4)
                #pp.pprint(students)
            cs.close()
                #Fine parte server
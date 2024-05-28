import socket
import random
import os

SERVER = "" # 0.0.0.0 significa che è server (ascolto su tutte le interfacce), 127.0.0.1 = localhost
PORT = 50000 # porta su cui ascoltare o connettersi
messaggio = "" # immagazzina il messaggio da mostrare al prossimo turno
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket TCP

# colori per l'interfaccia
I_RED='\033[0;91m'
I_GREEN='\033[0;92m'
I_BLUE='\033[0;94m'
COLOR_OFF='\033[0m'

def header():
    os.system('cls') # pulisco il terminale

def simboli(num): # trasforma i numeri della matrice in simboli per l'interfaccia grafica
    if num == 0: # se nella matrice c'è 0
        return " " # nella griglia lascio vuoto
    elif num == 1: # se nella matrice c'è 1
        return I_GREEN + "■" + COLOR_OFF # nella griglia mostro ■, ovvero nave posizionata
    elif num == 2: # se nella matrice c'è 2
        return I_BLUE + "•" + COLOR_OFF # nella griglia mostro •, ovvero acqua colpita
    elif num == 3: # se nella matrice c'è 3
        return I_RED + "X" + COLOR_OFF # nella griglia mostro X, ovvero nave colpita
    
def legenda(): # mostra la legenda, la spiegazione a cosa corrispondono i simboli
    print("Legenda:")
    print("  " + I_GREEN + "■" + COLOR_OFF + " = nave") # nave posizionata verde
    print("  " + I_BLUE + "•" + COLOR_OFF + " = colpo in acqua") # acqua colpita blu
    print("  " + I_RED + "X" + COLOR_OFF + " = nave colpita") # nave colpita rossa

def print_matrix(matrix): # stampa a schermo la matrice (interfaccia grafica)
    # print(matrix)
    print("  ╒═0═╤═1═╤═2═╤═3═╤═4═╤═5═╤═6═╤═7═╤═8═╤═9═╕") # intestazione griglia con numeri colonne
    print("0 │", end="") # riga iniziale
    for i in range(10):
        print(f" {simboli(matrix[0][i])} │", end="") # stampa simboli prima riga
    for i in range(1, 10): # righe 1 - 9
        print(f"\n  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤\n{i} │", end="") # stampa griglia
        for j in range(10): # itera ogni colonna della riga
            print(f" {simboli(matrix[i][j])} │", end="") # stampa simboli di tutte le righe di tutte le colonne
    print("\n  ╘═0═╧═1═╧═2═╧═3═╧═4═╧═5═╧═6═╧═7═╧═8═╧═9═╛") # stampa trailer della griglia

def piazza_nave(matrix, dimensione, direzione, x, y):
    # controllo celle occupate
    if direzione == "v": # direzione verticale
        for i in range(dimensione): # scorro le celle della nave
            if y + i >= len(matrix) or matrix[y + i][x] == 1: # controllo se la cella è fuori dai limiti o già occupata
                print("Celle occupate")
                return False # se una cella è occupata o fuori dai limiti, ritorna False
    else: # direzione orizzontale
        for i in range(dimensione): # scorro le celle della nave
            if x + i >= len(matrix[0]) or matrix[y][x + i] == 1: # controllo se la cella è fuori dai limiti o già occupata
                print("Celle occupate")
                return False # se una cella è occupata o fuori dai limiti, ritorna False         
    # posiziono navi
    if direzione == "v": # direzione verticale
        for i in range(dimensione): # scorro le celle della nave
            matrix[y + i][x] = 1 # piazza la nave
    else: # direzione orizzontale
        for i in range(dimensione): # scorro le celle della nave
            matrix[y][x + i] = 1 # piazza la nave

    return True # nave posizionata con successo
    
def display(): # mostra i messaggi per vedere se ho colpito un anve avversaria o una mia nave è stata colpita
    global messaggio
    if messaggio != "":
        print(messaggio)
        messaggio = ""
    
def send(data): # per comodità creo metodo send per inviare dati
    client_socket.sendall(data.encode())

def receive(): # per comodità creo il metodo receive per ricevere i dati
    return client_socket.recv(1024).decode()

def die(message): # messaggio di vittoria/sconfitta e fine programma
    print(message)
    exit()

def coord_input(ADV_MATRIX):
    #global ADV_MATRIX
    x = -1 # inizializzazione coordinate
    y = -1
    while x not in range(10) or y not in range(10): # finche x e y non rispettano la matrice io chiedo input
        x = int(input("  ORIZZONTALE (x)  ")) # input x
        y = int(input("  VERTICALE (y)   ")) # input y
        if x not in range(10) or y not in range(10): # controllo se x e y rispettano la matrice
            print("Coordinate non valide!")
        if ADV_MATRIX[y][x] == 2 or ADV_MATRIX[y][x] == 3: # controllo se nelle cordinate inserite ho già sparato
            print("Hai già sparato in questa posizione!")
            x = -1
            y = -1
    return x, y

def gioco():
    MATRIX = [[0 for i in range(10)] for j in range(10)] # matrice di gioco 10x10 (0 acqua, 1 nave, 2 acqua colpita, 3 nave colpita)
    ADV_MATRIX = [[0 for i in range(10)] for j in range(10)] # matrice di gioco 10x10 avversario
    lunghezza_navi = [4, 3, 3, 2, 2, 2] # array contenente la lunghezza delle navi da piazzare
    celle_navi = sum(lunghezza_navi) # numero totale di blocchi nave
    CONTROL = 0
    header()
    # configurazione navi
    choice = int(input("Vuoi configurare il campo manualmente [1] o automaticamente? [2] "))
    if choice == 1: # manuale
        ship_index = 0 # contatore numero navi da posizionare
        for dim in lunghezza_navi:
            header() 
            print_matrix(MATRIX) # stampa griglia
            print(f"Inserite {ship_index} navi su {lunghezza_navi}") # stampa messaggio di quante navi già inserite
            graph = ""
            for i in range(dim): # stampa grafica della dimensione della nave
                graph += "■ "
            print(f"Posiziona nave da {dim} | {graph}") # stampa della nave da posizionare
            new_matrix = MATRIX # copia della matrice
            piazzata = False # flag per controllare se la nave è stata posizionata correttamente
            while piazzata == False:
                x, y = coord_input(ADV_MATRIX) # input e controllo coordinate
                direction = input("  DIREZIONE (v/h)  ")  # input direzione
                if direction != "v" and direction != "h": # controllo direzione inserita
                    print("Direzione non valida!")
                    continue # mi permette di far rimettere l'input della direzione se sbagliato
                new_matrix = MATRIX # copia dove poter fare casini
                try:
                    piazzata = piazza_nave(new_matrix, dim, direction, x, y) # tenta di posizionare la nave
                except IndexError:
                    print("La nave va fuori i confini del campo di battaglia!")
                except Exception:
                    print("Non puoi sovrapporre le navi!")
                if piazzata: # se la nave è stata piazzata
                    MATRIX = new_matrix # aggiorna la matrice vera
            ship_index += 1 # incremento contatore
    else: # automatica
        contento = "0" 
        while contento == "0":
            for dim in lunghezza_navi:
                piazzata = False
                ship_index = 0 # contatore navi
                new_matrix = MATRIX # copia matrice
                while piazzata == False: # finchè non piazzo la nave
                    x = random.randint(0, 9) # random per la x
                    y = random.randint(0, 9) # random per la y
                    direction = random.choice(["v", "h"]) # direzione random
                    new_matrix = MATRIX 
                    try:
                        piazzata = piazza_nave(new_matrix, dim, direction, x, y) # tenta di piazzare nave
                    except:
                        pass # riprova al ciclo successivo
                    if piazzata: # se piazzo la nave
                        MATRIX = new_matrix # aggiorno la matrice vera
                ship_index += 1 # incremento contatore
            header()
            print_matrix(MATRIX) # stampo a schermo la matrice
            print("Configurazione automatica completata! \nSei contento della configurazione?")
            print("1. Si")
            print("2. No")
            contento = input()
            if contento == "2": # se non contento svuota matrice e rifai da capo
                MATRIX = [[0 for i in range(10)] for j in range(10)]
                contento = "0"

    # gioco     
    while True:
        # header()
        legenda()
        print("CAMPO BATTAGLIA AVVERSARIO")
        print_matrix(ADV_MATRIX) # matrice avversario
        print("CAMPO BATTAGLIA PROPRIO")
        print_matrix(MATRIX) # matrice propria

        if sum([row.count(3) for row in ADV_MATRIX]) == 16: # controllo se le celle col numero 3 (navi colpite) sono 16
            die("Hai vinto!")
            server_socket.close()
        if sum([row.count(3) for row in MATRIX]) == 16:
            die("Hai perso!")

        display()
        send(f"{CONTROL}") # mando il messaggio del turno al client
        if CONTROL == 0: # turno server
            print("È il tuo turno!")
            x, y = coord_input(ADV_MATRIX) # input e controllo coordinate
            send(f"{x},{y}") # mando coordinate al client
            while True:
                result = receive() # risposta del client
                if result in ["hit", "miss"]: # client mi risponde con hit (se colpisco una sua nave) o miss (se colpisco l'acqua)
                    break
            if result == "hit": # se ho colpito una nave avversaria
                ADV_MATRIX[y][x] = 3 # imposto a 3 quella cella (nave colpita)
                messaggio = f"Hai colpito in ({x}, {y})!" # stampo messaggio 
            else:
                ADV_MATRIX[y][x] = 2 # imposto a 2 la cella (acqua)
                messaggio = f"Hai sparato in ({x}, {y}) e hai mancato!" # stampo messaggio
        else:
            print("In attesa del turno avversario...") # turno client
            x, y = receive().split(",") # ricevo coordinate mandate dal client
            x = int(x)
            y = int(y)
            if MATRIX[y][x] == 1: # se nella cella c'è l'1 (quindi una nave)
                MATRIX[y][x] = 3 # imposta cella a 3 (nave propria colpita)
                send("hit") # invio al client che sono stato colpito
                messaggio = f"Sei stato colpito in ({x}, {y})!"
            else:
                MATRIX[y][x] = 2 # imposta cella a 2 (acqua colpita)
                send("miss") # invio al client che non sono stato colpito
                messaggio = f"L' avversario ha sparato in ({x}, {y}) e ha mancato!"

        # dai controllo all'avversario
        if CONTROL == 0: # se è il mio turno
            CONTROL = 1 # do il turno al client
        else:
            CONTROL = int(receive()) # ricevo il messaggio del turno dal client

header()
print("SERVER")
SERVER = "127.0.0.1" # indirizzo server (localhost)
try:
    PORT = 50000 # porta server
    server_socket.bind((SERVER, PORT)) # tenta di associare il socket del server all'indirizzo e alla porta specificati
except:
    die("Impossibile attivare il server!") # errore

server_socket.listen(1) # il server ascolta 1 connessione
print("In attesa di connessioni dal client...") # aspetta che il client si connetta

client_socket, client_address = server_socket.accept() # accetta la connessione con il client
print(f"Connesso con {client_address}")

# connessione
try:
    while True:
        data = client_socket.recv(1024).decode() # ricezione dei dati del client
        if not data: # se non ci sono dati 
            break
        print(f"Client: {data}") # stampa dati client
        client_socket.sendall("Messaggio ricevuto dal server".encode()) # risponde al client
        gioco() # start del gioco
except ConnectionResetError: # client si disconnette
    print("Connessione interrotta dal client.") # errore
from tkinter import *
import socket
import random
import time
import threading

window = Tk()
window.title("Peer")

name = StringVar()  # Variável para receber o nome do usuário
message = StringVar()  # Variável para receber a mensagem que será enviada
port = random.randint(10000, 11000)  # Gera um volar aleatório entre 10.000 e 11.000 que será utilizado para criar porta de conexão entre os peers
ip = "0.0.0.0"  # Aceita conexão de qualquer origem
target_port = 9999  # Porta de conexão com o servidor
# target_host = "localhost" # Endereço do servidor que possui os usuários online
target_host = "192.168.1.108"  # Endereço do servidor que possui os usuários online

# -------------------------------------------
# Functions


# Função para criar servidor que receberá msgs dos peers
def peerServer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket utilizando protocolo IPv4 e protocolo TCP
    server.bind((ip, port))  # Atribui ao socket endereço e porta de conexão
    server.listen(5)  # Define que o servidor está pronto para receber conexões com no máximo 5
    print("[*] Listening on", ip, ":", port)  # Imprime os endereços IP e Porta que o servidor está sendo executado

    while True:
        # Bloqueia o serviço até receber um pedido de conexão com os valores de conexão (socket cliente) e endereço
        client, addr = server.accept()
        print("[*] Accepted connection from:", addr[0], ":", addr[1])  # Imprime os endereços IP e Porta respectivamente
        request = client.recv(8192)  # Recebe dados do socket remoto em um determinado tamanho de buffer
        cmd = str(request, "utf-8").split(":")[0]  # Atribui a msg recebida de um peer à variável cmd
        print(cmd)  # Imprime a mensagem recebida
        listRcvMsg.insert(END, cmd)  # Insere a msg recebida no final da Listbox
        client.close()  # Fecha conexão com o peer


# Função para enviar (cadastrar) o nome, IP e porta do peer para o servidor que possui a lista de usuários online
def cmdSendName():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket utilizando protocolo IPv4 e protocolo TCP
    client.connect((target_host, target_port))  # Conecta a um socket remoto (servidor) passando os parâmetros host, porta
    client.send(str.encode("0:"+name.get()+":"+str(port)))  # Envia conjunto de bytes (mensagens) para o socket remoto (servidor)


# Função para enviar msg ao peer selecionado na Listbox de usuários online
def cmdSendMsg(selection):
    dstIP = str(selection).split(":")[1]  # Atribui o endereço IP do peer remoto à variável dstIP
    dstPort = str(selection).split(":")[2]  # Atribui a porta do peer remoto à variável dstPort
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket utilizando protocolo IPv4 e protocolo TCP
    client.connect((dstIP, int(dstPort)))  # Conecta a um socket remoto (peer) passando os parâmetros host, porta
    client.send(str.encode(name.get() + " -> " + message.get()))  # Envia conjunto de bytes (mensagens) para o socket remoto (peer)


# Função para requisitar ao servidor a lista de usuários online
def handleRequestUsers():
    while True:
        time.sleep(30)  # Faz a requisição a cada 30s
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket utilizando protocolo IPv4 e protocolo TCP
        client.connect((target_host, target_port))  # Conecta a um socket remoto (servidor) passando os parâmetros host, porta
        client.send(str.encode("1:"))  # Envia conjunto de bytes (mensagens) para o socket remoto (servidor)
        request = client.recv(8192)  # Recebe a lista de usuários online
        listUsers = str(request, "utf-8").split("@")  # Separa a lista de usuários que estão concatenados pelo @
        print(listUsers)  # Imprime a lista de usuários
        listOnline.delete(0, END)  # Apaga a lista de usuários da Listbox
        for user in listUsers:  # Laço para armazenar a nova lista de usuários online
            if user != "":
                listOnline.insert(END, user)  # Adiciona cada usuário online no final da Listbox


# -------------------------------------------
# widgets
frameLeft = Frame(window)
frameRight = Frame(window)

lblOnLine = Label(frameRight, text="Online", font="Arial 12 bold")
listOnline = Listbox(frameRight, height=16, width=40)

lblName = Label(frameLeft, text="Name:", font="Arial 12 bold")
lblMsg = Label(frameLeft, text="Message:", font="Arial 12 bold")
eName = Entry(frameLeft, textvariable=name)
btnSendName = Button(frameLeft, text="Send Name", border=3, relief="groove", command=cmdSendName)
lblSendMsg = Label(frameLeft, text="Type Message:", font="Arial 12 bold")
eSendMsg = Entry(frameLeft, textvariable=message)
btnSndMsg = Button(frameLeft, text="Send", border=3, relief="groove", command=lambda: cmdSendMsg(listOnline.get(listOnline.curselection())))
lblRcvMsg = Label(frameLeft, text="Received Messages", font="Arial 12 bold")
listRcvMsg = Listbox(frameLeft)


# -------------------------------------------
# layout
lblName.grid(row=0, column=0, sticky=W)
eName.grid(row=0, column=1, sticky=W)
btnSendName.grid(row=1, column=1, sticky=W)
lblSendMsg.grid(row=2, column=0, sticky=W)
eSendMsg.grid(row=2, column=1, sticky=W)
btnSndMsg.grid(row=3, column=1, sticky=W)
lblRcvMsg.grid(row=4, column=0, sticky=W)
listRcvMsg.grid(row=5, columnspan=2, sticky="WE")

lblOnLine.grid()
listOnline.grid()

# Cria uma thread passando como parâmetros a função handleRequestUsers
client_handler = threading.Thread(target=handleRequestUsers)
client_handler.start()  # Inicia a thread

# Cria uma thread passando como parâmetros a função peerServer
peerS = threading.Thread(target=peerServer)
peerS.start()  # Inicia a thread

frameLeft.grid(row=0, column=0)
frameRight.grid(row=0, column=1, sticky="N")
window.mainloop()

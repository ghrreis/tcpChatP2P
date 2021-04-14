import socket
import threading

bind_ip = "0.0.0.0"  # Aceita conexão de qualquer origem
bind_port = 9999  # Porta que o servidor "escuta"
usersOnline = []  # Lista de usuários online

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket utilizando protocolo IPv4 e protocolo TCP

server.bind((bind_ip, bind_port))  # Atribui ao socket endereço e porta de conexão

server.listen(5)  # Define que o servidor está pronto para receber conexões com no máximo 5

print("[*] Listening on", bind_ip, ":", bind_port)  # Imprime os endereços IP e Porta que o servidor está sendo executado


def handleClient(client_socket, addrIP):
    request = client_socket.recv(8192)  # Recebe dados do socket remoto em um determinado tamanho de buffer
    cmd = str(request, "utf-8").split(":")[0]  # Recebe o valor do comando passado pelo cliente
    print(cmd)
    if int(cmd) == 0:  # Comando 0 = cadastra o nome, porta e IP do cliente
        # Converte a mensagem de byte para string e imprime a mensagem recebida separa por espaços em branco
        print("[*] Received:", str(request, "utf-8"))  # Imprime a msg recebida do cliente
        name = str(request, "utf-8").split(":")[1]  # Atribui o nome do cliente à variável name
        port = str(request, "utf-8").split(":")[2]  # Atribui a porta do cliente à variável port
        usersOnline.append(name + ":" + addrIP + ":" + port)  # Insere nome, IP e porta na lista de usuários online
        print(usersOnline)  # Imprime a lista de usuários online
    elif int(cmd) == 1:  # Comando 1 = envia a lista de usuários online para o cliente
        print("Sending online users...")  # Imprime msg de envio de lista
        msg = ""
        for user in usersOnline:  # Percorre a lista de usuários online
            msg = msg + user + "@"  # Concatena a lista de usuários separados por @
        client_socket.send(msg.encode())  # Envia conjunto de bytes (mensagens) para o socket remoto (cliente)
        print("Done!")  # Imprime msg de lista enviada
    client_socket.close()  # Fecha conexão com o socket remoto (cliente)


while True:
    # Bloqueia o serviço até receber um pedido de conexão com os valores de conexão (socket cliente) e endereço
    client, addr = server.accept()

    print("[*] Accepted connection from:", addr[0], ":", addr[1])  # Imprime os endereços IP e Porta respectivamente

    # Cria uma thread passando como parâmetros a função handle_client e o socket do cliente
    client_handler = threading.Thread(target=handleClient, args=(client, addr[0]))
    client_handler.start()  # Inicia a thread

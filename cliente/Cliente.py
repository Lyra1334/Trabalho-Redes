import threading, socket, os

def nomeValido(nome:str): #nome válido
    invalidos = " ,.;}{[]@*"
    if nome.isnumeric():
        return False
    else:
        for i in range(len(invalidos)):
            if invalidos[i] in nome:
                return False
    return True

"""
Inicio do código do cliente:
- funções separadas para facilitar a manipulação entre cliente-servidor
"""
def main(): #inicia a conexão e chama as funções 1 ou 2
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.15.5"
    port = 45454
    try:
        client.connect((host,port))
    except:
        return "Não foi possível conectar ao servidor"
    
    #Thread1 = threading.Thread(target= recebeMgs, args=[client]) #aqui para testes, mas tera q ser ativado na troca de telas
    #Thread2 = threading.Thread(target= enviaMgs, args=[client])
    return client
    
def criarConta(client: socket.socket, username: str, password: str, email: str, loc:str): #1 cria uma conta nova
    if nomeValido(username):
        try:
            client.send(bytes("NUSR {"+username+"} {"+password+"} {"+email+"} {"+loc+"}END\n",'utf-8'))
            resultado = client.recv(4096).decode()
            if resultado.split("END\n")[0] == "1":
                #carrega a pagina dos grupos
                return 1
            else:
                pass
        except:
            return "Não foi possível conectar ao servidor"
    else:
        return "Nome inválido"

def login(client: socket.socket, username: str, password: str): #2 verifica se conta existe e entra 
    try:
        client.send(bytes("LOGN {"+username+"} {"+password+"}END\n",'utf-8'))
        resultado = client.recv(4096).decode()
        if resultado.split("END\n")[0] == "1":
            return 1
        else:
            return resultado.split("END\n")

    except:
        return "Não foi possível conectar ao servidor"

def logout(client: socket.socket): #fecha a conexão e guarda a ultima hora online
    client.send(bytes("LOGF END\n",'utf-8'))
    #fechar o socket do cliente
    client.close() 

def onlineUsers(client: socket.socket): #lista de usuários online
    client.send(bytes("LIUS END\n",'utf-8'))
    resposta = client.recv(4096).decode().split("END\n")
    online = resposta.split()
    return online

def listaUsers(client: socket.socket): #lista de usuários 
    client.send(bytes("LTUS END\n",'utf-8'))
    resposta = client.recv(4096).decode().split("END\n")
    listaUsuarios = resposta[0].split()
    return listaUsuarios

def mostrarPerfil(client: socket.socket, user: str): #busca as infos do usuário
    client.send(bytes("USER {"+user+"}END\n",'utf-8'))
    resposta = client.recv(4096).decode().split("END\n")
    info = resposta[0].split()
    return info 

def criaGrupo(client: socket.socket, gcName:  str): 
    if nomeValido(gcName): #caracteres invalidos = " ,.;}{[]@*"
        client.send(bytes("MKGC {"+gcName+"}END\n",'utf-8'))
        resposta = client.recv(4096).decode().split("END\n")
        if resposta == "1":
            return "Grupo criado com sucesso!"
        else:
            return resposta
    else:
        return "Nome inválido"


def addGrupo(client: socket.socket, group: str, user: str):
    client.send(bytes("ATGC {"+group+"} {"+user+"}END\n",'utf-8'))
    resposta = client.recv(4096).decode().split("END\n")
    if resposta == "1":
        return "Adicionado com sucesso!"
    else:
        return resposta
    
def saiGrupo(client: socket.socket, group: str):
    client.send(bytes("LVGC {"+group+"}END\n",'utf-8'))
    resposta = client.recv(4096).decode().split("END\n")
    if resposta == "1":
        return "Removido com sucesso!"
    else:
        return resposta

def deletaGrupo(client: socket.socket, group: str): #apaga o prupo
    client.send(bytes("DLGC {"+group+"}END\n",'utf-8'))
    resposta = client.recv(4096).decode().split("END\n")
    if resposta == "1":
        return "Grupo deletado com sucesso!"
    else:
        return resposta

def requestGrupo(client: socket.socket, group: str):
    client.send(bytes("REGC {"+group+"}END\n",'utf-8'))
    return "Request feita"

def listaRequest(client: socket.socket, group: str):
    client.send(bytes("LRGC {"+group+"}END\n",'utf-8'))
    resposta = client.recv(4096).decode().split("END\n")
    listaR = resposta.split()
    return listaR

def rmvGrupo(client: socket.socket, group: str, user:str): #remove usuário do grupo
    try:
        client.send(bytes("RMGC {"+group+"} {"+user+"}END\n",'utf-8'))
        return "Usuário removido com sucesso!"
    except:
        return "Não foi possível remover o usuário: " + user 
    
def carregaGrupo(client: socket.socket): #lista de grupos s
    client.send(bytes("LIGC END\n",'utf-8'))
    resposta = client.recv(4096).decode().split("END\n")
    grupos = resposta[0].split()
    return grupos[:-1]

def carregaMsg(client: socket.socket, group: str): #carrega as mensagens do arquivo .txt do servidor
    lista_msg = []
    r = ""
    client.send(bytes("LOAD {"+ group +"} END\n",'utf-8'))
    resposta = client.recv(4096)
    if len(resposta) == 4096:
        while len(resposta) == 4096:
            r += resposta.decode()
            resposta = client.recv(4096)
    else:
        r = resposta.decode()

    
    mensagens = r.split("@")

    for msg in mensagens:
        msgf = msg[1:-1].split("} {")
        mensagem = "-> "+ msgf[0] + " (" + msgf[1] + ") - " + msgf[2]
        lista_msg.append(mensagem) #ajustar para o prograva de visualização
    lista_msg[-1] = lista_msg[-1][:-4]
    return lista_msg

def listaAdm(client: socket.socket, group: str): 
    client.send(bytes("LADM {"+group+"}END\n",'utf-8'))
    resposta = client.recv(4096).decode().split("END\n")
    listaA = resposta.split()
    return listaA

def makeAdm(client: socket.socket, group: str, name: str):
    client.send(bytes("MADM {"+group+"} {"+name+"}END\n",'utf-8'))
    resposta = client.recv(4096).decode().split("END\n")
    return resposta

def enviaMgs(client: socket.socket, group: str, mensagem: str):
    try:
        client.send(bytes("MSGS {"+group+"} {"+mensagem+"}END\n",'utf-8'))
    except:
        print("Falha na conexão...")

def recebeMgs(client: socket.socket): #(PUSH é enviado e chama essa função)
    while True:
        try:
            resposta = client.recv(4096).decode().split("END\n")
            msg = resposta.split("PUSH")
            msgf = msg[1:-1].split("} {")
            mensagem = "-> "+ msgf[0] + " (" + msgf[1] + ") - " + msgf[2]
        except:
            print("Falha na conexão...")
            break

def uArq(client: socket.socket,group: str, nomeArq: str, arq): #upload
    #arq é o endereço do arquivo
    tamanhoArq = os.path.getsize(arq)
    client.send(bytes("SARQ {"+group+"} {"+nomeArq+"} {"+str(tamanhoArq)+"}END\n",'utf-8')) #SARQ
    resposta = client.recv(4096).decode().split("END\n")
    if resposta == "PODE MANDAR":
        with open(arq,"rb") as file:
            client.sendfile(file)
            return "Arquivo enviado"

def dArq(client: socket.socket, group: str, nomeArq: str): #download
    client.send(bytes("RARQ {"+group+"} {"+nomeArq+"}END\n",'utf-8')) #RARQ
    respostaS = client.recv(4096).decode().split("END\n")
    print(respostaS)
    respostaC = input("deseja baixar esse arquivo? \n")
    if respostaC == "SIM":
        client.send(bytes(respostaC,'utf-8'))
        with open(nomeArq, 'wb') as file:
            while 1:
                data = client.recv(4096)
                if not data:
                    break
                file.write(data)
    else:
        pass


def listaArq(client: socket.socket, group: str): #mostra lista de arquivos du grupo
    client.send(bytes("LARQ {"+group+"}END\n",'utf-8'))
    resposta = client.recv(4096).decode().split("END\n")
    listaArq = resposta.split()
    return listaArq

def ping(client: socket.socket): #testa se há conexão (avisa apenas se não tiver)
    try:
        client.send(bytes("PING END\n", 'utf-8'))
        resposta = client.recv(4096).decode().split("END\n")
        try:
            client.send(bytes("PING END\n", 'utf-8'))
        except:
            return "ERRO na conexão"
    except:
        return "ERRO na conexão"

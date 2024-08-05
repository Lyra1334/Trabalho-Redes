import socket, threading, datetime, os

def serve_client(soquete : socket.socket, user : str, endereco, semaforoOnline : threading.Lock, semaforoLogin : threading.Lock, fila = []):

    retorno = ""
    quebrar = False
    horarioUltimaComm = datetime.datetime.now()

    soquete.sendall(bytes("1END\n","utf-8"))


    soquete.sendall(bytes(retorno.strip(),"utf-8"))
    
    while True:
        
        
        while len(fila) != 0:
            
            numPac = 0
            adminsDoChat = []
            chatsDoUsuario = []
            usuariosDoChat = []
            requestsDoGrupo = []
            texto = ""
            retorno = ""
            comando = fila[0]
            admin = False
            documento = []

            match comando[0]:

            
                case "MSGS":
                    #O cliente deseja mandar uma mensagem
                    print("to mandando uma mensagem")

                    retorno = "{"+user+"} {"+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)+"} {"+comando[2]+"}"
                    #Arruma o formato de uma mensagem, para guardar e mandar de volta

                    if os.path.exists("servidorRedes/chats/"+comando[1]):
                        #Verificando se o grupo existe mesmo
                        print("o grupo "+comando[1]+" existe")

                        if comando[1] != "all":

                            usuariosDoChat = listarUsuariosDeUmChat(comando[1])

                        
                        if comando[1] == "all":

                            soquete.sendall(bytes("1END\n",'utf-8'))

                            with open("servidorRedes/chats/"+comando[1]+"/log.txt","a") as log:
                                log.write(retorno+"\n")

                            #O grupo all é o de todos usuários
                            semaforoOnline.acquire_lock()

                            for Usuario in usuariosOnline:
                                
                                if Usuario != user:
                                    print("mandei pro usuario "+Usuario)
                                    #processos[Usuario][0].sendall(bytes("PUSH "+retorno+"END\n","utf-8"))

                            
                            semaforoOnline.release_lock()
                        

                        elif (user in usuariosDoChat):
                            #Verifica primeiro se o grupo é um dos grupos do usuário

                            soquete.sendall(bytes("1END\n",'utf-8'))

                            with open("servidorRedes/chats/"+comando[1]+"/log.txt","a") as log:
                                log.write(retorno+"\n")
                            
                            for usuario in usuariosDoChat:
                                if usuario in usuariosOnline:
                                    pass
                                    #processos[usuario][0].sendall(bytes("PUSH "+retorno+"END\n",'utf-8'))

                                        

                        else:
                            soquete.sendall(bytes("ERRO Você não está no grupo.END\n",'utf-8'))

                    else:
                        soquete.sendall(bytes("ERRO Grupo não existe.END\n",'utf-8'))

                case "USER":
                    #USER {usuario}
                    
                    if comando[1] in usuarios.keys():

                        retorno = usuarios[comando[1]][1]+" "+usuarios[comando[1]][2]+" END\n"
                        soquete.sendall(bytes(retorno,'utf-8'))
                    else:
                        soquete.sendall(bytes("ERRO Usuário não encontrado.END\n",'utf-8'))

                case "LIUS":
                    #Lista os usuários online


                    semaforoOnline.acquire_lock()

                    for usuario in usuariosOnline:
                        retorno += usuario+" "

                    semaforoOnline.release_lock()
                    retorno+= "END\n"
                    soquete.sendall(bytes(retorno.strip(),"utf-8"))

                case "LTUS":
                    
                    semaforoLogin.acquire_lock()
                    for usuario in list(usuarios.keys()):
                        retorno += usuario+" "
                    semaforoLogin.release_lock()

                    retorno+= "END\n"
                    soquete.sendall(bytes(retorno.strip(),"utf-8"))


                case "NUSR":
                    #Cria novo usuário.

                    semaforoLogin.acquire_lock()

                    with open("servidorRedes/users.txt", "a") as docLogin:
                        docLogin.write(comando[1]+" "+comando[2]+"\n")

                    os.mkdir("servidorRedes/usuarios/"+comando[1])
                    with open("servidorRedes/usuarios/"+comando[1]+"/chats.txt", 'w') as listadechats:
                        listadechats.write("\n")

                    usuarios[comando[1]] = comando[2]
                    semaforoLogin.release_lock()
                
                case "DELE":
                    chatsDoUsuario = listarChatsDeUmUsuario(user)
                    fila = [[]]

                    for chat in chatsDoUsuario:
                        usuariosDoChat = listarUsuariosDeUmChat(chat)

                        if  len(usuariosDoChat) == 1:
                            fila.append([["DLGC"][chat]])

                        else:
                            adminsDoChat = listarAdminsDeUmChat(chat)
                            if (len(adminsDoChat) == 1) and (adminsDoChat[0] == user):
                                with open("servidorRedes/chats/"+chat+"/admins.txt","w") as listaDeAdmins:
                                    listaDeAdmins.write(usuariosDoChat[0]+"\n")
                    
                    os.system("rm -r servidorRedes/usuarios/"+user)

                    fila.append([["LOGF"]])

                case "LOGF":
                    #Desloga e fecha o thread.
                    semaforoOnline.acquire_lock()
                    processos.pop(user)
                    usuariosOnline.remove(user)
                    semaforoOnline.release_lock()
                    quebrar = True

                case "LOAD":

                    if os.path.exists("servidorRedes/chats/"+comando[1]):
                        if comando[1] != "all":
                            usuariosDoChat = listarUsuariosDeUmChat(comando[1])
                        if (user in usuariosDoChat) or (comando[1] == "all"):
                            with open("servidorRedes/chats/"+comando[1]+"/log.txt", "r") as logDoGrupo:
                                retorno = ""
                                texto = logDoGrupo.readline().strip()
                                while texto != "":
                                    retorno += texto+"@"
                                    texto = logDoGrupo.readline().strip()
                                retorno = retorno[:-1]


                                soquete.sendall(bytes(retorno+"END\n",'utf-8'))
                        
                        else:
                            soquete.sendall(bytes("ERRO Você não está no grupo.END\n",'utf-8'))
                    
                    else:
                        soquete.sendall(bytes("ERRO Grupo não existe.END\n",'utf-8'))



                case "MKGC":
                    #cria um chat

                    if os.path.exists("servidorRedes/chats/"+comando[1]) == False:

                        soquete.sendall(bytes("1END\n",'utf-8'))

                        os.mkdir("servidorRedes/chats/"+comando[1])
                        
                        with open("servidorRedes/chats/"+comando[1]+"/admins.txt","w") as listaDeAdmins:
                            listaDeAdmins.write(user)

                        with open("servidorRedes/chats/"+comando[1]+"/log.txt","w") as log:
                            log.write("")

                        with open("servidorRedes/chats/"+comando[1]+"/requests.txt","w") as listaDeReq:
                            listaDeReq.write("")

                        os.mkdir("servidorRedes/chats/"+comando[1]+"/arquivos")

                        with open("servidorRedes/usuarios/"+user+"/chats.txt", "a") as listaDeChats:
                            listaDeChats.write("\n"+comando[1])
                    else:
                        soquete.sendall(bytes("ERRO Grupo já existe.END\n",'utf-8'))


                case "LVGC":

                    if os.path.exists("servidorRedes/chats/"+comando[1]):
                        usuariosDoChat = listarUsuariosDeUmChat(comando[1])

                        if user in usuariosDoChat:

                            soquete.sendall(bytes("1END\n",'utf-8'))

                            with open("servidorRedes/usuarios/"+user+"/chats.txt","r") as listadechats:
                                texto = listadechats.readline().strip()
                                while texto != "":
                                    documento.append(texto)
                                    texto = listadechats.readline().strip()

                            with open("servidorRedes/usuarios/"+user+"/chats.txt","w") as listadechats:
                                for linha in documento:
                                    if linha != comando[1]:
                                        listadechats.write(linha+"\n")
                        else:
                            soquete.sendall(bytes("ERRO Usuário não está no grupo.END\n",'utf-8'))

                    
                    else:
                        soquete.sendall(bytes("ERRO Grupo não existe.END\n",'utf-8'))

                case "ATGC": #{grupo} {nome}
                    #Adiciona o usuario em um grupo
                    adminsDoChat = listarAdminsDeUmChat(comando[1])
                    
                    
                    if os.path.exists("servidorRedes/chats/"+comando[1]):
                        if user in adminsDoChat:

                            usuariosDoChat = listarUsuariosDeUmChat(comando[1])

                            if comando[2] not in usuariosDoChat:

                                requestsDoGrupo = listarRequestsDeUmGrupo(comando[1])

                                if comando[2] in requestsDoGrupo:

                                    with open("servidorRedes/chats/"+comando[1]+"/requests.txt","r") as listaDeReq:
                                        texto = listaDeReq.readline().strip()
                                        while texto != "":
                                            documento.append(texto)
                                            texto = listaDeReq.readline().strip()

                                    with open("servidorRedes/chats/"+comando[1]+"/requests.txt","w") as listaDeReq:
                                        for linha in documento:
                                            if linha != comando[2]:
                                                listaDeReq.write(linha+"\n")

                                soquete.sendall(bytes("1END\n",'utf-8'))

                                with open("servidorRedes/usuarios/"+comando[2]+"/chats.txt","w") as listadechats:
                                    listadechats.write(comando[1]+"\n")
                            
                            else:
                                soquete.sendall(bytes("ERRO Usuário já estava no grupo.END\n",'utf-8'))
                        
                        else:
                            soquete.sendall(bytes("ERRO Precisa ser administrador para executar a ação.END\n",'utf-8'))
                    else:
                        soquete.sendall(bytes("ERRO Grupo não existe.END\n",'utf-8'))
                        
                case "REGC":

                    requestsDoGrupo = listarRequestsDeUmGrupo(comando[1])
                    


                    if user not in requestsDoGrupo:
                        usuariosDoChat = listarUsuariosDeUmChat(comando[1])

                        if user not in usuariosDoChat:
                            soquete.sendall(bytes("1END\n",'utf-8'))
                            with open("servidorRedes/chats/"+comando[1]+"/requests.txt", "a") as requests:
                                requests.write(user+"\n")

                        else:
                            soquete.sendall(bytes("ERRO Usuário já está no grupo.END\n",'utf-8'))
                    else:

                        soquete.sendall(bytes("ERRO Usuário já pediu para participar.END\n",'utf-8'))
                
                case "LRGC":

                    requestsDoGrupo = listarRequestsDeUmGrupo(comando[1])


                    for req in requestsDoGrupo:
                        retorno += req+" "
                        
                    retorno += "END\n"
                    soquete.sendall(bytes(retorno.strip(),"utf-8"))



                case "RMGC":

                    adminsDoChat = listarAdminsDeUmChat(comando[1])
                    
                    
                    if os.path.exists("servidorRedes/chats/"+comando[1]):

                        if user in adminsDoChat:

                            usuariosDoChat = listarUsuariosDeUmChat(comando[1])

                            if comando[2] in usuariosDoChat:

                                soquete.sendall(bytes("1END\n",'utf-8'))

                                with open("servidorRedes/usuarios/"+comando[2]+"/chats.txt","r") as listadechats:
                                    texto = listadechats.readline().strip()
                                    while texto != "":
                                        documento.append(texto)
                                        texto = listadechats.readline().strip()

                                with open("servidorRedes/usuarios/"+comando[2]+"/chats.txt","w") as listadechats:
                                    for linha in documento:
                                        if linha != comando[1]:
                                            listadechats.write(linha+"\n")
                                
                                documento = []

                                if comando[2] in adminsDoChat:
                                    with open("servidorRedes/chats/"+comando[1]+"/admins.txt","r") as listaDeAdm:
                                        texto = listaDeAdm.readline().strip()
                                        while texto != "":
                                            documento.append(texto)
                                            texto = listaDeAdm.readline().strip()

                                    with open("servidorRedes/chats/"+comando[1]+"/admins.txt","w") as listaDeAdm:
                                        for linha in documento:
                                            if linha != comando[2]:
                                                listaDeAdm.write(linha+"\n")
                            
                            else:
                                soquete.sendall(bytes("ERRO Usuário não está no grupo.END\n",'utf-8'))

                        else:
                            soquete.sendall(bytes("ERRO Precisa ser administrador para executar a ação.END\n",'utf-8'))
                    else:
                        soquete.sendall(bytes("ERRO Grupo não existe.END\n",'utf-8'))
                

                case "DLGC":
                    
                    adminsDoChat = listarAdminsDeUmChat(comando[1])
                    if os.path.exists("servidorRedes/chats/"+comando[1]):
                        if user in adminsDoChat:

                            soquete.sendall(bytes("1END\n",'utf-8'))
                    
                            usuariosDoChat = listarUsuariosDeUmChat()
                            #nesse for removemos menções do chat dos outros usuários
                            for usuario in usuariosDoChat:

                                with open("servidorRedes/usuarios/"+usuario+"/chats.txt","r") as listadechats:
                                    texto = listadechats.readline().strip()
                                    while texto != "":
                                        documento.append(texto)
                                        texto = listadechats.readline().strip()

                                with open("servidorRedes/usuarios/"+usuario+"/chats.txt","w") as listadechats:
                                    for linha in documento:
                                        if linha != comando[1]:
                                            listadechats.write(linha+"\n")
                        
                            #agora deletamos o documento dele
                            os.system("rm -r servidorRedes/chats/"+comando[1])
                        
                        else:
                            soquete.sendall(bytes("ERRO Precisa ser administrador para executar a ação.END\n","utf-8"))

                    else:
                        soquete.sendall(bytes("ERRO Grupo não existe.END\n","utf-8"))
                
                
                case "LIGC":
                    #Lista os chats que o usuário faz parte

                    chatsDoUsuario = listarChatsDeUmUsuario(user)

                    for chat in chatsDoUsuario:
                        retorno += chat+" "
                        
                    retorno += "END\n"
                    soquete.sendall(bytes(retorno.strip(),"utf-8"))

                case "MADM": #{grupo} {nome}

                    if os.path.exists("servidorRedes/chats/"+comando[1]):
                        adminsDoChat = listarAdminsDeUmChat(comando[1])
                        if user in adminsDoChat:
                            if comando[2] not in adminsDoChat:

                                usuariosDoChat = listarUsuariosDeUmChat(comando[1])

                                if comando[2] in usuariosDoChat:

                                    soquete.sendall(bytes("1END\n",'utf-8'))

                                    with open("servidorRedes/chats/"+comando[1]+"/admins.txt","a") as listaDeAdmins:
                                        listaDeAdmins.write("\n"+comando[2])
                                
                                else:
                                    soquete.sendall(bytes("ERRO Usuário não está no grupo.END\n",'utf-8'))

                            else:
                                soquete.sendall(bytes("ERRO Usuário já era administrador.END\n",'utf-8'))
                        
                        else:
                            soquete.sendall(bytes("ERRO Precisa ser administrador para executar a ação.END\n","utf-8"))
                    
                    else:
                        soquete.sendall(bytes("ERRO Grupo não existe.END\n","utf-8"))


                case "LADM":
                    if os.path.exists("servidorRedes/chats/"+comando[1]):

                        adminsDoChat = listarAdminsDeUmChat(comando[1])

                        for admin in adminsDoChat:
                            retorno += admin+" "
                        
                        retorno += "END\n"
                        soquete.sendall(bytes(retorno.strip(),"utf-8"))


                case "SARQ":
                    #SARQ {nomeDoChat} {Nome do arquivo} {tamanho do arquivo} END\n ARQUIVO
                    comando[3] =  int(comando[3])

                    arquivosDoChat = listarArquivosDeUmChat(comando[1])
                    if comando[2] not in arquivosDoChat:

                        soquete.sendall(bytes("PODE MANDAREND\n","utf-8"))

                        with open("servidorRedes/chats/"+comando[1]+"/arquivos/"+comando[2],"wb") as newArquivo:

                            numPac = comando[3]//4096
                            if numPac > 0:
                                for _ in range(numPac):
                                    newArquivo.write(soquete.recv(4096))

                            newArquivo.write(soquete.recv(comando[3]%4096))

                case "RARQ":
                    #RARQ {nomeDoChat} {nomeDoArq}

                    arquivosDoChat = listarArquivosDeUmChat(comando[1])

                    if comando[2] in arquivosDoChat:

                        tamanhoDoArq = os.path.getsize("servidorRedes/chats/"+comando[1]+"/arquivos/"+comando[2])

                        soquete.sendall(bytes("ARQ {"+str(tamanhoDoArq)+"}END\n","utf-8"))
                        texto = soquete.recv(4096).decode().strip()

                        if texto == "SIM":
                            with open("servidorRedes/chats/"+comando[1]+"/arquivos/"+comando[2],"r") as arq:
                                soquete.sendfile(arq)
                        else:
                            soquete.sendall(bytes("1END\n","utf-8"))


                case "LARQ":

                    arquivosDoChat = listarArquivosDeUmChat(comando[1])

                    for arquivo in arquivosDoChat:
                        retorno += arquivo+" "
                        
                    retorno += "END\n"
                    soquete.sendall(bytes(retorno.strip(),"utf-8"))

                case "PING":
                    soquete.sendall(bytes("RINGEND\n","utf-8"))

                case "RING":
                    print("ping!")
                            
                case _:
                    print("nn li nada to burrão")

            fila.pop(0)

        fila = reader(soquete)

        #esse aqui era pra ser o teste de conexão mas eu nn tenho certeza. descartar para os testes iniciais pfv

        """
        if fila != []:
            horarioUltimaComm = datetime.datetime.now()
        else:
            if horarioUltimaComm.minute != datetime.datetime.now().minute:

                soquete.sendall(bytes("PINGEND\n","utf-8"))
        """

        if quebrar == True:
            break

    soquete.shutdown(2)
    soquete.close()

def listarUsuariosDeUmChat(nomeDoChat):
    lista = []
    nome = ''
    for usuario in os.listdir("servidorRedes/usuarios"):
        with open("servidorRedes/usuarios/"+usuario+"/chats.txt","r") as grupos:
            nome = grupos.readline().strip()
            while nome != "":
                if nome == nomeDoChat:
                    lista.append(usuario)
                nome = grupos.readline().strip()

    return lista[:]

def listarChatsDeUmUsuario(nomeDoUsuario):
    lista = []
    nome = ''
    with open("servidorRedes/usuarios/"+nomeDoUsuario+"/chats.txt", "r") as grupos:
        nome = grupos.readline().strip()
        while nome != "":
            lista.append(nome)
            nome = grupos.readline().strip()
    return lista[:]

def listarRequestsDeUmGrupo(nomeDoGrupo):
    lista = []
    nome = ''
    with open("servidorRedes/chats/"+nomeDoGrupo+"/requests.txt", "r") as requests:
        nome = requests.readline().strip()
        while nome != "":
            lista.append(nome)
            nome = requests.readline().strip()
    return lista[:]

def listarAdminsDeUmChat(nomeDoChat):
    lista = []
    nome = ''
    with open("servidorRedes/chats/"+nomeDoChat+"/admins.txt", "r") as grupos:
        nome = grupos.readline().strip()
        while nome != "":
            lista.append(nome)
            nome = grupos.readline().strip()
    
    return lista[:]

def listarChatsQueUmUsuarioEAdmin(nomeDoUsuario):
    chats = []
    lista = []
    nome = ''
    with open("servidorRedes/usuarios/"+nomeDoUsuario+"/chats.txt", "r") as grupos:
        nome = grupos.readline().strip()
        while nome != "":
            chats.append(nome)
            nome = grupos.readline().strip()

    for chat in chats:
        with("servidorRedes/chats/"+chat+"/admins.txt", "r") as listaDeAdmins:
            nome = listaDeAdmins.readline().strip()
            if nome == nomeDoUsuario:
                lista.append(chat)

    return lista[:]

def listarArquivosDeUmChat(nomeDoChat):
    return os.listdir("servidorRedes/chats/"+nomeDoChat+"/arquivos")


def reader(sock : socket.socket):
    string = ""
    lista = []
    comando = []

    novo = sock.recv(4096)

    if len(novo) == 4096:

        while len(novo) == 4096:
            string += novo.decode()
            novo = sock.recv(4096)

    else:
        string = novo.decode()
    

    lista = string.split("END\n")

    for i in range(len(lista)):
        lista[i] = lista[i].strip()

        if len(lista[i]) == 4:
            lista[i] = [lista[i]]

        else:
            comando = [lista[i][:4]]
            lista[i] = lista[i][4:]
            começoArg = lista[i].find('{')
            fimArg = lista[i].find('}')

            while (começoArg != -1) and (fimArg != -1):
                comando.append(lista[i][começoArg+1:fimArg].strip())
                lista[i] = lista[i][fimArg+1:]
                começoArg = lista[i].find("{")
                fimArg = lista[i].find('}')

            lista[i] = comando[:]
    if lista[:-1] != []:
        print("Comandos recebidos:",lista[:-1])
    return lista[:-1]
    


string = []

global processos, usuariosOnline, usuarios
processos = dict()
usuariosOnline = []
usuarios = dict()

conector = socket.socket()
host = "192.168.15.5"
port = 45454
conector.bind((host,port))
conector.listen(5)
semDicUs = threading.Lock()
listaOnlineLib = threading.Lock()

semDicUs.acquire_lock()
with open("servidorRedes/users.txt","r") as info:
    string = info.readline().strip()
    while string != "":
        string = string.split()
        usuarios[string[0]] = string[1:]
        string = info.readline().strip()
semDicUs.release_lock()


while True:

    novo = conector.accept()
    string = reader(novo[0])


    if string[0][0] == "NUSR":

        if string[0][1] not in usuarios.keys():

            semDicUs.acquire_lock()

            with open("servidorRedes/users.txt", "a") as docLogin:
                docLogin.write('\n'+string[0][1]+" "+string[0][2]+" "+string[0][3]+" "+string[0][4])

            os.mkdir("servidorRedes/usuarios/"+string[0][1])
            with open("servidorRedes/usuarios/"+string[0][1]+"/chats.txt", 'w') as listadechats:
                listadechats.write("")

            usuarios[string[0][1]] = [string[0][2],string[0][3],string[0][4]]
            semDicUs.release_lock()
                        
            if len(string) > 1:
                processos[string[0][1]] = (novo[0],novo[1],threading.Thread(target=serve_client,args=(novo[0],string[0][1],novo[1],listaOnlineLib, semDicUs, string[1:])))

            else:
                processos[string[0][1]] = (novo[0],novo[1],threading.Thread(target=serve_client,args=(novo[0],string[0][1],novo[1],listaOnlineLib, semDicUs)))

            processos[string[0][1]][2].start()
            listaOnlineLib.acquire_lock()
            usuariosOnline.append(string[0][1])
            listaOnlineLib.release_lock()
            

        else:
            novo[0].send(bytes("ERRO Já existe um usuário com esse nome.END\n",'utf-8'))


    elif string[0][0] == "LOGN":

        if (string[0][1] in usuarios.keys()) and (string[0][1] not in usuariosOnline):
            print("loguei "+ string[0][1])

            if usuarios[string[0][1]][0] == string[0][2]:
                if len(string) > 1:
                    processos[string[0][1]] = (novo[0],novo[1],threading.Thread(target=serve_client,args=(novo[0],string[0][1],novo[1],listaOnlineLib, semDicUs, string[1:])))

                else:
                    processos[string[0][1]] = (novo[0],novo[1],threading.Thread(target=serve_client,args=(novo[0],string[0][1],novo[1],listaOnlineLib, semDicUs)))

                processos[string[0][1]][2].start()
                listaOnlineLib.acquire_lock()
                usuariosOnline.append(string[0][1])
                listaOnlineLib.release_lock()
            
            else:
                novo[0].sendall(bytes("ERRO Senha incorreta.END\n","utf-8"))

        elif string[0][1] in usuariosOnline:
            novo[0].sendall(bytes("ERRO Usuário já logado.END\n","utf-8"))

    else:
        novo[0].sendall(bytes("ERRO Faça login antes de tentar outras ações.END\n","utf-8"))

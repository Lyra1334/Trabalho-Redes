

from encodings import search_function
from tkinter import END, RIGHT, Canvas, Listbox, PhotoImage, Scrollbar, messagebox, scrolledtext
import customtkinter
import tkinter as tk
import threading, socket, os
import Cliente


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

janela = customtkinter.CTk()

janela.geometry("700x550")

janela.title("Chat")


global usuarioo, varisock

framejanela = customtkinter.CTkFrame(master=janela) 
framejanela.pack(padx=50, pady=30)

texto = customtkinter.CTkLabel(master=framejanela, text= "Login de usuário:", font=("Arial", 24, "bold"))
texto.place(x=25, y=5)
texto.pack(padx=20, pady=20)


usuario = customtkinter.CTkEntry(master=framejanela,
                                 placeholder_text="E-mail:", width=200, height=10)
usuario.pack(padx=20, pady=20)

senha = customtkinter.CTkEntry(master=framejanela,
                               placeholder_text="Senha:",
                               show="*",width=200, height=10)
senha.pack(padx=20, pady=20)

pin = customtkinter.CTkEntry(master=framejanela, 
                             placeholder_text=" IP:", width=200, height=10 )
pin.pack(padx=20, pady=20)

portaServidor = customtkinter.CTkEntry(master=framejanela,
                                       placeholder_text="Porta do servidor:", width=200, height=10)
portaServidor.pack(padx=20, pady=20)

def menuPrincipal(username):
    if True:
        framejanela.pack_forget()
        frameMenu = customtkinter.CTkFrame(master=janela)
        frameMenu.pack(fill="both", expand=True)



        listaconversas = customtkinter.CTkScrollableFrame(master=frameMenu)
        listaconversas.pack(fill="both", expand=True)

        frame_pesquisa = customtkinter.CTkFrame(listaconversas)
        frame_pesquisa.pack(pady=20, padx=20, fill='x', anchor='n')

        # Barra de pesquisa
        barra_pesquisa = customtkinter.CTkEntry(frame_pesquisa,
                                                placeholder_text="Pesquisar por grupo...",
                                                placeholder_text_color="grey",
                                                width=540)
                                                
        barra_pesquisa.grid(row=0, column=0, padx=(5, 30))

        # Botão ao lado da barra de pesquisa
        botao_pesquisa = customtkinter.CTkButton(frame_pesquisa, text="Buscar", command=lambda: print("Pesquisando..."),width=5)
        botao_pesquisa.grid(row=0, column=1)



        grupoAll = customtkinter.CTkButton(master=listaconversas, text="all", width=300,command= lambda n="all" : open_chat_window(n))
        grupoAll.pack(pady=5)

        listaDeGrupos = Cliente.carregaGrupo(varisock)
        print(listaDeGrupos)
        botoesgrupo = dict()

        for grupo in listaDeGrupos:
            botoesgrupo[grupo] = customtkinter.CTkButton(master=listaconversas, text=grupo, command= lambda n=grupo : open_chat_window(n), width=300).pack(pady=5)
        

        areaMenu = customtkinter.CTkFrame(master=frameMenu, corner_radius=0)
        areaMenu.pack(side="right", expand=True, padx=5, pady=5)

        def volta():
            #frameMenu.pack_forget()
            #framejanela.pack(padx=50, pady=30)
            Cliente.logout(varisock)
            janela.destroy()

            
        
        def perfil(user):
            frameMenu.pack_forget()
            frameperfil = customtkinter.CTkFrame(master=janela)
            frameperfil.pack(fill="both", expand=True)

            listaDeInfo = Cliente.mostrarPerfil(varisock, user)

            user_data = {
                "username": user,
                "email": listaDeInfo[0],
                "localização": listaDeInfo[1],
                }
            
            def atualizaLabels():
                username.configure(text=user_data["username"])
                email.configure(text=f"Email: {user_data['email']}")
                localizacao.configure(text=f"Localização: {user_data['localização']}")
                #ip.configure(text=f"IP: {user_data['ip']}")
                #servidor.configure(text=f"Porta do servidor: {user_data['servidor']}")
                #telefone.configure(text=f"Telefone: {user_data['telefone']}")
                #recado.configure(text=f"Status: {user_data['recado']}")

            # Função de edição de perfil
            """
            def editaperfil():
            #    frameperfil.pack_forget()
                frameeditor = customtkinter. CTkFrame(master=janela)
                frameeditor.pack(fill="both", expand=True)

                

                # Widgets para edição
                customtkinter.CTkLabel(frameeditor, text="Nome de Usuário:").pack(pady=5)
                username_entry = customtkinter.CTkEntry(frameeditor, width=250)
                username_entry.insert(0, user_data["username"])
                username_entry.pack(pady=5)

                customtkinter.CTkLabel(frameeditor, text="Email:").pack(pady=5)
                email_entry = customtkinter.CTkEntry(frameeditor, width=250)
                email_entry.insert(0, user_data["email"])
                email_entry.pack(pady=5)

                #customtkinter.CTkLabel(frameeditor, text="Ip:").pack(pady=5)
                #ip_entry = customtkinter.CTkEntry(frameeditor, width=250)
                #ip_entry.insert(0, user_data["ip"])
                #ip_entry.pack(pady=5)

                #customtkinter.CTkLabel(frameeditor, text="Porta do servidor:").pack(pady=5)
                #servidor_entry = customtkinter.CTkEntry(frameeditor, width=250)
                #servidor_entry.insert(0, user_data["servidor"])
                #servidor_entry.pack(pady=5)

                #customtkinter.CTkLabel(frameeditor, text="Telefone:").pack(pady=5)
                #telefone_entry = customtkinter.CTkEntry(frameeditor, width=250)
                #telefone_entry.insert(0, user_data["telefone"])
                #telefone_entry.pack(pady=5)

                customtkinter.CTkLabel(frameeditor, text="Status:").pack(pady=5)
                recado_entry = customtkinter.CTkEntry(frameeditor, width=250)
                recado_entry.insert(0, user_data["recado"])
                recado_entry.pack(pady=5)


                #def save_changes():
                #    user_data["username"] = username_entry.get()
                #    user_data["email"] = email_entry.get()
                #    user_data["ip"] = ip_entry.get()
                #    user_data["servidor"] = servidor_entry.get()
                #    user_data["telefone"] = telefone_entry.get()
                #    user_data["recado"] = recado_entry.get()

                #    atualizaLabels()

                #    frameeditor.pack_forget()
                #    frameperfil.pack(fill="both", expand=True)
                    
                customtkinter.CTkButton(frameeditor, text="Salvar", command=save_changes).pack(pady=20)
            """

            #imagem
            #avatar = PhotoImage(file="projeto redes/avatardefault_92826.png") 
            #avatarlabel = customtkinter.CTkLabel(frameperfil, image=avatar, text="")
            #avatarlabel.pack(pady=10)
            

            # Nome de usuário

            LabelNome = customtkinter.CTkLabel(frameperfil, text=username, font=("Arial", 24, "bold"))
            LabelNome.pack(pady=10)

            #editar = customtkinter.CTkButton(frameperfil, text="Editar Perfil", command=editaperfil)
            #editar.pack(pady=10)
            

            # separador das informações pessoais
            separator = customtkinter.CTkFrame(frameperfil, height=2, width=600)
            separator.pack(pady=2)
            separator.pack_propagate(0)

            info = customtkinter.CTkFrame(frameperfil, width=600, height=300)
            info.pack(pady=20)
            info.pack_propagate(0)


            
            email = customtkinter.CTkLabel(info, text=f"Email: {user_data['email']}", font=("Arial", 16))
            email.pack(pady=10, anchor="w")

            
            localizacao = customtkinter.CTkLabel(info, text=f"Localização: {user_data['localização']}", font=("Arial", 16))
            localizacao.pack(pady=10, anchor="w")
        
            #servidor = customtkinter.CTkLabel(info, text=f"Porta do servidor: {user_data['servidor']}", font=("Arial", 16))
            #servidor.pack(pady=10, anchor="w")

            #telefone = customtkinter.CTkLabel(info, text=f"Telefone: {user_data['telefone']}", font=("Arial", 16))
            #telefone.pack(pady=10, anchor="w")

            #recado = customtkinter.CTkLabel(info, text=f"Status: {user_data['recado']}",font=("Arial", 16) )
            #recado.pack(pady=10, anchor="w")


            def vo():
                frameperfil.pack_forget()
                frameMenu.pack(fill="both", expand=True)

            vol = customtkinter.CTkButton(info, text="Voltar", width=10, command=vo )
            vol.pack(pady=10)




    
        meuPerfil = customtkinter.CTkButton(master=areaMenu, text="Meu perfil ", fg_color="green", width=120, height=20,
                                            command=lambda user=username :perfil(user)) #lambda n=grupo : open_chat_window(n)
        meuPerfil.pack(side="left", padx=20, pady=10)
        
        group_data = {
        "group_name": "",
        "description": "",
        "members": []
        }

        # Lista de grupos criados
        groups_list = []

        # Função para atualizar a lista de membros
        def update_member_listbox(member_listbox):
            member_listbox.delete(0, END)
            for member in group_data["members"]:
                member_listbox.insert(END, member)

        # Função para adicionar membro
        def add_member(member_entry, member_listbox):
            new_member = member_entry.get()
            if new_member:
                group_data["members"].append(new_member)
                update_member_listbox(member_listbox)
                member_entry.delete(0, END)

        # Função para criar o grupo
        def create_group(group_name_entry, description_entry):
            group_data["group_name"] = group_name_entry.get()
            group_data["description"] = description_entry.get()
            groups_list.append(group_data.copy())
            print("Grupo Criado:")
            print("Nome do Grupo:", group_data["group_name"])
            print("Descrição:", group_data["description"])
            print("Membros:", group_data["members"])
            create_group_window.destroy()
            update_groups_listbox()

        # Função para atualizar a lista de grupos
        def update_groups_listbox():
            for widget in groups_frame.winfo_children():
                widget.destroy()
            for group in groups_list:
                group_button = customtkinter.CTkButton(groups_frame, text=group["group_name"], command=lambda g=group: open_chat_window(g["group_name"]))
                group_button.pack(pady=5)

        # Função para abrir a tela de criação de grupo
        def open_create_group_window():
            global create_group_window
            create_group_window = customtkinter.CTkToplevel(janela)
            create_group_window.title("Criar Grupo de Chat")
            create_group_window.geometry("700x550")

            # Frame principal
            main_frame = customtkinter.CTkFrame(create_group_window, width=660, height=510)
            main_frame.pack(pady=20, padx=20)

            # Nome do grupo
            customtkinter.CTkLabel(main_frame, text="Nome do Grupo:", font=("Arial", 16)).pack(pady=5, anchor="w")
            group_name_entry = customtkinter.CTkEntry(main_frame, width=400)
            group_name_entry.pack(pady=5)

            # Descrição do grupo
            customtkinter.CTkLabel(main_frame, text="Descrição:", font=("Arial", 16)).pack(pady=5, anchor="w")
            description_entry = customtkinter.CTkEntry(main_frame, width=400)
            description_entry.pack(pady=5)

            # Adicionar membros
            customtkinter.CTkLabel(main_frame, text="Adicionar Membros:", font=("Arial", 16)).pack(pady=5, anchor="w")
            member_entry = customtkinter.CTkEntry(main_frame, width=250)
            member_entry.pack(pady=5)
            add_member_button = customtkinter.CTkButton(main_frame, text="Adicionar Membro", command=lambda: Cliente.addGrupo(varisock, group_name_entry.get(), member_entry.get())
)
            add_member_button.pack(pady=5)

            # Lista de membros
            customtkinter.CTkLabel(main_frame, text="Membros do Grupo:", font=("Arial", 16)).pack(pady=5, anchor="w")
            member_listbox = Listbox(main_frame, width=50, height=10)
            member_listbox.pack(pady=5)

            # Botão de criação de grupo
            create_group_button = customtkinter.CTkButton(main_frame, text="Criar Grupo", command=lambda: Cliente.criaGrupo(varisock, group_name_entry.get()))
            create_group_button.pack(pady=20)

        # Função para abrir a tela do chat do grupo
        def open_chat_window(group_name):

            frameMenu.pack_forget()
            frameChat2 = customtkinter.CTkFrame(master=janela)
            frameChat2.pack(fill="both", expand=True)

            def enviar_mensagem(grupo):
                mensagem = message_entry.get()
                if mensagem:
                    #chat_text.insert(customtkinter.END, f"Você: {mensagem}\n")
                    message_entry.delete(0, customtkinter.END)
                    Cliente.enviaMgs(varisock,grupo,mensagem)
                    atualizar(group_name)
                    atualizar(group_name)
                    

            # Função para resposta automática
            def resposta_automatica(mensagem):
                for msg in lista_msg:
                    resposta = f"resposta: '{msg}'"
                    chat_text.insert(customtkinter.END, f"{resposta}\n")


            #lista_msg = Cliente.carregaMsg
            #for msg in lista_msg:
            #    label = customtkinter.CTkLabel(chat_frame, text=msg)
            #    label.pack(pady=20, padx=20)

            #Thread1 = threading.Thread(target= Cliente.recebeMgs, args=[varisock]) #aqui para testes, mas tera q ser ativado na troca de telas
            Thread2 = threading.Thread(target= Cliente.enviaMgs, args=[varisock])

            #    chat_text.config(state=tk.NORMAL)
            #    chat_frame.insert(tk.END, msg)
            #    chat_text.config(state=tk.DISABLED)
            #    message_entry.delete(0, tk.END)

           # def send_message():
            #    message = message_entry.get()
            #    Cliente.enviaMgs(varisock, message)    

                    
                # Aqui você pode adicionar a lógica para enviar a mensagem para um servidor ou outro usuário.

            # Frame para o chat
            chat_frame = customtkinter.CTkFrame(frameChat2)
            chat_frame.pack(pady=10, padx=10, fill="both", expand=True)

            # Área de texto para o chat
            chat_text = tk.Text(chat_frame, state=tk.DISABLED, wrap=tk.WORD)#, bg="#F0F0F0" 
            chat_text.pack(padx=5, pady=5, fill="both", expand=True)

            # Frame para a entrada de mensagem
            input_frame = customtkinter.CTkFrame(frameChat2)
            input_frame.pack(pady=10, padx=10, fill="x")

            # Caixa de entrada de mensagem
            message_entry = customtkinter.CTkEntry(input_frame)
            message_entry.pack(side="left", fill="x", expand=True, padx=5)

            # Botão de enviar mensagem
            send_button = customtkinter.CTkButton(input_frame, text="Enviar", command=lambda n=group_name : enviar_mensagem(n))
            send_button.pack(side="right", padx=5)

            # Botão para abrir a janela de perfil

            def volt():
                frameChat2.pack_forget()
                frameMenu.pack(fill="both", expand=True)


            def dadosgrupo(nome):
                frameChat2.pack_forget()
                framedadosgrup = customtkinter.CTkFrame(master=janela)
                framedadosgrup.pack(fill="both", expand=True)

                customtkinter.CTkLabel(framedadosgrup, text="Nome do Grupo:", font=("Arial", 16)).pack(padx=50,pady=20, anchor="w")

                customtkinter.CTkLabel(framedadosgrup, text="Descrição:", font=("Arial", 16)).pack(padx=50,pady=20, anchor="w")

                customtkinter.CTkLabel(framedadosgrup, text="Membros do Grupo:", font=("Arial", 16)).pack(padx=50, pady=5, anchor="w")

                listamembros = Listbox(framedadosgrup, width=50, height=10)
                listamembros.pack(padx=50, pady=5)

                membro = customtkinter.CTkEntry(framedadosgrup, width=250)
                membro.pack(pady=5)

                addmembro = customtkinter.CTkButton(framedadosgrup, text="Adicionar Membro", command= lambda grupo=nome, userBox=membro:butAdicionar(grupo,userBox) )
                addmembro.pack(pady=5)

                remove = customtkinter.CTkButton(framedadosgrup, text="Remover Membro")
                remove.pack(pady=5)

                salvar = customtkinter.CTkButton(framedadosgrup, text="Salvar Alterações")
                salvar.pack(pady=20)

                def butAdicionar(nomDeGrup, caixaDeEntrada):
                    Cliente.addGrupo(varisock,nomDeGrup,caixaDeEntrada.get())

                def voltaaaa():
                    framedadosgrup.pack_forget()
                    frameChat2.pack(fill="both", expand=True)

                customtkinter.CTkButton(framedadosgrup, text="Voltar", width=20, height=10,
                                        command=voltaaaa).pack(side = "right", pady=20)

                sair = customtkinter.CTkButton(framedadosgrup, text="Sair do grupo",text_color="red", width=10, height=2)
                sair.pack(side="right", pady=10)


            def atualizar(grupoAtual):
                chat_text.configure(state=tk.NORMAL)
                chat_text.delete(1.0, customtkinter.END)
                #enviar_mensagem()
                #resposta_automatica()
                listaDeMsgs = Cliente.carregaMsg(varisock, grupoAtual)
                
                for msg in listaDeMsgs:
                    chat_text.insert(tk.END,msg+"\n")
                chat_text.configure(state=tk.DISABLED)
                

            atualiza = customtkinter.CTkButton(frameChat2, text="Atualizar", width=10, command=lambda n=group_name: atualizar(n))
            atualiza.pack(side="left", padx=10, pady=10)


            opcao = customtkinter.CTkButton(frameChat2, text="Opções", width=10, command=lambda n=group_name:dadosgrupo(n))
            opcao.pack(side="left", padx=10, pady=10)


            enviaraquivos = customtkinter.CTkButton(frameChat2, text="Enviar arquivo")
            enviaraquivos.pack(side="right", padx=15, pady=10)

            voltaaa = customtkinter.CTkButton(frameChat2, text="Voltar",command=volt, width=10)
            voltaaa.pack(side = "left", padx=10, pady=10)

            atualizar(group_name)



        

        # Frame para os botões dos grupos criados
        groups_frame = customtkinter.CTkFrame(master=listaconversas, width= 300)
        groups_frame.pack(pady=20)


        
        
        


        criarGrupo = customtkinter.CTkButton(master=areaMenu, text="+ Novo grupo ", fg_color="green", width=120, height=20, 
                                            command=open_create_group_window)
        criarGrupo.pack(side="left", padx=20, pady=10)

        def meuscontatos():
            frameMenu.pack_forget()
            frameMeuscontatos = customtkinter.CTkFrame(master=janela)
            frameMeuscontatos.pack(fill="both", expand=True)
            contatos = Cliente.listaUsers(varisock)
            for contato in contatos:
                customtkinter.CTkButton(frameMeuscontatos, text=contato, command=perfil, width=300)
                #contato1.pack(pady=5)



        contatos = customtkinter.CTkButton(master=areaMenu, text="Meus contatos", fg_color="green", width=120, height=20,command=meuscontatos)
        contatos.pack(side="left", padx=20, pady=10)

        voltaa = customtkinter.CTkButton(master=areaMenu, text="Sair", fg_color="green", width=120, height=20,
                                        command=volta)
        voltaa.pack(side="left", padx=20, pady=10)
  


def logar():
    global varisock
    varisock = Cliente.main()
    usuarioo = usuario.get()
    resultado = Cliente.login(varisock, usuario.get(), senha.get())
    print(resultado)
    if resultado == 1:
        menuPrincipal(usuarioo)
    else:
        pass

    


botaologin = customtkinter.CTkButton(master=framejanela, text="Entrar",
                                command=logar)
botaologin.pack(padx=20, pady=20)



def telacadastro():
    #exclui tela de login 
    framejanela.pack_forget()

    #tela de cadastro 
    framecadastro = customtkinter.CTkFrame(master=janela) 
    framecadastro.pack(padx=200, pady=40)

    textoc = customtkinter.CTkLabel(master=framecadastro, text= " Cadastro de usuário:",font=("Arial", 24, "bold"))
    

    nome = customtkinter.CTkEntry(master=framecadastro, 
                                  placeholder_text="Crie um nome de usuário:", width=200, height=10)
    
    
    senhac = customtkinter.CTkEntry(master=framecadastro,
                                placeholder_text="Crie uma senha:",
                                show="*",width=200, height=10)


    usuarioc = customtkinter.CTkEntry(master=framecadastro,
                                    placeholder_text="Informe seu e-mail:", width=200, height=10)
    

 
    localizacao = customtkinter.CTkEntry(master=framecadastro, 
                                placeholder_text="Informe sua localização:", width=200, height=10 )
    

    

    

    
    #termo= customtkinter.CTkCheckBox(master=framecadastro, text="Aceito todos os termos e políticas").place(x=10, y=365)
    
    def salva():
        global varisock
        mensagem = messagebox.showinfo(title="Status do cadastro", message="Usuário cadastrado com sucesso!")

        usuarioo = usuarioc.get()
        varisock = Cliente.main()
        r = Cliente.criarConta(varisock, nome.get(), senhac.get(), usuarioc.get(), localizacao.get() )
        print(r)
        if r == 1:
            framecadastro.pack_forget()
            menuPrincipal(usuarioo)

        
    
    usuarioo = nome.get()

    

    botaosalvarcadastro = customtkinter.CTkButton(master=framecadastro, text="Salvar novo usuário",
                                        command=salva)
    
    def voltar():
        framecadastro.pack_forget()
        framejanela.pack(padx=50, pady=30)

    botaovoltar = customtkinter.CTkButton(master=framecadastro, text="Voltar",
                                          command=voltar)
    
    textoc.pack(padx=20, pady=20)
    nome.pack(padx=20, pady=20)
    senhac.pack(padx=20, pady=20)
    usuarioc.pack(padx=20, pady=20)  
    localizacao.pack(padx=20, pady=20)
    botaosalvarcadastro.pack(side="left", padx=20, pady=10)
    botaovoltar.pack(side="left", padx=20,pady=10)



botaocadastro = customtkinter.CTkButton(master=framejanela, fg_color="green", text="Cadastrar",
                                        command= telacadastro)
botaocadastro.pack(padx=30, pady=10)

    





janela.mainloop()
import tkinter as tk
from tkinter import messagebox

#  armazenar usuários e senhas
usuarios = {}

def criar_usuario():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    if usuario in usuarios:
        messagebox.showerror("Erro", "Usuário já existe.")
    elif not usuario or not senha:
        messagebox.showerror("Erro", "Usuário e senha não podem estar vazios.")
    else:
        usuarios[usuario] = senha
        messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
        entrada_usuario.delete(0, tk.END)
        entrada_senha.delete(0, tk.END)

def verificar_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    if usuarios.get(usuario) == senha:
        messagebox.showinfo("Login bem-sucedido", "Bem-vindo, {}!".format(usuario))
    else:
        messagebox.showerror("Erro de Login", "Usuário ou senha incorretos.")


login= tk.Tk()
login.title("Tela de Login")
login.geometry("300x250")
login.resizable(False, False)
# largura = login.winfo_screenwidth()
# altura = login.winfo_screenheight()
# login.geometry(f"{largura}x{altura}")

#  entrada para o usuário
rotulo_usuario = tk.Label(login, text="Usuário:")
rotulo_usuario.pack(pady=5)
entrada_usuario = tk.Entry(login)
entrada_usuario.pack(pady=5)

# entrada para a senha
rotulo_senha = tk.Label(login, text="Senha:")
rotulo_senha.pack(pady=5)
entrada_senha = tk.Entry(login, show="*")
entrada_senha.pack(pady=5)

#  criar usuário e login
botao_criar = tk.Button(login, text="Criar Usuário", command=criar_usuario)
botao_criar.pack(pady=10)

botao_login = tk.Button(login, text="Login", command=verificar_login)
botao_login.pack(pady=10)


login.mainloop()

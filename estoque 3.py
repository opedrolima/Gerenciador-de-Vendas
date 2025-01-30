import tkinter as tk
import ttkbootstrap as ttk
import pandas as pd
import sqlite3
from tkinter import messagebox, filedialog, Label, Entry, Button

# Caminho do banco de dados SQLite
CAMINHO_BANCO = "dados.db"

# Função para criar a tabela no banco de dados se não existir
def criar_tabela():
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dados (
                nome_do_produto TEXT PRIMARY KEY,
                und TEXT,
                codigo TEXT, 
                estoque INTEGER,
                custo REAL,
                preco REAL
            )
        """)
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Erro ao criar a tabela: {e}")
    finally:
        conn.close()

# Função para carregar os dados do banco de dados para o DataFrame
def carregar_dados():
    global df
    conn = sqlite3.connect(CAMINHO_BANCO)
    df = pd.read_sql_query("SELECT * FROM dados", conn)
    conn.close()
    atualizar_treeview()

# Função para salvar o DataFrame em um arquivo Excel
def salvar_excel():
    caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])
    if caminho_arquivo:
        df.to_excel(caminho_arquivo, index=False, engine='openpyxl')
        print(f"Arquivo salvo em: {caminho_arquivo}")

# Função para salvar o DataFrame no banco de dados
def salvar_dados():              
    global df
    conn = sqlite3.connect(CAMINHO_BANCO)
    df.to_sql("dados", conn, if_exists="replace", index=False)
    conn.close()

# Função para adicionar uma linha ao DataFrame e atualizar a Treeview
def adicionar_linha():
    global df
    nome_do_produto_valor = entry_nome_do_produto.get().strip()
    und_valor = combobox_und.get().strip()  # Obter o valor do Combobox
    codigo_valor = entry_codigo.get().strip()
    estoque_valor = entry_estoque.get().strip()
    custo_valor = entry_custo.get().strip()
    preco_valor = entry_preco.get().strip()
    
    if not nome_do_produto_valor or not und_valor or not codigo_valor or not estoque_valor or not custo_valor or not preco_valor:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return
    
    try:
        estoque_valor = int(estoque_valor)
        custo_valor = float(custo_valor)
        preco_valor = float(preco_valor)
    except ValueError:
        messagebox.showerror("Erro", "Os campos 'Estoque', 'Custo' e 'Preço' devem ser numéricos!")
        return

    if nome_do_produto_valor in df['nome_do_produto'].values:
        messagebox.showinfo("Info", "O produto já existe. Atualize a linha existente se necessário.")
    else:
        nova_linha = pd.DataFrame({
            "nome_do_produto": [nome_do_produto_valor],
            "und": [und_valor],
            "codigo": [codigo_valor],
            "estoque": [estoque_valor],
            "custo": [custo_valor],
            "preco": [preco_valor]
        })
        df = pd.concat([df, nova_linha], ignore_index=True)
        salvar_dados()
        atualizar_treeview()
    
    # Limpar os campos após a inserção
    entry_nome_do_produto.delete(0, 'end')
    combobox_und.set('')  # Limpar o Combobox
    entry_codigo.delete(0, 'end')
    entry_estoque.delete(0, 'end')
    entry_custo.delete(0, 'end')
    entry_preco.delete(0, 'end')

# Função para atualizar a Treeview com o conteúdo do DataFrame
def atualizar_treeview():
    global df
    if df.empty:
        return
    
    for item in tree.get_children():
        tree.delete(item)

    for idx, row in df.iterrows():
        tree.insert('', 'end', iid=idx, values=list(row))

# Função para pesquisar produtos
def pesquisar():
    valor = entry_pesquisa.get().strip()
    if valor:
        resultado = df[df['codigo'] == valor]
        if resultado.empty:
            messagebox.showinfo("Resultado da Pesquisa", "Nenhum produto encontrado.")
        else:
            messagebox.showinfo("Resultado da Pesquisa", f"Produtos encontrados:\n{resultado}")
    else:
        messagebox.showwarning("Aviso", "Digite um código para pesquisa.")

# Função para importar dados de um arquivo CSV
def importar_csv():
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    if caminho_arquivo:
        try:
            dados_csv = pd.read_csv(caminho_arquivo)
            colunas_necessarias = {"nome_do_produto", "und", "codigo", "estoque", "custo", "preco"}
            if not colunas_necessarias.issubset(dados_csv.columns):
                messagebox.showerror("Erro", "O arquivo CSV deve conter as colunas necessárias.")
                return
            
            dados_csv = dados_csv.fillna('')
            global df
            df = pd.concat([df, dados_csv], ignore_index=True)
            salvar_dados()
            atualizar_treeview()
            print(f"Dados importados do arquivo: {caminho_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao importar o CSV: {e}")

# Configuração da interface gráfica
estoque = tk.Tk()
estoque.title("Estoque Casa dos Frios São José")
largura = estoque.winfo_screenwidth()
altura = estoque.winfo_screenheight()
estoque.geometry(f"{largura}x{altura}")

# Criar a tabela no banco de dados
criar_tabela()

# Frame de entrada
frame_entrada = tk.Frame(estoque)
frame_entrada.pack(pady=10)

# Campos de entrada
Label(frame_entrada, text="Nome do Produto:").grid(row=1, column=0)
entry_nome_do_produto = Entry(frame_entrada)
entry_nome_do_produto.grid(row=1, column=1)

# Combobox para a unidade com largura original e altura ajustada
Label(frame_entrada, text="Und:").grid(row=2, column=0)
options = ["Kg", "ml", "L", "G", "mg", "Unitario"]
combobox_und = ttk.Combobox(frame_entrada, values=options, width=17, height=5)  # Largura original e altura ajustada
combobox_und.grid(row=2, column=1)

Label(frame_entrada, text="Código:").grid(row=3, column=0)
entry_codigo = Entry(frame_entrada)
entry_codigo.grid(row=3, column=1)

Label(frame_entrada, text="Estoque:").grid(row=5, column=0)
entry_estoque = Entry(frame_entrada)
entry_estoque.grid(row=5, column=1)

Label(frame_entrada, text="Custo:").grid(row=6, column=0)
entry_custo = Entry(frame_entrada)
entry_custo.grid(row=6, column=1)

Label(frame_entrada, text="Preço:").grid(row=7, column=0)
entry_preco = Entry(frame_entrada)
entry_preco.grid(row=7, column=1)

# Campo de entrada para pesquisa
Label(frame_entrada, text="Pesquisar").grid(row=1, column=2)
entry_pesquisa = Entry(frame_entrada)
entry_pesquisa.grid(row=1, column=3)

# Treeview para exibir os dados
tree = ttk.Treeview(estoque, columns=("nome_do_produto", "und", "codigo", "estoque", "custo", "preco"), show='headings')
tree.heading("nome_do_produto", text="Nome do Produto", anchor="center")
tree.heading("und", text="Unidade", anchor="center")
tree.heading("codigo", text="Código", anchor="center")
tree.heading("estoque", text="Estoque", anchor="center")
tree.heading("custo", text="Custo", anchor="center")
tree.heading("preco", text="Preço",anchor="center")

tree.column("nome_do_produto", anchor="center")
tree.column("und", anchor="center")
tree.column("codigo", anchor="center")
tree.column("estoque", anchor="center")
tree.column("custo", anchor="center")
tree.column("preco", anchor="center")


tree.pack(pady=20)

# Carregar os dados
carregar_dados()

# Frame de Botões
frame_botoes = tk.Frame(estoque)
frame_botoes.pack(pady=10)
Button(frame_botoes, text="Adicionar", command=adicionar_linha, bg="gray", fg="black", font=("Arial", 12)).pack(side="left", padx=5)
Button(frame_botoes, text="Pesquisar", command=pesquisar, bg="gray", fg="black", font=("Arial", 12)).pack(side="left", padx=5)
Button(frame_botoes, text="Importar CSV", command=importar_csv, bg="gray", fg="black", font=("Arial", 12)).pack(side="left", padx=5)
Button(frame_botoes, text="Salvar Excel", command=salvar_excel, bg="gray", fg="black", font=("Arial", 12)).pack(side="left", padx=5)

# Iniciar a aplicação
estoque.mainloop()
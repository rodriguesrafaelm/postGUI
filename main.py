from tkinter import *
from tkinter import messagebox
import psycopg

with open('kwd.txt', 'r') as kwd: #kwd.txt é um arquivo no formato -> "host", "nome do bd", "usuario", "senha"
    infos = kwd.readlines()
    dbhost = infos[0].strip()
    db = infos[1].strip()
    dbuser = infos[2].strip()
    pwd = infos[3].strip()


def connect_db(): #conector
    con = psycopg.connect(host=dbhost,
                          dbname=db,
                          user=dbuser,
                          password=pwd)
    return con


def get_list():
    clear_list(limpardados=False)
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM clientes "
                "ORDER BY cliente_id")
    global row
    row = cur.fetchall()
    cur.close()
    for item in reversed(row):
        lista.insert(0, f'{item[0]:<27}{item[1]}')
    con.close()


def add_client():
    if checkbox_status.get() == 0:
        messagebox.showerror('Caixa de seleção', message='Marque a caixa "MODIFICAR TABELA" para continuar.')
        return
    if e_name.get() == '' or e_cpf.get() == '':
        messagebox.showerror('Falta de dados', message='Nome ou CPF em branco.')
        return

    con = connect_db()
    id_cliente = row[-1][0] + 1
    nome = e_name.get()
    cpf = e_cpf.get()
    telefone = e_phone.get()
    endereco = e_end.get()
    email = e_email.get()
    servico = e_servico.get()

    cur = con.cursor()
    try:
        cur.execute("INSERT INTO clientes (cliente_id, nome, cpf, telefone, endereco, email, servico)"
                    f"VALUES(%s, %s, %s, %s, %s, %s, %s)", (id_cliente, nome, cpf, telefone, endereco, email, servico))
    except psycopg.errors.UniqueViolation:
        messagebox.showerror('UniqueViolation', message='CPF já foi cadastrado préviamente')
    cur.close()
    con.commit()
    con.close()


def update_client():
    if checkbox_status.get() == 0:
        messagebox.showerror('Caixa de seleção', message='Marque a caixa "MODIFICAR TABELA" para continuar.')
        return
    dados=[]
    dados.append(e_id.get())
    con = connect_db()
    cur = con.cursor()
    dados.append(e_name.get())
    dados.append(e_cpf.get())
    dados.append(e_phone.get())
    dados.append(e_end.get())
    dados.append(e_email.get())
    dados.append(e_servico.get())
    for elemento in dados:
        elemento.replace('', 'null')
    try:
        cur.execute("UPDATE clientes "
                    f"SET nome = %s, "
                    f"cpf = %s, "
                    f"telefone = %s, "
                    f"endereco = %s, "
                    f"email = %s, "
                    f"servico = %s "
                    f"WHERE cliente_id = %s;", ([dados[1],dados[2] ,dados[3] ,dados[4] ,dados[5] ,dados[6]
                    ,dados[0]]))
    except psycopg.errors.UniqueViolation:
        messagebox.showerror('UniqueViolation', message='CPF já foi cadastrado préviamente')
    cur.close()
    con.commit()
    con.close()
    get_list()


def get_person():
    if e_id.get() != '':
        coluna = "cliente_id"
        dado = e_id.get()
    elif e_name.get() != '':
        coluna = "nome"
        dado = e_name.get().capitalize()
    elif e_cpf.get() != '':
        coluna = "cpf"
        dado = e_cpf.get()
    else:
        messagebox.showerror('Ausência de dados', message='Insira ID, Nome ou CPF para buscar.')
        return

    con = connect_db()
    cur = con.cursor()
    cur.execute(f"SELECT * FROM clientes WHERE {coluna} = %s;", ([dado]))
    cliente = cur.fetchone()
    clear_list()
    if cliente:
        lista.insert(0, cliente)
        e_id.insert(0, cliente[0])
        e_name.insert(0, cliente[1])
        e_cpf.insert(0, cliente[2])
        e_phone.insert(0, cliente[3])
        e_end.insert(0, cliente[4])
        e_email.insert(0, cliente[5])
        e_servico.insert(0, cliente[6])
    else:
        messagebox.showerror('Falha na busca', message='Verifique os dados inseridos e tente novamente')
    cur.close()
    con.close()


def remove_user():
    if checkbox_status.get() == 0:
        messagebox.showerror('Caixa de seleção', message='Marque a caixa "MODIFICAR TABELA" para continuar.')
        return
    if e_id.get() != '':
        id_cliente = e_id.get()
        msgbox = messagebox.askyesno(title='Deletar Cliente', message=f"Deseja deletar o cliente de id {id_cliente}?")
        if not msgbox:
            return
    else:
        lista.insert(0, 'DIGITE o ID para remover alguem')
        return

    con = connect_db()
    cur = con.cursor()
    cur.execute("DELETE FROM clientes "
                f"WHERE cliente_id = %s;", id_cliente)
    cur.close()
    con.commit()
    con.close()
    clear_list()


def clear_list(limparlista=True, limpardados=True):
    if limpardados:
        e_id.delete('0', 'end')
        e_name.delete('0', 'end')
        e_cpf.delete('0', 'end')
        e_phone.delete('0', 'end')
        e_end.delete('0', 'end')
        e_email.delete('0', 'end')
        e_servico.delete('0', 'end')
    if limparlista:
        lista.delete('0', 'end')


def onselect(event):
    try:
        w = event.widget
        index = int(w.curselection()[0])
        value = int(w.get(index)[0]) -1
        clear_list(limparlista=False)
        e_id.insert(0, row[value][0])
        e_name.insert(0, row[value][1])
        e_cpf.insert(0, row[value][2])
        e_phone.insert(0, row[value][3])
        e_end.insert(0, row[value][4])
        e_email.insert(0, row[value][5])
        e_servico.insert(0, row[value][6])
    except IndexError:
        pass

# Parte de configuração do GUI
root = Tk()
root.geometry("700x400")
root.title("SQL PYTHON TEST")
idlista = Label(root, text='ID do Cliente', font=('bold', 8))
idlista.place(x=390, y=15)
nomelista = Label(root, text='Nome do cliente', font=('bold', 8))
nomelista.place(x=470, y=15)
id = Label(root, text='Cliente ID', font=('bold', 10))
id.place(x=20, y=30)
name = Label(root, text='Nome', font=('Bold', 10))
name.place(x=20, y=60)
phone = Label(root, text='Telefone', font=('Bold', 10))
phone.place(x=20, y=90)
cpf = Label(root, text='CPF', font=('Bold', 10))
cpf.place(x=20, y=120)
end = Label(root, text='Endereço', font=('Bold', 10))
end.place(x=20, y=150)
email = Label(root, text='Email', font=('Bold', 10))
email.place(x=20, y=180)
servico = Label(root, text='Serviços em Aberto', font=('Bold', 10))
servico.place(x=20, y=210)
e_id = Entry()
e_id.place(x=150, y=30)
e_name = Entry()
e_name.place(x=150, y=60)
e_phone = Entry()
e_phone.place(x=150, y=90)
e_cpf = Entry()
e_cpf.place(x=150, y=120)
e_end = Entry()
e_end.place(x=150, y=150)
e_email = Entry()
e_email.place(x=150, y=180)
e_servico = Entry()
e_servico.place(x=150, y=210)
exibirlista = Button(root, text="Mostrar Todos", font=("italic", 10), bg="white", command=get_list)
exibirlista.place(x=18, y=340)
insert = Button(root, text="Adicionar", font=("italic", 10), bg="white", command=add_client)
insert.place(x=20, y=300)
delete = Button(root, text='Deletar Cliente', font=("italic", 10), bg="white", command=remove_user)
delete.place(x=600, y=330)
update = Button(root, text='Atualizar', font=("italic", 10), bg="white", command=update_client)
update.place(x=90, y=300)
get = Button(root, text='Buscar', font=("italic", 10), bg="white", command=get_person)
get.place(x=180, y=300)
clear = Button(root, text='Limpar', font=("italic", 10), bg="white", command=clear_list)
clear.place(x=235, y=300)
checkbox_status = IntVar()
checkbox = Checkbutton(root, text='MODIFICAR TABELA', variable=checkbox_status)
checkbox.place(x=20, y=250)
lista = Listbox(root, width=50)
lista.place(x=390, y=30)
lista.bind("<<ListboxSelect>>", onselect)
get_list()  # First fetch to set variables
root.mainloop()

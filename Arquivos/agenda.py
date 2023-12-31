import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

def deletar(treeview):
    try:
        item = treeview.selection()
        valor = treeview.item(item, 'values')
        treeview.delete(item)

        banco = sqlite3.connect('Agenda.db')
        
        cursor = banco.cursor()
        cursor.execute("DELETE FROM 'Agenda' WHERE Telefone = '" + valor[1] + "'")
        
        banco.commit()
    except:
        messagebox.showerror("Aviso!!!", "Selecione o ítem que pretendes excluir")
    
def guardar(contacto, nome, treeview, c, n):
    if contacto == '' or nome == '':
        messagebox.showwarning("Aviso!!!", "Preencha todos os campos.")
        return 5
    try:
        banco = sqlite3.connect("Agenda.db")
        
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE 'Agenda' (Nome TEXT, Telefone TEXT)")
        
        cursor.execute(f"INSERT INTO 'Agenda' VALUES('{nome}', '{contacto}')")
        
        banco.commit()
        banco.close()
        
        messagebox.showinfo("Aviso!!!", "Contacto guardado com muito sucesso!!!")
        treeview.insert("", END, values=(nome, contacto))
        c.set("")
        n.set("")
    except:
        banco = sqlite3.connect("Agenda.db")
        
        cursor = banco.cursor()
        
        cursor.execute(f"INSERT INTO 'Agenda' VALUES('{nome}', '{contacto}')")
        
        banco.commit()
        banco.close()
        messagebox.showinfo("Aviso!!!", "Contacto guardado com muito sucesso!!!")
        treeview.insert("", END, values=(nome, contacto))
        c.set("")
        n.set("")
# ! CONFIGURAÇÃO DA JANELA
window = Tk()
window.geometry('500x500+450+120')
window["bg"] = '#ABCDEF'
window.title('Agenda')
window.iconbitmap('Ícones e imagem/NoteBook1.ico')
window.resizable(False, False)
window["cursor"] = ""
# ! CONFIGURAÇÃO DA JANELA

# ? CONFIGURAÇÃO DO CABEÇALHO
titulo = Label(window, text="Minha agenda", bg='#ABCDEF')
titulo['font'] = ["Monotype Corsiva", 20]
titulo.place(x=170, y=10)

img = PhotoImage(file='Ícones e imagem/NoteBook1.png')
img = img.subsample(5, 5)
imagem = Label(window, image=img, bg='#ABCDEF')
imagem.place(x=210, y=50)
# ? CONFIGURAÇÃO DO CABEÇALHO

# * CONFIGURAÇÃO DO TREEVIEW
tv = ttk.Treeview(window, columns=("nome", "telefone"), show="headings")
tv.column("nome", minwidth=0, width=230)
tv.column("telefone", minwidth=0, width=170)
tv.heading("nome", text="Nome:")
tv.heading("telefone", text="Telefone:")
tv.place(x=50, y=120)
# * CONFIGURAÇÃO DO TREEVIEW
try:
    banco = sqlite3.connect("Agenda.db")

    cursor = banco.cursor()
    lista = cursor.execute("SELECT * FROM 'Agenda'")

    banco.commit()
    for (n, num) in lista:
        tv.insert("", END, values=(n, num))
except:
    print()


# - CONFIGURAÇÃO DAS LABEL DAS ENTRADAS DE TEXTO

texto_1 = Label(window, text="Nome:", bg="#ABCDEF", font=("Times new Roman", 13, "bold"))
texto_1.place(x=50, y=365)

texto_1 = Label(window, text="Contacto:", bg="#ABCDEF", font=("Times new Roman", 13, "bold"))
texto_1.place(x=50, y=425)

# - CONFIGURAÇÃO DAS LABEL DAS ENTRADAS DE TEXTO

# ! CONFIGURAÇÃO DAS ENTRADAS DE TEXTO
in_1 = StringVar()
entrada_1 = Entry(window, width=30, font=("Times new Roman", 13), textvariable=in_1)
entrada_1.place(x=50, y=390)

in_2 = StringVar()
entrada_2 = Entry(window, width=30, font=("Times new Roman", 13), textvariable=in_2)
entrada_2.place(x=50, y=450)
# ! CONFIGURAÇÃO DAS ENTRADAS DE TEXTO

# ? CONFIGURANDO OS BOTÕES NECESSÁRIOS
botao_guardar = Button(window, text="guardar",
                       width=7,
                       font=("Times new Roman", 10)
                       , bg="green",
                       command=lambda: guardar(entrada_2.get(), entrada_1.get(), tv, in_1, in_2))
botao_guardar.place(x=389, y=390)

botao_deletar = Button(window,
                       text="deletar",
                       width=7,
                       font=("Times new Roman", 10),
                       bg="red",
                       command=lambda: deletar(tv))
botao_deletar.place(x=389, y=443)
# ? CONFIGURANDO OS BOTÕES NECESSÁRIOS

window.mainloop()
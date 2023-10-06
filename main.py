import tkinter
from tkinter import ttk
import sqlite3

class Funcs():
    def conectar_db(self):
        self.conn = sqlite3.connect('tarefas.db')
        self.cursor = self.conn.cursor()
    def desconectar_db(self):
        self.conn.close()
    def criar_lista(self):
        self.conectar_db()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tarefas (
            codigo INTEGER PRIMARY KEY,
            nome_tarefa CHAR(40) NOT NULL,
            data_criacao CHAR(40),
            prazo CHAR(40),
            conclusao CHAR(40)
            );
        """)
        self.conn.commit()
        self.desconectar_db()
    def limpar_entrys(self):
        self.tarefa_entry.delete(0, 'end')
        self.prazo_entry.delete(0, 'end')
        self.codigo_entry.delete(0, 'end')

    def var_entrys(self):
        self.tarefa = self.tarefa_entry.get()
        self.prazo = self.prazo_entry.get()
        self.conclusao = False
        self.data_criacao = 0
        self.codigo = self.codigo_entry.get()

    def atualizar_lista(self):
        self.tarefas.delete(*self.tarefas.get_children())
        self.conectar_db()
        lista = self.cursor.execute("""SELECT codigo, nome_tarefa, conclusao, prazo, data_criacao FROM tarefas
            ORDER BY codigo ASC;
        """)
        for i in lista:
            self.tarefas.insert('', 'end', values=i)
        self.desconectar_db()
    def add_tarefa(self):
        self.var_entrys()
        self.conectar_db()
        self.cursor.execute("""INSERT INTO tarefas(nome_tarefa, data_criacao, prazo, conclusao)
            VALUES(?,?,?,?)
        """, (self.tarefa, self.data_criacao, self.prazo, self.conclusao))
        self.conn.commit()
        self.desconectar_db()
        self.limpar_entrys()
        self.atualizar_lista()
    def OnDoubleClick(self, event):
        self.limpar_entrys()
        self.tarefas.selection()
        for n in self.tarefas.selection():
            col0 , col1, col2, col3, col4 = self.tarefas.item(n, 'values')
            self.codigo_entry.insert('end', col0)
            self.tarefa_entry.insert('end', col1)
            self.prazo_entry.insert('end', col3)
    def del_tarefa(self):
        self.var_entrys()
        self.conectar_db()
        self.conn.execute("""DELETE FROM tarefas WHERE codigo = ?""", (self.codigo,))
        self.conn.commit()
        self.desconectar_db()
        self.limpar_entrys()
        self.atualizar_lista()
    def edt_tarefa(self):
        self.var_entrys()
        self.conectar_db()
        self.cursor.execute("""UPDATE tarefas SET nome_tarefa = ?, prazo = ?
            WHERE codigo = ?
        """,(self.tarefa, self.prazo, self.codigo,))
        self.conn.commit()
        self.desconectar_db()
        self.limpar_entrys()
        self.atualizar_lista()
    def conc_tarefa(self):
        self.var_entrys()
        self.conclusao = True
        self.conectar_db()
        self.cursor.execute("""UPDATE tarefas SET conclusao = ?
            WHERE codigo = ?""", (self.conclusao, self.codigo,))
        self.conn.commit()
        self.desconectar_db()
        self.limpar_entrys()
        self.atualizar_lista()
class App(Funcs):
    def __init__(self):
        self.root = tkinter.Tk()
        self.variaveis()
        self.criar_lista()
        self.config()
        self.widget()
        self.frame_01()
        self.lista_tarefas()
        self.atualizar_lista()
        self.root.mainloop()
    def variaveis(self):
        self.cor_fundo_root = '#3a3636'
        self.cor_fundo_tabela = '#7a7474'
        self.titulo_fonte = ('Times', 22)
        self.label_fonte = ('Times', 18)
        self.fg_root = 'White'
    def config(self):
        self.root.title('to-do')
        self.root.geometry('400x600')
        self.root.configure(bg=self.cor_fundo_root)
    def widget(self):
        #Label Title
        self.titulo = tkinter.Label(self.root, text='To-Do App', fg=self.fg_root,
                               bg=self.cor_fundo_root, font=self.titulo_fonte).pack()
        #Label Tarefa
        self.label_tarefa = tkinter.Label(self.root, text='Tarefa', fg=self.fg_root,
                                     bg=self.cor_fundo_root, font=self.label_fonte).place(x=35, y=80)
        #Entry Tarefa
        self.tarefa_entry = tkinter.Entry(self.root)
        self.tarefa_entry.place(x=37, y=110)

        #Label Prazo
        self.label_prazo = tkinter.Label(self.root, text='Prazo', fg=self.fg_root,
                                    bg=self.cor_fundo_root, font=self.label_fonte).place(x=35, y=160)
        #Entry Prazo
        self.prazo_entry = tkinter.Entry(self.root)
        self.prazo_entry.place(x=37, y=190)

        # Entry Codigo
        self.codigo_entry = tkinter.Entry(self.root)

        #Botão Adicionar Tarefa
        self.bt_add = tkinter.Button(self.root, text='Adicionar Tarefa',
                                width=13, command=self.add_tarefa).place(x=265, y=80)
        # Botão Editar Tarefa
        self.bt_edt = tkinter.Button(self.root, text='Editar Tarefa',
                                width=13, command=self.edt_tarefa).place(x=265, y=120)
        # Botão Deletar Tarefa
        self.bt_del = tkinter.Button(self.root, text='Deletar Tarefa',
                                width=13, command=self.del_tarefa).place(x=265, y=160)
        # Botão Concluir Tarefa
        self.bt_conc = tkinter.Button(self.root, text='Concluir Tarefa',
                                     width=13, command=self.conc_tarefa).place(x=265, y=200)

    def frame_01(self):
        self.frame_tarefas = tkinter.Frame(self.root, bg= self.cor_fundo_tabela,
                                      width=370 ,height=305).place(x=16, y=275)
    def lista_tarefas(self):
        self.tarefas = ttk.Treeview(self.frame_tarefas, height=11, columns=('col1', 'col2', 'col3', 'col4'))
        self.tarefas.heading('#0', text='')
        self.tarefas.heading('#1', text='Codigos')
        self.tarefas.heading('#2', text='Tarefas')
        self.tarefas.heading('#3', text='Conclusão')
        self.tarefas.heading('#4', text='Prazo')
        self.tarefas.column('#0', width=0)
        self.tarefas.column('#1', width=55)
        self.tarefas.column('#2', width=140)
        self.tarefas.column('#3', width=65)
        self.tarefas.column('#4', width=75)
        self.tarefas.place(x=25,y=300)
        self.tarefas.bind("<Double-1>", self.OnDoubleClick)
        self.scroll_tarefas = tkinter.Scrollbar(self.frame_tarefas, orient='vertical', width=16, command=self.tarefas.yview)
        self.tarefas.configure(yscrollcommand=self.scroll_tarefas.set)
        self.scroll_tarefas.place(x=361, y=301, height=244)

App()

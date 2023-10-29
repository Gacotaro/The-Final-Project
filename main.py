#Импотр библиотек
import tkinter as tk
from tkinter import ttk
import sqlite3

#Класс главного окна, на котором будут располагаться кнопки, таблица 
class Main(tk.Frame):
    #Метод инициализатора 
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    #Метод добавления интерфейса на главное окно(Кнопки, таблица, панель инструментов)
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e8', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file='./img/add.png')
        button_open_dialog = tk.Button(
            toolbar, bg='#d7d8e8', bd=0, image=self.add_img, command=self.open_dialog)
        button_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', "tel", 'email', 'zp'), height=45, show='headings')
        
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('zp', width=150, anchor=tk.CENTER)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')            
        self.tree.heading('email', text='E-mail')
        self.tree.heading('zp', text='Заработная плата')

        self.tree.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e8', bd=0, image=self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e8', bd=0, image=self.delete_img, command=self.delete_record)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e8', bd=0, image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e8', bd=0, image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)
        
    #Метод связи дочернего окна с кнопкой добавления контакта
    def open_dialog(self):
        Child()
    
        #Метод записи значений в таблицу 
    def records(self, name, tel, email, zp):
        self.db.insert_data(name, tel, email, zp)
        self.view_records()

    #Метод отображения значений в таблице 
    def view_records(self):
        self.db.c.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    #Метод связи дочернего окна с кнопкой изменения таблицы
    def open_update_dialog(self):
        Update()

    #Метод записи изменений в контакты таблицы
    def update_records(self, name, tel, email, zp):
        self.db.c.execute('UPDATE db SET name=?, tel=?, email=?, zp=? WHERE id=?', (name, tel, email, zp, self.tree.set(self.tree.selection()[0], '#1')),)
        self.db.conn.commit()
        self.view_records()

    #Метод записи удаления контактов из таблицы 
    def delete_record(self):
        for select_item in self.tree.selection():
            self.db.c.execute('DELETE FROM db WHERE id=?', self.tree.set(select_item, '#1'))
        self.db.conn.commit()
        self.view_records()

    #Метод связи дочернего окна с кнопкой поиска по имени
    def open_search_dialog(self):
        Search()

    #Метод записи поиска контакта по имени
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute('SELECT * FROM db WHERE name LIKE ?', (name))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

#Класс окна добавления контактов
class Child(tk.Toplevel):
    #Метод инициализатора
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    #Метод добавления интерфейса но окно поиска(Кнопки, строки для вписывания данных)
    def init_child(self):
        self.title('Добавить контакт')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        
        self.label_name = tk.Label(self, text='ФИО:')
        self.label_name.place(x=50, y=30)
        self.label_select = tk.Label(self, text='Телефон:')
        self.label_select.place(x=50, y=60)
        self.label_sum = tk.Label(self, text='E-mail:')
        self.label_sum.place(x=50, y=90)
        self.label_zp = tk.Label(self, text='Заработная плата:')
        self.label_zp.place(x=50, y=120)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=30)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=60)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=90)
        self.entry_zp = ttk.Entry(self)
        self.entry_zp.place(x=200, y=120)

        self.btn_cansel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cansel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')   
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event:
                         self.view.records(self.entry_name.get(),
                                           self.entry_email.get(),
                                           self.entry_tel.get(),
                                           self.entry_zp.get()))
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')

#Класс окна изменения данных контакта
class Update(Child):
    #Метод инициализатора
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    #Метод добавления интерфейса на окно изменения (Кнопки, строки для изменения данных)
    def init_edit(self):
        self.title('Редактирование контакта')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=210, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_records(self.entry_name.get(),
                                               self.entry_email.get(),
                                               self.entry_tel.get(),
                                               self.entry_zp.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    #Метод добавления интерфейса на окно изменения (Кнопки, строки для изменения данных)
    def default_data(self):
        self.db.c.execute('SELECT * FROM db WHERE id=?', (self.view.tree.set(self.view.tree.selection() [0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_zp.insert(0, row[4])

#Класс окна поиска по имени 
class Search(tk.Toplevel):
    #Метод инициализатора
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    #Метод добавления интерфейса из окна поиска (Кнопки, сторока для поиска)
    def init_search(self):
        self.title('Поиск контакта')
        self.geometry('300x100')
        self.resizable(False, False)

        lable_search = tk.Label(self, text='Имя:')
        lable_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        #Кнопка запрограмированная на закрытие окна после поиска
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)
        
        #Кнопка запрограмированная на запуск поиска по имени 
        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=185, y=50)
        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_records(self.entry_search.get()))
        #Программирование автоматического закрытия окна после исполнения того же поиска 
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')
        
#Класс базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS db (
            id INTEGER PRIMARY KEY,
            name TEXT,
            tel TEXT,
            email TEXT,
            zp TEXT
        );''')
        self.conn.commit()


    def insert_data(self, name, tel, email, zp):
        self.c.execute('''INSERT INTO db (name, tel, email, zp) VALUES (?, ?, ?, ?)''', (name, tel, email, zp))
        self.conn.commit()

if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга')
    root.geometry('780x450')
    root.resizable(False, False)
    root.mainloop()
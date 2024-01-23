import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Aplikacja bazy danych")
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            database='hurtownia1',
            autocommit=True)
        self.show_main_menu()
        style = ttk.Style()
        style.configure("Treeview", rowheight=40, highlightthickness=1)
        font = 'TkDefaultFont', 10, 'bold'
        style.configure("Treeview.Heading", font=font)

    def show_main_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.button_adding = tk.Button(self.master, text='Dodawanie', command=self.open_adding)
        self.button_adding.pack()
        self.button_removing = tk.Button(self.master, text='Usuwanie', command=self.open_removing)
        self.button_removing.pack()
        self.button_updating = tk.Button(self.master, text='Aktualizowanie', command=self.open_updating)
        self.button_updating.pack()
        self.button_searching = tk.Button(self.master, text='Wyszukiwanie', command=self.open_searching)
        self.button_searching.pack()
# wyszukiwania
    def open_searching(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.button_orderdetails = tk.Button(self.master, text='Szczegoly zamowien klientow', command=self.orders_temp)
        self.button_orderdetails.pack()
        self.button_history = tk.Button(self.master, text="Historia zamowien", command=self.orders_history)
        self.button_history.pack()
        self.button_availability = tk.Button(self.master, text="Dostępność towarów", command=self.availability_temp)
        self.button_availability.pack()
        self.button_profit = tk.Button(self.master, text="Przychod w obecnym miesiacu", command=self.profit_month)
        self.button_profit.pack()
        self.button_best = tk.Button(self.master, text="Zestawienie klientów", command=self.best_clients)
        self.button_best.pack()
        self.button_bests = tk.Button(self.master, text="Zestawienie towarów", command=self.bestsellers)
        self.button_bests.pack()
        self.button_back_to_menu = tk.Button(self.master, text='Powrót do Menu', command=self.show_main_menu)
        self.button_back_to_menu.pack()

    def bestsellers(self):
        if not self.conn.is_connected():
            self.conn.reconnect()
        cursor = self.conn.cursor()
        sql_statement = '''call NajczesciejKupowane'''
        cursor.execute(sql_statement)
        records = cursor.fetchall()
        window = tk.Toplevel(self.master)
        window.title("Wyniki zapytania")
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        window.geometry(f"{width}x{height}+0+0")
        tree = ttk.Treeview(window, columns=(
            "IdTowaru", "Nazwa", "Suma sprzedanych sztuk", 'Przychod'))
        tree.column("#0", width=0, stretch=tk.NO)
        for column in tree["columns"]:
            tree.heading(column, text=column)
        for record in records:
            tree.insert("", "end", values=record)
        tree.pack(fill=tk.BOTH, expand=True)

    def best_clients(self):
        if not self.conn.is_connected():
            self.conn.reconnect()
        cursor = self.conn.cursor()
        sql_statement = '''call NajlepsiKlienci'''
        cursor.execute(sql_statement)
        records = cursor.fetchall()
        window = tk.Toplevel(self.master)
        window.title("Wyniki zapytania")
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        window.geometry(f"{width}x{height}+0+0")
        tree = ttk.Treeview(window, columns=(
            "IdKlienta", "Imie", "Nazwisko", 'Suma zamówień'))
        tree.column("#0", width=0, stretch=tk.NO)
        for column in tree["columns"]:
            tree.heading(column, text=column)
        for record in records:
            tree.insert("", "end", values=record)
        tree.pack(fill=tk.BOTH, expand=True)

    def profit_month(self):
        if not self.conn.is_connected():
            self.conn.reconnect()
        cursor = self.conn.cursor()
        sql_statement = '''call PrzychodMiesieczny'''
        cursor.execute(sql_statement)
        records = cursor.fetchall()
        window = tk.Toplevel(self.master)
        window.title("Wyniki zapytania")
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        window.geometry(f"{width}x{height}+0+0")
        tree = ttk.Treeview(window, columns=(
            "Średnia Wartość Zamówienia", "Łączny przychód", "Ilość zamówień"))
        tree.column("#0", width=0, stretch=tk.NO)
        for column in tree["columns"]:
            tree.heading(column, text=column)
        for record in records:
            tree.insert("", "end", values=record)
        tree.pack(fill=tk.BOTH, expand=True)

    def availability_temp(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.label_goodname = tk.Label(self.master, text='Podaj nazwe towaru')
        self.label_goodname.pack()
        self.entry_goodname = tk.Entry(self.master)
        self.entry_goodname.pack()
        self.button_conf = tk.Button(self.master, text="Zatwierdz", command=self.availability)
        self.button_conf.pack()
        self.button_back_to_menu = tk.Button(self.master, text='Powrót do Menu', command=self.show_main_menu)
        self.button_back_to_menu.pack()

    def availability(self):
        if not self.conn.is_connected():
            self.conn.reconnect()
        name = self.entry_goodname.get()
        cursor = self.conn.cursor()
        parameters = (name,)
        sql_statement = f'''
        SELECT IdTowaru,nazwa,cena,ilosc
        FROM towary
        where nazwa=%s;'''
        cursor.execute(sql_statement, parameters)
        records = cursor.fetchall()
        window = tk.Toplevel(self.master)
        window.title("Wyniki zapytania")
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        window.geometry(f"{width}x{height}+0+0")
        tree = ttk.Treeview(window, columns=(
            "IdTowaru", "Nazwa", "Cena", "Ilość dostępnych"))
        tree.column("#0", width=0, stretch=tk.NO)
        for column in tree["columns"]:
            tree.heading(column, text=column)
        for record in records:
            tree.insert("", "end", values=record)
        tree.pack(fill=tk.BOTH, expand=True)

    def orders_temp(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.label_clientID = tk.Label(self.master, text='Podaj ID klienta')
        self.label_clientID.pack()
        self.entry_clientID = tk.Entry(self.master)
        self.entry_clientID.pack()
        self.button_conf = tk.Button(self.master, text="Zatwierdz", command=self.order_details)
        self.button_conf.pack()
        self.button_back_to_menu = tk.Button(self.master, text='Powrót do Menu', command=self.show_main_menu)
        self.button_back_to_menu.pack()

    def order_details(self):
        if not self.conn.is_connected():
            self.conn.reconnect()
        cursor = self.conn.cursor()
        clientID = self.entry_clientID.get()
        sql_statement = """
           SELECT klienci.IdKlienta, klienci.nazwisko, klienci.adres, 
           zamowienia.idzamowienia, zamowienia.dataz, towary.nazwa, 
           szczegoly.ilosc, towary.cena*szczegoly.ilosc as Suma 
           FROM klienci 
           INNER JOIN (Towary 
           INNER JOIN (zamowienia 
           INNER JOIN szczegoly ON zamowienia.IdZamowienia = szczegoly.IdZamowienia) 
           ON Towary.IdTowaru = szczegoly.IdTowaru) 
           ON Klienci.IdKlienta = zamowienia.IdKlienta 
           WHERE zamowienia.IdKlienta = %s;
           """
        parameters = (clientID,)
        cursor.execute(sql_statement, parameters)
        records = cursor.fetchall()
        window = tk.Toplevel(self.master)
        window.title("Wyniki zapytania")
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        window.geometry(f"{width}x{height}+0+0")
        tree = ttk.Treeview(window, columns=(
            "IdKlienta", "Nazwisko", "Adres", "IdZamowienia", "DataZ", "IdTowaru", "Ilosc", "Suma"))
        tree.column("#0", width=0, stretch=tk.NO)
        for column in tree["columns"]:
            tree.heading(column, text=column)
        for record in records:
            tree.insert("", "end", values=record)
        tree.pack(fill=tk.BOTH, expand=True)

    def orders_history(self):
        if not self.conn.is_connected():
            self.conn.reconnect()
        cursor = self.conn.cursor()
        sql_statement = '''call NajrzadziejZamawiane'''
        cursor.execute(sql_statement)
        records = cursor.fetchall()
        window = tk.Toplevel(self.master)
        window.title("Wyniki zapytania")
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        window.geometry(f"{width}x{height}+0+0")
        tree = ttk.Treeview(window, columns=('IdZamowienia',
                                             "Ostatnia sprzedaż ", "IdTowaru", "Nazwa", "Ilosc"))
        tree.column("#0", width=0, stretch=tk.NO)
        for column in tree["columns"]:
            tree.heading(column, text=column)
        for record in records:
            tree.insert("", "end", values=record)
        tree.pack(fill=tk.BOTH, expand=True)
# dodawanie rekordow
    def open_adding(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.label_table = tk.Label(self.master, text='Podaj tabele')
        self.entry_table = tk.Entry(self.master)
        self.button_atributes = tk.Button(self.master, text='Pokaz atrybuty tabeli', command=self.show_attributes)
        self.label_table.pack()
        self.entry_table.pack()
        self.button_atributes.pack()
        self.button_records = tk.Button(self.master, text='Dodaj rekord', command=self.set_attributes)
        self.button_records.pack()
        self.button_back_to_menu = tk.Button(self.master, text='Powrót do Menu', command=self.show_main_menu)
        self.button_back_to_menu.pack()

    def set_attributes(self):
        table = self.entry_table.get()
        cursor = self.conn.cursor()
        for widget in self.master.winfo_children():
            widget.destroy()
        self.label_warning = tk.Label(self.master,
                                      text='Id nie jest liczone jako atrybut! Zostanie dodane automatycznie przy dodawaniu rekordu do bazy')
        self.label_warning.pack()

        self.l1 = tk.Label(self.master, text="Wartosc atrybutu 1")
        self.e1 = tk.Entry()
        self.l1.pack()
        self.e1.pack()

        self.l2 = tk.Label(self.master, text="Wartosc atrybutu 2")
        self.e2 = tk.Entry(self.master)
        self.l2.pack()
        self.e2.pack()

        self.l3 = tk.Label(self.master, text="Wartosc atrybutu 3")
        self.e3 = tk.Entry(self.master)
        self.l3.pack()
        self.e3.pack()

        self.l4 = tk.Label(self.master, text="Wartosc atrybutu 4")
        self.e4 = tk.Entry(self.master)
        self.l4.pack()
        self.e4.pack()

        self.l5 = tk.Label(self.master, text="Wartosc atrybutu 5")
        self.e5 = tk.Entry(self.master)
        self.l5.pack()
        self.e5.pack()

        self.l6 = tk.Label(self.master, text="Wartosc atrybutu 6")
        self.e6 = tk.Entry(self.master)
        self.l6.pack()
        self.e6.pack()

        self.l7 = tk.Label(self.master, text="Wartosc atrybutu 7")
        self.e7 = tk.Entry(self.master)
        self.l7.pack()
        self.e7.pack()

        self.button_setting = tk.Button(self.master, text='Zatwierdz rekord', command=lambda: self.add_records(table))
        self.button_setting.pack()
        self.button_back_to_menu = tk.Button(self.master, text='Powrót do Menu', command=self.show_main_menu)
        self.button_back_to_menu.pack()

    def add_records(self, table):
        cursor = self.conn.cursor()
        atr1 = self.e1.get()
        atr2 = self.e2.get()
        atr3 = self.e3.get()
        atr4 = self.e4.get()
        atr5 = self.e5.get()
        atr6 = self.e6.get()
        atr7 = self.e7.get()
        if table == 'Dzialy':
            sql_statement = 'Insert into dzialy(IdDzialu,NazwaD,IdKierownika) values (NULL,%s,%s);'
            parameters = (atr1, atr2,)
            cursor.execute(sql_statement, parameters)
            self.conn.commit()
        elif table == 'Kierownicy':
            sql_statement = 'Insert into Kierownicy(IdKierownika,Imie,Nazwisko,DataZatrudnienia,NrTelefonu,Email,Pensja,Premia) values (NULL,%s,%s,%s,%s,%s,%s,%s);'
            parameters = (atr1, atr2, atr3, atr4, atr5, atr6, atr7,)
            cursor.execute(sql_statement, parameters)
            self.conn.commit()
        elif table == 'Klienci':
            sql_statement = 'Insert into Klienci(IdKlienta,Imie,Nazwisko,Adres,NrTelefonu,Email) values (NULL,%s,%s,%s,%s,%s);'
            parameters = (atr1, atr2, atr3, atr4, atr5,)
            cursor.execute(sql_statement, parameters)
            self.conn.commit()
        elif table == 'Towary':
            sql_statement = 'Insert into Towary(IdTowaru,Nazwa,Cena,Ilosc,IdDzialu) values (NULL,%s,%s,%s,%s);'
            parameters = (atr1, atr2, atr3, atr4,)
            cursor.execute(sql_statement, parameters)
            self.conn.commit()
        self.show_records(table)
# aktualizowanie rekordow
    def open_updating(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.label_table2 = tk.Label(self.master, text='Podaj tabele')
        self.entry_table = tk.Entry(self.master)
        self.label_table2.pack()
        self.entry_table.pack()
        self.button_atributes2 = tk.Button(self.master, text='Pokaz atrybuty tabeli', command=self.show_attributes)
        self.button_atributes2.pack()
        self.button_records = tk.Button(self.master, text='Aktualizuj rekordy', command=self.set_updates)
        self.button_records.pack()
        self.button_back_to_menu = tk.Button(self.master, text='Powrót do Menu', command=self.show_main_menu)
        self.button_back_to_menu.pack()

    def set_updates(self):
        table = self.entry_table.get()
        self.show_records(table)
        widgets_to_remove = []

        for widget in self.master.winfo_children():

            if not isinstance(widget, (tk.Toplevel)):
                widgets_to_remove.append(widget)

        for widget in widgets_to_remove:
            widget.destroy()
        self.label_update3 = tk.Label(self.master, text='Podaj rekord do aktualizacji')
        self.label_update3.pack()
        self.entry_update3 = tk.Entry(self.master)
        self.entry_update3.pack()
        self.label_update = tk.Label(self.master, text='Podaj kolumne do aktualizacji')
        self.label_update.pack()
        self.entry_update = tk.Entry(self.master)
        self.entry_update.pack()
        self.label_newval = tk.Label(self.master, text='Podaj nowa wartosc')
        self.label_newval.pack()
        self.entry_newval = tk.Entry(self.master)
        self.entry_newval.pack()
        self.button_update = tk.Button(self.master, text='Zatwierdz', command=lambda: self.update_record(table))
        self.button_update.pack()
        self.button_back_to_menu = tk.Button(self.master, text='Powrót do Menu', command=self.show_main_menu)
        self.button_back_to_menu.pack()

    def update_record(self, table):
        if not self.conn.is_connected():
            self.conn.reconnect()
        recID = self.entry_update3.get()
        column = self.entry_update.get()
        newval = self.entry_newval.get()
        parameters = (newval, recID,)
        cursor = self.conn.cursor()
        if table == 'Dzialy':
            sql_statement = f'update {table} set {column}=%s where IdDzialu=%s'
            try:
                cursor.execute(sql_statement, parameters)
                self.conn.commit()
            except Exception as e:
                print(f"Błąd przy aktualizacji rekordów: {str(e)}")
        elif table == 'Kierownicy':
            sql_statement = f'update {table} set {column}=%s where IdKierownika=%s'
            try:
                cursor.execute(sql_statement, parameters)
                self.conn.commit()
            except Exception as e:
                print(f"Błąd przy aktualizacji rekordów: {str(e)}")
        elif table == 'Klienci':
            sql_statement = f'update {table} set {column}=%s where IdKlienta=%s'
            try:
                cursor.execute(sql_statement, parameters)
                self.conn.commit()
            except Exception as e:
                print(f"Błąd przy aktualizacji rekordów: {str(e)}")
        elif table == 'Towary':
            sql_statement = f'update {table} set {column}=%s where IdTowaru=%s'
            try:
                cursor.execute(sql_statement, parameters)
                self.conn.commit()
            except Exception as e:
                print(f"Błąd przy aktualizacji rekordów: {str(e)}")
        elif table == "Zamowienia":
            sql_statement = f'update {table} set {column}=%s where IdZamowienia=%s'
            try:
                cursor.execute(sql_statement, parameters)
                self.conn.commit()
            except Exception as e:
                print(f"Błąd przy aktualizacji rekordów: {str(e)}")
        elif table == "Szczegoly":
            sql_statement = f'update {table} set {column}=%s where IdZamowienia=%s'
            try:
                cursor.execute(sql_statement, parameters)
                self.conn.commit()
            except Exception as e:
                print(f"Błąd przy aktualizacji rekordów: {str(e)}")
        self.show_records(table)
# usuwanie rekordow
    def open_removing(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.label_table1 = tk.Label(self.master, text='Podaj tabele')
        self.entry_table1 = tk.Entry(self.master)
        self.label_table1.pack()
        self.entry_table1.pack()
        self.button_showrecords = tk.Button(self.master, text='Wybierz rekord', command=self.set_removed)
        self.button_showrecords.pack()
        self.button_back_to_menu = tk.Button(self.master, text='Powrót do Menu', command=self.show_main_menu)
        self.button_back_to_menu.pack()

    def set_removed(self):
        table = self.entry_table1.get()
        for widget in self.master.winfo_children():
            widget.destroy()
        self.label_recID = tk.Label(self.master, text='Podaj Id Rekordu')
        self.entry_recID = tk.Entry(self.master)
        self.label_recID.pack()
        self.entry_recID.pack()
        self.show_records(table)
        self.button_remove = tk.Button(self.master, text='Zatwierdz usuniecie',
                                       command=lambda: self.remove_record(table))
        self.button_remove.pack()
        self.button_back_to_menu = tk.Button(self.master, text='Powrót do Menu', command=self.show_main_menu)
        self.button_back_to_menu.pack()

    def remove_record(self, table):
        cursor = self.conn.cursor()
        recID = self.entry_recID.get()
        parameters = (recID,)
        if table == 'Dzialy':
            sql_statement = f'delete from {table} where IdDzialu=%s'
            try:
                cursor.execute(sql_statement, parameters)
                self.conn.commit()
            except Exception as e:
                print(f"Błąd przy usuwaniu rekordów: {str(e)}")
        elif table == 'Kierownicy':
            sql_statement = f'delete from {table} where IdKierownika=%s'
            try:
                cursor.execute(sql_statement, parameters)
                self.conn.commit()
            except Exception as e:
                print(f"Błąd przy usuwaniu rekordów: {str(e)}")
        elif table == 'Klienci':
            sql_statement = f'delete from {table} where IdKlienta=%s'
            try:
                cursor.execute(sql_statement, parameters)
                self.conn.commit()
            except Exception as e:
                print(f"Błąd przy usuwaniu rekordów: {str(e)}")
        elif table == 'Towary':
            sql_statement = f'delete from {table} where IdTowaru=%s'
            try:
                cursor.execute(sql_statement, parameters)
                self.conn.commit()
            except Exception as e:
                print(f"Błąd przy usuwaniu rekordów: {str(e)}")
        self.show_records(table)
# pomocnicze metody
    def show_attributes(self):
        table = self.entry_table.get()
        if not self.if_table_exists(table):
            messagebox.showerror("Błąd", f"Tabela o nazwie '{table}' nie istnieje.")
            return
        atributes = self.get_attributes(table)
        self.attributes_window(atributes)

    def if_table_exists(self, table):
        query = "SHOW TABLES LIKE %s"
        parameters = (table,)
        cursor = self.conn.cursor()
        cursor.execute(query, parameters)
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def get_attributes(self, table):
        query = f"DESCRIBE {table}"
        cursor = self.conn.cursor()
        cursor.execute(query)
        atributes = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return atributes

    def attributes_window(self, atributes):
        atr_window = tk.Toplevel(self.master)
        atr_window.title("Atrybuty Tabeli")
        listbox = tk.Listbox(atr_window)
        listbox.pack()
        atr_window.geometry("+500+600")
        for atribute in atributes:
            listbox.insert(tk.END, atribute)

    def show_records(self, table):
        if hasattr(self, 'window') and self.window:
            self.window.destroy()
        self.window = tk.Toplevel(self.master)
        self.window.title("Rekordy Tabeli")
        self.window.geometry("500x400+300+100")
        tree = ttk.Treeview(self.window)
        cursor = self.conn.cursor()
        table_columns_query = f"SHOW COLUMNS FROM {table}"
        cursor.execute(table_columns_query)
        column_names = [column[0] for column in cursor.fetchall()]
        tree["columns"] = column_names
        tree.column("#0", width=0, stretch=tk.NO)
        for column in column_names:
            tree.column(column, anchor="center", width=100)
            tree.heading(column, text=column)
        records_query = f"SELECT * FROM {table}"
        cursor.execute(records_query)
        records = cursor.fetchall()
        tree.rowconfigure(3, minsize=60)
        for record in records:
            tree.insert("", "end", values=record)
        tree.pack(fill=tk.BOTH, expand=True)

# inicjalizacja aplikacji
root = tk.Tk()
aplikacja = Application(root)
root.mainloop()
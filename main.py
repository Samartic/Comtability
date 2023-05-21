from helper import *
from os import startfile
from PIL import Image, ImageTk
from sqlite3 import connect
from tkinter import Tk, StringVar, messagebox, Text
from tkinter.ttk import Button, Entry, Frame, Label, OptionMenu, Style
from time import sleep



db = connect("test.db")
billid = None
title_font = 18
 
class App:
    def __init__(self, root=None, clientid=None):
        self.root = root
        self.clientid = clientid
        self.root.title("Fox Électronique Comptable")
        img = Image.open('template\logo.png')
        width, height = img.size
        self.logo = ImageTk.PhotoImage(img.resize((int(width*0.5), int(height*0.5))))
        self.frame = Frame(self.root)
        self.label_frame = Frame(self.frame)
        Label(self.label_frame, image=self.logo, justify= "center").pack(pady=30)
        Label(self.label_frame, text='Comptable',font=("TkDefaultFont", title_font), padding= 10).pack(pady=20)
        self.label_frame.pack()
        
        self.grid = Frame(self.frame)
        Button(self.grid, text= 'Ajouter un Client', command=self.make_addclient, width=30, padding=20).grid(column=1, row=1, padx=10, pady=10)
        Button(self.grid, text= 'Rechercher un Client', command=self.make_searchclient,width=30, padding=20).grid(column=2, row=1,padx=10, pady=10)
        Button(self.grid, text= 'Facturation', command=self.make_billing, width=30, padding=20).grid(column=1, row=2,padx=10, pady=10)
        Button(self.grid, text= 'Rechercher une Facture', command=self.make_searchbills,width=30, padding=20).grid(column=2, row=2,padx=10, pady=10)
        Button(self.grid, text= 'Rapport des Ventes', command=self.make_sales,width=30, padding=20).grid(column=1, row=3,padx=10, pady=10)
        Button(self.grid, text='Requête', command=self.make_query_page, width=30, padding=20).grid(column=2, row=3,padx=10, pady=10)
        self.grid.pack()
        Button(self.frame, text='Quitter', command=self.root.destroy, width=30, padding=20).pack()
        self.frame.pack(fill="both")
        
        # other usefull class
        self.addclient = Addclient(master=self.root, app=self, clientid = self.clientid)
        self.billing = Billing(master=self.root, app=self, clientid = self.clientid)
        self.sale = Sales(master=self.root, app=self) 
        self.searchbills = Searchbills(master=self.root, app=self)
        self.searchclient = Searchclient(master=self.root, app=self, clientid = self.clientid)
        self.query_page = Query(master=self.root, app=self)
               
    def main_page(self, clientid=None):
        self.frame.pack()
        self.clientid = clientid
                
    def make_addclient(self):
        self.frame.pack_forget()
        self.addclient.start_page()
             
    def make_billing(self):
        
        self.frame.pack_forget()
        self.billing.start_page(clientid=self.clientid)
        
    def make_sales(self):
        self.frame.pack_forget()
        self.sale.start_page()        
        
    def make_searchbills(self):
        self.frame.pack_forget()
        self.searchbills.start_page()
        
    def make_searchclient(self):
        self.frame.pack_forget()
        self.searchclient.start_page()    
 
    def make_query_page(self):
        self.frame.pack_forget()
        self.query_page.start_page()
                        
class Addclient:
    def __init__(self, master=None, app=None, clientid=None):
        self.master = master
        self.app = app
        self.clientid = clientid
        self.frame = Frame(self.master)
        Label(self.frame, text='Ajouter un Client', font=("TkDefaultFont", title_font), padding= 10).pack(pady=10)
        self.table=Frame(self.frame, borderwidth=100)
        self.firstname = StringVar(master=self.master)
        self.lastname = StringVar(master=self.master)
        self.cie = StringVar(master=self.master)
        self.phone = StringVar(master=self.master)
        self.email = StringVar(master=self.master)
        
        self.name =Frame(self.table)
        Label(self.name, text='Prenom*: ', width=85,justify="left").grid(column=1, row=1,)
        Entry(self.name, textvariable= self.firstname, width=85).grid(column=1, row=2, padx = 10)
        
        Label(self.name, text='Nom*: ', width=85, justify="left").grid(column=2, row=1, padx=10)
        Entry(self.name, textvariable= self.lastname, width=85).grid(column=2, row=2, padx=10)
        self.name.pack(pady=10, fill="x")
        
        Label(self.table, text='cie: ').pack(fill='x', expand=True, padx=10)
        Entry(self.table, textvariable= self.cie).pack(fill='x', expand=True, padx=10)
        Label(self.table, text=' ').pack(fill='x', expand=True)
        
        Label(self.table, text='Téléphone*: ').pack(fill='x', expand=True, padx=10)
        Entry(self.table, textvariable= self.phone).pack(fill='x', expand=True, padx=10)
        Label(self.table, text=' ').pack(fill='x', expand=True)
        
        Label(self.table, text='email: ').pack(fill='x', expand=True, padx=10)
        Entry(self.table, textvariable= self.email).pack(fill='x', expand=True, padx=10)
        self.table.pack(fill="x")
        self.button_grid = Frame(self.frame)
        Button(self.button_grid, text='Retour', command=self.go_back, padding=20).grid(column=1, row=1, padx=10, pady=10)
        Button(self.button_grid, text='Soumettre', command=self.submit, padding=20).grid(column=2, row=1, padx=10, pady=10)
        self.button_grid.pack(pady=20)
        
    def clear_out(self):
        self.firstname.set('')
        self.lastname.set('')
        self.cie.set('')
        self.phone.set('')
        self.email.set('')
        
    def go_back(self):
        self.frame.pack_forget()
        self.clear_out()
        self.app.main_page(clientid=self.clientid)
    
    def start_page(self):
        self.frame.pack(fill="both")
        
    def submit(self):
        try: 
            client = Client(
                self.firstname.get()
                , self.lastname.get()
                , self.cie.get()
                , self.phone.get()
                , self.email.get()
            )
            self.clientid = get_client_id(db, client)
              
        except Exception as e:
            messagebox.showerror(title='Error',message= e)
            
        message = str(f'Client id: {self.clientid} \n{client}')    
        messagebox.showinfo(title='Success', message= message)
        self.clear_out()
        self.frame.pack_forget()
        self.app.main_page(clientid=self.clientid)
         
class Billing:
    def __init__(self, master=None, app=None, clientid=None, total=None):
        self.master = master
        self.app = app
        self.clientid = clientid
        self.total = total
        
        self.frame = Frame(self.master)
    
        
        Label(self.frame, text='Facturation', font=("TkDefaultFont", title_font), padding= 10).pack()
        self.bills = []
        
        # client zone
        
        self.clientzone = Frame(self.frame, borderwidth=50)
        self.clientinfo = Frame(self.clientzone)
        
        self.str_clientid = StringVar()
        self.str_client_firstname = StringVar()
        self.str_client_lastname = StringVar()
        self.str_client_cie = StringVar()
        self.str_client_phone = StringVar()
        self.str_client_email = StringVar()
        
        
            
        Label(self.clientinfo, text= "ID: ").grid(column=1, row=1)
        Entry(self.clientinfo, textvariable=self.str_clientid, width=5).grid(column=1, row=2)
        Label(self.clientinfo, text="Prenom: ", justify="left").grid(column=1, row=3)
        Label(self.clientinfo, text="Nom: ").grid(column=2, row=3)
        Entry(self.clientinfo, textvariable=self.str_client_firstname).grid(column=1, row=4)
        Entry(self.clientinfo, textvariable=self.str_client_lastname, justify='left').grid(column=2, row=4)
        Label(self.clientinfo, text="Compagnie: ").grid(column=1, row=5)
        Entry(self.clientinfo, textvariable=self.str_client_cie, width=45).grid(row=6, columnspan=2, column=1)
        Label(self.clientinfo, text="Téléphone: ").grid(column=1, row=7)
        Label(self.clientinfo, text="e-mail: ").grid(column=2, row=7)
        Entry(self.clientinfo, textvariable=self.str_client_phone).grid(column=1, row=8)
        Entry(self.clientinfo, textvariable=self.str_client_email).grid(column=2, row=8)
        self.clientinfo.pack(fill="x")
        
        self.buttongrid = Frame(self.clientzone)
        Button(self.buttongrid, text='Réinitialiser', command=self.erase_client).grid(column=1, row=1, padx=10, pady=10) 
        Button(self.buttongrid, text="Confirmer le client", command=self.confirm_client).grid(column=2, row=1, padx=10, pady=10)   
        self.buttongrid.pack(fill="x")
        self.clientzone.pack(fill="x", anchor="s")
        
        # billed items
        self.added_item = Frame(self.frame)
        self.added_item.pack()
        
        self.itemsgrid = Frame(self.frame)
        self.qt = StringVar()
        self.product_name = StringVar()
        self.price = StringVar()
        

        # section for adding items
        Label(self.itemsgrid, text="Qt").grid(column=1, row=1)
        Label(self.itemsgrid, text="Produit").grid(column=2, row=1)
        Label(self.itemsgrid, text="price").grid(column=3, row=1)
        Entry(self.itemsgrid, textvariable=self.qt, width=5).grid(column=1, row=2,padx=5)
        Entry(self.itemsgrid, textvariable=self.product_name, width=40).grid(column=2, row=2, padx=5)
        Entry(self.itemsgrid, textvariable=self.price, width=5).grid(column=3, row=2, padx=5)
        self.itemsgrid.pack(pady=10)
        
        Button(self.frame, text="Ajouter", command=self.additem).pack()
        
        
        self.last_button = Frame(self.frame)
        Button(self.last_button, text="Retour", command=self.go_back, padding=20).grid(column=1, row=1, padx= 10)
        Button(self.last_button, text="Confirmer", command=self.finish, padding=20).grid(column=2, row=1, padx= 10)
        self.last_button.pack(pady=10)
                  
    def additem(self): 
        if self.qt == None or self.product_name == None or self.price == None:
            messagebox.showerror(title="Invalid", message="Un champ est vide")
        else:
            try:
                myproduct = Product(self.product_name.get(), self.price.get(), self.qt.get())
                if self.bills:
                    self.bills.append(myproduct)
                else:
                    self.bills = []
                    self.bills.append(myproduct)
            except Exception as e:
                messagebox.showerror(title="Invalid", message=e)
        self.qt.set("")
        self.product_name.set("")
        self.price.set("")
        self.frame.pack_forget()
        self.start_page(clientid=self.clientid, bills = self.bills, total= self.total)
    
    def confirm_client(self):
        if self.str_clientid.get():
            self.clientid = self.str_clientid.get()
            if self.clientid.isalnum:   
                self.start_page(clientid=self.clientid, bills=self.bills) 
            else:   
                self.clientid = confirm_client(
                            db
                            , self.str_client_firstname.get().title()
                            , self.str_client_lastname.get().title()
                            , self.str_client_cie.get().title()
                            , self.str_client_phone.get()
                            , self.str_client_email.get())
                
                self.start_page(clientid=self.clientid, bills=self.bills) 
                        
    def erase_client(self):
        self.str_clientid.set("")
        self.str_client_firstname.set("")
        self.str_client_lastname.set("")
        self.str_client_cie.set("")
        self.str_client_phone.set("")
        self.str_client_email.set("")
        
    def finish(self):
        if self.clientid and self.bills:
            total = float((self.total.get().replace("$","")).strip())
            billing_id = append_bill(db, self.bills, str(self.clientid), total)
            print("generating PDF")
            file = gen_pdf(get_client_fromid(self.clientid,db), self.clientid, self.bills, total, billing_id)
            printer(file)
            sleep(10)
            messagebox.showinfo(title="Succes", message="La facture a ete genere avec succes")
            self.go_back
    def go_back(self):
        self.frame.pack_forget()
        self.app.main_page()
    
    def start_page(self, clientid = None, bills = None, total = None ):
        self.frame.pack_forget()
        self.added_item.destroy()
        self.added_item = Frame(self.frame)
        self.clientid = clientid
        self.bills = bills
        self.total = total
        
        if self.clientid:
            self.myclient = get_client_fromid(self.clientid, db)
            self.str_clientid.set(self.clientid)
            self.str_client_firstname.set(self.myclient.firstname)
            self.str_client_lastname.set(self.myclient.lastname)
            self.str_client_cie.set(self.myclient.cie)
            self.str_client_phone.set(self.myclient.phone)
            self.str_client_email.set(self.myclient.email)

        self.list_variable = []
        i=0
        self.total = StringVar()
        total = 0
        if self.bills:
            for row in self.bills:
                self.list_variable.append(StringVar())
                self.list_variable[i].set(str(row))
                Label(self.added_item, textvariable=self.list_variable[i]).pack()
                total += (row.quantity) * (row.price)
                i += 1  
            self.total.set(f"{total:.2f} $")    
            Label(self.added_item, text="Total",font=("TkDefaultFont", 12)).pack(pady=20)
            Label(self.added_item, textvariable=self.total).pack()
            self.added_item.pack()
               
        self.frame.pack(fill="both")     
    
class Query:
    def __init__(self, master=None, app=None):
        self.app = app
        self.master = master
        self.frame = Frame(self.master)
        self.title = StringVar()
        self.table =Frame(self.frame, borderwidth=50)
        Label(self.frame, text="Requête",font=("TkDefaultFont", title_font)).pack(pady=20)
        Label(self.table, text="Titre: ").pack(pady=20)
        Entry(self.table, textvariable=self.title).pack(fill="x")
        Label(self.table, text="Requête SQL: ").pack(pady=20)
        self.query = Text(self.table)
        self.query.pack()
        self.table.pack()
        self.button_block = Frame(self.frame)
        Button(self.button_block, text="Retour", command=self.go_back, padding = 20).grid(column=1, row=1, padx=1, pady=1)
        Button(self.button_block, text="Generer", command=self.generate, padding=20).grid(column=2, row=1,padx=10, pady=10)
        self.button_block.pack(pady=20)

        
    def generate(self):
        try:
            success = query_generator(db, self.title.get(), self.query.get("1.0","end-1c"))
            if success:
               startfile(f"{self.title.get()}.csv","open")
        except Exception as e:
            messagebox.showerror(title="erreur", message=e)
    def go_back(self):
        self.frame.pack_forget()
        self.app.main_page()
        
    def start_page(self):
        self.frame.pack(fill="both")           
        
class Sales:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = Frame(self.master)
        Label(self.frame, text='Rapport des Ventes',font=("TkDefaultFont", title_font), padding= 10).pack()
        self.start_input = StringVar(master=self.master)
        self.end_input = StringVar(master=self.master)
        
        
        self.sales_grid = Frame(self.frame, borderwidth=200)
        Label(self.sales_grid, text="Debut", justify="left",).grid(column=1, row=1)
        Label(self.sales_grid, text="Fin", justify="left").grid(column=2, row=1)
        Entry(self.sales_grid, textvariable= self.start_input).grid(column=1, row=2,padx=10)
        Entry(self.sales_grid, textvariable= self.end_input).grid(column=2, row=2,padx=10)
        Label(self.sales_grid, text="", justify="left", padding=10).grid(column=1, row=3)
        Label(self.sales_grid, text="", justify="left", padding=10).grid(column=2, row=3)
        Button(self.sales_grid, text='Retour', padding=20, command=self.go_back).grid(column=1, row=4, padx=10, pady=10)
        Button(self.sales_grid, text='Soumettre', padding=20, command=self.sale_submit).grid(column=2, row=4, padx=10, pady=10)
        self.sales_grid.pack()
        
    def go_back(self):
        self.clear_out()
        self.frame.pack_forget()
        self.app.main_page()
        
    def sale_submit(self):
        try:
            file_name = get_report(db, self.start_input.get(), self.end_input.get())
            startfile(f"{file_name}", "open")
            self.frame.pack_forget()
            self.app.main_page()
            
        except Exception as e:
            messagebox.showerror("Erreur", e)
    def start_page(self):
        self.frame.pack(fill="both")
               
class Searchbills:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = Frame(self.master)
        Label(self.frame, text='Rechercher une Facture', font=("TkDefaultFont", title_font), padding= 10).pack()
        self.result = None
        self.grid = Frame(self.frame)
        self.start = StringVar()
        self.end = StringVar()
        self.firstname = StringVar()
        self.lastname = StringVar()
        self.phone = StringVar()
        self.total = StringVar()
        
        Label(self.grid, text="Debut:").grid(column=1, row=1)
        Label(self.grid, text="Fin:").grid(column=2, row=1)
        Entry(self.grid, textvariable=self.start).grid(column=1, row=2)
        Entry(self.grid, textvariable=self.end).grid(column=2,row=2)
        Label(self.grid, text="Prenom:").grid(column=1, row=3)
        Label(self.grid, text="Nom:").grid(column=2, row=3)
        Entry(self.grid, textvariable=self.firstname).grid(column=1, row=4)
        Entry(self.grid, textvariable=self.lastname).grid(column=2,row=4)
        Label(self.grid, text="Téléphone:").grid(column=1, row=5)
        Label(self.grid, text="Total: ").grid(column=2, row=5)
        Entry(self.grid, textvariable=self.phone).grid(column=1,row=6)
        Entry(self.grid, textvariable=self.total).grid(column=2, row=6)
        Label(self.grid, text="").grid(column=1, row=7)
        self.grid.pack()
        
        self.grid_button = Frame(self.frame)
        Button(self.grid_button, text='Go back', command=self.go_back).grid(column=1, row=1)
        Button(self.grid_button, text="Recherche",command=self.get_bills).grid(column=2, row=1)
        self.grid_button.pack()
        
    def clear_out(self):
        self.start.set("") 
        self.end.set("") 
        self.firstname.set("") 
        self.lastname.set("") 
        self.phone.set("") 
        self.total.set("")     

    def go_back(self):
        self.clear_out()
        self.frame.pack_forget()
        self.app.main_page()
        
    def get_bills(self):
        self.frame.pack_forget()
        if self.result:
            self.result.destroy()
        self.frame.pack()
        self.result = Frame(self.frame)
        
        try:
            result = search_bills(
                                db
                                , self.start.get()
                                , self.end.get()
                                , self.firstname.get()
                                , self.lastname.get()
                                , self.phone.get()
                                ,self.total.get()
                                )                       
                
            if result:
                result = format_result(result)
                self.str_row = []                           
                i = 0
                for row in result:
                    self.str_row.append(StringVar())
                    self.str_row[i].set(row)
                    Label(self.result, textvariable=self.str_row[i]).pack(pady=20)
                    i += 1
                self.result.pack(pady=20)
                self.frame.pack()
            else:
                Label(self.result, text="Aucun resultat").pack()
                self.result.pack(pady=20)
                self.frame.pack()
                
        except Exception as e:
            messagebox.showerror(title="Probleme", message=e)
                 
    def start_page(self):
            if self.result:
                self.result.destroy()
                self.frame.pack()

class Searchclient:
    def __init__(self, master=None, app=None, clientid=None):
        self.master = master
        self.app = app
        self.frame = Frame(self.master)
        self.clientid = clientid
        Label(self.frame, text='Rechercher un Client', font=("TkDefaultFont", title_font), padding= 10).pack(pady=10)
        
        OPTION = ['Nom', 'Téléphone', 'id']
        self.variable = StringVar(self.frame)
        self.variable.set(OPTION[0]) # default value
        self.search_grid = Frame(self.frame)
        self.menu = OptionMenu(self.search_grid, self.variable, *OPTION).grid(column=1, row=1)
        self.input = StringVar(self.frame)
        Entry(self.search_grid, textvariable= self.input, width= 70).grid(column=2, row=1)
        self.search_grid.pack(pady=20)
        
        self.button_grid = Frame(self.frame)
        Button(self.button_grid, text='Retour', command=self.go_back, padding=20).grid(column=1, row=1, padx=10, pady=10)
        Button(self.button_grid, text='Soumettre', command=self.submit, padding=20).grid(column=2, row=1, padx=10, pady=10)
        self.button_grid.pack(pady=20)
        
    def clear_out(self):
        self.input.set('')
             
    def go_back(self):
        self.frame.pack_forget()
        self.clear_out()
        self.app.main_page()
   
    def start_page(self):
            self.frame.pack(fill="both")   
        
    def submit(self):
        result = search_client(db, self.variable.get(), self.input.get())
        if result == None:
            messagebox.showinfo(title="Rien", message= "aucun resultat ne correspond a votre recherche")
        else:
            message = message_format(result)
            messagebox.showinfo(title='Success', message=message)
            self.clientid = get_id(result)
            self.clear_out()
            self.frame.pack_forget()
            self.app.main_page(clientid=self.clientid)
          

            
def main():
    root = Tk()
    root.geometry("1280x800")
    style = Style()
    root.call("source", "template/tkBreeze-master/breeze-dark/breeze-dark.tcl")
    style.theme_use("breeze-dark")
    App(root)
    root.mainloop()

if __name__ == '__main__':
    main()

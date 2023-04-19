import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import sqlite3
from helper import Client, get_client_id


db = sqlite3.connect("test.db")

clientid = None
billid = None
title_font = 18
 
class myApp:
    def __init__(self, root=None):
        self.root = root
        self.root.title("Fox Electronique Comptable")
        img = Image.open('logo.png')
        width, height = img.size
        self.logo = ImageTk.PhotoImage(img.resize((int(width*0.5), int(height*0.5))))
        self.frame = ttk.Frame(self.root)
        self.label_frame = ttk.Frame(self.frame)
        ttk.Label(self.label_frame, image=self.logo, justify= "center").pack(pady=30)
        ttk.Label(self.label_frame, text='Comptable',font=("TkDefaultFont", title_font), padding= 10).pack(pady=20)
        self.label_frame.pack()
        
        self.grid = ttk.Frame(self.frame)
        ttk.Button(self.grid, text= 'Add a Client', command=self.make_addclient, padding=20).grid(column=1, row=1, padx=10, pady=10)
        ttk.Button(self.grid, text= 'Search Client', command=self.make_searchclient, padding=20).grid(column=2, row=1,padx=10, pady=10)
        ttk.Button(self.grid, text= 'Make a bills', command=self.make_billing, padding=20).grid(column=1, row=2,padx=10, pady=10)
        ttk.Button(self.grid, text= 'Search bills', command=self.make_searchbills, padding=20).grid(column=2, row=2,padx=10, pady=10)
        ttk.Button(self.grid, text= 'Sales', command=self.make_sales, padding=20).grid(column=1, row=3,padx=10, pady=10)
        ttk.Button(self.grid, text='Quitter', command=self.root.destroy, padding=20).grid(column=2, row=3,padx=10, pady=10)
        self.grid.pack()
        self.frame.pack()
        # other usefull class
        self.addclient = Addclient(master=self.root, app=self)
        self.searchclient = Searchclient(master=self.root, app=self)
        self.billing = Billing(master=self.root, app=self)
        self.searchbills = Searchbills(master=self.root, app=self)
        self.sale = Sales(master=self.root, app=self)  
              
    # methodes
    def main_page(self):
        self.frame.pack()
        
    def make_addclient(self):
        self.frame.pack_forget()
        self.addclient.start_page()
        
    def make_searchclient(self):
        self.frame.pack_forget()
        self.searchclient.start_page()
        
    def make_billing(self):
        self.frame.pack_forget()
        self.billing.start_page()
        
    def make_searchbills(self):
        self.frame.pack_forget()
        self.searchbills.start_page()
        
    def make_sales(self):
        self.frame.pack_forget()
        self.sale.start_page()
    

                
class Addclient:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        ttk.Label(self.frame, text='Add Client', padding= 10).pack(pady=10)
        
        self.firstname = tk.StringVar(master=self.master)
        self.lastname = tk.StringVar(master=self.master)
        self.cie = tk.StringVar(master=self.master)
        self.phone = tk.StringVar(master=self.master)
        self.email = tk.StringVar(master=self.master)
        
        ttk.Label(self.frame, text='Prenom*: ').pack(fill='x', expand=True)
        ttk.Entry(self.frame, textvariable= self.firstname).pack(fill='x', expand=True,)
        ttk.Label(self.frame, text=' ').pack(fill='x', expand=True)
        
        ttk.Label(self.frame, text='Nom*: ').pack(fill='x', expand=True)
        ttk.Entry(self.frame, textvariable= self.lastname).pack(fill='x', expand=True)
        ttk.Label(self.frame, text=' ').pack(fill='x', expand=True)
        
        ttk.Label(self.frame, text='cie: ').pack(fill='x', expand=True)
        ttk.Entry(self.frame, textvariable= self.cie).pack(fill='x', expand=True)
        ttk.Label(self.frame, text=' ').pack(fill='x', expand=True)
        
        ttk.Label(self.frame, text='Telephone*: ').pack(fill='x', expand=True)
        ttk.Entry(self.frame, textvariable= self.phone).pack(fill='x', expand=True)
        ttk.Label(self.frame, text=' ').pack(fill='x', expand=True)
        
        ttk.Label(self.frame, text='email: ').pack(fill='x', expand=True)
        ttk.Entry(self.frame, textvariable= self.email).pack(fill='x', expand=True)
        
        self.button_grid = ttk.Frame(self.frame)
        ttk.Button(self.button_grid, text='Go back', command=self.go_back, padding=20).grid(column=1, row=1, padx=10, pady=10)
        ttk.Button(self.button_grid, text='Submit', command=self.submit, padding=20).grid(column=2, row=1, padx=10, pady=10)
        self.button_grid.pack(pady=20)
        
    def clear_out(self):
        self.firstname.set('')
        self.lastname.set('')
        self.cie.set('')
        self.phone.set('')
        self.email.set('')
        
    def start_page(self):
        self.frame.pack()

    def go_back(self):
        self.frame.pack_forget()
        self.clear_out()
        self.app.main_page()
        
    def submit(self):
        try: 
            client = Client(
                self.firstname.get()
                , self.lastname.get()
                , self.cie.get()
                , self.phone.get()
                , self.email.get()
            )
            clientid = get_client_id(db, client)   
        except Exception as e:
            messagebox.showerror(title='Error',message= e)
            
        message = str(f'Client id: {clientid} \n{client}')    
        messagebox.showinfo(title='Success', message= message)
        self.clear_out()
        self.frame.pack_forget
        self.app.main_page()
        
class Searchclient:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        ttk.Label(self.frame, text='Recherche Client', padding= 10).pack(pady=10)
        
        self.firstname = tk.StringVar(master=self.master)
        self.lastname = tk.StringVar(master=self.master)
        self.cie = tk.StringVar(master=self.master)
        self.phone = tk.StringVar(master=self.master)
        self.email = tk.StringVar(master=self.master)
        
        ttk.Label(self.frame, text='Prenom*: ').pack(fill='x', expand=True)
        ttk.Entry(self.frame, textvariable= self.firstname).pack(fill='x', expand=True,)
        ttk.Label(self.frame, text=' ').pack(fill='x', expand=True)
        
        ttk.Label(self.frame, text='Nom*: ').pack(fill='x', expand=True)
        ttk.Entry(self.frame, textvariable= self.lastname).pack(fill='x', expand=True)
        ttk.Label(self.frame, text=' ').pack(fill='x', expand=True)
        
        ttk.Label(self.frame, text='cie: ').pack(fill='x', expand=True)
        ttk.Entry(self.frame, textvariable= self.cie).pack(fill='x', expand=True)
        ttk.Label(self.frame, text=' ').pack(fill='x', expand=True)
        
        ttk.Label(self.frame, text='Telephone*: ').pack(fill='x', expand=True)
        ttk.Entry(self.frame, textvariable= self.phone).pack(fill='x', expand=True)
        ttk.Label(self.frame, text=' ').pack(fill='x', expand=True)
        
        ttk.Label(self.frame, text='email: ').pack(fill='x', expand=True)
        ttk.Entry(self.frame, textvariable= self.email).pack(fill='x', expand=True)
        
        self.button_grid = ttk.Frame(self.frame)
        ttk.Button(self.button_grid, text='Go back', command=self.go_back, padding=20).grid(column=1, row=1, padx=10, pady=10)
        ttk.Button(self.button_grid, text='Submit', command=self.submit, padding=20).grid(column=2, row=1, padx=10, pady=10)
        self.button_grid.pack(pady=20)
        
    def clear_out(self):
        self.firstname.set('')
        self.lastname.set('')
        self.cie.set('')
        self.phone.set('')
        self.email.set('')
        
    def start_page(self):
        self.frame.pack()

    def go_back(self):
        self.frame.pack_forget()
        self.clear_out()
        self.app.main_page()
        
    def submit(self):
        try: 
            client = Client(
                self.firstname.get()
                , self.lastname.get()
                , self.cie.get()
                , self.phone.get()
                , self.email.get()
            )
            clientid = get_client_id(db, client)   
        except Exception as e:
            messagebox.showerror(title='Error',message= e)
            
        message = str(f'Client id: {clientid} \n{client}')    
        messagebox.showinfo(title='Success', message= message)
        self.clear_out()
        self.frame.pack_forget
        self.app.main_page()
        
class Billing:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        ttk.Label(self.frame, text='Billing', padding= 10).pack()
        ttk.Button(self.frame, text='Go back', command=self.go_back).pack()
        
    def start_page(self):
        self.frame.pack()

    def go_back(self):
        self.frame.pack_forget()
        self.app.main_page()
        
class Searchbills:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        ttk.Label(self.frame, text='Search Bills', padding= 10).pack()
        ttk.Button(self.frame, text='Go back', command=self.go_back).pack()
        
    def start_page(self):
        self.frame.pack()

    def go_back(self):
        self.frame.pack_forget()
        self.app.main_page()
        
class Sales:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        ttk.Label(self.frame, text='Sales', padding= 10).pack()
        ttk.Button(self.frame, text='Go back', command=self.go_back).pack()
        
    def start_page(self):
        self.frame.pack()

    def go_back(self):
        self.frame.pack_forget()
        self.app.main_page()

def main():
    root = tk.Tk()
    root.geometry("800x600")
    style = ttk.Style()
    root.tk.call("source", "tkBreeze-master/breeze-dark/breeze-dark.tcl")
    style.theme_use("breeze-dark")
    app = myApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()

import re
from datetime import date
import sqlite3

""" 
                      THI IS THE HELPER FILE
                      
        the class manage all the validation of the input of the data
    so once we manage to create one of these object, the are correctly insert in the database
        That way we ensure that the database remain as clean as possible.    
"""

class Client:
    def __init__(self, firstname, lastname, cie, phone, email):
        self.firstname = firstname
        self.lastname = lastname
        self.cie = cie
        self.phone = phone
        self.email = email
    def __str__(self):
        return f"First name: {self.firstname} \nLast name: {self.lastname}\nCompagnie: {self.cie}\nPhone: {self.phone}\nE-mail: {self.email}"
    
    @property
    def firstname(self):
        return self._firstname
    
    @firstname.setter
    def firstname(self, firstname):
        matches = re.search(r"^[a-z]+?(-|\s)?([a-z]+)", firstname.lower())
        if not matches:
            raise ValueError("Invalid name")
        self._firstname = firstname.title()
        
    @property
    def lastname(self):
        return self._lastname
    
    @lastname.setter
    def lastname(self, lastname):
        matches = re.search(r"^[a-z]+?(-|\s)?([a-z]+)", lastname.lower())
        if not matches:
            raise ValueError("Invalid Name")
        self._lastname = lastname.title()
    
    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, phone):
        # regional
        matches = re.search(r"\d\d\d-\d\d\d-\d\d\d\d", phone)
        if not matches:
			# nationa
            matches = re.search(r"\d-\d\d\d-\d\d\d-\d\d\d\d", phone)
            if not matches:
			# international
                matches = re.search(r"+\d\d\s(.+)")
                if not matches: 
                    raise ValueError("Invalid phone number")
        self._phone = phone
        
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        matches = re.search(r".+@.+\.[a-z][a-z]?[a-z]", email)
        if not matches:
            raise ValueError("invalid Email")
        self._email = email
            
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def __str__(self):
        return f"{self.quantity:1}  | {self.name} | {self.price:2f}$"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        matches = re.search(r"^[a-z]+", name.lower())
        if not matches:
            raise ValueError("Invalid Name")
        self._name = name.title()

        
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
        self._price = float(price)
        
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity):
        self._quantity = float(quantity)
        
class ticket:
    def __init__(self, ids, note):
        self.id = ids 
        self.note = note
    
    def __str__(self):
        return f"Ticket id: {self.id}\n\n{self.note}"
    
    
"""
This is Where Function Begin !! 
the Goal is to use append_bill in one line so it get all the informatation one shot as follow:

append_bill(db,listed,get_billing_id(db,get_client_id(db,client),sumy),ticket)

""" 
 
   
def append_bill(db, listed,billing_id, ticket=None):
    for item in listed:
        db.execute("INSERT INTO bill (biling_id, product_qt, product_name, product_price)",
                   billing_id, item.quantity, item.name, item.price)
        
        db.execute("INSERT INTO tickets (note) VALUES (?)", ticket.note)
        pdf_gen()
        
    
def get_billing_id(db, client_id, sumy):
    today = date.today()
    db.execute("INSERT INTO billings (client_id, bill_date, total) VALUES (?,?,?)",
               client_id, today, sumy)
    
    return db.execute("SELECT id FROM billing WHERE client_id = ? and bill_date= ?, total = ?",
                      client_id, today, sumy)
    
    
def get_client_id(db, client):
    
    mycursor = db.cursor()
    mycursor.execute("SELECT id FROM clients WHERE firstname = ? AND lastname = ? AND phone = ?", (client.firstname, client.lastname, client.phone))
    clientid = mycursor.fetchone()
    if clientid == None:
        mycursor.close()
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO clients (firstname, lastname, cie, phone, email) VALUES (?,?,?,?,?)",
                (client.firstname, client.lastname, client.cie, client.phone, client.email))
        db.commit()
        
        mycursor.execute("SELECT id FROM clients WHERE firstname = ? AND lastname = ? AND phone = ?",
                        (client.firstname, client.lastname, client.phone))
        clientid = mycursor.fetchone()
        mycursor.close()    
    return format_id(clientid)

def format_id(id):
    id = str(id)
    id = id.replace('(','')
    id = id.replace(')','')
    return id.replace(',','')

def get_sum(listed):
    sumy = 0
    for item in listed:
        sumy += (item.quantity * item.price)
    return sumy

def pdf_gen():
    pass


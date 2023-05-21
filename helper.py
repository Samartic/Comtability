from csv import writer
from datetime import date
from fpdf import FPDF
from re import search
from subprocess import call
from win32print import GetDefaultPrinter

""" 
                      THI IS THE HELPER FILE
                      
        the class manage all the validation of the input of the data
    so once we manage to create one of these object, the are correctly insert in the database
        That way we ensure that the database remain as clean as possible.    
"""
today = date.today()
pw = 210 - 20

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
        matches = search(r"^[a-z]+?(-|\s)?([a-z]+)", firstname.lower())
        if not matches:
            raise ValueError("Invalid name")
        self._firstname = firstname.title()
        
    @property
    def lastname(self):
        return self._lastname
    
    @lastname.setter
    def lastname(self, lastname):
        matches = search(r"^[a-z]+?(-|\s)?([a-z]+)", lastname.lower())
        if not matches:
            raise ValueError("Invalid Name")
        self._lastname = lastname.title()
    
    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, phone):
        # regional
        matches = search(r"\d\d\d-\d\d\d-\d\d\d\d", phone)
        if not matches:
			# nationa
            matches = search(r"\d-\d\d\d-\d\d\d-\d\d\d\d", phone)
            if not matches:
			# international
                matches = search(r"+\d\d\s(.+)")
                if not matches: 
                    raise ValueError("Invalid phone number")
        self._phone = phone
        
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        matches = search(r".+@.+\.[a-z][a-z]?[a-z]", email)
        if not matches:
            raise ValueError("invalid Email")
        self._email = email
   
class PDF(FPDF):
    def __init__(self):
        super().__init__()
    def header(self):
        self.set_font('Arial', '', 8)
        self.image("template\logo.png", w=(pw/3))
        self.cell(w=(pw/2),h=5,txt= "YOUR CIE NAME", border =0,ln= 0) # add your own info
        self.cell(w=(pw/2),h=5, txt=f"Date: {today}", border=0, ln=1, align="R") 
        self.cell(0, 5, "YOUR ADDRESS LINE 1", 0, 1, "L") # add your own info
        self.cell(0, 5, "TOWN (PV) POS123",0) # add your own info
        
    def footer(self):
        self.set_y(-25)
        self.set_font('Arial', "BI", 12)
        self.cell(0, 25, 'Merci de votre confiance !', 0, 0, 'C')   
            
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def __str__(self):
        return f"{self.quantity:1}  | {self.name} | {self.price:.2f}$"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        matches = search(r"^[a-z]+", name.lower())
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

append_bill(db,listed,get_billing_id(db,get_client_id(db,client),total),ticket)

""" 
 
   
def append_bill(db, listed, clientid, total = 0, ticket=None):
    if clientid == None:
        raise TypeError("Vous avez besoin d'un client")
    if not listed:
        raise TypeError("Aucun produit a facture")
    else:
        billing_id = get_billing_id(db, clientid, total)
        for row in listed:
            cur = db.cursor()
            cur.execute("INSERT INTO bills (billing_id, product_qt, product_name, product_price) VALUES (?,?,?,?)",
                        (billing_id, row.quantity, row.name, row.price))
            db.commit()
        cur.close()
        if ticket:
            cur = db.cursor()
            cur.execute("INSERT INTO tickets (note) VALUE (?)", (ticket,))
            db.commit()
    return billing_id

def confirm_client(db, firstname =None, lastname = None, cie=None, phone = None, email=None):
    query = "SELECT id FROM clients WHERE "
    values = []
    if firstname:
        query += "firstname = ? "
        values.append(firstname)
        if lastname or cie or phone or email:
            query += "AND "
    if lastname:
        query += "lastname = ? "
        values.append(lastname)
        if cie or phone or email:
            query += "AND "
    if cie:
        query += "cie = ? "
        values.append(cie)
        if phone or email:
            query += "AND "
    if phone:
        query += "phone = ? "
        values.append(phone)
        if email:
            query += "AND "
    if email:
        query += "email = ?"
        values.append(email)
    query.strip
    cur = db.cursor()
    cur.execute(query,values)
    return format_id(cur.fetchall())
                          
def format_id(id):
    id = str(id)
    id = id.replace('(','')
    id = id.replace(')','')
    id = id.replace("[", "")
    id = id.replace("]", "")
    id = id.replace(',','')
    return id.strip()

def format_result(result):
    result[:] = [str(entry) for entry in result]
    result[:] = [entry.replace("(", "")  for entry in result]
    result[:] = [entry.replace(")", "") for entry in result]
    result[:] = [entry.replace("'","") for entry in result]
    result[:] = [entry.strip() for entry in result]
    result[:] = [entry.replace(",", "   ") for entry in result]
    return result

def gen_pdf(Client=None, clientid=None, list=None, Sum=None, billid = 0): 
    pdf = PDF()
    pdf.set_font('Arial', '', 10)
    pdf.add_page()
    pdf.set_y(50)
    
    
    # client
    pdf.cell((pw/2),5,f"ID: {clientid}",0,0,"L")
    pdf.cell((pw/2),5,f"Facture : {billid}",0,1,"R")
    pdf.cell((pw),5, f"Nom: {Client.firstname} {Client.lastname}",0,1, "L")
    pdf.cell((pw),5, f"Cie: {Client.cie}",0,1, "L")
    pdf.cell((pw), 5, f"Téléphone: {Client.phone}",0,1, "L")
    pdf.cell((pw), 5, f"E-mail: {Client.email}",0,1, "L")
    
    pdf.set_y(85)
    pdf.set_left_margin(15)
    
    # header 
    pdf.set_font("Arial", "B", 10)
    pdf.cell(25,10, "Qt", 0,0, "C")
    pdf.cell((2*pw/3),10, '  Produit',0,0, "C")
    pdf.cell(35,10, "Prix", 0,1, "C")
    pdf.line(20,95,pw,95)
    
    # Table
    pdf.set_font("Arial", "", 10)
    for row in list:
        qt = row.quantity
        if qt.is_integer():
            pdf.cell(25,5, f"{row.quantity:.0f}", 0,0,"C")
        else:
            pdf.cell(25,5, f"{row.quantity:.1f}", 0,0,"C")
        pdf.cell((2*pw/3) ,5,f"{row.name}",0,0,"L")
        pdf.cell(35,5, f"{row.price:.2f} $", 0, 1, "C")
        
    
    pdf.set_y(-50)
    pdf.set_font("Arial", "", 14)
    pdf.cell((2*pw/3)+25,10, "Total: ",0,0,"R") 
    pdf.set_font("Arial", "B", 14)
       
    pdf.cell(35,10,f"{Sum:.2f} $",1,1, "C")
    pdf.line(20,270,pw,270)
    file = f'./facture/facture_{billid}.pdf' 
    pdf.output(file, 'F')
    file = file.replace("./","")
    return file
 
def get_billing_id(db, client_id, total):
    today = date.today()
    cur = db.cursor()
    cur.execute("INSERT INTO billings (clients_id, bill_date, total) VALUES (?,?,?)",
               (client_id, today, total))
    db.commit()
    cur.close()
    cur = db.cursor()
    cur.execute("SELECT id FROM billings WHERE clients_id = ? AND bill_date= ? AND total = ?",
                      (client_id, today, total))
    result = str(cur.fetchone())
    result = result.replace("(","")
    result = result.replace(")","")
    result = result.replace(",","")
    return result.strip()

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
 
def get_client_fromid(clientid, db):
    cur = db.cursor()
    cur.execute("SELECT * FROM clients WHERE id = ?", (clientid,))
    result = cur.fetchall()
    result[:] = [str(entry) for entry in result]
    result[:] = [entry.replace("(", "")  for entry in result]
    result[:] = [entry.replace(")", "") for entry in result]
    result[:] = [entry.strip() for entry in result]
    for row in result:
        list = row.split(",")
        list[:] = [entry.strip() for entry in list]
        list[:] = [entry.replace("'", "") for entry in list]
        
        client = Client(list[1], list[2], list[3], list[4], list[5])
    cur.close()
    return client    

def get_id(result):
    result[:] = [str(entry) for entry in result]
    result[:] = [entry.replace("(", "")  for entry in result]
    result[:] = [entry.replace(")", "") for entry in result]
    result[:] = [entry.strip() for entry in result]
    for row in result:
        list = row.split(",")
        list[:] = [entry.strip() for entry in list]
        list[:] = [entry.replace("'", "") for entry in list]
                   
    return str(list[0])

def get_date(input):
    if "/" in input:
        year, month, day = input.split("/")
        return date(int(year), int(month), int(day))
    
    elif "-" in input:
        year, month, day = input.split("-")
        return date(int(year), int(month), int(day))
    else:
        raise ValueError("Date invalid")

def get_sum(listed):
    total = 0
    for item in listed:
        total += (item.quantity * item.price)
    return total

def get_report(db, start, end):
    start = get_date(start)
    end = get_date(end)
    cur = db.cursor()
    cur.execute("SELECT billings.bill_Date, product_qt, product_name, product_price  FROM bills LEFT JOIN billings ON billings.id = bills.billing_id WHERE billing_id IN (SELECT id FROM billings WHERE bill_Date > ? AND bill_Date < ? )"
            , (start, end))
    result = cur.fetchall()
    cur.close()
    if result:
        try: 
            report = f"sale_report {start} - {end}.csv"
            header = ["Date", "Qt", "Produit", "prix"]
            with open(report, 'w') as f:
                wt = writer(f)
                wt.writerow(header)
                for row in result:
                    wt.writerow(row)
                return report
        except Exception as e:
            return e
    else:
        return "No result"
    
def message_format(result):
    message = ""
    result[:] = [str(entry) for entry in result]
    result[:] = [entry.replace("(", "")  for entry in result]
    result[:] = [entry.replace(")", "") for entry in result]
    result[:] = [entry.strip() for entry in result]
    for row in result:
        list = row.split(",")
        list[:] = [entry.strip() for entry in list]
        list[:] = [entry.replace("'", "") for entry in list]
        
        client = Client(list[1], list[2], list[3], list[4], list[5])        
        message += "ID: " + str(list[0]) + "\n" + str(client) + "\n"
    return message

def printer(str_file):
    acrobat = "C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"
    defaultPrinter = GetDefaultPrinter()
    print(defaultPrinter)
    call([acrobat, "/T", str_file, defaultPrinter])      
   
def query_generator(db, title, query):
    cur= db.cursor()
    cur.execute(query)
    result = cur.fetchall()
    with open(f"{title}.csv", "w") as f:
        wt = writer(f)
        for row in result:
            wt.writerow(row)
        return True
        
def search_bills(db, start=None, end=None, firstname=None, lastname=None, phone=None, total=None):
    cur = db.cursor()
  
    query = "SELECT bill_Date, billings.id, clients.firstname, clients.lastname, total FROM billings LEFT JOIN clients ON clients_id = clients.id WHERE"
    variable = []

    if start:
        query += f" bill_Date > ? AND"
        variable.append(get_date(start))
    if end:
        query += f" bill_date < ? AND"
        variable.append(get_date(end))
    if firstname or lastname or phone:
        query += " clients_id IN (SELECT id FROM clients WHERE "
    
    
        if firstname:
            if lastname or phone:
                query += "firstname = ? OR"

            else:
                query += "firstname = ?"

            variable.append(firstname.title())
        if lastname:
            if phone:
                query += f"lastname = ? OR"

            else:
                query += f"lastname = ?"

            variable.append(lastname.title())
        if phone:
            query += f"phone = ?"
            variable.append(phone)
        query += ")"
        
    if total:
        if firstname or lastname or phone:
            query += " AND total = ?"
        else:
            query += " total = ?"
        variable.append(total)
        
   

    cur.execute(query, variable)
    result = cur.fetchall()
    cur.close()
    return result
            
def search_client(db ,option, input):
    cur = db.cursor()
    if option == "Nom":
        if " " in input:
            firstname, lastname = input.title().split(" ")
            cur.execute("SELECT * FROM clients WHERE firstname = ? OR lastname = ?"
                        , (firstname, lastname))
        else:
            input = input.title()
            cur.execute("SELECT * FROM clients WHERE firstname = ? OR lastname = ?"
                        , (input.title(), input.title()))
    else:
        if option == "Téléphone":
            option = "phone"

        cur.execute("SELECT * FROM clients WHERE ?=?", (option, input))
        
    test = cur.fetchall()
    cur.close()
    return test
    



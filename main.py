# Imports
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date
import psycopg2

# ------- Window init & configuration ------- #
root = tk.Tk() 
root.geometry("1280x720")
root.title("Stationzuil")

# ---------------- Variables ---------------- #
optionMenuText = tk.StringVar()
optionMenuText.set("Selecteer een station")

hostname = "localhost"
database = "postgres"
username = "postgres"
pwd = ""
port_id = "5432"
conn = None
cur = None

# ------------- Base functions -------------- #
# Make the widgets invisible
class PlaceholderEvent:
    def __init__(self, name="Placeholder Event"):
        self.name = name

    def execute(self):
        pass  # This is a no-op function, it does nothing

# Create a placeholder event
event = PlaceholderEvent()

def data_manipulation(operation):
    try:
        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id)
        cur = conn.cursor()

        # Fetch login records
        if operation == 0:
            cur.execute("""SELECT station_city FROM station_service;""")
            listOfRecords = []
            for record in cur.fetchall():
                listOfRecords.append(record[0])
            return listOfRecords
        elif operation == 1:
            script = """SELECT * FROM gebruiker;"""
            cur.execute(script)
            listOfRecords = []
            for record in cur.fetchall():
                listOfRecords.append(record)
            return listOfRecords
        elif operation == 2:
            List = []
            with open("Stationzuil/berichten.csv", "r") as file:
                lines = file.readlines()
            with open("Stationzuil/gemodereerde_berichten.csv", "r") as file:
                afgewezen_lines = file.readlines()
            with open("Stationzuil/berichten.csv", "w") as file:
                for line in lines:
                    line = line.strip('\n')
                    line = line.split(';')
                    line.append("yes")
                    insert1 = []
                    for attribute in line:
                        insert1.append(attribute)
                    insert1 = tuple(insert1)
                    List.append(insert1)
            with open("Stationzuil/gemodereerde_berichten.csv", "w") as file:
                for line in afgewezen_lines:
                    line = line.strip('\n')
                    line = line.split(';')
                    line.append("no")
                    insert2 = []
                    for attribute in line:
                        insert2.append(attribute)
                    insert2 = tuple(insert2)
                    List.append(insert2)
            insert_script = 'INSERT INTO messages VALUES (%s, %s, %s, %s, %s);'
            for record in List:
                cur.execute(insert_script, record)
        elif operation == 3:
            cur.execute("SELECT * FROM messages WHERE goedgekeurd = 'yes';")
            table = cur.fetchall()# TODO You should fetch records and Datetime.datetime is weird man bro ik zweer jou!
            list(table)
            for i in range(0, len(table)):
                table[i] = list(table[i])
            for item in table:
                item[3] = item[3].strftime('%Y-%m-%d %H:%M:%S')
            return table

        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
options = data_manipulation(0)

def make_visable(widget):
   widget.pack()

# Make the widgets visible
def make_invisible(widget):
   widget.pack_forget()

# Make Frames with grid layout invisable
def change_screen(invisable, visable):
   invisable.pack_forget()
   visable.pack(fill=tk.BOTH, expand=True)

def toggle_moderator_panel(invisable, visable):
    invisable.grid_forget()
    visable.columnconfigure(0, weight=1)
    visable.columnconfigure(1, weight=1)
    visable.columnconfigure(2, weight=1)
    visable.columnconfigure(3, weight=70)
    visable.rowconfigure(0, weight=1)
    visable.rowconfigure(1, weight=1)
    visable.rowconfigure(2, weight=1)
    visable.rowconfigure(3, weight=1)
    visable.grid(row=1)

def check_credentials(usrInput, pswInput):
    List = data_manipulation(1)
    for i in range(0, len(List)):
        if usrInput.lower() == List[i][0].strip(' '):
            if pswInput == List[i][1].strip(' '):
                if List[i][2]:
                    change_screen(loginScreen, mainScreen)
                    toggle_moderator_panel(messageInputFrame, adminFrame)
                else:
                    change_screen(loginScreen, mainScreen)
                    toggle_moderator_panel(adminFrame, messageInputFrame)
       

def send_pending_message():
    name = "Anonymous"
    if nameEntry.get() != "":
        name = nameEntry.get()
    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")
    today_date = str(date.today()) + " "
    finalTime = today_date + currentTime
    with open('Stationzuil/berichten.csv', 'a+') as file:
        text = name + ";" + optionMenuText.get() + ";" + messagebar.get() + ";" + finalTime + "\n"
        file.write(text)
        file.close()

def check_message_contents():
    if len(nameEntry.get()) <= 16 and optionMenuText.get() in options and len(messagebar.get()) <= 140 and len(messagebar.get()) >= 10:
        send_pending_message()
        nameEntry.delete(0, tk.END)
        messagebar.delete(0, tk.END)
    else:
        messagebox.showinfo(title="Ongeldige verzending", message="Je bericht moet minimaal 10 en maximaal 140 characters bevatten, je naam mag maximaal 16 characters lang zijn en je moet een station kiezen waar je een bericht over wilt schrijven.")

def frame_clearing():
    for widget in message_container.winfo_children():
        widget.destroy()

def file_reader():
    result = []
    with open('Stationzuil/berichten.csv') as file:
        text = file.read()
        lines = text.split('\n')
        for line in lines:
            if line:
                parts = line.split(';')
                result.append(parts)
    return result

def delete_line(item):
    text = item[0] + ";" + item[1] + ";" + item[2] + ";" + item[3] + "\n"
    text1 = item[0] + ";" + item[1] + ";" + item[2] + ";" + item[3]
    
    with open('Stationzuil/berichten.csv', "r") as file:
        lines = file.readlines()
        savedLine = ""

    with open('Stationzuil/gemodereerde_berichten.csv', "a+") as file:
        for line in lines:
            if line == text:
                file.write(text)
        if lines[-1] == text1:
            file.write(text)

    with open('Stationzuil/berichten.csv', "w") as file:
        for line in lines:
            if line != text and line != text1:
                file.write(line)

def print_message(event):
    frame_clearing()
    if adminFrame.winfo_ismapped():
        result = file_reader()
    elif not adminFrame.winfo_ismapped():
        result = data_manipulation(3)
    print(result)
    List = []
    line = 0
    for item in result:
        if item[1].strip() == optionMenuText.get():
            List.append(item)
    for item in List:
        # Name label
        lbl = tk.Label(message_container, text="    " + item[0], font=('Arial', 12), bg="#C0C0C0")
        lbl.grid(row=line, column=0, sticky='nw', pady=20)
        # Time Stamp label
        lbl1 = tk.Label(message_container, text=item[3], font=('Arial', 12), bg="#C0C0C0")
        lbl1.grid(row=line, column=1, sticky='ne', pady=20)
        # Message label
        lbl = tk.Label(message_container, text=item[2], font=('Arial', 12), bg="#C0C0C0")
        lbl.grid(row=line, column=0, sticky='w', pady=20)
        # Delete button
        if adminFrame.winfo_ismapped():
            button = tk.Button(message_container, text="Delete", font=('Arial', 12), bg="#C0C0C0", command=lambda:delete_line(item))
            button.grid(row=line, column=1, sticky='e', pady=30)
        canvas = tk.Canvas(message_container, height=1, bg="black")
        canvas.grid(row=line, column=0, columnspan=2, sticky="ews")
        canvas.create_line(0, 0, 1920, 0, fill="black", width=1)
        line += 1

# ------------------------------------ Widget implementation ------------------------------------ #
# Login screen init
loginScreen = tk.Frame(root)
loginScreen.pack(fill=tk.BOTH, expand=True)

# Main screen init
mainScreen = tk.Frame(root)
mainScreen.columnconfigure(0, weight=1)
mainScreen.rowconfigure(0, weight=20)
mainScreen.rowconfigure(1, weight=1)
mainScreen.pack(fill=tk.BOTH, expand=True)

# ----------- Login page content ----------- #
# Login text
loginLabel = tk.Label(loginScreen, text="Stationzuil login", font=('Arial', 48), width=40)
loginLabel.pack(pady=100)

# Username label & Entry
usrLabel = tk.Label(loginScreen, text="Username:                                      ", font=('Arial', 16))
usrLabel.pack()
 
usrEntry = tk.Entry(loginScreen, width=42)
usrEntry.pack()

# Password label & Entry
pswLabel = tk.Label(loginScreen, text="Password:                                      ", font=('Arial', 16))
pswLabel.pack()

pswEntry = tk.Entry(loginScreen, width=42)
pswEntry.pack()

# Login button init
loginButton = tk.Button(loginScreen, text="Login", width=4, height=1, command=lambda:check_credentials(usrEntry.get(), pswEntry.get()), font=('Arial', 16))
loginButton.pack(pady=20)

# --------- Main page content (user) -------- #
# Messagebox init
message_container = tk.Frame(mainScreen, bg="#C0C0C0")
message_container.columnconfigure(0, weight=1)
message_container.columnconfigure(1, weight=1)
message_container.rowconfigure(0, weight=1)
message_container.rowconfigure(1, weight=1)
message_container.rowconfigure(2, weight=1)
message_container.rowconfigure(3, weight=1)
message_container.rowconfigure(4, weight=1)
message_container.rowconfigure(5, weight=1)
message_container.rowconfigure(6, weight=1)
message_container.rowconfigure(7, weight=1)
message_container.grid(row=0, sticky="news")

# Messege Input Frame
messageInputFrame = tk.Frame(mainScreen)
messageInputFrame.grid(row=1)

# Name label
nameLabel = tk.Label(messageInputFrame, text="Name")
nameLabel.grid(row=0, column=0)

# Name entry
nameEntry = tk.Entry(messageInputFrame)
nameEntry.grid(row=0, column=1)

# Option menu station
optionMenu = tk.OptionMenu(messageInputFrame, optionMenuText, *options, command=print_message)
optionMenu.grid(row=0, column=4)

# Messagebar
messagebar = tk.Entry(messageInputFrame)
messagebar.grid(row=1, column=0, sticky="ew", columnspan=6)

# Enterbutton
enterButton = tk.Button(messageInputFrame, text="Enter", width=4, height=1, font=('Arial', 16), command=check_message_contents)
enterButton.grid(row=2, column=0, columnspan=6)

# Logout button init
logoutButton = tk.Button(messageInputFrame, text="Logout", width=4, height=1, font=('Arial', 16), command=lambda:change_screen(mainScreen, loginScreen))
logoutButton.grid(row=3, column=0, columnspan=6)

# -------- Main page content (admin) -------- #
adminFrame = tk.Frame(mainScreen)
adminFrame.rowconfigure(0, weight=1)
adminFrame.rowconfigure(1, weight=1)
adminFrame.rowconfigure(2, weight=1)
adminFrame.rowconfigure(3, weight=1)
adminFrame.grid(row=1)

optionMenu1 = tk.OptionMenu(adminFrame, optionMenuText, *options, command=print_message)
optionMenu1.grid(row=0)

reloadButton = tk.Button(adminFrame, text="Reload", width=10, height=1, command=lambda:print_message(event))
reloadButton.grid(row=1)

sendDataButton = tk.Button(adminFrame, text="Send messages", width=10, height=1, command=lambda:data_manipulation(2))
sendDataButton.grid(row=2)

logoutButton1 = tk.Button(adminFrame, text="Logout", width=4, height=1, command=lambda:change_screen(mainScreen, loginScreen))
logoutButton1.grid(row=3)

make_invisible(loginScreen)
#toggle_moderator_panel(messageInputFrame, adminFrame)
toggle_moderator_panel(adminFrame, messageInputFrame)

# --------------- Window loop --------------- #
root.mainloop()
from tkinter import *
import serial as s
import threading

''' Globální proměnné '''
isText = True
port = NONE

''' Funkce, které GUI appka pouzívá'''
def send():
    try:
        global port
        port.write(bytes(fieldInput.get(), 'ascii'))
    except:
        print("Something messed up")


def hex():
    global isText
    if(isText):
        isText = False
    else:
        isText = True


def read(port):
    ''' Běží ve vlákně, čte data, které port přijal '''
    while(True):
        ''' Z nějakého důvodu je komunikace příjímána ve stylu b'ZPRAVA', proto substring '''
        global isText
        dataRead = port.read(255)
        dataRead = str(dataRead)[2 : len(str(dataRead)) - 1]
        if isText:
            fieldOutput.config(state='normal')
            fieldOutput.insert(INSERT, dataRead + " ")
            fieldOutput.config(state='disabled')
        else:
            fieldOutput.config(state='normal')
            for char in dataRead:
                fieldOutput.insert(INSERT, str(ord(char)) + " ")
            fieldOutput.insert(INSERT, "\n")
            fieldOutput.config(state='disabled')



def setPort():
    global port
    try:
        port = s.Serial("COM" + spinBoxPort.get(), spinBoxBaudrate.get())
        labelCurrentPort.config(text=("Current port: COM" + spinBoxPort.get()))
        threading.Thread(target=read, args=(port,), daemon=True).start()
        buttonSetPort.config(state=DISABLED)
    except:
        labelCurrentPort.config(text=("Current port: ERROR"))


''' Vytvoř okno a panel '''
window = Tk()
window.title("Serial communicator")
window.resizable(False, False)
frame = Frame(master=window, width=500, height=500)
frame.pack()

''' Přidej na panel komponenty '''
labelHeader = Label(master=frame, text="Serial communicator", font=("Consolas", 20))
labelHeader.place(x=10, y=5)
labelInput = Label(master=frame, text="Send message: ", font=("Consolas", 14))
labelInput.place(x=10, y=60)
fieldInput = Entry(master=frame, width=60)
fieldInput.place(x=10, y=90)
buttonSend = Button(master=frame, text="SEND", command=send)
buttonSend.place(x=400, y=85)

labelOutput = Label(master=frame, text="Received: ", font=("Consolas", 14))
labelOutput.place(x=10, y=120)
fieldOutput = Text(master=frame, width=60, state=DISABLED)
fieldOutput.place(x=10, y=150, width=360, height=75)
buttonHex= Button(master=frame, text="HEX/TXT", command=hex)
buttonHex.place(x=400, y=150)

''' Sekce nastavení '''
labelHeader = Label(master=frame, text="Settings", font=("Consolas", 20))
labelHeader.place(x=10, y=300)
labelPort = Label(master=frame, text="COM...", font=("Consolas", 14))
labelPort.place(x=10, y=355)
spinBoxPort = Spinbox(master=frame, from_=0, to=255)
spinBoxPort.place(x=150, y=360)
labelBaudrate = Label(master=frame, text="Baudrate...", font=("Consolas", 14))
labelBaudrate.place(x=10, y=390)
spinBoxBaudrate = Spinbox(master=frame, from_=1200, to=256000, increment=1200)
spinBoxBaudrate.place(x=150, y=390)
buttonSetPort = Button(master=frame, text="SET PORT", command=setPort)
buttonSetPort.place(x=400, y=390)
labelCurrentPort = Label(master=frame, text="Current port: ", font=("Consolas", 14))
labelCurrentPort.place(x=10, y=420)



window.mainloop()




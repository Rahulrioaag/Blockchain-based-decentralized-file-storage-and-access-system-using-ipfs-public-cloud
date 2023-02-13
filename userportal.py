import os
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import numpy as np
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import ipfshttpclient
import pickle
import hashlib
from pathlib import Path

client = ipfshttpclient.connect()
authstatus=0;
filenamealone="none"
class AccessInfo:
    def __init__(self,ipfshash,filecon,fileconhas,keys):
        self.ipfshash=ipfshash
        self.filecon=filecon
        self.fileconhas=fileconhas
        self.keys=keys

def getAccessFile():
    global accessfile
    global statuslabel,e1,e2
    global authstatus,filenamealone
    accessfile = fd.askopenfilename()

    filenamealone=Path(accessfile).stem

    
    keys=e1.get()
    with open(accessfile, "rb") as infile:
        ai = pickle.load(infile)

    if keys==ai.keys:
        statuslabel.config(text='Authentication sucess')
        authstatus=1
    else:
        statuslabel.config(text='Authentication failed')
        authstatus=0


def getFilefromIPFS():
    global filenametoget
    global statuslabel,e1,e2
    global authstatus
    global accessfile
    global filenamealone

    keys=e1.get()
    key=bytes(keys, 'utf-8')
    cipher = AES.new(key, AES.MODE_CBC)

    ks=len(key)
    if ks!=16:
        messagebox.showerror("Error", "key should be 16 characters")
        return

    if authstatus==0:
        messagebox.showerror("Error", "Authenticaiton is not done")
        return
    
    with open(accessfile, "rb") as infile:
        ai = pickle.load(infile)


    try:
        res2=client.block.get(ai.ipfshash)
    except:
        messagebox.showinfo("showinfo","Invalid hash key")
        return 
         
    file_out = open('downloadfile', "wb")
    file_out.write(ai.filecon)
    file_out.close()
    
    
    
    
    file_in = open('downloadfile', 'rb') # Open the file to read bytes
    iv = file_in.read(16) # Read the iv out - this is 16 bytes long
    ciphered_data = file_in.read() # Read the rest of the data
    file_in.close()

    filename = 'downloadfile'
    md5_hash = hashlib.md5()
    with open(filename,"rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
    
    hashcon=md5_hash.hexdigest()
    
    stt= 'File hash for encypted is ' + hashcon   
    print('File hash for encypted is ',hashcon)
    print('Hash in block chain is ',ai.fileconhas)

    stt= stt + '\n'+ ' Hash in block chain is ' + ai.fileconhas      
    if hashcon==ai.fileconhas:
        print('Hash are equal, file in integral')
        stt= stt + '\n'+ 'Hash are equal, file in integral'
    else:
        print('Hash are not equal file is corrupted');
        stt= stt + '\n'+ 'Hash are not equal file is corrupted'      
        

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # Setup cipher
    original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size) # Decrypt and then up-pad the result

    txtdata=original_data.decode('utf-8')

    #open text file
    decfile="decrypt-"+filenamealone + ".txt"
    text_file = open(decfile, "w")
 
    #write string to file
    text_file.write(txtdata)
 
    #close file
    text_file.close()
        
    messagebox.showinfo("showinfo", "decoded content written to "+decfile)


    
    statuslabel.config(text=stt)

import PIL.Image

if __name__ == "__main__":
    global parent
    global label
    global e1,e2,e3,e4,variable
    global mselabel
    global filenametostore   
    
    global statuslabel

    parent = tk.Tk()
    parent.geometry("700x500")
    parent.configure(bg='white')
    parent.title("Secure Access controlled data retreival")

    frame = tk.Frame(parent)
    frame.pack()

    fp = open('./bc.jpg',"rb")
    image2=PIL.Image.open(fp);
    import PIL.ImageTk       
    image1 = PIL.ImageTk.PhotoImage(image2)

    your_label = Label(master=parent, image=image1)
    your_label.place(x=0, y=0, relwidth=1, relheight=1)
    your_label.pack()
    

    w = tk.Label(frame, text="Data Retreival",
                     fg = "#0b102b",
                     font = ("Alfa Slab One", 40,"bold"))
    w.pack()

    w=tk.Label(frame, 
             text="Enter the 16 digit Secret Key",font=40)
    w.pack()
    e1 = tk.Entry(frame,bd=0,bg='white',highlightthickness=0,width=50,font=('Cooper 24'))
    e1.pack(padx=10, pady=7)

    # Separator object
    separator = ttk.Separator(frame, orient='horizontal')
    separator.pack(fill='x')

    
    text_disp= tk.Button(frame, 
                       text="BROWSE ACCESS FILE",bg='#283747',fg='white',activebackground='white',activeforeground='black',borderwidth='2',relief=tk.SOLID,font='Banhschrift 20',cursor='hand2',highlightbackground='red',
                       command=getAccessFile
                       )

    text_disp.pack()
    

    # Separator object
    separator = ttk.Separator(frame, orient='horizontal')
    separator.pack(fill='x')




    text_disp= tk.Button(frame, 
                       text="GET FILE",bg='#283747',fg='white',activebackground='white',activeforeground='black',borderwidth='2',relief=tk.SOLID,font='Banhschrift 20',cursor='hand2',highlightbackground='red',
                       command=getFilefromIPFS
                       )
    text_disp.pack()
     

    # Separator object
    separator = ttk.Separator(frame, orient='horizontal')
    separator.pack(fill='x')
    
    statuslabel=tk.Label(frame, 
             text="",fg="blue")
    statuslabel.pack()

    
    parent.mainloop()    

    


    

    

    



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
import PIL.Image
from pathlib import Path

client = ipfshttpclient.connect()
class AccessInfo:
    def __init__(self,ipfshash,filecon,fileconhas,keys):
        self.ipfshash=ipfshash
        self.filecon=filecon
        self.fileconhas=fileconhas
        self.keys=keys

def browseTextFile():
    global filenametostore,e1
    global statuslabel
    global client
    filenametostore = fd.askopenfilename(filetypes = (('text files','*.txt'),))
    statuslabel.config(text="File uploaded to cloud")

    filenamealone=Path(filenametostore).stem
    print("File name alone",filenamealone)

    keys=e1.get()
    key=bytes(keys, 'utf-8')
    cipher = AES.new(key, AES.MODE_CBC)

    ks=len(key)
    if ks!=16:
        messagebox.showerror("Error", "key should be 16 characters")
        return
        
    text_file = open(filenametostore, "r")
    data = text_file.read()
    text_file.close()

    bdata=bytes(data,'utf-8')
    ciphered_data = cipher.encrypt(pad(bdata, AES.block_size))

    

    file_out = open('encryptfile', "wb") 
    file_out.write(cipher.iv) 
    file_out.write(ciphered_data) 
    file_out.close()

    f = open("encryptfile", 'rb')
    binarycontent = f.read(-1)
    f.close()

    filename = 'encryptfile'
    md5_hash = hashlib.md5()
    with open(filename,"rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
    
    hashcon=md5_hash.hexdigest()

    res = client.add('encryptfile')
    
    print("File upload to IPFS hash is " + res['Hash'])
       
    stt="File upload to IPFS hash is " + res['Hash'];
    statuslabel.config(text=stt)
    
    ai=AccessInfo(res['Hash'],binarycontent,hashcon,keys)

    outfilename=filenamealone +".pickle"
    
    with open(outfilename, "wb") as outfile:
        # "wb" argument opens the file in binary mode
        pickle.dump(ai, outfile)
    

    messagebox.showinfo("Done", "File upload complete")
    

def addAccesscontrol():
    global filenametostore
    global statuslabel
    statuslabel.config(text="Added access control for users")

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
    parent.title("Secure Data Storage to Cloud")



    frame = tk.Frame(parent)
    frame.pack()

    fp = open('./bc.jpg',"rb")
    image2=PIL.Image.open(fp);
    import PIL.ImageTk       
    image1 = PIL.ImageTk.PhotoImage(image2)

    your_label = Label(master=parent, image=image1)
    your_label.place(x=0, y=0, relwidth=1, relheight=1)
    your_label.pack()
    
   
    w = tk.Label(frame, text="Data Storage",
                     fg = "#0b102b",
                     font = ("Alfa Slab One", 40,"bold"))
    w.pack()

    w=tk.Label(frame, 
             text="             Secret key (of length 16 characters)               ",font=40)
    w.pack()
    e1 = tk.Entry(frame,bd=0,bg='white',highlightthickness=0,width=50,font=('Cooper 24'))
    e1.pack(padx=10, pady=7)

    w=tk.Label(frame, 
             text="")
    w.pack() 

    # Separator object
    separator = ttk.Separator(frame, orient='horizontal')
    separator.pack(fill='x')

    
    text_disp= tk.Button(frame,
                       text="UPLOAD FILE",bg='#283747',fg='white',activebackground='white',activeforeground='black',borderwidth='2',relief=tk.SOLID,font='Banhschrift 20',cursor='hand2',highlightbackground='red',
                       command=browseTextFile
                       )
    text_disp.pack()


    w=tk.Label(frame, 
             text="")
    w.pack()
    
    
  

    # Separator object
    separator = ttk.Separator(frame, orient='vertical')
    separator.pack(fill='x')

    #w=tk.Label(frame, 
    #         text="ACCESS CONTROL")
    #w.pack()


    #w=tk.Label(frame, 
    #         text="USER ALLOWED ACCESS")
    #w.pack()
    #e2 = tk.Entry(frame)
    #e2.pack()

    #w=tk.Label(frame, 
    #         text="")
    #w.pack()


    #text_disp= tk.Button(frame, 
    #                   text="ADD ACCESS CONTROL", 
    #                   command=addAccesscontrol
    #                   )
    #text_disp.pack()
     

    statuslabel=tk.Label(frame, 
             text="",fg="blue")
    statuslabel.pack()

    
    parent.mainloop()    

    


    

    

    



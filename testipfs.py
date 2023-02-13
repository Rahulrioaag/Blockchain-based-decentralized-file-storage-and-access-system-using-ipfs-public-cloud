import ipfshttpclient
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
client = ipfshttpclient.connect()

#res = client.add('encryptfile')


#res2=client.block.get(res['Hash'])

#file_out = open('encryptfile', "wb") 
#file_out.write(res2) 
#file_out.close()

    
#f = open("encryptfile", 'rb')
#binarycontent = f.read(-1)
#res=client.block.put(binarycontent)

#print(res["key"])
    
keys='1234123412341234'
key=bytes(keys, 'utf-8')
file_in = open('encryptfile', 'rb') # Open the file to read bytes
iv = file_in.read(16) # Read the iv out - this is 16 bytes long
ciphered_data = file_in.read() # Read the rest of the data
file_in.close()
    

cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # Setup cipher
original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size) # Decrypt and then up-pad the result

txtdata=original_data.decode('utf-8')

print(txtdata)

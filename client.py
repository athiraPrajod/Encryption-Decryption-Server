from socket import *
import os
from cryptography.fernet import Fernet

serverName = '192.168.2.131'
serverPort = 7000

clientSocket = socket (AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

""" Encoding """
string=input("Input a string to encode into binary:")

clientSocket.send(string.encode())
modifiedString = clientSocket.recv(1024)
print("From Server: ", modifiedString.decode())



""" Decoding """
binary = input("Input a binary number (with spaces) to decode it: ")

clientSocket.send(binary.encode())
modifiedBinary = clientSocket.recv(1024)

print("From Server: ", modifiedBinary.decode())



""" Files """
SEPARATOR = ";"

BUFFER_SIZE = 1024

filename = "username.csv"

filesize = os.path.getsize(filename)

key = Fernet.generate_key()
  
with open('filekey.key', 'wb') as filekey:
   filekey.write(key)
   filekey.close()

key_file = "filekey.key"
keyFilesize = os.path.getsize(key_file)

with open('filekey.key', 'rb') as filekey:
    key = filekey.read()
    filekey.close()
  
fernet = Fernet(key)
  
with open('username.csv', 'rb') as origFile:
    original = origFile.read()
    origFile.close()
      
encrypted = fernet.encrypt(original)
with open('username.csv', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)
    
    
clientSocket.send(f"{filename}{SEPARATOR}{key_file}".encode())


with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            print("Nothing read")
            break
        print("In username read")
        clientSocket.sendall(bytes_read)
    f.close()


with open(key_file, "rb") as key:
    while True:
        bytes_read = key.read(keyFilesize)
        print(bytes_read)
        if not bytes_read:
            print("reading key file")
            break
        print("In key file")
        clientSocket.sendall(bytes_read)
    key.close()
        
clientSocket.close()   
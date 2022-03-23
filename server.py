from socket import *
from cryptography.fernet import Fernet
import os

serverPort = 7000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print("The server is ready to receive")


while True:
    connectionSocket, addr = serverSocket.accept()
    string = connectionSocket.recv(1024).decode()

    # Encoding

    binaryStr = ""
    for i in string:
        ascii_val = ord(i)
        bin_value = bin(ascii_val)
        binaryStr += bin_value[2:]

    connectionSocket.send(binaryStr.encode()) 

    # Decoding
    binary = connectionSocket.recv(1024).decode()
    bin_list = list(map(str, binary.split()))
    decoded_str = ""
    for i in bin_list:
        i_len = len(i)
        temp_ascii = 0
        for j in i:
            temp_ascii += int(j) * 2**(i_len - 1)
            i_len -= 1
        
        decoded_str += chr(temp_ascii)

    connectionSocket.send(decoded_str.encode())     


    # files
    #IP = gethostbyname(socket.gethostname())
    IP = '10.20.206.226'
    BUFFER_SIZE = 1024
    ADDR = (IP, serverPort)
    SEPARATOR = ";"

    received_file = connectionSocket.recv(BUFFER_SIZE).decode()
    print("received file ", received_file)
    print("split: ", received_file.split(SEPARATOR))
    filename, keyFile = received_file.split(SEPARATOR)
    # filename = "username.csv"
    # keyFile = "filekey.key"


    filename = filename.strip()
    keyFile = keyFile.strip()
    
    print(filename, keyFile)
    filename = os.path.basename(filename)
    keyFile = os.path.basename(keyFile)
    #keyFilesize = int(keyFilesize)

    with open(filename, "wb") as f:
        contents = ""
        while True:
            bytes_read = connectionSocket.recv(BUFFER_SIZE)
            if not bytes_read:  
                print("Nothing read")  
                break
            print("in username file read")
            f.write(bytes_read)
        f.close()
    
    key = ""
    with open(filename, "r") as f:
        print("filename = ", filename)
        noOfChars = 0
        while True:
            c = f.read(1)
            #print("c - ",c)
            if not c:
                break
            noOfChars += 1
        
        f.seek(noOfChars - 44)
        while True:
            c = str(f.read(1))
            if not c:
                break
            key += c
        print("key = ", key)
        f.close()

    with open(keyFile, "w") as kf:
        contents = ""
        kf.write(key)
        kf.close()
    connectionSocket.close()


    """ Decryption """

    key = ""
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()
    fernet = Fernet(key)
  
    with open('username.csv', 'rb') as enc_file:
        encrypted = enc_file.read()
    
    decrypted = fernet.decrypt(encrypted)
    
    with open('username.csv', 'wb') as dec_file:
        dec_file.write(decrypted)

serverSocket.close()
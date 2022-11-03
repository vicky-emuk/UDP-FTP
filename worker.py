import socket
import time
import os
from os.path import exists

localIP = "127.0.0.1"
bufferSize = 1024
serverAddressPort = (localIP, 20001)

# Create a datagram socket
# Binding to address and ip
UDPWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPWorkerSocket.bind((localIP, 20004))

print('UDP Worker is connected and operating.')

while True:
    time.sleep(0.1)
    bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    print('Worker is doing something...')

    file_name = message.decode('utf-8')
    script_dir = os.path.dirname('cAssignment1')  # <-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, file_name)

    if exists(file_name):
        new_file = open(file_name, 'rb')
        data = new_file.read(bufferSize)
        while data:
            if UDPWorkerSocket.sendto(data, serverAddressPort):
                data = new_file.read(bufferSize)
                time.sleep(1)
            print('Sent file to server.')
    else:
        UDPWorkerSocket.sendto(str.encode('NO_FILE'), serverAddressPort)
        print(f'No file {file_name} was found.')
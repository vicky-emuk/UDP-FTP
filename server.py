import socket
import time

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
workerAddressPorts = [(localIP, 20003), (localIP, 20004), (localIP, 20005)]
clientAddressPort = (localIP, 20002)

# Create a datagram socket
# Binding to address and ip
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

print('UDP server up and listening.')

while True:
    time.sleep(0.1)
    client_buffer = UDPServerSocket.recvfrom(bufferSize)[0]
    clientMsg = 'Message from client:{}'.format(client_buffer.decode('utf-8'))
    print(clientMsg)
    for workerAddressPort in workerAddressPorts:
        UDPServerSocket.sendto(client_buffer, workerAddressPort)    # sending file name to worker
        print(f'Client buffer sent to worker {workerAddressPort[0]}.')
        worker_buffer = UDPServerSocket.recvfrom(bufferSize)[0]     # saving data from worker to buffer
        print(f'Buffer received from worker {workerAddressPort[0]}.')
        UDPServerSocket.sendto(worker_buffer, clientAddressPort)    # sending buffer data to client
        print('Worker buffer sent to client')
        while not worker_buffer:                                    # splitting the file to prevent buffer overflow
            worker_buffer = UDPServerSocket.recvfrom(bufferSize)[0]
            print(f'Buffer received from worker {workerAddressPort[0]}.')
            UDPServerSocket.sendto(worker_buffer, clientAddressPort)
            print('Worker buffer sent to client')
    print('Sent file to client.')
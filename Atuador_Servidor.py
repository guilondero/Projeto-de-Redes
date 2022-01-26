#Importação de bibliotecas 
import socket
import serial
import struct
import time

#Defininação do IP, Porta, tamanho do buffer, e porta do arduino a ser usado
serverIP     = "192.168.100.2"
serverPort   = 9888
bufferSize   = 1024
arduinoPort  = 'COM4'

# Iniciando conexão serial
arduino = serial.Serial(port=arduinoPort, baudrate = 9600, timeout=1)
time.sleep(1)
arduino.setDTR(0)

print('\nObtendo informações sobre a comunicação serial\n')
print('Status Porta: %s ' %arduino.isOpen())
print('Dispositivo conectado: %s ' %arduino.name)
print('Configuração do dispositivo: %s\n'%arduino)

# Criação de uma socket UDP (datagram socket)
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Timeout das conexões foi definido como sendo de 5 segundos
UDPServerSocket.settimeout(5) 
print('Socket inicializada!')

# Bind da socket
UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
UDPServerSocket.bind((serverIP, serverPort))
print('Bind da socket realizada com sucesso!')

# Estado de Listen - esperando recepção de datagramas

while(1):

    #Recendo informação do controlador
    graus = UDPServerSocket.recvfrom(bufferSize)

    #Pegando valores em bytes 
    buffer = bytearray()
    buffer += graus[0]
    hexbytes = ''.join(format(x, '02X') for x in buffer)
   
    control_value = (buffer)
    
    #Fazendo unpack para float
    control_value = struct.unpack('>f', control_value)

    #Enviando informação para o arduino
    arduino.write(struct.pack('>B',int(control_value[0])))
    print("Posição do motor:", (control_value[0]),'°')
    

UDPServerSocket.close()
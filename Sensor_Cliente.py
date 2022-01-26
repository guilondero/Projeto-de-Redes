from os import name, read
import socket
import serial
import struct
import time
import sys

################################ CÓDIGO CLIENTE SENSOR/CONTROLADOR ######################################

# IP e Máscara do computador
# Endereço IPv4. . . . . . . .  . . . . . . . : 192.168.0.100
# Máscara de Sub-rede . . . . . . . . . . . . : 255.255.255.0

#Defininação do IP, Porta, tamanho deo buffer, e porta do arduino a ser usado
broadcastIP = '192.168.100.255'  #será usado pelo cliente para mandar os pacotes 
serverPORT = 9876
buffersize = 1024
arduinoPort = 'COM3'

# Criação de uma socket UDP para o cliente enviar para o servidor
UDPClientSendSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSendSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
print('Socket inicializada com sucesso!')

# Iniciando conexão serial
arduino = serial.Serial(port=arduinoPort, baudrate = 9600, timeout=1)

# Criando vetor de dados
sensor_value = []
print('\nObtendo informações sobre a comunicação serial\n')
print('Status Porta: %s ' %arduino.isOpen())
print('Dispositivo conectado: %s ' %arduino.name)
print('Configuração do dispositivo: %s\n'%arduino)


while (1):

    # Leitura dos valores medidos pelo sensor
    x = float(arduino.readline())
    sensor_value = str(x)

    #Resetando buffer     
    arduino.reset_input_buffer()
        
    
    #Verificando se é um vetor de 7 bytes (81209.0) ou de 8 bytes (121209.0)
    if (len(sensor_value) == 7 ):
        R = sensor_value[0]
        R = float(R)
        G = sensor_value[1:3]
        G = float(G)
        B = sensor_value[3:5]
        B = float(B)
    else:
        R = sensor_value[0:2]
        R = float(R)
        G = sensor_value[2:4]
        G = float(G)
        B = sensor_value[4:6]
        B = float(B)


    print(R, G, B)
    print ('#######################################')


    #Enviando informação através de bytes
    buffer = bytearray()
    buffer += bytearray(struct.pack(">f", R)) # ">" for "big endian" / "<" for "little endian"
    buffer += bytearray(struct.pack(">f", G)) # ">" for "big endian" / "<" for "little endian"
    buffer += bytearray(struct.pack(">f", B)) # ">" for "big endian" / "<" for "little endian"
    hexbytes = ''.join(format(x, '02X') for x in buffer)

    #Envia dados para o Servidor
    UDPClientSendSocket.sendto(buffer, (broadcastIP,serverPORT))
    
    
        
UDPClientSendSocket.close()
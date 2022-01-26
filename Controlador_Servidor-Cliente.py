import socket
import struct

###################### CÓDIGO CONTROLADOR COMO CLIENTE (CONTROLADOR -> ATUADOR) ######################


#Função que recebe a posição que o motor deve ir 
def control_client(graus):

    #Será usado pelo cliente para mandar os pacotes
    broadcastIP = '192.168.100.255'  
    #Porta em que envia dados ao Servidor Atuador
    serverPORT = 9888 

    # Criação de uma socket UDP para o cliente enviar para o servidor
    UDPClientSendSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSendSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    print('Socket inicializada com sucesso!')

    #Envia informação atraves de bytes
    MV_posicao = float(graus)
    buffer = bytearray()
    buffer += bytearray(struct.pack(">f", MV_posicao)) # ">" for "big endian" / "<" for "little endian"

    #Envia dados para o Servidor
    UDPClientSendSocket.sendto(buffer, (broadcastIP,serverPORT)) 

    UDPClientSendSocket.close()

#Defininação do IP, Porta, tamanho deo buffer
serverIP     = "192.168.100.2"
receivePort   = 9876 #Porta em que recebe dados do Cliente Sensor
bufferSize  = 1024


#Função que faz escolher qual cor o motor deve parar
def switch():
    print("Pressione 1 para: Azul claro \n Pressione 2 para: Azul escuro \n Pressione 3 para: Vinho \n Pressione 4 para: Vermelho \n ")
    option = int(input("Escolha a cor desejada: "))
     
    if option == 1:
        print("Cor escolhida: Azul claro")
        return 1
 
    elif option == 2:
        print("Cor escolhida: Azul escuro")
        return 2

    elif option == 3:
        print("Cor escolhida: Vinho")
        return 3

    elif option == 4:
        print("Cor escolhida: Vermelho")
        return 4

    else:
        print("Opção incorreta!") 
 
cor_desejada = switch()

# Criação de uma socket UDP (datagram socket)
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Timeout das conexões foi definido como sendo de 5 segundos
UDPServerSocket.settimeout(5) 
print('\nSocket inicializada!')

# Bind da socket
UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
UDPServerSocket.bind((serverIP, receivePort))
print('Bind da socket realizada com sucesso!')


contador = 0
contagem_max = 0
matriz = []
posicao_inicial = 0
posicao = 0
while(1):

    #Armazena a informação recebida do cliente na variavel message
    message = UDPServerSocket.recvfrom(bufferSize)
        
    #Adicionando os valores em um vetor
    buffer = bytearray()
    buffer += message[0]
    hexbytes = ''.join(format(x, '02X') for x in buffer)

   #Definição de quais bytes correspondem ao RED e aplicando o unpack nele 
    R = (buffer[0:4])
    R = struct.unpack('>f', R)
   
    #Definição de quais bytes correspondem ao GREEN e aplicando o unpack nele 
    G = (buffer[4:8])
    G = struct.unpack('>f', G)

    #Definição de quais bytes correspondem ao BLUE e aplicando o unpack nele 
    B = (buffer[8:12])
    B = struct.unpack('>f', B)
    


    print('Frequências:      [ R    G     B ]')
    print ('Mensagem cliente: ', R[0],G[0],B[0])

    ########################## FREQUÊNCIAS DE CADA COR #########################################
    setpoint_azul_claro = [23, 19, 12]
    setpoint_azul_forte = [22, 20, 14]
    setpoint_vinho      = [13, 16, 12]
    setpoint_vermelho   = [10, 15, 12] 

    ########################## IMPLEMENTAÇÃO DO CÓDIGO DE CONTROLE #############################
    R = int(R[0])
    G = int(G[0])
    B = int(B[0])

    #Armazenando os valores do sensor 
    PV = [R, G, B]

    #
    if(cor_desejada==1):

        #Definição do erro de cada variavel
        R_erro = setpoint_azul_claro[0] - R
        G_erro = setpoint_azul_claro[1] - G
        B_erro =  setpoint_azul_claro[2] - B
        
        #Erro
        erro = [R_erro, G_erro, B_erro]

        MV = 0 
        MV = int(MV)

        #Definição dos erros aceitaveis (padrão para todas as cores)
        if (erro == [0,0,0] or erro == [1,0,0] or erro == [0,1,0] or erro == [0,0,1] or erro == [1,2,1] or erro == [2,1,1] or erro==[1,1,2]):

            #Criação de um contador para saber quantas vezes ficou parado na cor
            contador = contador + 1
        else:

            #Caso não seja um aerro aceitavel o motor se move 5° e o contador zera 
            MV = 5
            contador = 0
    
    elif(cor_desejada==2):
        R_erro = setpoint_azul_forte[0] - R
        G_erro = setpoint_azul_forte[1] - G
        B_erro =  setpoint_azul_forte[2] - B
        
        erro = [R_erro, G_erro, B_erro]

        MV = 0 
        MV = int(MV)

        if (erro == [0,0,0] or erro == [1,0,0] or erro == [0,1,0] or erro == [0,0,1] or erro == [1,2,1] or erro == [2,1,1] or erro==[1,1,2]):
            MV = 0
            
            contador = contador + 1
        else:
            MV = 5
            contador = 0
    elif(cor_desejada==3):
        R_erro = setpoint_vinho[0] - R
        G_erro = setpoint_vinho[1] - G
        B_erro =  setpoint_vinho[2] - B

        erro = [R_erro, G_erro, B_erro]

        MV = 0 
        MV = int(MV)

        if (erro == [0,0,0] or erro == [1,0,0] or erro == [0,1,0] or erro == [0,0,1] or erro == [1,2,1] or erro == [2,1,1] or erro==[1,1,2]):
            MV = 0
            
            contador = contador + 1
        else:
            MV = 5
            contador = 0
    
    elif(cor_desejada==4):
        R_erro = setpoint_vermelho[0] - R
        G_erro = setpoint_vermelho[1] - G
        B_erro =  setpoint_vermelho[2] - B

        erro = [R_erro, G_erro, B_erro]

        MV = 0 
        MV = int(MV)

        if (erro == [0,0,0] or erro == [1,0,0] or erro == [0,1,0] or erro == [0,0,1] or erro == [1,2,1] or erro == [2,1,1] or erro==[1,1,2]):
            MV = 0

            contador = contador + 1
        else:
            MV = 5
            contador = 0
    
    #Fazendo o motor ir de 0 a 180
    if(posicao_inicial == 0):
        posicao = posicao + int(MV)
        if(posicao>180):
            posicao_inicial = 180


    #Fazendo o motor ir de 180 a 0
    if(posicao_inicial==180):
        posicao = posicao - int(MV)
        if(posicao<=0):
            posicao_inicial=0

    #Definição do contador maximo
    if (contador > contagem_max):
        contagem_max = contador


    print('Erro calculado: ', erro)
    print('Motor deve andar: ', MV, ' graus')
    print('Posição do motor: ', posicao, ' graus')
    print('Contagem de acerto: ', contador)
    print('Contagem mais alta: ', contagem_max)
    print('##############################################')

    #Enviando informação pra função de movimentação
    control_client(posicao)
    #Limpando a matriz para proxima leitura
    matriz.clear()

UDPServerSocket.close()
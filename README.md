# Projeto de Redes: Controle de Servo Motor por Sensor de Cor

Um sistema de controle em malha fechada que utiliza um sensor de cor RGB para posicionar um servo motor. A comunicação entre os componentes (sensor, controlador e atuador) é realizada via rede, utilizando o protocolo UDP em modo broadcast.

## Arquitetura do Sistema
O projeto é dividido em três partes principais que se comunicam em uma rede local:

1.  **Cliente Sensor**: Um Arduino com um sensor de cor TCS230 lê os valores RGB de uma superfície e os envia para o Controlador via UDP.
2.  **Controlador/Servidor**: Um script Python que recebe os dados do sensor, compara com um valor de cor pré-definido (setpoint) e calcula a ação de controle necessária. Em seguida, envia um comando de posição para o Atuador.
3.  **Servidor Atuador**: Um segundo Arduino conectado a um servo motor SG90. Ele recebe os comandos de posição do Controlador e movimenta o motor para o ângulo especificado.

As conexões entre os Arduinos e o computador se dão via porta serial, e a comunicação em rede utiliza pacotes IP em broadcast sobre Ethernet.

<div align ="center">
<img src="https://user-images.githubusercontent.com/97804927/155147966-a067b077-9e8d-4640-9aa6-0305228fbc45.JPG" width="400px" />
</div>

## Componentes Utilizados

### Hardware
| Componente | Imagem |
| :--- | :---: |
| Arduino Mega | <img src="https://user-images.githubusercontent.com/97804927/155144845-809fa950-8638-434a-8b82-aa4d068c321a.JPG" width="250px" /> |
| Sensor RGB TCS 230 | <img src="https://user-images.githubusercontent.com/97804927/155146315-5feb449e-571b-4784-afe5-b81d05c852e1.JPG" width="200px" /> |
| Micro Servo Motor SG90 | <img src="https://user-images.githubusercontent.com/97804927/155146924-6ede3100-5880-42a8-88b1-74bba54358aa.JPG" width="200px" /> |
| Jumpers | <img src="https://user-images.githubusercontent.com/97804927/155145996-f7ba2879-0ef5-4519-8f14-506224338981.JPG" width="200px" /> |

### Software e Scripts
- **`Sensor_Cliente.py`**: Script responsável por ler os dados da porta serial vinda do Arduino (sensor) e enviá-los via UDP para o controlador.
- **`Controlador_Servidor-Cliente.py`**: O cérebro do sistema. Recebe os dados do sensor, aplica a lógica de controle e envia os comandos para o atuador.
- **`Atuador_Servidor.py`**: Script que escuta os comandos do controlador e os repassa para o Arduino (atuador) via porta serial para mover o servo.

## Lógica de Controle

### Setpoints de Cor
Quatro cores foram escolhidas para a aplicação: Azul claro, Azul forte, Vinho e Vermelho. Para cada cor, foi realizado um mapeamento das frequências RGB detectadas pelo sensor, gerando os seguintes setpoints:
<div align ="center">
<img src="https://user-images.githubusercontent.com/97804927/155150429-041a3abc-27e6-498c-a7be-494fc5c3e843.JPG" width="600px" />
</div>

### Margem de Erro
Devido a variações na leitura do sensor, foi definida uma margem de erro para estabilizar o controle. O sistema considera que a cor correta foi encontrada se o vetor de erro `[R_erro, G_erro, B_erro]` for um dos seguintes:
`[0,0,0]`, `[1,0,0]`, `[0,1,0]`, `[0,0,1]`, `[1,2,1]`, `[2,1,1]`, `[1,1,2]`.

## Montagem Física
Para garantir a precisão das leituras do sensor de cor, foi construída uma estrutura para isolar o sistema da luz ambiente, garantindo medições consistentes.

<div align ="center">

| | |
| :---: | :---: |
| <img src="https://user-images.githubusercontent.com/97804927/155155644-6defe6fb-dcb7-4b42-9309-71079d6b6057.JPG" width="300px" /> | <img src="https://user-images.githubusercontent.com/97804927/155156447-a13d399e-aad0-4567-af39-6ca1af5eab9b.JPG" width="300px" /> |
| <img src="https://user-images.githubusercontent.com/97804927/155156877-bdeb75de-4718-46fe-b80a-cecfc88a0b35.JPG" width="300px" /> | |

</div>

## Como Executar

### 1. Pré-requisitos
- Python 3.x
- Biblioteca PySerial: `pip install pyserial`
- Dois Arduinos com os respectivos sketches carregados (sensor e atuador).

### 2. Configuração
1.  **Rede**: Certifique-se de que o computador executando os scripts Python esteja na mesma sub-rede configurada nos arquivos (ex: `192.168.100.x`).
2.  **Portas Seriais**: Verifique e, se necessário, altere as portas seriais (`COM3`, `COM4`) nos scripts `Sensor_Cliente.py` e `Atuador_Servidor.py` para corresponder às portas em que os Arduinos estão conectados.

### 3. Execução
Para iniciar o sistema, execute os scripts Python em terminais separados, na seguinte ordem:

1.  **Inicie o servidor do atuador:**
    ```bash
    python Atuador_Servidor.py
    ```
2.  **Inicie o cliente do sensor:**
    ```bash
    python Sensor_Cliente.py
    ```
3.  **Inicie o controlador principal:**
    ```bash
    python Controlador_Servidor-Cliente.py
    ```
    - Ao executar o controlador, você será solicitado a escolher a cor alvo no terminal.


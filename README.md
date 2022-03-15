# Projeto de Redes
Projeto que realiza o controle em malha fechada de um servo motor através de leituras de cores feitas por um sensor RGB TCS 230. Para realizar a comunicação, os dispositivos da planta foram conectados em um barramento lógico virtual utilizando protocolo de transporte UDP, pacotes IP em broadcast e Ethernet. O projeto compriu todos 
## Materiais Utilizados
  - Arduino Mega 
  <div align ="center">
  <img src="https://user-images.githubusercontent.com/97804927/155144845-809fa950-8638-434a-8b82-aa4d068c321a.JPG" width="250px" />
  </div>
   
   - Jumpers
  <div align ="center">
  <img src="https://user-images.githubusercontent.com/97804927/155145996-f7ba2879-0ef5-4519-8f14-506224338981.JPG" width="200px" />
  </div>

 - Sensor RGB TCS 230
  <div align ="center">
  <img src="https://user-images.githubusercontent.com/97804927/155146315-5feb449e-571b-4784-afe5-b81d05c852e1.JPG" width="200px" />
  </div>
  
  - Micro Servo Motor SG90
  <div align ="center">
  <img src="https://user-images.githubusercontent.com/97804927/155146924-6ede3100-5880-42a8-88b1-74bba54358aa.JPG" width="200px" />
  </div>

## Comunicação 
As conexões entre os Arduinos e o computador se dão via porta serial, utilizando cabos seriais USB. Os elementos estão conectados em um barramento lógico virtual utilizando o
protocolo de transporte UDP, pacotes IP em broadcast e Ethernet.
<div align ="center">
<img src="https://user-images.githubusercontent.com/97804927/155147966-a067b077-9e8d-4640-9aa6-0305228fbc45.JPG" width="400px" />
</div>

## Setpoint das cores
Quatro cores foram escolhidas para a aplicação: Azul claro, Azul forte, Vinho e Vermelho Fraco. Cada cor possui uma intensidade de Red, Green e Blue (RGB), utilizando o sensor foi possivel fazer um mapeamento das intesidades de cada cor, o que gerou os seguinte setpoint
<div align ="center">
<img src="https://user-images.githubusercontent.com/97804927/155150429-041a3abc-27e6-498c-a7be-494fc5c3e843.JPG" width="600px" />
</div>

  ### Margem de erro
  Apos a análise de vários ciclos, foi possível determinar uma margem de erro sem que interferisse muito no resultado do sensor. Esse erro foi estipulado devido a baixa qualidade de leitura do sensor. Os erros determinados foram: **[0,0,0], [1,0,0], [0,1,0], [0,0,1], [1,2,1], [2,1,1], [1,1,2]**

## Planta montada 
Para o sensor conseguir fazer uma medição com maior precisão, foi necessario impedir a entrada de luz no sistema.
<div align ="center">
<img src="https://user-images.githubusercontent.com/97804927/155155644-6defe6fb-dcb7-4b42-9309-71079d6b6057.JPG" width="300px" />
</div>

<div align ="center">
<img src="https://user-images.githubusercontent.com/97804927/155156447-a13d399e-aad0-4567-af39-6ca1af5eab9b.JPG" width="300px" />
</div>

<div align ="center">
<img src="https://user-images.githubusercontent.com/97804927/155156877-bdeb75de-4718-46fe-b80a-cecfc88a0b35.JPG" width="300px" />
</div>





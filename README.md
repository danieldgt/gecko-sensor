# Automação de Terrário para Gecko Leopardo

Este projeto tem como objetivo gerenciar automaticamente um terrário projetado especificamente para o Gecko Leopardo, garantindo condições ideais e estáveis de temperatura, umidade e ventilação. A automação é realizada através da leitura contínua e precisa dos parâmetros internos do terrário utilizando sensores digitais (DHT22), permitindo ajustes automáticos nos sistemas de aquecimento, umidificação e ventilação.

## Principais Características

1. Monitoramento em tempo real: Captura precisa da temperatura e umidade com sensores DHT22.
2. Controle Automático: Ajuste automático e contínuo dos níveis de temperatura, umidade e ventilação, mantendo o ambiente ideal.
3. Sistema de Segurança: Notificações e alertas em caso de parâmetros fora das faixas seguras.
4. Facilidade de Uso: Interface clara e comandos simples para monitoramento e configuração.

## Tecnologias Utilizadas

- Tinker Board S
- Python 3
- Biblioteca ASUS.GPIO
- Sensores DHT22 (Temperatura e Umidade)

Este projeto facilita a manutenção de um ambiente ideal para o Gecko Leopardo, contribuindo para seu conforto, saúde e bem-estar.

# Guia Rápido para Instalar o Ambiente do Sensor DHT22 na Tinker Board S

## 1. Atualização Inicial

```bash
sudo apt update
sudo apt upgrade -y
```

## 2. Dependências Essenciais

```bash
sudo apt install python3 python3-pip python3-dev -y
```

## 3. Biblioteca ASUS.GPIO

```bash
sudo pip3 install ASUS.GPIO
```

## 4. Configuração do Projeto

Clonne e acesse o diretório do projeto:

```bash
cd ~/gecko-sensors
```

O arquivo Python (`le_dht22.py`) é uma poc de leitura de temperatura e umidade usando o sensor: Módulo Sensor De Umidade E Temperatura Am2302 Dht22.


## 5. Executar o Script

```bash
sudo python3 le_dht22.py
```

Agora sua Tinker Board S estará pronta e funcionando novamente com seus sensores DHT22.

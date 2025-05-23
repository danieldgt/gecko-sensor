Projeto para gestão de sensores e atuadores do viveiro do Gecko

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

sudo python3 le_dht22.py

Agora sua Tinker Board S estará pronta e funcionando novamente com seus sensores DHT22.

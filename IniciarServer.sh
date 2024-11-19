#!/bin/bash

# Fecha todos os navegadores Chromium
echo "Fechando todos os processos do Chromium..."
pkill chromium-browser

# Verifica e fecha processos que estão utilizando a porta 5000
echo "Fechando processos usando a porta 5000..."
fuser -k 5000/tcp

# Aguarda 2 segundos para garantir que os processos foram fechados
sleep 2

# Inicia o subprocesso Python (garanta que o nome e o caminho do script estão corretos)
python3 SubProccess.py &

# Aguarda 2 segundos para garantir que o subprocesso foi iniciado
sleep 2

# Abre o Chromium com o endereço desejado, sem notificações e em modo quiosque (sem interface extra)
chromium-browser --disable-gpu --no-sandbox --no-zygote --start-maximized --kiosk "http://localhost:5000" &

# Aguarda 5 segundos para garantir que o Chromium tenha iniciado
sleep 5

# Não há necessidade de usar xdotool se o Chromium já foi aberto em modo quiosque (kiosk)
# Se você precisar fazer algo adicional, como encontrar a janela, use o xdotool conforme necessário.

# Exemplo de verificação de janela com xdotool, caso precise
window_id=$(xdotool search --onlyvisible --class "Chromium" | head -n 1)
if [ -z "$window_id" ]; then
    echo "Não foi possível encontrar a janela do Chromium."
    exit 1
fi

echo "Janela encontrada, ID: $window_id"

# Ativa a janela do Chromium, se necessário
xdotool windowactivate --sync $window_id

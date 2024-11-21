#!/bin/bash

> /tmp/iniciar_servico.log

echo "Iniciando o serviço em $(date)" >> /tmp/iniciar_servico.log

# Exporta a variável DISPLAY para o usuário correto
export DISPLAY=:0
export XAUTHORITY=/home/sgtrack/.Xauthority

# Permite acesso ao servidor X para o usuário atual
xhost +SI:localuser:$(whoami)

# Aguarda até o ambiente gráfico estar completamente carregado
while [ -z "$DISPLAY" ] || ! xhost &>/dev/null; do
    echo "Esperando ambiente gráfico carregar..." >> /tmp/iniciar_servico.log
    sleep 2
done
echo "Ambiente gráfico carregado." >> /tmp/iniciar_servico.log

# Move o mouse para fora da tela e verifica se o comando executa corretamente
echo "Movendo o mouse para fora da tela..." >> /tmp/iniciar_servico.log
if xdotool mousemove -- -1000 -1000; then
    echo "Mouse movido com sucesso." >> /tmp/iniciar_servico.log
else
    echo "Falha ao mover o mouse." >> /tmp/iniciar_servico.log
fi

# Aguarda até a internet estar disponível
while ! ping -c 1 8.8.8.8 &>/dev/null; do
    echo "Esperando conexão com a internet..." >> /tmp/iniciar_servico.log
    sleep 2
done
echo "Conexão com a internet estabelecida." >> /tmp/iniciar_servico.log

# Fecha todos os navegadores Chromium
echo "Fechando todos os processos do Chromium..." >> /tmp/iniciar_servico.log
pkill -f chromium-browser

echo "Ambiente gráfico e internet prontos. Iniciando serviço..." >> /tmp/iniciar_servico.log

# Seu comando ou aplicação aqui
python3 /home/sgtrack/Documents/Monitorpy/index.py >> /tmp/iniciar_servico.log 2>&1 &
chromium-browser --disable-gpu --no-sandbox --no-zygote --start-maximized --kiosk --lang=pt-BR "http://localhost:5000" >> /tmp/iniciar_servico.log 2>&1 &

# Aguarda 5 segundos para garantir que o Chromium tenha iniciado
sleep 4

unclutter -idle 0 -root

# Mantém o script rodando para evitar reinício do serviço
while :; do
    sleep 3600
done

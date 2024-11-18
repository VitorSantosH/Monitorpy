import os
import serial
import datetime
import subprocess
from flask import Flask, render_template, jsonify

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Função para listar os dispositivos seriais disponíveis
def listar_dispositivos_seriais():
    serial_dir = "/dev/serial/by-id/"
    return [os.path.join(serial_dir, device_path) for device_path in os.listdir(serial_dir)] if os.path.exists(serial_dir) else []

# Função para interpretar a string de dados do rastreamento
def interpretar_string(dados):
    partes = dados.split(';')
    return {
        "SerialRastreador": partes[0].split('#')[1],
        "DataHoraRastreador": datetime.datetime.strptime(partes[1], "%d-%m-%Y %H:%M:%S"),
        "Latitude": float(partes[3]),
        "Longitude": float(partes[4]),
        "Velocidade": int(partes[6]),
        "IgnicaoLigada": partes[10] == "1",
        "BloqueioAtivo": partes[11] == "1",
        "NumeroIButton": partes[12],
        "APM": int(partes[13]),
        "Horimetros": [int(partes[i]) for i in range(14, 20)],
        "HorimetroSensorPulsos1": int(partes[20]),
        "HorimetroSensorPulsos2": int(partes[21]),
        "CercaEletronica": int(partes[22]),
        "Temperaturas": [float(partes[i]) for i in range(23, 33)],
        "AlertaVelocidade": int(partes[33]),
        "TempoAlertaVelocidade": int(partes[34]),
        "ContagemMotorOcioso": int(partes[35]),
        "TempoMotorOcioso": int(partes[36]),
        "VelocidadeMaximaDentroCerca": partes[37] == "1",
        "VelocidadeMaximaDentroMicroCerca": partes[38] == "1",
        "ConexaoGPASAtivada": partes[39] == "1",
        "ServidorRemotoRespondendo": partes[40] == "1",
        "BetoneiraStatus": int(partes[41]),
        "JammerDetectado": partes[42] == "1",
        "BateriaExternaRemovida": partes[43] == "1",
        "SensoresStatus": [int(partes[i]) for i in range(44, 50)],
        "VelocidadeMaxCerca": int(partes[50]),
        "VelocidadeMaxMicroCerca": int(partes[51]),
        "dadosBrutos": dados
    }

# Função para obter os dados do rastreador
def obter_dados_rastreamento():
    dispositivos = listar_dispositivos_seriais()
    if not dispositivos:
        return "Nenhum dispositivo serial encontrado."

    try:
        port_path = dispositivos[0]
        with serial.Serial(port_path, 19290, timeout=1) as ser:
            ser.write("#STATUS\n".encode())
            response = ser.readline().decode('utf-8', errors='ignore').strip()
            return interpretar_string(response) if response else "Sem dados recebidos."
    except Exception as e:
        return f"Erro ao acessar o dispositivo serial: {e}"
    
# Função para iniciar o Chromium em modo tela cheia
def abrir_chromium():
    # Comando para abrir o Chromium em modo fullscreen (F11) com a flag --no-sandbox
    try:
        subprocess.Popen(['chromium-browser', '--start-fullscreen', '--no-sandbox', 'http://localhost:5000'])
    except FileNotFoundError:
        print("Erro: O Chromium não foi encontrado. Certifique-se de que ele está instalado.")

# Rota principal para exibir a página index
@app.route('/')
def index():
    return render_template('index.html')

# Rota para retornar os dados do rastreador como JSON
@app.route('/dados_rastreamento')
def dados_rastreamento():
    return jsonify(obter_dados_rastreamento())

# Iniciar a aplicação Flask
if __name__ == '__main__':
    abrir_chromium()  # Abre o Chromium em modo F11
    app.run(host='0.0.0.0', port=5000, debug=False)

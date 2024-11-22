import os
import serial
import datetime
import requests
import subprocess
import binascii
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
        "NumeroIButton": hex_to_integer(partes[12]),
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
        "dadosBrutos": dados,
        "chuva":  int(partes[35]),
        "chuva2" :  int(partes[34]),
        "chuva3":  int(partes[36])
    }

# Função para obter os dados do rastreador
def obter_dados_rastreamento():
    dispositivos = listar_dispositivos_seriais()
    if not dispositivos:
        return {"error": "Nenhum dispositivo serial encontrado."}

    try:
        port_path = dispositivos[0]
        with serial.Serial(port_path, 115200, timeout=1) as ser:
            ser.write("#STATUS\n".encode())
            response = ser.readline().decode('utf-8', errors='ignore').strip()
            return {"data": interpretar_string(response)} if response else {"error": "Sem dados recebidos."}
    except Exception as e:
        return {"error": f"Erro ao acessar o dispositivo serial: {e}"}
    
def abrir_chromium():
    # Verificar se o servidor Flask está respondendo antes de abrir o navegador
    try:
        response = requests.get('http://localhost:5000')
        if response.status_code == 200:
            print("Servidor Flask está rodando, abrindo o navegador...")

            try:
                # Tente abrir o Chromium
                process = subprocess.Popen(
                    ['chromium-browser', '--start-fullscreen', '--no-sandbox', 'http://localhost:5000'],
                    stdout=subprocess.PIPE,  # Redireciona a saída padrão
                    stderr=subprocess.PIPE   # Redireciona os erros
                )

                # Captura a saída de erro
                stdout, stderr = process.communicate()
                if stderr:
                    print("Erros encontrados:", stderr.decode())
                else:
                    print("Navegador aberto com sucesso.")

            except Exception as e:
                print(f"Erro ao abrir o navegador: {e}")

        else:
            print(f"Servidor Flask não está respondendo. Status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar ao servidor Flask: {e}")


def hex_to_integer(hex_string):
    # Remove os zeros à esquerda
    trimmed_hex = hex_string.lstrip('0')
    print(f"Hex sem zeros à esquerda: {trimmed_hex}")
    
    # Converter a string hexadecimal para um array de bytes
    byte_array = bytes.fromhex(trimmed_hex)
    
    # Reverter a ordem dos bytes
    reversed_byte_array = bytes(reversed(byte_array))
    print(f"Array de bytes invertido: {reversed_byte_array}")
    
    # Converter o array de bytes invertido para um número inteiro
    integer_value = int.from_bytes(reversed_byte_array, byteorder='big')
    print(f"Valor inteiro: {integer_value}")
    
    return integer_value

# Rota principal para exibir a página index
@app.route('/')
def index():
    return render_template('index.html')

# Rota para retornar os dados do rastreador como JSON
@app.route('/dados_rastreamento')
def dados_rastreamento():
    resposta = obter_dados_rastreamento()
    if "error" in resposta:
        return jsonify(resposta), 400
    return jsonify(resposta)

# Iniciar a aplicação Flask
if __name__ == '__main__':
    #abrir_chromium()  # Abre o Chromium em modo F11
    app.run(host='0.0.0.0', port=5000, debug=True)

#include <iostream>
#include <windows.h>
#include <string>

// Função para configurar a porta serial
HANDLE configurarPortaSerial(const std::string& dispositivo) {
    // Abrir a porta COM4 (ajuste conforme necessário)
    HANDLE hSerial = CreateFile(
        dispositivo.c_str(),                // Nome do dispositivo
        GENERIC_READ | GENERIC_WRITE,        // Permissões
        0,                                   // Sem compartilhamento
        NULL,                                // Sem atributos de segurança
        OPEN_EXISTING,                       // Abrir se existir
        0,                                   // Sem atributos
        NULL                                 // Sem modelo de template
    );

    if (hSerial == INVALID_HANDLE_VALUE) {
        std::cerr << "Erro ao abrir a porta serial." << std::endl;
        return INVALID_HANDLE_VALUE;
    }

    // Configurar as propriedades da porta serial
    DCB dcbSerialParams = {0};
    if (!GetCommState(hSerial, &dcbSerialParams)) {
        std::cerr << "Erro ao obter os parâmetros da porta serial." << std::endl;
        CloseHandle(hSerial);
        return INVALID_HANDLE_VALUE;
    }

    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);
    dcbSerialParams.BaudRate = CBR_115200;  // Taxa de baud 19200
    dcbSerialParams.ByteSize = 8;           // 8 bits por caractere
    dcbSerialParams.StopBits = ONESTOPBIT;  // 1 bit de parada
    dcbSerialParams.Parity = NOPARITY;      // Sem paridade

    if (!SetCommState(hSerial, &dcbSerialParams)) {
        std::cerr << "Erro ao configurar a porta serial." << std::endl;
        CloseHandle(hSerial);
        return INVALID_HANDLE_VALUE;
    }

    // Configurar o tempo de leitura
    COMMTIMEOUTS timeouts = {0};
    timeouts.ReadIntervalTimeout = 50;
    timeouts.ReadTotalTimeoutConstant = 50;
    timeouts.ReadTotalTimeoutMultiplier = 10;
    timeouts.WriteTotalTimeoutConstant = 50;
    timeouts.WriteTotalTimeoutMultiplier = 10;

    if (!SetCommTimeouts(hSerial, &timeouts)) {
        std::cerr << "Erro ao configurar os timeouts da porta serial." << std::endl;
        CloseHandle(hSerial);
        return INVALID_HANDLE_VALUE;
    }

    return hSerial;
}

// Função para escrever um comando na porta serial
void enviarComando(HANDLE hSerial, const std::string& comando) {
    DWORD bytesEscritos;
    BOOL resultado = WriteFile(hSerial, comando.c_str(), comando.length(), &bytesEscritos, NULL);
    if (!resultado) {
        std::cerr << "Erro ao enviar comando." << std::endl;
    }
}

// Função para ler dados da porta serial
std::string lerDadosSerial(HANDLE hSerial) {
    char buffer[256];
    DWORD bytesLidos;
    BOOL resultado = ReadFile(hSerial, buffer, sizeof(buffer) - 1, &bytesLidos, NULL);
    if (!resultado || bytesLidos == 0) {
        std::cerr << "Erro ao ler da porta serial." << std::endl;
        return "";
    }
    buffer[bytesLidos] = '\0';  // Adiciona o terminador de string
    return std::string(buffer);
}

int main() {
    std::string dispositivo = "COM4";  // Porta COM4 no Windows

    // Abrir a porta serial
    HANDLE hSerial = configurarPortaSerial(dispositivo);
    if (hSerial == INVALID_HANDLE_VALUE) return 1;

    int count = 10;
    for (size_t i = 0; i < count; i++)
    {
        // Enviar o comando "#STATUS\n"
        std::string comando = "#STATUS\n";  // Comando que você mencionou
        enviarComando(hSerial, comando);
        
        // Aguardar e ler a resposta do rastreador
        std::string resposta = lerDadosSerial(hSerial);
        std::cout << "Resposta do rastreador: " << resposta << std::endl;
    }

    // Fechar a porta serial após o uso
    CloseHandle(hSerial);

    return 0;
}

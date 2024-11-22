#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <vector>
#include <cstdlib>
#include <cstdio>
#include <cstring>

// Função para configurar a porta serial
int configurarPortaSerial(const std::string& dispositivo) {
    int fd = open(dispositivo.c_str(), O_RDWR | O_NOCTTY | O_NDELAY);
    if (fd == -1) {
        std::cerr << "Erro ao abrir a porta serial." << std::endl;
        return -1;
    }

    struct termios options;
    tcgetattr(fd, &options);
    cfsetispeed(&options, B19200); // Configurando a taxa de baud para 19200
    cfsetospeed(&options, B19200);

    options.c_cflag |= (CLOCAL | CREAD); // Ativar a leitura e ignorar o controle de linha
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8; // 8 bits por caractere
    options.c_cflag &= ~PARENB; // Sem paridade
    options.c_cflag &= ~CSTOPB; // 1 bit de parada
    options.c_cflag &= ~CRTSCTS; // Desabilitar controle de fluxo

    tcsetattr(fd, TCSANOW, &options); // Aplicar as configurações

    return fd;
}

// Função para escrever um comando na porta serial
void enviarComando(int fd, const std::string& comando) {
    int n = write(fd, comando.c_str(), comando.length());
    if (n < 0) {
        std::cerr << "Erro ao enviar comando." << std::endl;
    }
}

// Função para ler dados da porta serial
std::string lerDadosSerial(int fd) {
    char buffer[256];
    int n = read(fd, buffer, sizeof(buffer) - 1);
    if (n < 0) {
        std::cerr << "Erro ao ler da porta serial." << std::endl;
        return "";
    }
    buffer[n] = '\0'; // Adiciona o terminador de string
    return std::string(buffer);
}

int main() {
    std::string dispositivo = "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_CPA6b126810-if00-port0";
    
    // Abrir a porta serial
    int fd = configurarPortaSerial(dispositivo);
    if (fd == -1) return 1;

    // Enviar o comando "#STATUS\n"
    std::string comando = "#STATUS\n";  // Comando que você mencionou
    enviarComando(fd, comando);
    
    // Aguardar e ler a resposta do rastreador
    std::string resposta = lerDadosSerial(fd);
    std::cout << "Resposta do rastreador: " << resposta << std::endl;

    // Fechar a porta serial após o uso
    close(fd);

    return 0;
}

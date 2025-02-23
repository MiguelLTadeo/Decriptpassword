import socket
import pickle

host = '192.168.15.7'
port = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg_envio = input("Digite a mensagem:")
word_size = input("Digite o tamanho:")
serial_data = pickle.dumps((msg_envio, word_size))
client_socket.sendto(serial_data,(host,port))
dados_recebidos, endereco_servidor = client_socket.recvfrom(4096)

tentativa_senha, tempo_total = pickle.loads(dados_recebidos)

print(f"Senha recebida: {tentativa_senha}")
print(f"Tempo de execução recebido: {tempo_total} segundos")
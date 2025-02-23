import hashlib
import threading
import itertools
import socket
import time
import pickle


host ='192.168.15.7'
port = 8000
alphabet = "abcdefghijklmnopqrstuvwxyz"
inverted_alphabet = alphabet[::-1]
lock = threading.Lock()
found = False

def crack_password(tipo, crack, alphabet, repeat, start, end, server_socket, address_ip_client):
    inicio = time.time()
    global found
    print(f"Thread {tipo} iniciada para o intervalo {start} a {end}")
    combinations = itertools.product(alphabet, repeat=repeat)
    sliced_combinations = itertools.islice(combinations, start, end)

    for combination in sliced_combinations:
        if found:
            break

        tentativa_senha = ''.join(combination)
        print(f"{tipo}: {tentativa_senha}")

        hash_md5 = hashlib.md5(tentativa_senha.encode('utf-8')).hexdigest()

        if hash_md5 == crack:
            with lock:
                if not found:
                    found = True
                    print(f"Senha encontrada: {tentativa_senha}")
                    fim = time.time()
                    tempo_total = fim - inicio
                    print(f"Tempo de execução: {tempo_total:.4f} segundos")
                    dados_serializados = pickle.dumps((tentativa_senha, tempo_total))
                    server_socket.sendto(dados_serializados, address_ip_client)
            break

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host,port))
dados_recebidos, endereco_client = server_socket.recvfrom(4096)
msg_envio, word_size = pickle.loads(dados_recebidos)

print(word_size)
print(msg_envio)


repeat = int(word_size)

probability = 26 ** repeat

start_1, end_1 = 0, int(probability / 4)
start_2, end_2 = int(probability / 4), int(probability / 3)
start_3, end_3 = int(probability / 3), int(probability /2)
start_4, end_4 = int(probability /2), int(probability)

parts =[(start_1, end_1),(start_2, end_2),(start_3, end_3),(start_4, end_4)]

threads= []

for start, end in parts:
    thread_normal = threading.Thread(target=crack_password, args=("normal",msg_envio, alphabet, repeat, start, end, server_socket, endereco_client))
    threads.append(thread_normal)
    thread_reverse = threading.Thread(target=crack_password, args=("invertido",msg_envio,inverted_alphabet,repeat,start, end, server_socket, endereco_client))
    threads.append(thread_reverse)

for thread in threads:
    thread.start()


for thread in threads:
    thread.join()





    



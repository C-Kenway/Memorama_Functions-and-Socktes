import socket
import random
import time

HOST = "localhost"
PORT = 12345
buffer_size = 1024

def start_game(client_socket, difficulty):
    if difficulty == "1":
        words = ['gato', 'perro', 'oso', 'conejo']
        board_size = 8
        client_socket.send("Modo: Principiante".encode())
    elif difficulty == "2":
        words = ['gato', 'perro', 'oso', 'conejo','pez','lobo','jirafa','canario','iguana']
        board_size = 18
        client_socket.send('Modo: Avanzado'.encode())
    else:
        client_socket.send('Opción inválida'.encode())
        return None

    board = random.sample(words * 2, board_size)
    random.shuffle(board)
    flipped = ['X'] * board_size
    print(board)
    return board, flipped, board_size

def play_game(client_socket, board, flipped, board_size):
    attempts = 0
    last_choice = None
    while True:
        print("Escucho peticion del cliente")
        choice = int(client_socket.recv(buffer_size).decode().strip())
        if choice < 0 or choice >= board_size:
            client_socket.send(str('Intente de nuevo.').encode())
            client_socket.send(str('Opción inválida').encode())
            attempts = 0
        elif flipped[choice] != 'X':
            client_socket.send(str("Anterior:" + carta_previa).encode())
            client_socket.send(str('Carta ya seleccionada').encode())
            attempts = 0
        else:
            attempts += 1
            flipped[choice] = board[choice]
            carta = board[choice]
            if attempts == 2:
                client_socket.send(str(carta).encode())
                if board[choice] == board[last_choice]:
                    client_socket.send(str('\n¡Felicidades! Ha formado una pareja').encode())
                    flipped[last_choice] = board[last_choice]
                    flipped[choice] = board[choice]
                    attempts = 0
                    if "X" not in flipped:
                        client_socket.sendall(str('\n¡Felicidades! Ha ganado el juego\n').encode())
                        break
                else:
                    client_socket.sendall(str('No fue pareja. Sigue jugando\n').encode())
                    flipped[last_choice] = 'X'
                    flipped[choice] = 'X'
                    attempts = 0
            elif attempts == 1:
                print(carta)
                client_socket.sendall(str(carta).encode())
                client_socket.sendall(str('Siguiente tiro').encode())
                last_choice = choice
                carta_previa = carta



def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"El servidor está escuchando en {HOST}:{PORT}")
    client_socket, client_address = server_socket.accept()
    print(f"Se ha establecido una conexión desde {client_address[0]}:{client_address[1]}")
    client_socket.send(str("Dificultad: 1)Principiante 2)Avanzado \n Ingrese numero:").encode())
    difficulty = client_socket.recv(buffer_size).decode().strip()
    game = start_game(client_socket, difficulty)
    print("Antes de la funcion game")
    if game is not None:
        board, flipped, board_size = game
        print("listo para jugar")
        play_game(client_socket, board, flipped, board_size)
    else:
        print(game)
        print("Algo malo paso")
    # Cerrar la conexión con el cliente
    client_socket.close()

if __name__ == "__main__":
    run_server()

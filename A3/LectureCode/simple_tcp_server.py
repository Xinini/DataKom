from socket import *
from threading import Thread

def handle_client(connection_socket):
    request = "aslkdj"
    print("Request: " + request)
    while request != "game over\n":
        request = connection_socket.recv(100).decode()
        if request == "game over\n":
            break
        try:
            request = request.replace("\n", "")
            request_lst = request.split("+")
            print(request_lst)
            response_int = int(request_lst[0]) + int(request_lst[1])
            response_str = str(response_int)
            connection_socket.send(response_str.encode())
        except:
            response = "error"
            connection_socket.send(response.encode())
    print("Client connection closed")
    connection_socket.close()

def start_server():
    welcome_socket = socket(AF_INET, SOCK_STREAM)
    welcome_socket.bind(("", 5678))
    welcome_socket.listen(1) #1 represents queue size
    print("Listening on port 5678")
    server_on = True
    while server_on:
        connection_socket, client_address = welcome_socket.accept()
        print("Client Connected: ", client_address)
        client_thread = Thread(target=handle_client, args=(connection_socket, ))
        client_thread.start()
    welcome_socket.close()
if __name__ == '__main__':
    start_server()
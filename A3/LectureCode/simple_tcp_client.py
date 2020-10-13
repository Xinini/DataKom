from socket import *
import random
import time

HOST = "localhost"
PORT = 5678

client_socket = None

def connect_to_server(host, port):
    global client_socket

    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        return True
    except:
        return False

def close_connection():
    global client_socket
    try:
        client_socket.close()
        return True
    except:
        return False

def send_request_to_server(message):
    message += "\n"

    global client_socket

    try:
        client_socket.send(message.encode())
        return True
    except:
        return False

def read_response_from_server():
    global client_socket
    try:
        response = client_socket.recv(1000)
        response_str = response.decode()
        return response_str.replace('\n', ' ')
    except:
        return None

def run_client_test():
    print("TCP client Started")
    if not connect_to_server(HOST, PORT):
        return "Error: Failed to connect to Server"
    else:
        print("Connection Established")
    
    a = random.randint(1, 20)
    b = random.randint(1, 20)

    request = "{}+{}".format(a, b)

    if not send_request_to_server(request):
        return "Error: Failed to Send Request"
    print("Sent request: " + request)

    response = read_response_from_server()
    if response is None:
        return "Error: Failed to Receive Response"
    print("Server Responeded with: " + response)
    
    seconds_to_sleep = 2 + random.randint(0, 5)
    print("Sleeping {} seconds to allow simulate long client server connection".format(seconds_to_sleep))
    time.sleep(seconds_to_sleep)


    request = "ra+ra"
    if not send_request_to_server(request):
        return "Error: Failed to send Request"
    print("Sent request: " + request)

    response = read_response_from_server()
    if response is None:
        return "Error: Failed to Receive Response"
    print("Server Responeded with: " + response)

    if not(send_request_to_server("game over") and close_connection()):
        return "Error: Could not finish the conversation with server"
    
    print("Game over, connection closed")

    if send_request_to_server("2+2"):
        return "ERROR: sending message should have failed"
    
    print("Fully closed connection")
    return "Simple TCP client finished"

if __name__ == '__main__':
    print(run_client_test())
    try:
        close_connection()
    except:
        pass

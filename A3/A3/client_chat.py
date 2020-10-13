from socket import *


# --------------------
# Constants
# --------------------
# The states that the application can be in
states = [
    "disconnected",  # Connection to a chat server is not established
    "connected",  # Connected to a chat server, but not authorized (not logged in)
    "authorized"  # Connected and authorized (logged in)
]
TCP_PORT = 1300  # TCP port used for communication
SERVER_HOST = "datakomm.work"  # Set this to either hostname (domain) or IP address of the chat server
ADDRESS = (SERVER_HOST, TCP_PORT)
# --------------------
# State variables
# --------------------
current_state = "disconnected"  # The current state of the system
# When this variable will be set to false, the application will stop
must_run = True
# Use this variable to create socket connection to the chat server
# Note: the "type: socket" is a hint to PyCharm about the type of values we will assign to the variable
client_socket = None  # type: socket


def quit_application():
    """ Update the application state so that the main-loop will exit """
    # Make sure we reference the global variable here. Not the best code style,
    # but the easiest to work with without involving object-oriented code
    global must_run
    must_run = False


def send_command(command, arguments = None):
    """
    Send one command to the chat server.
    :param command: The command to send (login, sync, msg, ...(
    :param arguments: The arguments for the command as a string, or None if no arguments are needed
        (username, message text, etc)
    :return:
    """
    global client_socket

    if arguments != None:
        client_socket.send("{} {}\n".format(command, arguments).encode())
    else:
        client_socket.send("{}\n".format(command).encode())
    # TODO: Implement this (part of step 3)
    # Hint: concatenate the command and the arguments
    # Hint: remember to send the newline at the end
    return


def read_one_line(sock):
    """
    Read one line of text from a socket
    :param sock: The socket to read from.
    :return:
    """
    newline_received = False
    message = ""
    while not newline_received:
        character = sock.recv(1).decode()
        if character == '\n':
            newline_received = True
        elif character == '\r':
            pass
        else:
            message += character
    return message


def get_servers_response():
    """
    Wait until a response command is received from the server
    :return: The response of the server, the whole line as a single string
    """
    # TODO Step 4: implement this function
    # Hint: reuse read_one_line (copied from the tutorial-code)
    try:
        response = read_one_line(client_socket)
        return response
    except:
        print("Error: Failed to recieve response from server")
    return None


def connect_to_server():
    # Must have these two lines, otherwise the function will not "see" the global variables that we will change here
    global client_socket
    global current_state

    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(ADDRESS)
        current_state = states[1] #Connected
        print("Sucsessfully connected to server: ", ADDRESS)
        send_command("sync")
        if get_servers_response() == "modeok":
            print("Switched to Sync Mode")
        else:
            print("Failed to swith to Sync Mode")
    except:
        print("Error: Failed to establish connecention")
    return
    


def disconnect_from_server():
    # TODO Step 2: Implement disconnect
    # Hint: close the socket, handle exceptions, update current_state accordingly

    # Must have these two lines, otherwise the function will not "see" the global variables that we will change here
    global client_socket
    global current_state
    try:
        client_socket.close()
        print("Closed connection")
        current_state = states[0]
        return True
    except IOError as error:
        print("Failed to close connection", error)
        return False
    
def login():
    global current_state

    username = input("Enter a username: ")
    send_command("login", username)

    response = get_servers_response()
    if response == "loginok":
        print("Login succsessful")
        current_state = states[2]
    elif response == "loginerr username already in use":
        print("Failed Login: Username already in use \n" + response)
    elif response == "loginerr incorrect username":
        print("Failed Login: Please only use alphanumeric characters: letters or digits \n" + response)
    return

def send_public_message():
    message = input("Enter a message: ")
    send_command("msg", message)

    response = get_servers_response().split(" ")
    if response[0] == "msgok":
        print("Message sent to {} users".format(response[1]))
    elif response[0] == "msgerror":
        print("Error: Failed to send message", response[1])
    return

def send_private_message():
    reciver = input("Enter a user for the message: ")
    message = input("Enter a message: ")
    arg = reciver + " " + message
    send_command("privmsg", arg)

    response = get_servers_response().split(" ")
    if response[0] == "msgok":
        print("Message sent to {} user(s)".format(response[1]))
    elif response[0] == "msgerr":
        print("Error: Failed to send message")
    return

def users():
    send_command("users")
    response = get_servers_response()
    user_list = response.split(" ")
    del user_list[0]
    user_list = sorted(user_list)
    print("Users: ")
    for i in user_list:
        print(i)
    return

def inbox():
    global client_socket
    send_command("inbox")
    response = get_servers_response()
    inbox_header = response.split(" ")
    number_of_messages = int(inbox_header[1])
    if number_of_messages > 0:
        print (str(number_of_messages) + " messages received")
        for i in range(number_of_messages):
            rcv_message = get_servers_response().split(" ")
            if rcv_message[0] == "msg":
                print("Global message from {}: {}".format(*rcv_message[1:]))
            elif rcv_message[0] == "privmsg":
                print("Privat message from {}: {}".format(*rcv_message[1:]))
    else:
        print("Inbox is empty :<")
    return







# TODO Step 6 - implement sending a public message
        # Hint: ask the user to input the message from the keyboard
        # Hint: you can reuse the send_command() function to send the "msg" command
        # Hint: remember to read the server's response: whether the message was successfully sent or not


"""
The list of available actions that the user can perform
Each action is a dictionary with the following fields:
description: a textual description of the action
valid_states: a list specifying in which states this action is available
function: a function to call when the user chooses this particular action. The functions must be defined before
            the definition of this variable
"""

available_actions = [
    {
        "description": "Connect to a chat server",
        "valid_states": ["disconnected"],
        "function": connect_to_server
    },
    {
        "description": "Disconnect from the server",
        "valid_states": ["connected", "authorized"],
        "function": disconnect_from_server
    },
    {
        "description": "Authorize (log in)",
        "valid_states": ["connected", "authorized"],
        "function": login
    },
    {
        "description": "Send a public message",
        "valid_states": ["connected", "authorized"],
        "function": send_public_message
    },
    {
        "description": "Send a private message",
        "valid_states": ["authorized"],
        "function": send_private_message
    },
    {
        "description": "Read messages in the inbox",
        "valid_states": ["connected", "authorized"],
        # TODO Step 9 - implement reading messages from the inbox.
        # Hint: send the inbox command, find out how many messages there are. Then parse messages
        # one by one: find if it is a private or public message, who is the sender. Print this
        # information in a user friendly way
        "function": inbox
    },
    {
        "description": "See list of users",
        "valid_states": ["connected", "authorized"],
        # TODO Step 7 - Implement getting the list of currently connected users
        # Hint: use the provided chat client tools and analyze traffic with Wireshark to find out how
        # the user list is reported. Then implement a function which gets the user list from the server
        # and prints the list of usernames
        "function": users
    },
    {
        "description": "Get a joke",
        "valid_states": ["connected", "authorized"],
        # TODO - optional step - implement the joke fetching from the server.
        # Hint: this part is not described in the protocol. But the command is simple. Try to find
        # out how it works ;)
        "function": None
    },
    {
        "description": "Quit the application",
        "valid_states": ["disconnected", "connected", "authorized"],
        "function": quit_application
    },
]


def run_chat_client():
    """ Run the chat client application loop. When this function exists, the application will stop """

    while must_run:
        print_menu()
        action = select_user_action()
        perform_user_action(action)
    print("Thanks for watching. Like and subscribe! 👍")


def print_menu():
    """ Print the menu showing the available options """
    print("==============================================")
    print("What do you want to do now? ")
    print("==============================================")
    print("Available options:")
    i = 1
    for a in available_actions:
        if current_state in a["valid_states"]:
            # Only hint about the action if the current state allows it
            print("  %i) %s" % (i, a["description"]))
        i += 1
    print()


def select_user_action():
    """
    Ask the user to choose and action by entering the index of the action
    :return: The action as an index in available_actions array or None if the input was invalid
    """
    number_of_actions = len(available_actions)
    hint = "Enter the number of your choice (1..%i):" % number_of_actions
    choice = input(hint)
    # Try to convert the input to an integer
    try:
        choice_int = int(choice)
    except ValueError:
        choice_int = -1

    if 1 <= choice_int <= number_of_actions:
        action = choice_int - 1
    else:
        action = None

    return action


def perform_user_action(action_index):
    """
    Perform the desired user action
    :param action_index: The index in available_actions array - the action to take
    :return: Desired state change as a string, None if no state change is needed
    """
    if action_index is not None:
        print()
        action = available_actions[action_index]
        if current_state in action["valid_states"]:
            function_to_run = available_actions[action_index]["function"]
            if function_to_run is not None:
                function_to_run()
            else:
                print("Internal error: NOT IMPLEMENTED (no function assigned for the action)!")
        else:
            print("This function is not allowed in the current system state (%s)" % current_state)
    else:
        print("Invalid input, please choose a valid action")
    print()
    return None

# Entrypoint for the application. In PyCharm you should see a green arrow on the left side.
# By clicking it you run the application.
if __name__ == '__main__':
    run_chat_client()

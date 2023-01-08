import socket
import configparser
import json
from knapsack import *
from solitaire import solitaire, solitaireOffset

PORT = 8002

def generateSecret():
    deck = list(range(28,55))
    random.shuffle(deck)
    return deck

def clientComm(server):
    #connect to another other client
    s = socket.socket()				
    s.connect(('localhost', PORT - 1))
    print('Connected to the communication on port ' + str(PORT - 1) + ' ...')

    print('Sending request to get the public key of client 1 ...')
    server.sendall(json.dumps({
        'request': 'getKey',
        'clientId': PORT - 1,
    }).encode())

    data = server.recv(1024).decode()
    data = json.loads(data)
    print('Got the public key of client 1!')

    server.close()

    public_key1 = data['pubKey']

    key2 = generateSecret()
    key2_encrypted = encryptKnapsack(str(key2), public_key1)

    #receiving
    data = s.recv(1024).decode()
    data = json.loads(data)
    key1 = decryptKnapsack(data['secret'], private_key)
    key1 = json.loads(key1)

    #send the secret
    s.sendall(json.dumps({
        'secret': key2_encrypted,
    }).encode())

    print(key1)
    print(key2)
    key = key1 + key2	

    print(key)	
    offset = 0

    print('You will recieve a message , be patient!')
    print('by typing QUIT you can exit the conversation .')

    while True:
        #getting a message
        response = s.recv(1024).decode()
        response = json.loads(response)

        print('Received message: ', response)

        msg = response['msg']
        print('The encrypted message : ' + msg)
        if msg == 'QUIT':
            print('The other client left....')
            s.close()
            break

        response_offset = response['offset']
        if offset > response_offset:
            print('Your offset is not working as it can, wait for fixing.')
            offset = response_offset
            
            #read initial key from config file again
            parser = configparser.ConfigParser()
            parser.read('config.txt')
            key = parser.get('config','key')
            key = json.loads(key)
            solitaireOffset(key, offset)
        
        elif offset < response_offset:
            print('Your offset is not working as it can, wait for fixing.')
            solitaireOffset(key, response_offset - offset)
            offset = response_offset

        msg = solitaire(msg, key)
        print('Your decrypted message: ' + msg)

        offset += len(msg)	
        print('If you want send a response message.')

        msg = input()
        if msg == 'QUIT':
            print('Thanks for using this chat, we wait you back!')
            s.sendall(json.dumps({
                'offset': offset,
                'msg': 'QUIT'
            }).encode())
            s.close()
            break
        
        print('Your typed message: ' + msg)
        msg = solitaire(msg, key)
        print('Your encrypted message: ' + msg)

        s.sendall(json.dumps({
            'offset': offset,
            'msg': msg
        }).encode())
        print('Message sent! Waiting for response...')

        offset += len(msg)	

def registerKey(public_key, server):
    print('Registering ...')
    server.sendall(json.dumps({
        'request': 'registration',
        'id': PORT,
        'pubKey': public_key
    }).encode())
    msg = server.recv(1024).decode()
    print(msg)

if __name__ == '__main__':
    private_key, public_key = GenerateKeypair()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	

    server.connect(('localhost', 8000))
    print('Connected to the server on port 8000...')
    msg = server.recv(1024).decode()
    print('Got this message: ' + msg)

    registerKey(public_key, server)
    clientComm(server)
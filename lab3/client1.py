import socket
import configparser
import json
from solitaire import solitaire, solitaireOffset
from knapsack import *

PORT = 8001

def generateSecret():
    deck = list(range(1,28))
    random.shuffle(deck)
    return deck

def clientComm(server):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('localhost', PORT))
    s.listen(1)	
    print('Starting communication on port: ' + str(PORT))

    client, addr = s.accept()			
    print('The other client with address', addr, 'is now connected to you!')

    print('Sending request to get key of the other client')
    server.sendall(json.dumps({
        'request': 'getKey',
        'clientId': PORT + 1,
    }).encode())

    data = server.recv(1024).decode()
    data = json.loads(data)
    print('Got the key of the other client.')

    server.close()

    #get public key of client 2
    public_key2 = data['pubKey']

    #generate a random secret
    key1 = generateSecret()
    key1_encrypted = encryptKnapsack(str(key1), public_key2)

    #send the half secret to client 2
    client.sendall(json.dumps({
        'secret': key1_encrypted,
    }).encode())

    #receive the other half from client 2
    data = client.recv(1024).decode()
    data = json.loads(data)
    key2 = decryptKnapsack(data['secret'], private_key)
    key2 = json.loads(key2)

    #the common key will be the concatenation of the two half secrets
    print(key1)
    print(key2)
    key = key1 + key2

    print(key)

    #initial offset is 0
    offset = 0

    print('Send a message!')
    print('You can also exit the conversation by typing QUIT.')

    while True:
        #sending a message
        print('Send a message ...')

        msg = input()

        if msg == 'QUIT':
            print('Se you soon!')
            client.sendall(json.dumps({
                'offset': offset,
                'msg': 'QUIT'
            }).encode())
            client.close()
            break
        
        print('Your message: ' + msg)
        msg = solitaire(msg, key)
        print('Your encrypted message: ' + msg)

        client.sendall(json.dumps({
            'offset': offset,
            'msg': msg
        }).encode())
        print('Message sent! Waiting for resp..')

        offset += len(msg)

        #getting response
        resp = client.recv(1024).decode()
        resp = json.loads(resp)

        print('Received message is:', resp)

        msg = resp['msg']
        print('The encrypted message you got: ' + msg)
        if msg == 'QUIT':
            print('The other client left...')
            s.close()
            break

        resp_offset = resp['offset']
        if offset > resp_offset:
            print('Your offset is not working as it can, wait for fixing')
            offset = resp_offset
            
            #read initial key from config file again
            parser = configparser.ConfigParser()
            parser.read('config.txt')
            key = parser.get('config','key')
            key = json.loads(key)
            solitaireOffset(key, offset)
        
        elif offset < resp_offset:
            print('Your offset is not working as it can, wait for fixing')
            solitaireOffset(key, resp_offset - offset)
            offset = resp_offset

        msg = solitaire(msg, key)
        print('Your decrypted message: ' + msg)

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



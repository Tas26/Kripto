import math
import random

def GenerateKeypair():
    w = []
    w.append(random.randint(2,10))
    total = w[0]

    for i in range(1,8):
        w.append(random.randint(total + 1, 2 * total))
        total += w[i]
    
    q = random.randint(total + 1, 2 * total)
   
    while True:
        r = random.randint(2, q - 1)
        if math.gcd(q, r) == 1:
            break

    beta = []

    for w_i in w:
        beta.append((r * w_i) % q)

    private_key = (w, q, r)
    public_key = beta

    return private_key, public_key

def BitToByte(bits):
    byte = 0
    for bit in bits:
        byte *= 2
        if bit:
            byte += 1
    return byte

def ByteToBit(byte):
    out = []
    for i in range(8):
        out.append(byte & 1)
        byte >>= 1
    return out[::-1]



def encryptKnapsack(msg, public_key):
    msg = bytes(msg, 'ascii')
    msg_bits = []
    encrypted_bytes = []

    for byte in msg:
        msg_bits.append(ByteToBit(byte))
    
    for chunk in msg_bits:
        c = 0
        for i in range(8):
            c += chunk[i] * public_key[i]
        encrypted_bytes.append(c)
    
    return encrypted_bytes

def decryptKnapsack(msg, private_key):
    w, q, r = private_key
    s = modularInverse(r, q)
    decrypted_msg = []

    for i in range(len(msg)):
        msg[i] = (msg[i] * s) % q

    for c in msg:
        a = []
        for i in reversed(range(8)):
            if w[i] > c:
                a.append(0)
            else:
                a.append(1)
                c -= w[i]
        a = reversed(a)
        decrypted_msg.append(chr(BitToByte(a)))
    
    return ''.join(decrypted_msg)

def modularInverse(a, b):
    """Returns the modular inverse of a mod b. Pre: a < b and gcd(a, b) = 1
    Adapted from https://en.wikibooks.org/wiki/Algorithm_Implementation/
    Mathematics/Extended_Euclidean_algorithm#Python
    """
    saved = b
    x, y, u, v = 0, 1, 1, 0
    while a:
        q, r = b // a, b % a
        m, n = x - u*q, y - v*q
        b, a, x, y, u, v = a, r, u, v, m, n
    return x % saved

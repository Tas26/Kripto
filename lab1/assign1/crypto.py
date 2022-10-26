#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: <YOUR NAME>
SUNet: <SUNet ID>

Replace this with a description of the program.
"""
from math import ceil
from pydoc import plain
from unittest import result
import utils

# Caesar Cipher

def encrypt_caesar(plaintext):
    """Encrypt plaintext using a Caesar cipher.

    Add more implementation details here.
    """
    result = ''
    for i in range(len(plaintext)):
        result += chr((ord(plaintext[i]) + 3 - 65) % 26 + 65)
 
    return result



def decrypt_caesar(ciphertext):
    """Decrypt a ciphertext using a Caesar cipher.

    Add more implementation details here.
    """
    result = ''
    for i in range(len(ciphertext)):
        result += chr((ord(ciphertext[i]) - 3 - 65) % 26 + 65)
 
    return result


# Vigenere Cipher

def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    result =''
    plaintext = plaintext.upper()
    keyword = keyword.upper()
    length = len(keyword)
    for i in range(0, len(plaintext)):
        c = plaintext[i]
        k = keyword[i % length]
        result += chr((ord(c) - 65 + ord(k) - 65) % 26 + 65)
    return result    


def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    result =''
    ciphertext = ciphertext.upper()
    keyword = keyword.upper()
    length = len(keyword)
    for i in range(0, len(ciphertext)):
        c = ciphertext[i]
        k = keyword[i % length]
        result += chr((ord(c) - 65 - ord(k) - 65) % 26 + 65)
    return result    


# Scytale Cipher

def encrypt_scytale(plaintext, circumference):
    result = []
    for k in range(0, circumference):
        for i in range(0, ceil(len(plaintext)/circumference)):
            result.insert(i + (k*(ceil(len(plaintext)/circumference))), plaintext[(i*circumference)+k])
    crypted = ''
    for i in range(0, len(result)):
        crypted += str(result[i])        
    return crypted        


def decrypt_scytale(ciphertext, circumference):
    result = []
    for k in range(0, ceil(len(ciphertext)/circumference)):
        for i in range(0,  circumference):
            result.insert(i + (k*circumference), ciphertext[(i*(ceil(len(ciphertext)/circumference))) + k])
    decrypted = ''
    for i in range(0, len(result)):
        decrypted += str(result[i])        
    return decrypted     

# Railfence Cipher


def encrypt_railfence(plaintext, num_rails):

    matrix = [[' ' for i in range(len(plaintext))] for j in range(num_rails)]

    direction = 0
    row = 0
    for i in range(len(plaintext)):
        matrix[row][i] = plaintext[i]
        if row == num_rails-1:
            direction = 1
        elif row == 0:
            direction = 0

        if direction == 0:
            row = row + 1
        else: row = row - 1

    # for i in range(0, num_rails):
    #     print(matrix[i], ' ')     

    crypted = ''
    for i in range(0, num_rails):
        for j in range(0, len(plaintext)):
            if matrix[i][j] != ' ':
                crypted += str(matrix[i][j])

    return crypted

def decrypt_railfence(ciphertext, num_rails):

    matrix = [[' ' for i in range(len(ciphertext))] for j in range(num_rails)]

    direction = 0
    row, col = 0, 0

    # Making the zigzag pattern and mark the spots
    for i in range(len(ciphertext)):
        if row == 0:
            direction = 1
        if row == num_rails - 1:
            direction = 0
 
        matrix[row][col] = '+'
        col += 1

        if direction:
            row += 1
        else:
            row -= 1  

    # biuld the zigzag matrix
    index = 0
    for i in range(num_rails):
        for j in range(len(ciphertext)):
            if ((matrix[i][j] == '+') and
               (index < len(ciphertext))):
                matrix[i][j] = ciphertext[index]
                index += 1            

    # Read zigzag the matrix
    decrypted = ''
    row = 0
    col = 0 
    for i in range(len(ciphertext)):
        if row == 0:
            direction = 1
        if row == num_rails-1:
            direction = 0
             
        if (matrix[row][col] != ' '):
            decrypted += str(matrix[row][col])
            col += 1
             
        if direction:
            row += 1
        else:
            row -= 1
    return decrypted    

# Merkle-Hellman Knapsack Cryptosystem

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    raise NotImplementedError  # Your implementation here

def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    raise NotImplementedError  # Your implementation here


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    raise NotImplementedError  # Your implementation here

def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    raise NotImplementedError  # Your implementation here


def main():
    print(encrypt_railfence('WEAREDISCOVEREDFLEEATONCE', 3))
    print(decrypt_railfence('WECRLTEERDSOEEFEAOCAIVDEN', 3))
    
   

if __name__ == "__main__":
    main()

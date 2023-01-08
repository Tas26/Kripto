# trim2092

# d - deck; j1 = first joker; j2 = second joker

def moveWhiteJoker(d):
    i = d.index(53)

    if i < 53:
        d[i], d[i+1] = d[i+1], d[i]
    else:
        d.remove(53)
        d.insert(1, 53)

def moveBlackJoker(d):
    i = d.index(54)

    if i < 52:
        d[i], d[i+1] = d[i+1], d[i]
        d[i+1], d[i+2] = d[i+2], d[i+1]
    elif i == 52:
        d.remove(54)
        d.insert(1, 54)
    else:
        d.remove(54)
        d.insert(2, 54)

def swapJoker(d):
    j1 = d.index(53)
    j2 = d.index(54)

    if j1 > j2:
        j1, j2 = j2, j1
    
    j2 += 1
    d[j2:], d[:j1] = d[:j1], d[j2:]

def swapLast(d):
    last = d[53]

    d[last:53], d[:last] = d[:last], d[last:53]

def solitaire_steps(d):
    moveWhiteJoker(d)
    moveBlackJoker(d)
    swapJoker(d)
    swapLast(d)

def getNumber(d):
    while True:
        solitaire_steps(d)
        first = d[0]

        if first < 53:
            return d[first] % 2

def getByte(d, n):
    byte_list = []

    for _ in range(n):
        ch = '0'
        for j in range(7):
            nr = getNumber(d)
            ch += str(nr)
        byte_list.append(int(ch, 2))
    
    return bytes(byte_list)

def getByteOffset(d, n):
    for _ in range(n):
        for _ in range(7):
            nr = getNumber(d)

def solitaire(old, key):
    new = []
    n = len(old)
    binary_old = bytes(old, 'ascii')

    byte_list = getByte(key, n)

    for i in range(n):
        new.append(chr(binary_old[i] ^ byte_list[i]))

    return ''.join(new)

def solitaireOffset(key, offset):
    for _ in range(offset):
        getByteOffset(key, offset)
    
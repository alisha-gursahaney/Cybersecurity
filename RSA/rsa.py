#!/usr/bin/python3
# RSA skeleton code from the https://aaronbloomfield.github.io/ics/hws/hw-rsa.html assignment

import sys, random, math, hashlib


# An RSA key, either public (if d is None), private (if e is None), or both
# (if neither are None)
class rsakey:
    l = None  # the bit length
    e = None  # the public key (or None if it's just a private key)
    d = None  # the private key (or None if it's just a public key)
    n = None  # the modulus (n=p*q)

    def __init__(self, _l, _e, _d, _n):
        (self.l, self.e, self.d, self.n) = (_l, _e, _d, _n)


# Ciphertext class
class ciphertext:
    c = []  # the list of the encrypted blocks
    l = None  # the length of the original plaintext file or string in bytes
    b = None  # the length of each block in bytes

    def __init__(self, _c, _l, _b):
        (self.c, self.l, self.b) = (_c, _l, _b)


# Whether to print verbose messages.  This is useful for debugging, as it will
# never be set to true (via the -verbose flag) during grading.
verbose = False

# Whether the values of p and q are displayed during key generation.  This is
# useful for debugging, and it *is* something that we will test during grading.
showPandQ = False


# This will write an RSA key to a file (or files) in the standard format used
# for this assignment.  If the key contains both d and e, then two files
# (one private, one public) are written.  Given the file basename of
# <filebasename>, the key files are <filebasename>-public.key and
# <filebasename>-private.key.
def writeKeyToFile(key, filebasename):
    if key.e is not None:  # it's a public key
        with open(filebasename + "-public.key", "w") as f:
            print("public\n" + str(key.l) + "\n" + str(key.e) + "\n" + str(key.n) + "\n", file=f)
    if key.d is not None:  # it's a private key
        with open(filebasename + "-private.key", "w") as f:
            print("private\n" + str(key.l) + "\n" + str(key.d) + "\n" + str(key.n) + "\n", file=f)


# This will read an RSA key from a file in the standard format used for this
# assignment
def readKeyFromFile(filename):
    with open(filename) as f:
        if f.readline().strip() == "public":
            return rsakey(int(f.readline().strip()), int(f.readline().strip()), None, int(f.readline().strip()))
        else:
            return rsakey(int(f.readline().strip()), None, int(f.readline().strip()), int(f.readline().strip()))


# This will read cipher text from a file in the standard format used for this
# assignment
def readCipherTextFromFile(inputFileName):
    c = []
    with open(inputFileName) as f:
        l = f.readline().strip().split(" ")
        while True:
            x = f.readline().strip()
            if x == '':
                break
            c.append(int(x))
    return ciphertext(c, l[0], l[1])


# This will write cipher text to a file in the standard format used for this
# assignment
def writeCipherTextToFile(outputFileName, cipherText):
    with open(outputFileName, "w") as f:
        print(cipherText.l, cipherText.b, file=f)
        for c in cipherText.c:
            print(c, file=f)


# this function is included here because there is a Java version, but it
# is not needed in Python: to convert a SHA-256 hash to hex form, just use:
# hashlib.sha256(bytes(plaintext,'ascii')).hexdigest()
def convertHash():
    assert False


# Given an ASCII string, this will convert it to an integer representation
def convertFromASCII(text):
    return int.from_bytes(bytes(text, 'ascii'), "big")


# Given an integer representation of an ASCII string, this will convert it to
# ASCII
def convertToASCII(block):
    h = hex(block)[2:]
    if len(h) % 2 == 1:
        h = '0' + h
    return bytes.fromhex(h).decode('ascii')


# Given a bit size and a certainty, this will generate a (probably) prime
# number of the desired size
def generate_prime(bits, k):
    count = 0
    while True:
        # generate a number, make sure it's odd
        n = random.randint(1, 2 ** (bits + 1) - 1)
        if n % 2 == 0:
            n += 1
        count += 1
        # run the Fermat primality test
        iterations = 0
        for _ in range(k):
            a = random.randint(1, n - 1)
            if pow(a, n - 1, n) != 1:  # it's composite
                break
            else:  # prime so far
                iterations += 1
        if iterations == k:
            return n


# ----------------------------------------
# You have to implement these functions

# Given the passed bitlength (int) and the seed (int), it will generate a key.
# One should initialize the random number generator with the passed seed via
# random.seed(). This returns a rsakey object.

# RSA key Object: l, e, d, n

def generateKeys(bitlength, seed):
    p = generate_prime(bitlength, 25)
    q = generate_prime(bitlength, 50)
    # divide bit length by any value to make it less than p and q
    n = p * q
    to_div = int((math.log(n) // math.log(2)))
    e = generate_prime((to_div- 2), 25)
    d = pow(e, -1, ((p - 1) * (q - 1)))
    # base is not invertible for the given modulus
    key = rsakey(bitlength, e, d, n)
    return key


# Given the passed rsakey object and string, thclis will perform the RSA
# encryption. It should return a ciphertext object.
def encrypt(key, plaintext):
    new_string = []
    size = sys.getsizeof(plaintext)
    chunks = int((int.bit_length(key.n)-1)/8)
    for i in range(0, len(plaintext), chunks):
        m = convertFromASCII(plaintext[i:i+chunks])
        new_string.append(pow(m, key.e, key.n))
        # unsupported operand type(s) for ** or pow(): 'int', 'NoneType', 'int'
        #new_string += str(c)
    final = ciphertext(new_string, size, chunks)
    return final


# Given the provided rsakey object and ciphertext object plaintext, this will
# perform the RSA decryption. It should return a string.
def decrypt(key, cipherText):
    # list = cipherText.split(' ')
    x = ''
    # for i in list:
    #     c = int(list[i])
    #     value = pow(c, key.d, key.n)
    #     x += value
    # result = ' '.join(x[i:i + 2] for i in range(0, len(x), 2))
    # list2 = result.split()
    # final = ''
    # for j in list2:
    #     word = convertToASCII(j)
    #     final += word
    for i, val in enumerate(cipherText.c):
        ciphertext.c[i] = convertToASCII(pow(cipherText.c[i], key.d, key.n))
        x += ciphertext.c[i]
    return x


# Given the passed rsakey, which will not have a private (d) key, it will
# determine the private key by attempting to factor n.  It returns a rsakey
# object.
def crack(key):
    # cipher text ?
    # prime numbers p and q must be in the range 3 to sqrt(n) and check every other value
    for p in range(3, int(math.sqrt(key.n)), 2):
        if key.n % p == 0:
            q = key.n // p
            pq = (p - 1) * (q - 1)
            # ValueError: base is not invertible for the given modulus
            key.d = (pow(key.e, -1, pq))
            return key


# Given the passed rsakey object and string, it will return a ciphertext object that
# is the digital signature of the text, signed with the private key.
def sign(key, plaintext):
    h = hashlib.sha256(bytes(plaintext, 'ascii')).hexdigest()
    c = encrypt(key, h)
    # problem with encrypt
    m = plaintext + c
    return m


# Given the passed rsakey object, string, and ciphertext object, this will
# check the signature; it only returns True (if the signature is valid) or
# False (if not).
def checkSign(key, plaintext, signature):
    if plaintext in signature:
        i = signature.find(plaintext)
        j = i + len(plaintext)
        delimiter = signature[j]
        list = signature.split(signature[j])
        # list[0] = plaintext
        # list[1] = the +c (encrypted portion)
        list[1] = delimiter + list[1]
        h1 = decrypt(key, list[1])
        h2 = hashlib.sha256(bytes(plaintext, 'ascii')).hexdigest()
        if h1 == h2:
            return True
        else:
            return False


# ----------------------------------------
# Don't modify this!  Or, if you do modify this, make sure you submit the
# original version when you submit the assignment.  This is necessary for our
# testing code.

def main():
    global verbose, showPandQ, outputFileName, inputFileName
    outputFileName = "output.txt"
    inputFileName = "input.txt"
    keyName = "default"
    seed = 0

    i = 1
    while i < len(sys.argv):

        if sys.argv[i] == "-verbose":
            verbose = not verbose

        elif sys.argv[i] == "-output":
            i = i + 1
            outputFileName = sys.argv[i]

        elif sys.argv[i] == "-input":
            i = i + 1
            inputFileName = sys.argv[i]

        elif sys.argv[i] == "-key":
            i = i + 1
            keyName = sys.argv[i]

        elif sys.argv[i] == "-showpandq":
            showPandQ = true

        elif sys.argv[i] == "-keygen":
            i = i + 1
            bitLength = int(sys.argv[i])
            key = generateKeys(bitLength, seed)
            writeKeyToFile(key, keyName)

        elif sys.argv[i] == "-encrypt":
            key = readKeyFromFile(keyName + "-public.key")
            plaintext = open(inputFileName).read()
            cipherText = encrypt(key, plaintext)
            writeCipherTextToFile(outputFileName, cipherText)

        elif sys.argv[i] == "-decrypt":
            key = readKeyFromFile(keyName + "-private.key")
            cipherText = readCipherTextFromFile(inputFileName)
            plaintext = decrypt(key, cipherText)
            with open(outputFileName, "w") as f:
                print(plaintext, file=f, end='')

        elif sys.argv[i] == "-sign":
            key = readKeyFromFile(keyName + "-private.key")
            plaintext = open(inputFileName).read()
            signature = sign(key, plaintext)
            writeCipherTextToFile(inputFileName + ".sign", signature)

        elif sys.argv[i] == "-checksign":
            key = readKeyFromFile(keyName + "-public.key")
            plaintext = open(inputFileName).read()
            signature = readCipherTextFromFile(inputFileName + ".sign")
            result = checkSign(key, plaintext, signature)
            if not result:
                print("Signatures do not match!")

        elif sys.argv[i] == "-crack":
            key = readKeyFromFile(keyName + "-public.key")
            cracked = crack(key)
            writeKeyToFile(cracked, keyName + "-cracked")

        elif sys.argv[i] == "-seed":
            seed = int(sys.argv[++i])

        else:
            print("Unknown parameter: '" + str(sys.argv[i]) + "', exiting.")
            exit()

        i += 1


if __name__ == '__main__':
    main()
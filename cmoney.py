import hashlib
import binascii
import rsa
import sys
import datetime

# gets the hash of a file; from https://stackoverflow.com/a/44873382
def hashFile(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

# given an array of bytes, return a hex reprenstation of it
def bytesToString(data):
    return binascii.hexlify(data)

# given a hex reprensetation, convert it to an array of bytes
def stringToBytes(hexstr):
    return binascii.a2b_hex(hexstr)

# Load the wallet keys from a filename
def loadWallet(filename):
    with open(filename, mode='rb') as file:
        keydata = file.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
    pubkey = rsa.PublicKey.load_pkcs1(keydata)
    return pubkey, privkey

# save the wallet to a file
def saveWallet(pubkey, privkey, filename):
    # Save the keys to a key format (outputs bytes)
    pubkeyBytes = pubkey.save_pkcs1(format='PEM')
    privkeyBytes = privkey.save_pkcs1(format='PEM')
    # Convert those bytes to strings to write to a file (gibberish, but a string...)
    pubkeyString = pubkeyBytes.decode('ascii')
    privkeyString = privkeyBytes.decode('ascii')
    # Write both keys to the wallet file
    with open(filename, 'w') as file:
        file.write(pubkeyString)
        file.write(privkeyString)
    return


def main():
    command = sys.argv[1]
    if command == 'name':
        print("AlishaMeenaDollar(TM)")

    if command == 'genesis':
        f = open('block_0.txt', 'w')
        f.write('Green eggs and ham')
        f.close()
        print("Genesis block created in 'block_0.txt'")

    if command == 'generate':
        wallet = sys.argv[2]
        (pubkey, privkey) = rsa.newkeys(1024)
        saveWallet(pubkey, privkey, wallet)
        tag = hashFile(wallet)[:16]
        print("New wallet generated in", wallet, "with tag", tag)

    if command == 'address':
        wallet = sys.argv[2]
        tag = hashFile(wallet)[:16]
        print(wallet, "wallet tag:", tag)

    if command == 'fund':
        file = sys.argv[7]
        amount = sys.argv[6]
        wallet = sys.argv[2]
        tag = hashFile(wallet)[:16]
        # print("TAG", tag)
        id = 'bigfoot'
        f = open(file, 'w')
        # print("CHECK FILE", file)
        f.write('Amount' + amount + 'AlishaMeenaDollars' +
                'from' + id + 'to' + tag + 'on' + str(datetime.datetime.now()))
        print("Funded wallet", tag,
              "with", amount, "AlishaMeenaDollars",
              "on", str(datetime.datetime.now()))

    if command == 'transfer':
        from_name = sys.argv[2]
        amount = sys.argv[7]
        wallet = sys.argv[6]
        file = sys.argv[8]
        #f = open(file, 'w')
        #line = 'From: ' + str(hashFile(wallet)[:16]) + '\n' + "To: " + str(wallet) + '\n' + "Amount: " + str(amount) + '\n' + "Date: " + str(datetime.datetime.now())
        #f.write(line)
        #f.close()
        print("Transferred", amount, "from", from_name, "to", wallet, "and the statement to", file, "on", str(datetime.datetime.now()))

    if command == 'balance':
        balance = 0
        wallet = sys.argv[2]
        tag = hashFile(wallet)[:16]
        # print("WALLET", wallet)
        # print("TAG", tag)
        # f = open('mempool.txt', 'r')
        # for each in f:
        #     # print("EACH", each)
        #     split = each.split()
        #     # print("SPLIT ARRAY", split)
        #     if split[0] == tag:
        #         balance -= int(split[1])
        #     elif split[4] == tag:
        #         balance += int(split[2])
        # f.close()
        print(balance)

    if command == 'verify':
        wallet = sys.argv[2]
        print("verify")

    if command == 'mine':
        nonce = 0
        count = 1
        block = 'block_' + str(count) + '.txt'
        value = sys.argv[2]
        f = open(block, 'w')
        mempool = open('mempool.txt', 'r+')

        print("Mempool transactions moved to", block, "and mined with difficulty", value, "and nonce", nonce)


    if command == 'validate':
        print("False")




if __name__ == '__main__':
    main()
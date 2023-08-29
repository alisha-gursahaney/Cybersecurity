# Name: Alisha Meena Gursahaney
# Net Id: amg9zd

import sys, hashlib

dictionaryfile = sys.argv[1]
passwordfile = sys.argv[2]
salt = sys.argv[3]

with open(dictionaryfile, 'r') as dictionary:
    # reading each line
    for line in dictionary:
        # reading each word
        for word in line.split():
            with_salt = word+salt
            check = hashlib.sha256(bytes(with_salt, 'ascii')).hexdigest()
            with open(passwordfile, 'r') as passwords:
                for each in passwords:
                    one = each.split()
                    # one[1] is the hex next to the given password
                    if one[1] == check:
                    # if the hex matches our dictionary hex, then print the password
                        print("password for " + one[0] + " is: " + word)

import sys
import os

w = 8
words_file = '/usr/share/dict/cracklib-small'

with open(words_file) as f:
    word_list = f.readlines()

passphrase = []

while True:
    b = os.urandom(2)
    n = int.from_bytes(b, sys.byteorder)

    try:
        passphrase.append(word_list[n].rstrip('\n'))
    except IndexError:
        continue

    if len(passphrase) == w:
        break

print(' '.join(passphrase))


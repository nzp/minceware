import sys
import os

w = 8
words_file = '/usr/share/dict/cracklib-small'

with open(words_file) as f:
    word_list = f.readlines()

passphrase = []

while True:
    n = int.from_bytes(os.urandom(2), sys.byteorder)

    try:
        passphrase.append(word_list[n].rstrip('\n'))
    except IndexError:
        continue

    if len(passphrase) == w:
        break

print(' '.join(passphrase))


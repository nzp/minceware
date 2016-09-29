#! /usr/bin/env python3

"""
Minceware generates truly random Diceware style passphrases on a computer.

Exported functions:
get_length_from_entropy -- calculate passphrase length based on entropy and word list length
generate_passphrase -- generates passphrase from a given word list

For standalone usage and command line arguments run

``minceware (--help|-h)``

"""

import sys
import os
import math


def get_length_from_entropy(entropy, list_length):
    """Calculate the number of words in a passphrase.

    The length returned is rounded up so that we always have at least
    ``entropy`` bits in a passphrase.

    Arguments:
    entropy -- desired minimum entropy of a passphrase in bits (shannons)
    list_length -- number of words in the word list
    """
    return math.ceil(entropy/math.log(list_length, 2))


def generate_passphrase(passphrase_length, word_list):
    """Generate the passphrase string.

    For each word, read 2 bytes from the kernel-space CSPRNG via ``os.urandom``
    and convert them to an integer which serves as a list index.  A list of
    65,536 words is probably enough so we don't need more than 2 bytes
    (“2 bytes should be enough for everyone.”).

    Return a space delimited string of words, for the same reason Diceware
    recommends spaces to be included in the passphrase.  Additionally, spaces
    make it much more legible.

    Arguments:
    passphrase_length -- number of words in the resulting passphrase
    word_list -- list of words from which the passphrase is generated
    """
    passphrase = []

    while True:
        n = int.from_bytes(os.urandom(2), sys.byteorder)

        try:
            passphrase.append(word_list[n].rstrip('\n'))
        except IndexError:
            continue

        if len(passphrase) == passphrase_length:
            break

    return ' '.join(passphrase)


if __name__ == '__main__':
    import argparse


    parser = argparse.ArgumentParser(
        description='Securely generate Diceware style passphrases on a computer.'
    )
    parser.add_argument('-i',
                        dest='info',
                        action='store_true',
                        help='Info/calculator mode.')
    parser.add_argument('-f',
                        dest='words_file',
                        default='/usr/share/dict/cracklib-small',
                        type=argparse.FileType('r'),
                        help='File which contains the word list.  Default: %(default)s',
                        metavar='PATH_TO_WORD_LIST')
    strength = parser.add_mutually_exclusive_group()
    strength.add_argument('-w',
                          dest='number_of_words',
                          type=int,
                          help='Number of words in the passphrase.  \
                            Mutually exclusive with -e.')
    strength.add_argument('-e',
                          dest='bits',
                          type=int,
                          default=128,
                          help='Minimum strength of passphrase in bits.  \
                            Mutually exclusive with -w.  Default: %(default)s.')

    args = parser.parse_args()

    word_list = args.words_file.readlines()
    args.words_file.close()


    if args.info:
        l = len(word_list)  # We need this >=1 times so calculate only once.
        h = math.log(l, 2)

        if args.number_of_words:
            print('{H:.2f} bits ({h:.2f} bit/word)'.format(
                H=args.number_of_words*h,
                h=h))
            sys.exit()
        # Test for '-e' flag explicitly because args.bits is always set (has
        # a default value).
        elif '-e' in sys.argv:
            print('{w} words ({h:.2f} bit/word)'.format(
                w=get_length_from_entropy(args.bits, l),
                h=h))
            sys.exit()
        else:
            print('{l} words, {h:.2f} bit/word'.format(l=l, h=h))
            sys.exit()


    if args.number_of_words:
        length = args.number_of_words
    else:
        length = get_length_from_entropy(args.bits, len(word_list))

    print(generate_passphrase(length, word_list))

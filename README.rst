Minceware
==========

Minceware generates secure_ Diceware_ style passphrases from user supplied Unix
words formatted lists of words.


Why?
-----

I'm a big fan of Diceware: it produces (relatively) easy to remember, measurably
strong passphrases.  However, rolling dice enough times, looking the words up,
etc. especially when you need to generate a few passwords at a time becomes
tiring quickly, and discourages good passphrases.  Assuming your computing
environment isn't compromised (and if it is, analogue passphrase generation
will hardly help since you'll eventually be using them in a compromised
environment), there's no reason why this should be done manually **iff**
kernel-space randomness is used to pick words.  Somewhat shockingly, a quick
search will reveal a solid amount of horrible ideas on this front: about a dozen
online, in-browser generators and even an `entrepreneurial kid who will roll the
dice for you and snail mail you a passphrase for a small fee`__ (this is so
brilliantly assertive that I feel bad for lumping it together with browser JS
crypto snake oil salesmen — the kid is a genius).

.. __: http://www.dicewarepasswords.com/


Usage
------
``minceware.py [-h] [-f PATH_TO_WORD_LIST] [-w NUMBER_OF_WORDS | -e BITS]``

Optional arguments:
  -h, --help            show this help message and exit
  -i                    Info/calculator mode.
  -f PATH_TO_WORD_LIST  File which contains the word list. Default:
                        /usr/share/dict/cracklib-small
  -w NUMBER_OF_WORDS    Number of words in the passphrase. Mutually exclusive
                        with -e.
  -e BITS               Minimum strength of passphrase in bits. Mutually
                        exclusive with -w. Default: 128.

By default (without arguments), Minceware generates ~141 bit strong passphrases
from ``cracklib-small`` list of words as distributed by Ubuntu (i.e.
``/usr/share/dict/cracklib-small``), which gives 9 words.  The default strength
is 128 bits, but since Minceware rounds the number of required words up, and
each cracklib word is worth 15.7 bits, we get the high number.  With 8 words
you would get ~125 bits, so you're probably more than safe if you just omit one
word from the default output.

The ``-i`` flag puts the program in “calculator” mode where you can see how
many bits (if combined with ``-w``) a passphrase has, how long a
passphrase of certain strength would be (if combined with ``-e``), or how many
words the given word list contains (when used alone).  All variants show bits
per word in parentheses.

The ``-f`` flag is a path to the word list file which needs to be simply a
Unix words formatted (newline delimited list of words) file.  Value of ``-``
makes the program take the list from standard input.  Currently the program
reads just 2 bytes from the RNG as it's easier to just ignore indexes in the list
larger than 16 bit integers than it is to ignore index values larger than
realistic length of such lists, or to massage the RNG output to have realistic
values below 16,777,216 (3 bytes).  Therefore, it makes little sense to feed it
a list with more than 65,536 words, which is probably a reasonable upper limit;
the number of words in the list is inversely proportional to passphrase length
for a given strength, so excessively large lists could potentially produce
passphrases that are too short in terms of individual characters.

Flags ``-e`` (required entropy) and ``-w`` (required number of words) are
mutually exclusive.

Apart from word lists that come with any Unix system, obvious excellent ready made
choices for words are original lists found on the `Diceware site`__, as well as
`EFF's alternative lists`__.  To use them just do something like ::

 cut -f 2 infile > outfile

to remove dice indexing (lists from the Diceware site also contain PGP signature
blocks so remove those too).


Preemptive FAQ
---------------

**Q**: Why “Minceware”?

**A**: Because you're not dicing, you're *mincing*! ... :D \*ba-dum tsss\*

.. _secure:

**Q**: Isn't this less secure/random than Diceware?

**A**: Depends.  If you're using high quality casino dice, and casting them
properly, then Diceware is *maybe* more random.  This program uses Python's
``os.urandom`` source of random bits, which uses native system's kernel-space
CSPRNG_, i.e. a source which is (or *should* be) indistinguishable from “true”
randomness.  So if you are, and you most likely *are*, using cheap Yahtzee dice,
what this program produces is most certainly more random than Diceware.  As for
security, this is only as secure as your whole OS is secure.  Dice and paper
can't be backdoored (unless someone really wants you in particular), etc., but
they are much less convenient.  So there.  All considerations concerning word
lists in Diceware apply here also.  Since this is a fairly trivial program,
the main gist of it being simply a wrapper around OS's CSPRNG, it would probably
be better if it was written in C, just to absolutely ensure at source code level
the right source of randomness is being used, and to ensure the passphrase is
properly managed in memory, but that would forego all the convenience of using
a language like Python.


.. _Diceware: http://world.std.com/~reinhold/diceware.html
.. _CSPRNG: https://en.wikipedia.org/wiki/Cryptographically_secure_pseudorandom_number_generator
__ Diceware_
.. __: https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases

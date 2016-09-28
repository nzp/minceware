Minceware
==========

Minceware generates secure Diceware_ style passphrases from user supplied Unix
words formatted lists of words.

Why?
-----

I'm a big fan of Diceware: it produces (relatively) easy to remember, measurably
strong passphrases. ... TK

Usage
------

TK


FAQ
----

**Q**: Why “Minceware”?

**A**: Because you're not dicing, you're *mincing*! ... :D \*ba-dum tsss\*

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
lists in Diceware apply here also.


.. _Diceware: http://world.std.com/~reinhold/diceware.html
.. _CSPRNG: https://en.wikipedia.org/wiki/Cryptographically_secure_pseudorandom_number_generator


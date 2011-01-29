**Enigma Machine Simulator**
============================

Usage: `python enigma.py`

A new machine is created automatically, but must be configured with a number of scramblers and letter swaps.

To add a scrambler, type `add a:b` where **a** is the id of the scrambler (a seed number used to generate the same scrambling system each time that one is used) and **b** is the letter that the scrambler is currently oriented to. This process can be repeated as many times as you like to add many layers of scrambling.

To swap two letters around for the scrambling, type `swap a:b` where **a** and **b** are the letters to be swapped. This process can be repeated as many times as you like to swap many letters for scrambling.

To unscramble, simply set up a new machine, configure it to exactly the same way as for scrambling, and then input the ciphertext. When scrambled, this will produce the plaintext because of the encryption and decryption being a mirror process.
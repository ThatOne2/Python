# Security 1 - mandatory handin 2

I got a lot of my code from different places. links to these are in the server file.

## About the program

The program works as so:

- Alice tells Bob she wants to roll a dice
- Bob decides on and sends Alice the genarators g and p
- Alice makes a guess on what she thinks the dice will land on
- Alice uses these and another random int to hash her guess and sends this hashed guess to Bob
- Both Bob and Alice commits (in the same way as Alices guess) a number that will be used to generate the die roll
- Alice and Bob both send their numbers so that they can open the random number and calculate the roll
- Alice sends the unhashed guess and the random int to Bob
- Bob does the same hashing to see if he gets the same number as Alice's hashed commit
- If it matches Bob Accepts the guess and tells that to Alice
- If Alice guessed correct she gets a message saying she got it

The TLS protocol is achived using the ssl python libaray ontop of the python socket library.
I created a Certificate Authority, certificates and keys using openssl. To see excatly how see here:
<https://quaint-larkspur-ffd.notion.site/Creating-certificates-ce19c4acddb04c9a80671d46c2bd78b6>

Read more:
<https://docs.python.org/3/library/ssl.html>

## Running the program

first run the server by
´´python .\Bob.py´´
(It will stay open in a forever loop)

Each time you want Alice to roll a dice you have to run the script:
´´python .\Alice´´

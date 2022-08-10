# Python-Enigma

## About
A working Enigma Machine built using Python. This program will perfectly mimic the behavior of an Enigma machine, and can be used to encode any any alphabetical message. If one has knows the original settings, they can also be used to decode an Enigma message.

## 
ow To Use

### Simple Run
For a basic run, simply edit the message at the top, and run the program using your IDE of choice. This will then encode your desired message in Enigma.

## How An Enigma Works

There are 4 parts of an Enigma machine. The plugboard, rotors, and reflector. We will work by seeing the journey the letter "H" takes as it goes through the Engima, with Plugboard settings "ZYXWVUTSRQPONMLKJIHG", using rotors 1, 2, and 3 in that order, in the settings 12, 4, 20.  

## Plugboard.

A Plugboard is the first and last thing we run into. It works by making 10 pairs of letters. In our example, the letter Pairs are ZY, XW, VU, TS,  RQ,  PO,  NM, LK,  JI, HG. If a plugboard accepts a letter in a pair, it turns it into its partner. 

Since we started with "H", our letter immediately becomes a "G", as in our settings, H and G were paired. If we instead recieved a "Q" it would instead become an "R".

If a letter is not part of a pair, it goes to the Rotors unchanged.

## Rotors Forward. 

Rotors accept a letter, and then output a new letter. They also have an attribute called "Orientation".

Before they process the letter, they go through a shift. That way, the same letter in the input won't necessarily become the same letter in the output. 

The shifting mechanism is complicated, and not necessary to understand. Just know for this example, after the shift, the rotors we have are [1, 2, 3], and the rotor orientatsions are 11, 3, and 20 respectively. 

If orientation of a rotor is 0, that means it treats an all inputs as it is. A would be A, be would be B, and so on. But if it's orientation is 1, that means it will treat an input of A as a B, and input of Z as A, and so on.

Since we go backwards in Rotor order, we start with Rotor 3, in orientation 20. Thus, it will treat our "G" like an A. All rotors have specific mappings they obey, and the mappings are at the bottom of this README. Rotor 3 specifically outputs a "B" when given an "A". 

Finally, the Rotor's orientation also affects output, but in reverse. A setting of 1 means the Enigma machine will treat a Rotor's output of A as a "Z", a "B" as an "A" and so on. Since this rotor has an orientation of 20, it turns the rotors output of "A" into an "H".

The other 2 rotors follow a similar pattern. Rotor 2's orientation turns the "H' into a "K", then into an "L", then finally back into "I", and the third rotor (Rotor 1 with orientation 11), turns the "I" into a "T", then into a "P", and finally into an "E". 

## Reflector. 

The Reflector behaves very similarly to the plugboard, except for 2 key differences. One, all letters are paired, and two, the parings cannot be altered.

As it is, "E" is paired with "Q" on the reflector, so the reflector in this case outputs a "Q".

## Running backwards.

After the reflector, we go through the rotors and plugboard backwards.

Going through the rotors backwards is very similar to going through forwards in terms of orientation. However, we go through them in reverse order. In this case, that means Rotor One in orientation 11. The orientation means it will treat the input as a "B". However, it does not output a "K", but rather a "W". That is because, going backwards, it has the reverse mappings as when going forwards. Had Rotor One recieved a "W" going forwards, it would have output a "B". Hence, as it recieved a "B" goign backwards, it outputs a "W", which gets turned into an "L" after we reverse the orientation.

The other 2 rotors work the same; Rotor 2 with orientation 3 turns the "L" into an "O", then into a "Y", then into a "V". Rotor 3 with orientation 20 turns the "V" into a "P", then into an "H", then finally back into an "N".

Finally, we go through the plugboard again, which is exactly the same as going through it forwards. Since "N" was paired with "M", that means we turn the "N" into an "M", and that is our final encrypted answer.

For our next letter, we just shift all the rotors, and go through the process again.


## Decrypting
Enigma is known as a "Self-Decrypting Cypher", which means decrypting a letter is actually exactly the same process as the encrypting, provided we have the settings of the Rotors and plugboard as when the message was encrypted. 

For example, if we started with an M with the same configurations described above, we would eventually get back to an "H". 


## Configuring an Enigma.

The Enigma accepts 3 parameters as inputs to its constructor.

The first parameter is the plugboard settings. Simply type a 20 long string containing only capital letters without repeats. The first and second letter will be paired, as will the third and forth, and so on.

To choose the rotors, send in a 3 digit number as a string in the second Parameter. Make sure each digit is between 1 and 5 inclusive, and that there are no repeats.

The choose the settigns of the rotors, provdie the third parameter in the form of a 3 element Array of integers. The integers must be between 0 and 25 inclusive.

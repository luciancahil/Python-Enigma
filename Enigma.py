msg = "Hello There" # Change the message Here

def intToChar(int):
    if(int == 0):
        return "Z"          #26 % 26 = 0, so we might end up recieving a 0 when we have to return a "Z"
    return chr(int + 64)

def charToInt(char):        #Only meant for capital letters
    return ord(char) - 64


"""
TODO: Explain Engima
"""

class Enigma:
    rotors = [None,None,None]
    secondCritical = False
    #pbSettings are a string where 0 and 1 are switched, 2 and 3 are switched, and so forth
    #Rotor order is a 3 digit number in string form saying which rotor should go where.
    #Rotor settings is an array of integers saying the orientations of the rotors
    def __init__(self, pbSettings, rotorOrder, rotorSettings):
        self.pb = Plugboard(pbSettings.upper())

        for i in range(3):
            rSelection = rotorOrder[i]
            rOrient = rotorSettings[i]
            if(rOrient < 1 or rOrient > 26):
                raise ValueError("Not A Valid Rotor Orientation")

            if(rSelection == '1'):
                self.rotors[i] = RotorOne(rOrient)
            elif(rSelection == '2'):
                self.rotors[i] = RotorTwo(rOrient)
            elif(rSelection == '3'):
                self.rotors[i] = RotorThree(rOrient)
            elif(rSelection == '4'):
                self.rotors[i] = RotorFour(rOrient)
            elif(rSelection == '5'):
                self.rotors[i] = RotorFive(rOrient)
            else:
                raise ValueError(rSelection + " is not a valid Rotor")
        
        
        self.secondCritical = self.rotors[1].orientation == self.rotors[1].turnkey - 1  #check if the second rotor will make it's turkey

        if(self.secondCritical and self.rotors[2].orientation == self.rotors[2].turnkey - 1):   #if both the third and second are about to make their
            self.secondCritical = False                                                         #turnkeys, then we must prevent the second rotor from
            self.rotors[0].shift()                                                              #turning twice (by setting secondCritical to false) and turn the first rotor (since we turn before running anyway, this is the same difference)
    
    def scramble(self, message):
        cleaned = self.cleanString(message.upper())
        scrambled = ""
        
        for x in cleaned:
            scrambled += x

        return scrambled
    
    def cleanString(self, message):
        cleaned = ""

        for x in message:
            if(charToInt(x) <= 26 and charToInt(x) >= 1):
                cleaned += x
    
        return cleaned
    

    """
    Before a letter is passed through the Enigma machine, the rotors are shifted.

    Signals go from the third Rotor to the First Rotor, and the shift is no different

    First, we shift the third rotor, no matter what.

    If the third rotor made it's "turnkey" (like Q to R for RotorOne), shift the second Rotor as well.

    That's all simple, but the "second critical" part will give nightmares.

    If the second rotor gets shifted onto the first part of it's turnkey(Q for Rotor One), then
    next shift, the first and second rotors will also shift. We mark this by setting "second critical" to True

    Rotors will also only shift once, so if the third rotor makes it's turnkey while the second not turn twice.
    In this situation, all 3 rotors will switch once, just like a regular second critical.
    
    Fortunately, this can only happen right at the begining. I can avoid having to check if secondCritical is true everytime
    I go turn the first Rotor, I'll simply check to see if this special ocasion rises as I initiate.

    If it does, I just shift the first rotor and set second critical to false. Since the rotors are shifted before the character
    is encrypted, it won't matter that the first rotor is different from how it's meant to be before the first run, and will 
    be where they need to be after the first shift
    """
    def shiftRotors(self):
        if(self.rotors[2].shift()):
            self.rotors[1].shift()
        
        if(self.secondCritical):
            self.rotors[0].shift()
            self.rotors[1].shift()
            self.secondCritical = False
        
        if(self.rotors[1].orientation == self.rotors[1].turnkey - 1):
            self.secondCritical = True


    def __str__(self):
        rs = self.rotors[0].__str__()

        for i in range(1,3):
            rs += ", " + self.rotors[i].__str__()

        return "Enigma: " + self.pb.__str__() + "; " + "[" + rs + "]"



"""
The plugboard is the first and last thing that a letter goes through.
In the PlugBoard, 10 letters are connected to annother letter A to B, B to A, so on
If a character enters the plug board, it will exit as the letter its connected to (or itself if that letter isn't connected)
(in the above example, an entered B would become an A, and an A would become a B)
"""
class Plugboard:
    pbWires = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    def __init__(self, setting):
        self.upperSettings = setting.upper()
        self.checkValidity(self.upperSettings)
        
        #starting to make the actual Connections form
        for i in range(0, 20, 2):
            j = charToInt(self.upperSettings[i]) - 1
            k = charToInt(self.upperSettings[i + 1]) - 1

            if(self.pbWires[j] != intToChar(j + 1) or self.pbWires[k] != intToChar(k + 1)):
                raise ValueError("No Duplicate characters allowed")


            temp = self.pbWires[j]
            self.pbWires[j] = self.pbWires[k]
            self.pbWires[k] = temp

    def checkValidity(self, setting):
        if(len(setting) != 20):
            raise ValueError("Please enter 10 character pairs")
        
        for i in range(20):
            if(charToInt(setting[i]) <= 0 or charToInt(setting[i]) > 26):
                raise ValueError("Please only enter Characters")
    
    def runWire(self, char):                        #changes the characeter by running it throught the "Wire"
        return self.pbWires[charToInt(char) - 1]


    def __str__(self):
        set = "@ "
        for i in range(20):
            set += self.pbWires[i]
        return "PB " + set

"""
A rotor works by taking a letter and outputting a different one. 
For example, if Rotor One in position 0 were to recieve an "A" goign forward, it would output an "E".
A signal can also go backwards. If Rotor One recieved an "E" going backwards, it woudl return an "A"

A rotor can be spun in one of 26 positions. If a rotor is spun forwards one, then it would 
return a "K" if fed an e going forwards, and "D" if fed an "E" going backwards. 
Then we have to take the orientation backwards, so the final of "K" would be "H"

Orientation refers to how far along it's spun. "1" means input "A" matches with "A"
"2" means input "A" gets fed into "B"

"""
            
class Rotor:
    def __init__(self, orientation, type):
        self.orientation = orientation - 1      # -1 because an orietation of "1" means A goes into A, so no change
        self.turnkey = 0
        self.forwardWires = []
        self.backwardWires = []
        self.type = type
    
    def shift(self):
        if (self.orientation is 25):
            self.orientation = 0
        else:
            self.orientation += 1
        
        return self.orientation == self.turnkey

    def run(self, char, direction):
        asNum = charToInt(char)                         #convert to number
        asNum = asNum + self.orientation - 1            #add orientation, subtract one because arrays start at 0
        asNum = asNum % 26                              #cycle through to find a letter
        if(direction == "F"):   # "F"stands for forward, "B" stands for back
            asNum = charToInt(self.forwardWires[asNum])     #run through the Forward wires, then get the number representation of the new number
        elif direction == "B":
            asNum = charToInt(self.backwardWires[asNum])    # run through the back wires instead
        else:
            raise ValueError("Invalid Direction")
        asNum = asNum - self.orientation                #go back the orientation
        asNum = (asNum + 26 ) % 26                      #fix any negative numbers
        return intToChar(asNum)
    
    def __str__(self):
        return "Rotor Type " + str(self.type) + " @ " + intToChar(self.orientation + 1)

    def __repr__(self):
        return "Rotor Type " + str(self.type) + " @ " + intToChar(self.orientation + 1)

        
        

class RotorOne(Rotor):
    def __init__(self, orientation):
        super().__init__(orientation, 1)
        self.turnkey = 18 #turns as it goes from Q to R
        self.forwardWires = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
        self.backwardWires = "UWYGADFPVZBECKMTHXSLRINQOJ"

class RotorTwo(Rotor):
    def __init__(self, orientation):
        super().__init__(orientation, 2)
        self.turnkey = 5 #turns after going from E to F
        self.forwardWires = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
        self.backwardWires = "AJPCZWRLFBDKOTYUQGENHXMIVS"

class RotorThree(Rotor):
    def __init__(self, orientation):
        super().__init__(orientation, 3)
        self.turnkey = 22   #turns after going from V to W
        self.forwardWires = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
        self.backwardWires = "TAGBPCSDQEUFVNZHYIXJWLRKOM"

class RotorFour(Rotor):
    def __init__(self, orientation):
        super().__init__(orientation, 4)
        self.turnkey = 10 #turns after going from J to K
        self.forwardWires = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
        self.backwardWires = "HZWVARTNLGUPXQCEJMBSKDYOIF"

class RotorFive(Rotor):
    def __init__(self, orientation):
        super().__init__(orientation, 5)
        self.turnkey = 0    #turns after going from Z to A
        self.forwardWires = "VZBRGITYUPSDNHLXAWMJQOFECK"
        self.backwardWires = "QCYLXWENFTZOSMVJUDKGIARPHB"     


#public static void main
e = Enigma("ABCDEFGHIJKLMNOPQRST", '123', [12,5,22])
print(e.rotors)
e.shiftRotors()
print(e.rotors)
e.shiftRotors()
print(e.rotors)
e.shiftRotors()
print(e.rotors)

"""
All the letters:

1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26
A   B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U   V   W   X   Y   Z

Rotor One: Q to R
Input:      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U   V   W   X   Y   Z
Forward:    E   K   M   F   L   G   D   Q   V   Z   N   T   O   W   Y   H   X   U   S   P   A   I   B   R   C   J
Back:       U   W   Y   G   A   D   F   P   V   Z   B   E   C   K   M   T   H   X   S   L   R   I   N   Q   O   J

Rotor Two: E to F
Input:      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U   V   W   X   Y   Z
Forward:    A   J   D   K   S   I   R   U   X   B   L   H   W   T   M   C   Q   G   Z   N   P   Y   F   V   O   E
Back:       A   J   P   C   Z   W   R   L   F   B   D   K   O   T   Y   U   Q   G   E   N   H   X   M   I   V   S

Rotor Three:V to W
Input:      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U   V   W   X   Y   Z
Forward:    B   D   F   H   J   L   C   P   R   T   X   V   Z   N   Y   E   I   W   G   A   K   M   U   S   Q   O
Back:       T   A   G   B   P   C   S   D   Q   E   U   F   V   N   Z   H   Y   I   X   J   W   L   R   K   O   M

Rotor Four: J to K
Input:      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U   V   W   X   Y   Z
Forward:    E   S   O   V   P   Z   J   A   Y   Q   U   I   R   H   X   L   N   F   T   G   K   D   C   M   W   B
Back:       H   Z   W   V   A   R   T   N   L   G   U   P   X   Q   C   E   J   M   B   S   K   D   Y   O   I   F

Rotor Five: Z to A
Input:      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U   V   W   X   Y   Z
Forward:    V   Z   B   R   G   I   T   Y   U   P   S   D   N   H   L   X   A   W   M   J   Q   O   F   E   C   K
Back:       Q   C   Y   L   X   W   E   N   F   T   Z   O   S   M   V   J   U   D   K   G   I   A   R   P   H   B

"""
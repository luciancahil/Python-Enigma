msg = "Hello There" # Change the message Here

def intToChar(int):
    if(int == 0):
        return "Z"          #26 % 26 = 0, so we might end up recieving a 0 when we have to return a "Z"
    return chr(int + 64)

def charToInt(char):        #Only meant for capital letters
    return ord(char) - 64

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
    def __init__(self, orientation):
        self.orientation = orientation - 1      # -1 because an orietation of "1" means A goes into A, so no change
        self.turnkey = 0
        self.forwardWires = []
        self.backwardWires = []
    
    def shift(self):
        if (self.orientation is 26):
            self.orientation = self.orientation
        else:
            print(12)
        
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
        
        

class RotorOne(Rotor):
    def __init__(self, orientation):
        super().__init__(orientation)
        self.turnkey = 18 #turns as it goes from Q to R
        self.forwardWires = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
        self.backwardWires = "UWYGADFPVZBECKMTHXSLRINQOJ"
        

#public static void main
r1 = RotorOne(1)
for i in range (1, 27):
    print(r1.run(intToChar(i),"F"))

print("")

for i in range (1, 27):
    print(r1.run(intToChar(i),"B"))

print()
rotorOne = RotorOne(10)

print(rotorOne.run("D", "F"))
print()
print(rotorOne.run("D", "B"))

print("")
try:
    rotorOne.run("D", "N")
except ValueError:
    print("Invalid Direction Caught")

"""
All the letters:

1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26
A   B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U   V   W   X   Y   Z

Rotor One:
Input:      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U   V   W   X   Y   Z
Forward:    E   K   M   F   L   G   D   Q   V   Z   N   T   O   W   Y   H   X   U   S   P   A   I   B   R   C   J
Back:       U   W   Y   G   A   D   F   P   V   Z   B   E   C   K   M   T   H   X   S   L   R   I   N   Q   O   J

"""
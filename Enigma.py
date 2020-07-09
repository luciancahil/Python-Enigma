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

            

plugB = Plugboard("abcdefghijklmnopqrsz")

print(plugB.runWire('A'))

msg = "Hello There" # Change the message Here

def intToChar(int):
    if(int == 0):
        return "Z"          #26 % 26 = 0, so we might end up recieving a 0 when we have to return a "Z"
    return chr(int + 64)

def charToInt(char):        #Only meant for capital letters
    return ord(char) - 64


print(intToChar(0))
print(intToChar(13))
print(intToChar(1))
print(charToInt("A"))

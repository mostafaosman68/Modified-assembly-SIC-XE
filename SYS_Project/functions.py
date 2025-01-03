def cleanstring(line):
    x = line.strip().split(" ")
    columns = [columns for columns in x if columns != ""]
    return columns 

def cleareg(line):
    x = line.strip().split(",")
    reg = [reg for reg in x if reg != ""]
    return reg 

def getbinary(opcode):
    x = int(opcode, 16)
    y = x >> 2 
    return f"{y:06b}"

def getreg(opcode):
    x = int(opcode, 16)
    return f"{x:04b}"

def calculate_disp(pc, target_address):
   
    disp = target_address - pc
    if disp < 0:
        disp = (1 << 12) + disp  
    
    return f"{disp:03x}"

def convertbintohex(str):
    print(str)
    x=int(str,2)
    return  f"{x:03x}"


def getbase(lines, symtab):
    for line in lines:
        tokens = cleanstring(line)
        if tokens[1].lower() == 'base':
            return int(symtab[tokens[2]]["address"], 16)
    return 0

def convertdectohexa(x):
    y=int(x)
    return f"{y:03x}"


def no_Object(line):
    x=["base","ltorg","start","end","resw","resb"]
    for s in x:
        if s in line.lower():
            return  True
    return False


def pad_to_six_chars(input_string):

    return input_string + 'X' * (6 - len(input_string)) if len(input_string) < 6 else input_string
import functions as F
Instructions = {
    "FIX": {"opcode": 'C4', "format": 1},
    "FLOAT": {"opcode": 'C0', "format": 1},
    "HIO": {"opcode": 'F4', "format": 1},
    "NORM": {"opcode": 'C8', "format": 1},
    "SIO": {"opcode": 'F0', "format": 1},
    "TIO": {"opcode": 'F8', "format": 1},
    "ADDR": {"opcode": '90', "format": 2},
    "CLEAR": {"opcode": 'B4', "format": 2},
    "COMPR": {"opcode": 'A0', "format": 2},
    "DIVR": {"opcode": '9C', "format": 2},
    "DIVF": {"opcode": '64', "format": 3},
    "MULR": {"opcode": '98', "format": 2},
    "RMO": {"opcode": 'AC', "format": 2},
    "SHIFTL": {"opcode": 'A4', "format": 2},
    "SHIFTR": {"opcode": 'A8', "format": 2},
    "SUBR": {"opcode": '94', "format": 2},
    "SVC": {"opcode": 'B0', "format": 2},
    "TIXR": {"opcode": 'B8', "format": 2},
    "ADD": {"opcode": '18', "format": 3},
    "ADDF": {"opcode": '58', "format": 3},
    "AND": {"opcode": '40', "format": 3},
    "COMP": {"opcode": '28', "format": 3},
    "DIV": {"opcode": '24', "format": 3},
    "J": {"opcode": '3C', "format": 3},
    "JEQ": {"opcode": '30', "format": 3},
    "JGT": {"opcode": '34', "format": 3},
    "JLT": {"opcode": '38', "format": 3},
    "JSUB": {"opcode": '48', "format": 3},
    "LDA": {"opcode": '00', "format": 3},
    "LDB": {"opcode": '68', "format": 3},
    "LDCH": {"opcode": '50', "format": 3},
    "LDF": {"opcode": '70', "format": 3},
    "LDL": {"opcode": '08', "format": 3},
    "LDS": {"opcode": '6C', "format": 3},
    "LDT": {"opcode": '74', "format": 3},
    "LDX": {"opcode": '04', "format": 3},
    "LPS": {"opcode": 'D0', "format": 3},
    "MUL": {"opcode": '20', "format": 3},
    "MULF": {"opcode": '60', "format": 3},
    "SSK": {"opcode": 'EC', "format": 3},
    "OR": {"opcode": '44', "format": 3},
    "RD": {"opcode": 'D8', "format": 3},
    "RSUB": {"opcode": '4C', "format": 3},
    "STA": {"opcode": '0C', "format": 3},
    "STB": {"opcode": '78', "format": 3},
    "STCH": {"opcode": '54', "format": 3},
    "STF": {"opcode": '80', "format": 3},
    "STI": {"opcode": 'D4', "format": 3},
    "STS": {"opcode": '7C', "format": 3},
    "STSW": {"opcode": 'E8', "format": 3},
    "STT": {"opcode": '84', "format": 3},
    "STL": {"opcode": '14', "format": 3},
    "STX": {"opcode": '10', "format": 3},
    "SUB": {"opcode": '1C', "format": 3},
    "SUBF": {"opcode": '5C', "format": 3},
    "TD": {"opcode": 'E0', "format": 3},
    "TIX": {"opcode": '2C', "format": 3},
    "WD": {"opcode": 'DC', "format": 3},  
    "CADD": {"opcode": 'BC', "format": 4}, #  new format 4f
    "CSUB": {"opcode": '8C', "format": 4}, #  new format 4f
    "CLOAD": {"opcode": 'E4', "format": 4}, #  new format 4f
    "CSTORE": {"opcode": 'FC', "format": 4}, #  new format 4f
    "CJUMP": {"opcode": 'CC', "format": 4}  # new format 4f
}
registers={ "A": '0', "X": '1', "L": '2', "B": '3' , "S": '4', "T": '5', "F": '6' }
SymbolTable = {}
LITable = {}
Blocks = {"Default": {"start": 0, "location_counter": 0, "length": 0}}
blockname = ["DEFAULT", "DEFAULTB", "CDATA", "CBLKS"]

start_address = 0
progname = ""
proglength = 0 
error = False




def pass1(): 
    code = open("code.txt", 'r')
    pass1 = open("outpass1.txt",'w')
    symb = open("symbolTable.txt",'w')
    lines = code.readlines()
    block = "Default"
    global start_address  #NEW
    global progname  #NEW
    global proglength  #NEW 
    global error
    for line in lines:
        if line.strip().startswith("."):
            continue
        columns = F.cleanstring(line)
        # location_counter = Blocks[block]["location_counter"]
        if len(columns) == 3: 
            inst = columns[1] 
            Label = columns[2] 
            if columns[1].lower() == "start": 
                start_address = int(columns[2], 16) 
                progname = columns[0] 
                location_counter = int(columns[2], 16) 
                Blocks["Default"]["start"] = location_counter 
                Blocks["Default"]["location_counter"] = location_counter 
                pass1.write(f"{location_counter:04x}" + " " + line.strip() + "\n")  #NEW 
                continue
            SymbolTable[columns[0]] = {"block": block, "address": hex(location_counter)} # NEW 
        elif len(columns) == 2:
            inst = columns[0]
            Label = columns[1]
            if inst.lower() == "use":
                block = Label
                if block not in blockname:
                    print("block "+block+" is not defined")
                    error=True
                    break
        elif len(columns) == 1:
            inst = columns[0]
            if inst.lower() == "use":
                block = "Default"
        if Blocks.get(block) is None:
            Blocks[block] = {"start": start_address, "location_counter": start_address, "length": 0}
        location_counter = Blocks[block]["location_counter"]
        pass1.write(f"{location_counter:04x}".upper() + " " + line.strip() + "\n")
        if Label.lower().startswith("=x"):
            LITable[Label] = {"address": None, "length": (len(Label) - 4) // 2, "value": Label[3:-1],"block":block}
        elif Label.lower().startswith("=c"):
            lc = Label[3:-1]
            lit_hexa = ""
            for ch in lc:
                lit_hexa += f"{ord(ch):02x}"
                LITable[Label] = {"address": None, "length": (len(Label) - 4), "value": lit_hexa,"block":block}

        if inst.startswith("+"):  
            location_counter += 4
        elif Instructions.get(inst) != None:
            location_counter += Instructions[inst]["format"]
        elif inst.lower() == "word":  
            location_counter += 3
        elif inst.lower() == "byte":
            if len(columns) > 2:  
                Label = columns[2]
                if Label.startswith("X"):  
                    location_counter += (len(Label) - 3) // 2  
                elif Label.startswith("C"):  
                    location_counter += (len(Label) - 3)  
        elif inst.lower() == "resw":  
                location_counter += int(columns[2]) * 3
        elif inst.lower() == "resb":  
                location_counter += int(columns[2]) 
        elif inst.lower() == "end" or inst.lower() == "ltorg":
            for lc in LITable:
                if LITable[lc]["address"] == None:
                    LITable[lc]["address"] = location_counter
                    LITable[lc]["block"]=block

                    pass1.write(f"{location_counter:04x}".upper()+ " * " + lc + "\n")
                    location_counter = location_counter + LITable[lc]["length"]
        Blocks[block]["location_counter"] = location_counter
    if not error:
        for b in Blocks:
            Blocks[b]["length"] = Blocks[b]["location_counter"] - Blocks[b]["start"]
        addressdef = start_address
        length = Blocks["Default"]["length"]
        for b in Blocks: 
            proglength += Blocks[b]["length"]
            if b != "Default":
                Blocks[b]["start"] = addressdef + length
                addressdef = addressdef + length
                length = Blocks[b]["length"]
    pass1.close()
    symb.close()
    

def SsymbolTable():
    symb=open("symbolTable.txt","w")
    for sym in SymbolTable:
        address=int(SymbolTable[sym]["address"],16)
        address=address-start_address+Blocks[SymbolTable[sym]["block"]]["start"]
        symb.write(sym+" "+f"{address:04x}\n".upper())
    for lit in LITable:
        address=LITable[lit]["address"]
        address=address-start_address+Blocks[LITable[lit]["block"]]["start"]
        symb.write(lit+" "+f"{address:04x}\n".upper())
    symb.close()



def pass2():
    global error
    if error:
        return
    pass1 = open("outpass1.txt", 'r')
    pass2 = open("outpass2.txt",'w')
    lines = pass1.readlines()
    block = "Default"

    for line in lines:
        objectcode = ""
        columns = F.cleanstring(line)

        if len(columns) == 4:
            inst = columns[2]
            Label = columns[3]  # LOOP ADDR A,X
            if columns[2].lower() == "start":  # No object code
                pass2.write(f"{line.strip()}\n")
                continue
        elif len(columns) == 3:
            inst = columns[1]
            Label = columns[2]  
            if inst.lower() == "use":
                block = Label
            
        elif len(columns) == 2:
            inst = columns[1]
            if inst.lower() == "use":
                block = "Default"
                
        elif len(columns) == 1:
            inst = columns[0]
                
        if inst.startswith("+"):  # fomrat 4 opcode 
            opcode = Instructions[inst[1:]]["opcode"]
        
            
        if Instructions.get(inst) != None:
            format = Instructions[inst]["format"]
            opcode = Instructions[inst]["opcode"]
            
            if format == 1:
                objectcode = opcode
                
            elif format == 2:
                objectcode += opcode
                registers_str = Label.split(",")  #regs=['A','x']
                if len(registers_str) == 1:
                    objectcode += registers[registers_str[0]] + '0'
                    
                if len(registers_str) > 1:
                    objectcode += registers[registers_str[0]]
                    objectcode += registers[registers_str[1]]
                   
            elif format == 3:
                n, i, x, b, p, e = '1', '1', '0', '0', '0', '0'
                if inst.lower() == 'rsub':
                    objectcode = '4F0000'   # rsub always 4F0000 in sic/xe
                    pass2.write(f"{line.strip()} {objectcode}\n")
                    continue 
                if Label.startswith("@"):  #indirect
                    n='1' 
                    i = '0'
                elif Label.startswith("#"): #immed
                    i ='1'
                    n = '0'
    
                if Label.lower().endswith(",x"):  #index
                    Label=Label[:-2]
                    x='1'
                else:
                    x='0'
                    
                opcode_bin=F.getbinary(opcode) # convert opcode bin 6 bits
                
                if Label.startswith("="):  
                    target = LITable[Label]["address"]
                    target = target - start_address + Blocks[LITable[Label]["block"]]["start"]
                    pc = int(columns[0], 16) + 3
                    pc = pc - start_address + Blocks[block]["start"]
                    disp = target - pc
                    if disp >= -2048 and disp <= 2047:
                        b = '0'
                        p = '1'
                        disp = F.calculate_disp(pc, target)
                    else:
                        b = '1'
                        p = '0'
                        base = F.getbase(lines, SymbolTable)
                        base = base - start_address + Blocks[block]["start"]
                        disp = F.calculate_disp(base, target)
                    opcode_bin = opcode_bin + n + i + x + b + p + e
                    opcode_hexa = F.convertbintohex(opcode_bin)
                    objectcode = opcode_hexa + disp
                    
                if Label.startswith("#") or Label.startswith("@"):  # '#' and '@' doesnt affect object code
                    Label=Label[1:]
                    if Label.isdigit(): #if lable is number
                        disp = Label
                        disp=F.convertdectohexa(Label)
                        opcode_bin = opcode_bin + n + i + x + b + p + e
                        opcode_hexa = F.convertbintohex(opcode_bin)
                        objectcode = opcode_hexa + disp
                        pass2.write(line.strip() + " " + objectcode.upper() + "\n")
                        continue
                pc=int(columns[0],16)+3
                pc = pc - start_address + Blocks[block]["start"]
                if SymbolTable.get(Label) != None:
                    target = int(SymbolTable[Label]["address"], 16)
                    target = target - start_address + Blocks[SymbolTable[Label]["block"]]["start"]
                    disp=target-pc
                    if disp>=-2048 and disp<=2047: #check if pc relative        
                            b='0'
                            p='1'
                            disp = F.calculate_disp(pc, target)
                    else:
                            b='1'
                            p='0'
                            base=F.getbase(lines,SymbolTable)
                            disp = F.calculate_disp(base, target)

                    opcode_bin = opcode_bin + n + i + x + b + p + e
                    opcode_hexa= F.convertbintohex(opcode_bin)
                    objectcode=opcode_hexa+disp
                else:
                    if not Label.startswith("="):
                        print("Error Label "+Label+" is not defined")
                        error=True
                        break
                    
            elif format == 4:  # format 4f
                
                    registers_str1 = F.cleareg(Label) 

                    
                    if len(registers_str1) == 3 and registers_str1[0] in registers:
                        hamo = registers[registers_str1[0]]
                        hamo_bin = F.getreg(hamo)
                        
                        if registers_str1[2] == "Z" :  
                            condition_flag = "00" 
                        elif registers_str1[2] == "N" :  
                            condition_flag = "01"  
                        elif registers_str1[2] == "C" :  
                            condition_flag = "10"  
                        elif registers_str1[2] == "V" :  
                            condition_flag = "11" 
                        target = int(SymbolTable[registers_str1[1]]["address"], 16)
                        target = target - start_address + Blocks[SymbolTable[registers_str1[1]]["block"]]["start"]
                    elif len(registers_str1) == 2:
                        hamo_bin = "0000"
                        if registers_str1[1] == "Z" :  
                            condition_flag = "00" 
                        elif registers_str1[1] == "N" :  
                            condition_flag = "01" 
                        elif registers_str1[1] == "C" :  
                            condition_flag = "10"  
                        elif registers_str1[1] == "V" :  
                            condition_flag = "11"  
                        target = int(SymbolTable[registers_str1[0]]["address"], 16)
                        target = target - start_address + Blocks[SymbolTable[registers_str1[0]]["block"]]["start"]
                    opcode_bin=F.getbinary(opcode)
                    opcode_bin = opcode_bin + hamo_bin + condition_flag
                    opcode_hexa= F.convertbintohex(opcode_bin)
                    target_hex = f"{target:05X}"  

                   
                    objectcode = opcode_hexa + target_hex
                    
                     
        elif inst.startswith("+"):   # format 4
            n, i, x, b, p, e  = '0', '0', '0', '0', '0', '1'
            if Label.startswith("@"): #indirect
                n = '1'
            elif Label.startswith("#"): #imm
                i = '1'
            else:
                n, i = '1', '1'
            if Label.lower().endswith(",x"):
                Label = Label[:-2]
                x = '1'
            else:
                x = '0'
            opcode_bin = F.getbinary(opcode)

            opcode_bin = opcode_bin + n + i + x + b + p + e

            if Label.startswith("#") or Label.startswith("@"):
                Label=Label[1:]  # take the label without the # or @
                if SymbolTable.get(Label) is None:
                    print("Error Label "+Label+  "is not defined")
                    error=True
                    break
                
            opcode_hexa = F.convertbintohex(opcode_bin)
            target = int(SymbolTable[Label]["address"], 16)

            target = target - start_address + Blocks[SymbolTable[Label]["block"]]["start"]
            target_hex=f"{target:05x}"   # address of format 4 is in 5 bit 

            objectcode = opcode_hexa + target_hex
        else:
            if inst.lower() == "*":
                objectcode=LITable[Label]["value"]
            elif inst.lower() == "word":
                objectcode = f"{int(Label):06X}"            
            elif inst.lower() == "byte":
                if Label.startswith("C'") and Label.endswith("'"):
                    chars = Label[2:-1]  
                    ascii = [ord(c) for c in chars]  
                    objectcode = (''.join(f"{code:02X}" for code in ascii))  
                elif Label.startswith("X'") and Label.endswith("'"):
                    hex_value = Label[2:-1] 
                    objectcode = hex_value.upper() 
        if objectcode:
            pass2.write(f"{line.strip()} {objectcode.upper()}\n")
        else:
            pass2.write(line)
    pass2.close()
    

    
def generate_htme_records():
    if error:
        return

    t_records = []
    m_records = []
    current_t_start = None
    current_t_object_code = ""
    current_t_size = 0
    current_block_start = 0  

    with open("outpass2.txt", "r") as pass2:
        for line in pass2:
            line = line.strip()

            
            if not line or F.no_Object(line):
                continue

            
            columns = F.cleanstring(line)
            

            if len(columns) < 2:  
                print(f"Skipping malformed line: {line}")
                continue

            
            if "use" in line.lower():
                if len(columns) == 3:  
                    block_name = columns[2]
                    
                    current_block_start = Blocks.get(block_name, {}).get("start", 0)
                else:
                    current_block_start = 0  

                
                if current_t_object_code:
                    t_records.append(
                        f"T {current_t_start:06X}{len(current_t_object_code) // 2:02X}{current_t_object_code}"
                    )
                
                current_t_start = None
                current_t_object_code = ""
                current_t_size = 0
                continue

           
            try:
                address = int(columns[0], 16)  
            except ValueError:
                print(f"Invalid hexadecimal value in line: {line}")
                continue

            
            address = address - start_address + current_block_start

            
            object_code = columns[-1]
            if len(object_code) == 8:  
                m_records.append(f"M {address + 1:06X}05")

            
            if current_t_start is None:
                current_t_start = address

           
            if current_t_size + len(object_code) > 60:  
                t_records.append(
                      f"T{current_t_start:06X}{len(current_t_object_code) // 2:02X}{current_t_object_code}"
                )
                current_t_start = address
                current_t_object_code = object_code
                current_t_size = len(object_code)
            else:
                current_t_object_code += object_code
                current_t_size += len(object_code)

    
    if current_t_object_code:
        t_records.append(
            f"T {current_t_start:06X}{len(current_t_object_code) // 2:02X}{current_t_object_code}"
        )

    hamo_progname = F.pad_to_six_chars(progname)
    h_record = f"H {hamo_progname}{start_address:06X}{proglength:06X}"
    E_record = f"E {start_address:06X}"

    
    with open("HTME.txt", "w") as HTME_file:
        HTME_file.write(h_record + "\n")
        for record in t_records:
            HTME_file.write(record + "\n")
        for record in m_records:
            HTME_file.write(record + "\n")
        HTME_file.write(E_record + "\n")
        


def assemble():
    pass1()
    pass2()
    generate_htme_records()
    SsymbolTable()
    
assemble()
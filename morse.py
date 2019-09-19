morse = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g', 
         '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n',
         '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u',
         '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y', '--..': 'z', '.----': '1',
         '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
         '---..': '8', '----.': '9', '-----': '0'}

def get_char(code):
    try:
        return morse[code]
    except:
        return '@'

def attach_list(string, lst):
    ret_list = []
    for item in lst:
        if not '@' in item:
            ret_list.append(f'{string}{item}')
    return ret_list

def get_morse(code):
    if len(code) == 1:
        return [get_char(code)]
    elif len(code) == 2:
        x1 = morse[code]
        x2 = f'{get_char(code[0])}{get_char(code[1])}'
        return [x1,x2]
    elif len(code) == 3:
        x1 = get_char(code)
        x2 = f'{get_char(code[0])}{get_char(code[1:])}'
        x3 = f'{get_char(code[0])}{get_char(code[1])}{get_char(code[2])}'
        x4 = f'{get_char(code[:2])}{get_char(code[2])}'
        return [x1,x2,x3,x4]
    elif len(code) == 4:
        x1 = get_char(code)
        x2 = f'{get_char(code[0])}{get_char(code[1])}{get_char(code[2])}{get_char(code[3])}'
        x3 = f'{get_char(code[:2])}{get_char(code[2:])}'
        x4 = f'{get_char(code[0])}{get_char(code[1])}{get_char(code[2:])}'
        x5 = f'{get_char(code[0])}{get_char(code[1:3])}{get_char(code[3])}'
        x6 = f'{get_char(code[0])}{get_char(code[1:])}'
        x7 = f'{get_char(code[0:3])}{get_char(code[3])}'
        x8 = f'{get_char(code[:2])}{get_char(code[2])}{get_char(code[3])}'
        return [x1,x2,x3,x4,x5,x6,x7,x8]
    elif len(code) == 5:
        x1  = get_char(code)
        x2  = f'{get_char(code[:4])}{get_char(code[4])}'
        x3  = f'{get_char(code[0])}{get_char(code[1:])}'
        x4  = f'{get_char(code[:3])}{get_char(code[3:])}'
        x5  = f'{get_char(code[:3])}{get_char(code[3])}{get_char(code[4])}'
        x6  = f'{get_char(code[0])}{get_char(code[1:3])}{get_char(code[4])}'
        x7  = f'{get_char(code[:2])}{get_char(code[2:])}'
        x8  = f'{get_char(code[0])}{get_char(code[1])}{get_char(code[2:])}'
        x9  = f'{get_char(code[:2])}{get_char(code[2])}{get_char(code[3])}{get_char(code[4])}'
        x10 = f'{get_char(code[:2])}{get_char(code[2:4])}{get_char(code[4])}'
        x11 = f'{get_char(code[:2])}{get_char(code[2])}{get_char(code[3:])}'
        x12 = f'{get_char(code[0])}{get_char(code[1:3])}{get_char(code[3:])}'
        x13 = f'{get_char(code[0])}{get_char(code[1:3])}{get_char(code[3])}{get_char(code[4])}'
        x14 = f'{get_char(code[0])}{get_char(code[1])}{get_char(code[1:3])}{get_char(code[4])}'
        x15 = f'{get_char(code[0])}{get_char(code[1])}{get_char(code[2])}{get_char(code[3:])}'
        x16 = f'{get_char(code[0])}{get_char(code[1])}{get_char(code[2])}{get_char(code[3])}{get_char(code[4])}'
        return [x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16]
    else:
        ret_list = []
        ret_list.extend(attach_list(get_char(code[0]), get_morse(code[1:])))
        ret_list.extend(attach_list(get_char(code[:2]), get_morse(code[2:])))
        ret_list.extend(attach_list(get_char(code[:3]), get_morse(code[3:])))
        ret_list.extend(attach_list(get_char(code[:4]), get_morse(code[4:])))
        ret_list.extend(attach_list(get_char(code[:5]), get_morse(code[5:])))
        return ret_list

def main():
    # Need a function to weed out obviously bad results with this many permutations
    print(get_morse('-......-....-....'))

if __name__ == "__main__":
    main()

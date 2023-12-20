from os import listdir
from time import perf_counter


Inputs = "Sheets"
Outputs = "MachineNotes"


def where_next_non_float(string, start):  # return index of nonint #alpha+int,int
    """
    Pass in a str and where to start in that str
    Does not check at the stating index
    :return where the next non float is
    """
    i = start + 1  # skip first alpha
    if len(string) == i: return -1  # name only case
    while string[i].isdigit() or string[i] == '.' or string[i] == '-' or string[i] == '/':
        # after this, i is the index of non-interger #if digit
        if i == len(string) - 1:  # if checking last string #
            return -1
        i += 1
    return i


def where_correspond_bracket(string, start):
    pairs={'[':']','{':'}','(':')','<':'>'}
    pointer = start  # [[...]...]
    i = 1  # [ is positive, ] is negative
    while i > 0:
        pointer += 1  # skip the [
        try:
            if string[pointer] == string[start]:
                i += 1
            elif string[pointer] == pairs[string[start]]:
                i -= 1  # end when pointer at ] that reduce to 0
        except IndexError:
            return -1
    return pointer


#recursion = 0
def compiler(string) -> list[str]:  # function #1
    # global recursion
    # recursion += 1
    # if recursion > 10:
    #     raise RecursionError
    # print(recursion)
    """
    ';' - Multiplies the amount of times the letter(s) after it in 'notes'
            by the int directly after it (if no int is provided, it defaults to 2)
    '-' - Sets the amount of delay after the group directly in front of it
            by the int directly after it (if no int is provided, it defaults to 0)
    '[...]' - Makes the contained contents treated as one letter
    ',' - The group after is a stacato note
    """
    sheet = [[]]
    current_line = 0
    pointer = 0
    start = True

    def stringformat(string_part):  # [name,duration,dash,reduction]
        for i, e in enumerate(string_part):
            if e == '-':
                if string_part[1:i] == '':  # if no duration and yes '-' a-?
                    if string_part[i + 1:] == '':  # a-
                        return string_part[0] + '1-0'
                    return string_part[0] + '1' + string_part[i:]  # a-N
                elif string_part[i + 1:] == '':  # if yes duration and no reduction aN-
                    return string_part[0:i + 1] + '0'
                return string_part  # yes duration and yes reduction
        if len(string_part) == 1:
            return string_part + '1-1'  # when no - and no duration a
        else:
            return string_part[0:] + '-' + string_part[1:]  # when no- and yes duration aN

    def alpha_case():  # pointer must be at alpha
        nonlocal pointer, sheet
        next_alpha = where_next_non_float(string, pointer)
        if next_alpha == -1:
            sheet[current_line].append(stringformat(string[pointer:]))
            pointer = len(string)  # for exit
        else:
            sheet[current_line].append(stringformat(string[pointer:next_alpha]))
            pointer = next_alpha  # pointer is after the note

    while pointer < len(string):
        current_key = string[pointer]
        if current_key == '[':  # [notes]scalar
            corresponding_bracket = where_correspond_bracket(string, pointer)
            next_alpha = where_next_non_float(string, corresponding_bracket)  # end of scalar
            if next_alpha == -1:  # scalar is full
                temp = string[corresponding_bracket + 1:]
            else:
                temp = string[corresponding_bracket + 1:next_alpha]
            # scalar = 1.0 if temp == '' else ('-' if temp == '-' else eval(temp))
            if temp == '':
                scalar = 1.0
            elif temp == '-':
                scalar = '-'
            else:
                scalar = eval(temp)
            notesInBracket = compiler(string[pointer + 1: corresponding_bracket])
            for idx, note in enumerate(notesInBracket):  # for notes in the bracket
                a_duration = float(note[1:note.find('-',2)])
                a_deduction = float(note[note.find('-',2)+1:])
                if type(scalar) == float or type(scalar) == int:
                    replace_with = f'{note[0]}{a_duration * scalar}-{a_deduction * scalar}'
                elif idx == len(notesInBracket) - 1: # if last index and scalar = -
                    replace_with = f'{note[0]}{a_duration}-{a_deduction}'
                else: # scalar = -
                    a_duration = note[note.find('-',2):]
                    replace_with = f"{note[0:note.find('-',2)]}-0"
                sheet[current_line].append(replace_with)
            if next_alpha == -1:
                break
            else:
                pointer = next_alpha  # now pointer is a the character after the scalar
        elif current_key == '(':
            pointer = where_correspond_bracket(string, pointer) + 1
        elif current_key == '<':
            pointer = where_correspond_bracket(string, pointer) + 1
        elif current_key == ';':  # ;multi note , ;multi[notes]
            next_alpha = where_next_non_float(string, pointer)
            if string[pointer + 1:next_alpha].isdigit(): # find multi
                multiplier = int(string[pointer + 1:next_alpha])
            else:
                multiplier = 2  # if no number, = 2
            if string[next_alpha].isalpha():  # if case 1
                for _ in range(multiplier):  # repeat by the multiplier
                    pointer = next_alpha  # pointer = first
                    alpha_case()
            else:  # then next_alpha is [  case 2
                closing_bracket = where_correspond_bracket(string, next_alpha)
                for _ in range(multiplier):  # repeat by the multiplier
                    sheet[current_line].extend(compiler(string[next_alpha + 1:closing_bracket]))
                pointer = closing_bracket + 1
        elif current_key.isalpha() or current_key in [" ", '|']:  # note+notedata(*duration,*reduction)
            alpha_case()
        elif current_key == ',':  # ,[X-X] - >  .25X.5-X.5 .25
            ''' 
            for a note X, to ,X means to split X into 
            wait * .25, X * .5, wait * .25, maintaining total of 1
            if X comes in form Xa-b, meaning total = b, 
            wait * .25a, X * .5a should be conserved, 
            length is now .75a
            we wish it to be b, so to find the difference, we subtract .75a from b
            final wait becomes b-0.75a
            '''
            pointer += 1
            if string[pointer].isalpha():  # if ,Name
                alpha_case()
                toBeStak = sheet[current_line].pop(-1)
                duration = eval(toBeStak[1: toBeStak.find("-")])
                deduction = eval(toBeStak[toBeStak.find("-")+1:])
                deduced_from_e = duration - deduction
                sheet[current_line].append(f' {duration / 4}-{duration / 4}')  # wait
                sheet[current_line].append(f'{toBeStak[0]}{duration / 2}-{duration / 2}')  # note
                sheet[current_line].append(f' {deduction-0.75*duration}-{deduction / 4 - deduced_from_e}')  # wait
            elif string[pointer] == '[':
                pre_deduction = False # first key cannot be deducted(played asynchronously with the first key)
                for note in compiler(string[pointer + 1: where_correspond_bracket(string, pointer)]):
                    duration = eval(note[1: note.find("-")])
                    deduction = eval(note[note.find("-")+1:])
                    deduced_from_e = duration - deduction
                    if pre_deduction:
                        sheet[current_line].append(f' {duration / 4}-{0}')  # wait
                    else:
                        sheet[current_line].append(f' {duration / 4}-{duration / 4}')  # wait
                    sheet[current_line].append(f'{note[0]}{duration / 2}-{duration / 2}')  # note
                    sheet[current_line].append(f' {deduction-0.75*duration}-{duration / 4 - deduced_from_e}')  # wait
                    pre_deduction = deduction == 0
                pointer = where_correspond_bracket(string, pointer)+1
        elif current_key == "=":
            start = False
            sheet.append([])
            current_line += 1
            pointer += 1
        else:
            print(current_key,string[pointer-10:pointer+10])
            raise SyntaxError
    if start:
        return sheet[0]  # plugged in to 2nd function for the real notes which is in the test.py file
    else:
        return sheet


def main():
    # print(compiler(',[[abc]-]'))
    for file in listdir(Inputs):
        with open(Inputs + '/' + file) as input_f:
            lines = input_f.read().replace('\n', '')  # remove \n
            with open(Outputs + '/' + file, mode='w') as output_f:
                output_content = ''
                if "=" in lines:
                    for a in compiler(lines):
                        output_content += str(a) + '\n'
                else:
                    output_content = str(compiler(lines)) + '\n'
                output_f.write(output_content)
if __name__ == '__main__':
    start = perf_counter()
    main()
    print(f'Ended in {perf_counter()-start} secs.')

#print(compiler('[a-b]1/2'))

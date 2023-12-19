from os import listdir
from NoteCompiler import compiler

Inputs = 'Sheets'


def checker(check_file: list):
    """
    pass in a list of measures and this function will return which measures are incorrect
    Does syntax checking

    :note: This function will only function properly if the file it reads has each line equal to one measure
    """
    target_beats = 2
    for i, measure in enumerate(check_file):
        print(i)
        if '<' in measure:
            target_beats = int(measure[measure.find('<') + 1: measure.find('>')])
        measure.replace('=', '')
        assert target_beats is not None, f"No markers for how many beats there are in a measure in file, line {i+1}"
        #print(measure)
        assert measure.count('[') == measure.count(']'), f'Brackets extend beyond one measure, line {i+1}'
        assert measure.count('(') == measure.count(')'), f'Brackets extend beyond one measure, line {i+1}'
        notes = compiler(measure)
        beats_in_measure = 0
        for note in notes:
            if '|' in note:
                continue
            try:
                if note[0] == ' ':
                    beats_in_measure += eval(note[1:note.find('-', 2)])
                else:
                    beats_in_measure += eval(note[note.find('-', 2) + 1:])
            except Exception:
                pass
        if not (abs(beats_in_measure - target_beats) < .05 or beats_in_measure == 0):
            return f'''There {"aren't enough" if beats_in_measure < target_beats else "are too many"} beats in line {i+1}
                notes: {notes}\nbeats_in_measure:{beats_in_measure}\ntarget_beats:{target_beats}'''
    return 'All is good in this file'


file = '5.txt'
# print(checker([",[[q-e]2]"]))
with open(Inputs + '/' + file) as input_f:
    lines = input_f.read().split('\n')  # remove \n
    print(file, checker(lines))

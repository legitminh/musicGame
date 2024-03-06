"""
TODO: Get UndoTree and PieceTable working
    - UndoTree has no functionality
    - PieceTable works for insertion and backspace
"""
ORIGINAL = True
ADD = False

FILE = 0
LOCATION = 1
LENGTH = 2
PIECE_TABLE = list[tuple[bool, int, int]]

class UndoTree: 
    def __init__(self, val, *children) -> None:
        self.val = val
        self.children = list(children)
    
    def add(self, *children):
        self.children.extend(children)


class PieceTable:
    def __init__(self, original_text) -> None:
        self.original = original_text
        self.add = ""
        self.piece_table: PIECE_TABLE = [(ORIGINAL, 0, len(original_text))]
        self.root_node = UndoTree(self.piece_table)
        self.current_node = self.root_node

    def compile(self):
        return "".join([
            (self.original if piece[FILE] is ORIGINAL else self.add)
            [piece[LOCATION]: piece[LOCATION] + piece[LENGTH]] 
            for piece in self.piece_table
        ])

    def abs_to_rel(self, i):
        running_total = 0
        for piece in self.piece_table:
            running_total += piece[LENGTH]
            if running_total > i:
                return i - running_total + piece[LENGTH], piece
        raise IndexError(f"{i} is out of range, max length is {running_total}.")

    def insert(self, i, insert_text):
        p, q = self.abs_to_rel(i)
        a, b = self.split(p, q)
        
        j = len(self.add)
        self.add += insert_text
        self.piece_table.insert(p, a)
        self.piece_table.insert(p, [ADD, j, len(insert_text)])
        self.piece_table.insert(p, b)
    
    def split(self, i, piece):
        self.piece_table.remove(piece)
        
        a = (piece[FILE], piece[LOCATION], i)
        b = (piece[FILE], i, piece[LENGTH] - i)
        return a, b

    def backspace(self, i):
        p, q = self.abs_to_rel(i)
        a, b = self.split(p, q)
        a = (a[FILE], a[LOCATION], a[LENGTH] - 1)
        if a[LENGTH] == 0: 
            self.piece_table.insert(p, b)
            return
        if b[LENGTH] == 0: 
            self.piece_table.insert(p, a)
            return
        self.piece_table.insert(p, b)
        self.piece_table.insert(p, a)

    def delete(self, i):
        p, q = self.abs_to_rel(i)
        a, b = self.split(p, q)
        b = (b[FILE], b[LOCATION] + 1, b[LENGTH])
        if a[LENGTH] == 0: 
            self.piece_table.insert(p, b)
            return
        if b[LENGTH] == 0: 
            self.piece_table.insert(p, a)
            return
        self.piece_table.insert(p, b)
        self.piece_table.insert(p, a)

    def undo():
        pass

    def redo():
        pass


if __name__ == '__main__':
    test = PieceTable("0123456789")
    test.insert(5, "abc")
    print(test.piece_table)
    print(test.compile())

    test.backspace(6)
    print(test.piece_table)
    print(test.compile())

    test.delete(7)
    print(test.piece_table)
    print(test.compile())

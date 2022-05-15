import itertools
from platform import java_ver
import random


class Minesweeper():


    def __init__(self, height=8, width=8, mines=8):

        self.height = height
        self.width = width
        self.mines = set()

        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        self.mines_found = set()

    def print(self):
        
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        

        count = 0

        
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        
        return self.mines_found == self.mines


class Sentence():
   

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        
        if self.count == len(self.cells) and self.count != 0:
            return self.cells
        else:
            return set()

    def known_safes(self):
        
        if self.count == 0:
            return self.cells
        else:
            return set()


    def mark_mine(self, cell):
        
        if cell not in self.cells:
            return

        updated = set()

        for cell0 in self.cells:
            if cell0 == cell:
                continue
            updated.add(cell0)

        self.cells = updated
        if len(updated) == 0:
            self.count = 0
        else:
            self.count -= 1
        return

        
        

    def mark_safe(self, cell):
        
        
        if cell not in self.cells:
            return

        updated = set()

        for cell0 in self.cells:
            if cell0 == cell:
                continue
            updated.add(cell0)

        self.cells = updated
        return


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        
        self.moves_made.add(cell)

        self.safes.add(cell)
        
        new_cells = set()

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                    if i not in range(self.height) or j not in range(self.width):
                        continue
                    if(i,j) == cell:
                        continue
                    elif(i,j) in self.safes:
                        continue
                    elif(i,j) in self.mines:
                        count -= 1
                        continue
                    elif 0 <= self.height and 0 <= j < self.width:
                        new_cells.add((i,j))

        newSentence = Sentence(new_cells, count)
        self.knowledge.append(newSentence)
        
        for sentence in self.knowledge:
            for cell0 in sentence.cells:
                if cell0 in sentence.known_safes():
                    self.mark_safe(cell0)
                elif cell0 in sentence.known_mines():
                    self.mark_mine(cell0)

        
        updatedKnowledge = []
        for sentence0 in self.knowledge:
            for sentence1 in self.knowledge:
                if sentence0 == sentence1:
                    continue
                elif len(sentence0.cells) == 0 or len(sentence1.cells) == 0:
                    continue
                elif sentence0.count == 0 or sentence1.count == 0:
                    continue
                elif sentence0.cells.issubset(sentence1.cells):
                    updatedCells = sentence1.cells - sentence0.cells
                    updatedCount = sentence1.count - sentence0.count
                    newSentence = Sentence(updatedCells, updatedCount)
                    updatedKnowledge.append(newSentence)
                    
        for sentence in updatedKnowledge:
            self.knowledge.append(sentence)
        return

        



    def make_safe_move(self):
        
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):

        moves = []
        for i in range(self.height):
            for j in range(self.width):
                    if (i, j) not in self.moves_made:
                        if (i, j) not in self.mines:
                            moves.append((i, j))

        random.shuffle(moves)
        if 0 < len(moves):
            return moves[0]

        return None


from interface import Interface
from solver import Solver

with open('words.txt') as f:
    word_list = [line.strip() for line in f.readlines()]

interface = Interface(len(word_list[0]))
solver = Solver(word_list)
interface.gather()
print(solver.possible_answers(*interface.report()))
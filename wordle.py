import string

class Wordle:
    def __init__(self, word_list, alphabet=string.ascii_lowercase):
        self.master_word_list = set(word_list)
        self.word_length = len(word_list[0])
        self.alphabet = alphabet

    def transition(self, state, letter, index):
        new_state = state[:]
        new_state[index] = letter
        return new_state

    def successors(self, state, available_letters):
        if None not in state:
            return []

        slot_to_fill = state.index(None)
        for letter in available_letters:
            yield self.transition(state, letter, slot_to_fill)

    def is_valid(self, state, warm_letters):
        return warm_letters.issubset(set(state))

    def is_terminal(self, state):
        return all(state)

    def search(self, initial_state, warm_letters, cold_letters):
        possible_words = set()
        available_letters = set(self.alphabet) - cold_letters
        frontier = [initial_state]
        while frontier:
            current = frontier.pop(0)
            for state in self.successors(current, available_letters):
                if self.is_terminal(state):
                    if self.is_valid(state, warm_letters):
                        possible_words.add(''.join(state))
                else:
                    frontier.append(state)
        return possible_words

    def possible_answers(self, initial_state, warm_letters, cold_letters):
        search_results = self.search(initial_state, warm_letters, cold_letters)
        return search_results & self.master_word_list

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', help='Known letter positions: use an underscore (_) for unknown positions; e.g. "a__le"', type=str, default=[None] * 5)
    parser.add_argument('-w', help='Warm letters: letters that are in the word in some position; e.g. "sre"', type=str, default=set())
    parser.add_argument('-c', help='Cold letters: letters that are not in the word; pass a a string; e.g. "xqju"', type=str, default=set())
    args = parser.parse_args()
    initial_state = [char if char != '_' else None for char in args.k]
    warm_letters = set(list(args.w))
    cold_letters = set(list(args.c))
    with open('words.txt') as f:
        word_list = [line.strip() for line in f.readlines()]
    wordle = Wordle(word_list)
    print(wordle.possible_answers(initial_state, warm_letters, cold_letters))

import string

class Solver:
    def __init__(self, word_list, alphabet=string.ascii_lowercase):
        self.master_word_list = set(word_list)
        self.word_length = len(word_list[0])
        self.alphabet = alphabet

    def available_letters(self, warm_letters, cold_letters):
        all_available_letters = set(self.alphabet) - cold_letters
        letters_by_slot = [all_available_letters.copy() for _ in range(self.word_length)]
        for i, to_remove_from_slot in enumerate(warm_letters):
            if to_remove_from_slot:
                letters_by_slot[i] -= to_remove_from_slot
        return letters_by_slot

    def transition(self, state, letter, index):
        new_state = state[:]
        new_state[index] = letter
        return new_state

    def successors(self, state, available_letters):
        if None not in state:
            return []

        slot_to_fill = state.index(None)
        for letter in available_letters[slot_to_fill]:
            yield self.transition(state, letter, slot_to_fill)

    def is_valid(self, state, warm_letters):
        all_warm_letters = set().union(*warm_letters)
        return all_warm_letters.issubset(set(state))

    def is_terminal(self, state):
        return all(state)

    def search(self, initial_state, warm_letters, cold_letters):
        possible_words = set()
        available_letters = self.available_letters(warm_letters, cold_letters)
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

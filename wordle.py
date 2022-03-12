import string

class Wordle:
    def __init__(word_list):
        self.master_word_list = set(word_list)
        self.word_length = len(word_list[0])

    def transition(state, letter):
        pass

    def successors(state, available_letters):
        pass

    def is_valid(state, required_letters):
        pass

    def is_terminal(state):
        pass

    def search(initial_state, warm_letters, cold_letters):
        possible_words = set()
        available_letters = set(string.ascii_lowercase) - cold_letters
        frontier = [initial_state]
        while frontier:
            current = frontier.pop(0)
            for state in self.successors(current, available_letters):
                if self.is_terminal(state)
                    if self.is_valid(state, warm_letters):
                        possible_words.add(''.join(state))
                else:
                    frontier.append(state)
        return possible_words & self.master_word_list
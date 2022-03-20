import string

class Interface:
    def __init__(self, word_length):
        self.word_length = word_length
        self.known = [None] * word_length
        self.warm = [set() for _ in range(word_length)]
        self.cold = set()

    def gather(self):
        guess = 'initial'
        while guess:
            guess = self.take_guess()
            if guess:
                results = self.take_results()
                self.interpret(guess, results)

    def report(self):
        return self.known, self.warm, self.cold

    def is_valid(self, input, valid_chars=string.ascii_lowercase):
        return len(input) == self.word_length and all([char in valid_chars for char in input])

    def take_guess(self):
        done = False
        while not done:
            guess = input(f'Enter your {self.word_length}-letter guess word, or "D" to quit.\n').lower()
            done = guess == 'd' or self.is_valid(guess)
        return guess if guess != 'd' else None

    def take_results(self):
        done = False
        while not done:
            results = input(f'Enter your {self.word_length}-letter results: "K" for known, "W" for warm, or "C" for cold.\n').lower()
            done = self.is_valid(results, 'kwc')
        return results

    def interpret(self, guess, results):
        for i, (r, g) in enumerate(zip(results, guess)):
            if r == 'k':
                self.known[i] = g
            elif r == 'w':
                self.warm[i].add(g)
            elif r == 'c':
                self.cold.add(g)
            else:
                raise Exception(f'Invalid result token recieved: {r}')

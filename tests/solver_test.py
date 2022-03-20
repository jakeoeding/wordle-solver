import pytest
from wordle_solver.solver import Solver

@pytest.fixture()
def solver():
    word_list = ['abc', 'cde', 'def']
    return Solver(word_list, alphabet='abcdef')

class TestBase:
    @pytest.fixture(autouse=True)
    def _solver(self, solver):
        self.solver = solver

class TestAvailableLetters(TestBase):
    def test_without_restrictions(self):
        warm_letters = [set(), set(), set()]
        available_letters = self.solver.available_letters(warm_letters, set())
        for position in available_letters:
            assert sorted(position) == list('abcdef')

    def test_with_warm_letters(self):
        warm_letters = [{'a', 'b'}, {'c'}, set()]
        available_letters = self.solver.available_letters(warm_letters, set())
        assert sorted(available_letters[0]) == list('cdef')
        assert sorted(available_letters[1]) == list('abdef')
        assert sorted(available_letters[2]) == list('abcdef')

    def test_with_cold_letters(self):
        warm_letters = [set(), set(), set()]
        cold_letters = {'a', 'b'}
        available_letters = self.solver.available_letters(warm_letters, cold_letters)
        for position in available_letters:
            assert sorted(position) == list('cdef')

    def test_with_warm_and_cold_letters(self):
        warm_letters = [{'b'}, set(), {'d'}]
        cold_letters = {'a'}
        available_letters = self.solver.available_letters(warm_letters, cold_letters)
        assert sorted(available_letters[0]) == list('cdef')
        assert sorted(available_letters[1]) == list('bcdef')
        assert sorted(available_letters[2]) == list('bcef')

class TestTransition(TestBase):
    def test_updates_value(self):
        state = ['a', 'b', None]
        new_state = self.solver.transition(state, 'c', 2)
        assert ''.join(new_state) == 'abc'

    def test_maintains_original(self):
        state = [None]
        new_state = self.solver.transition(state, 'a', 0)
        assert state[0] is None

class TestSuccesors(TestBase):
    def test_terminal_state(self):
        terminal_state = ['a', 'b', 'c']
        available_letters = [{'d'}] * 3
        successors = self.solver.successors(terminal_state, available_letters)
        assert len(list(successors)) == 0

    def test_nonterminal_state(self):
        state = ['a', None]
        available_letters = [{'b', 'c', 'd'}] * 2
        successors = self.solver.successors(state, available_letters)
        assert sorted(successors) == [['a', 'b'], ['a', 'c'], ['a', 'd']]

class TestIsValid(TestBase):
    def test_valid_state_no_requirements(self):
        state = ['a', 'b', 'c']
        warm_letters = [set(), set(), set()]
        is_valid = self.solver.is_valid(state, warm_letters)
        assert is_valid

    def test_valid_state_with_requirements(self):
        state = ['a', 'b', 'c']
        warm_letters = [set(), {'c'}, {'a'}]
        is_valid = self.solver.is_valid(state, warm_letters)
        assert is_valid

    def test_invalid_state_with_requirements(self):
        state = ['a', 'b', 'c']
        warm_letters = [{'d'}, set(), set()]
        is_valid = self.solver.is_valid(state, warm_letters)
        assert not is_valid

class TestIsTerminal(TestBase):
    def test_terminal_state(self):
        state = ['a', 'b', 'c']
        is_terminal = self.solver.is_terminal(state)
        assert is_terminal

    def test_nonterminal_state(self):
        state = ['a', 'b', None]
        is_terminal = self.solver.is_terminal(state)
        assert not is_terminal

class TestSearch(TestBase):
    def test_no_starting_info(self):
        initial_state = [None] * 3
        warm_letters = [set(), set(), set()]
        possible_words = self.solver.search(initial_state, warm_letters, set())
        assert len(possible_words) == len(self.solver.alphabet) ** self.solver.word_length

    def test_with_cold_letters(self):
        initial_state = ['a', 'b', None]
        warm_letters = [set(), set(), set()]
        cold_letters = {'e', 'f'}
        possible_words = self.solver.search(initial_state, warm_letters, cold_letters)
        assert sorted(possible_words) == ['aba', 'abb', 'abc', 'abd']

    def test_with_warm_and_cold_letters(self):
        initial_state = ['a', 'b', None]
        warm_letters = [{'c'}, set(), set()]
        cold_letters = {'e', 'f'}
        possible_words = self.solver.search(initial_state, warm_letters, cold_letters)
        assert sorted(possible_words) == ['abc']

class TestPossibleAnswers(TestBase):
    def test_no_starting_info(self):
        initial_state = [None] * 3
        warm_letters = [set(), set(), set()]
        possible_answers = self.solver.possible_answers(initial_state, warm_letters, set())
        assert sorted(possible_answers) == sorted(self.solver.master_word_list)

    def test_with_starting_info(self):
        initial_state = ['a', 'b', None]
        warm_letters = [{'c'}, set(), set()]
        cold_letters = {'e', 'f'}
        possible_answers = self.solver.possible_answers(initial_state, warm_letters, cold_letters)
        assert sorted(possible_answers) == ['abc']
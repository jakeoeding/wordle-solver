# Wordle Solver
Command line solver for the game [Wordle](https://www.nytimes.com/games/wordle/index.html)

Uses the official NY Times answer list provided by [cfreshman](https://gist.github.com/cfreshman/a7b776506c73284511034e63af1017ee)

## Approach
The underlying mechanism of this solver is a state space search. In particular, I'm utilizing what is essentially a breadth first search.

We examine every possible state in the space of 5 English letter combinations in the worst case, i.e. 26^5 ≈ 12 million states. That is a pretty large number and is definitely not efficient. As a result, this tool is not going to be the most optimal solver.

However, after a single round or two of the game, enough information is typically gained (by fixing 1+ positions and/or reducing the branching factor) to reduce the search space by 98+%. This means the tool is "good enough", and the possible answers to the day's puzzle can be reduced to just a few words or less.

## Usage
Clone the repository. Navigate to the root directory. Run the following command to start the program:

`python3 wordle_solver`

You will be prompted to enter a guess, followed by the results from the guess using the following rules:
- Enter `k` (as in `known`) for the letters that are correct, i.e. 'green'
- Enter `w` (as in `warm`) for the letters that are in the answer, but in the wrong position, i.e. 'yellow'
- Enter `c` (as in `cold`) for the letters that are not in the answer, i.e. 'gray'

Repeat for as many guesses as you wish to enter.

The program will spit out the answer, or the potential answers if there are multiple given the current information.

## License
MIT

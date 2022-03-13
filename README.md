# Wordle Solver
Command line solver for the game [Wordle](https://www.nytimes.com/games/wordle/index.html)

Uses the official NY Times answer list provided by [cfreshman](https://gist.github.com/cfreshman/a7b776506c73284511034e63af1017ee)

## Approach
The underlying mechanism of this solver is a state space search. In particular, I'm utilizing what is essentially a breadth first search.

We examine every possible state in the space of 5 English letter combinations in the worst case, i.e. 26^5 ≈ 12 million states. That is a pretty large number and is definitely not efficient. As a result, this tool is not going to be the most optimal solver.

However, after a single round or two of the game, enough information is typically gained (by fixing 1+ positions and/or reducing the branching factor) to reduce the search space by 98+%. This means the tool is "good enough", and the possible answers to the day's puzzle can be reduced to just a few words or less.

## Usage
There are a few different arguments for the CLI. All are optional.

`-h` : provides help information on usage

`-k` : use this flag before passing in the known letters in the proper positions; fill in unknown positions with underscores (_)

`-w` : use this flag before passing in warm letters, i.e. letters you know are in the word, but the proper position is unkown

`-c` : use this flag before passing in cold letters, i.e. letters you know are NOT in the word

### Example Usage:
- I know the word starts with the letter `f`
- I know the word contains a `c` and an `o`, but I don't know the correct positions
- I know the word does not contain any of the following letters: `r, a, t, e, l, k`

Then I should run the program with the following command:

`python3 wordle.py -k f____ -w co -c ratelk`

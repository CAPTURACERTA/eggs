# movement
1. pieces can only move orthogonally (vertically and horizontally) 
2. pieces from the same group connected orthogonally can make chain moves. E.g.: the white pieces, in the first move, can go from a1 to e2:

(pretend that "◯" means an empty square)
6 [⚫,⚫,⚫,⚫,⚫]
5 [◯,◯,◯,◯,◯]
4 [◯,◯,◯,◯,◯]
3 [◯,◯,◯,◯,◯]
2 [◯,◯,◯,◯,⚪]
1 [◯,⚪,⚪,⚪,⚪]
    a, b, c, d, e

# capture
- Captures are mandatory, the highest capure being the "current mandatory move"
- You capture an egg by jumping over them, like in checkers, but orthogonally

# winning
You win a match on 3 different ways:
- By placing one of your eggs in the last row (enemy's initial row) stably. I.e.: Arriving the las row without immediately being able to capture or be captured. That's the main way of winning.
- By capturing all enemy's eggs. Rare, honestly.
- By "stalemating" your enemie. That is: your enemie doesn't have any legal moves left. Extremely rare.

# drawing
You draw a match by offering a draw or by repeting moves. 

# board
There's only one board of eggs, currently. The 5x6, which seems, to me, pretty "solved". After tests, I intend to try a bigger board with 2 rows of eggs to each player, like checkers, for more complexity.
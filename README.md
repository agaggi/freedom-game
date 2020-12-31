# Freedom Game (vs. Minimax Algorithm)

## Program Requirements

- Python 3.7 or newer
- The **NumPy** pip package

To install NumPy:

```bash
# Linux
pip3 install numpy

# Windows
pip install numpy
```

## Compilation and Execution

The `main.py` file is the file specified to be run; attempting to run any other file will result in no output. The program should be run following this format:

```bash
# Linux
python3 main.py [difficulty]

# Windows
py .\main.py [difficulty]
```

### Arguments

| Argument       | Board Dimensions | 
| :------------: | :--------------: | 
| `beginner`     | 6x6              | 
| `novice`       | 8x8              | 
| `experienced`  | 10x10            |

### Entering stone coordinates

The following board shows how stones should be placed on the board. When it is your turn, you will be prompted to enter coordinates, the **x**-coordinate followed by the **y**-coordinate. Your input will be checked whether it is valid. If not, you will be prompted to re-enter.

Further rules and explanation can be found [here](https://boardgamegeek.com/boardgame/100480/freedom).

```
  0 1 2 3 4 5 6 7 8 9
0 * * * * * * * * * *
1 * * * * * * * * * *
2 * * * * * * * * * *
3 * * * * * * * * * *
4 * * * * * * * * * *
5 * * * * * * * * * *
6 * * * * * * * * * *
7 * * * * * * * * * *
8 * * * * * * * * * *
9 * * * * * * * * * *
```

## Analysis

After completion of the minimax function, I tested the board with various conditions. The first condition I tested was the `beginner` board with the minimax function checking **3** moves ahead. While playing the game I observed that the AI was making smart moves, such as going for points, or reducing my points by forcing me to place 5 stone in a row. It was still relatively easy to beat the program, but if you made a bad move, you were punished.

I then set the number of moves minimax would look ahead to **6**. I first played the `beginner` board and I was able to win sometimes. I believe where you start makes an impact, but the AI was much more aware this time. I then tested the `novice` and `experienced` boards, and I was not able to win. It was difficult for me to get points, besides the initial move going diagonal.
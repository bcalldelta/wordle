# Command Line Wordle
# By @bcalldelta on GitHub (bettercalldelta@gmail.com), 24.09.2022
from random import choice
from os.path import exists

if not exists('.wordlestats'):
    open('.wordlestats', 'w').write('0:0:0:0:0:0:0:0:0')

atts = 0
barwidth = 40

answers, guesses = open('data.txt').read().split('\n')

answers = [answers[i:i+5] for i in range(0, len(answers), 5)]
guesses = [guesses[i:i+5] for i in range(0, len(guesses), 5)]
answer = choice(answers)

colors = ["\x1b[30;102m", "\x1b[30;103m", "\x1b[0m"]
bar_colors = ["\x1b[1;42m", "\x1b[1;102m"]

clear_prev = "\x1b[A\r\x1b[2K"
clear_color = "\x1b[0m"

bar_new = "|  "
bar_entered = "\x1b[1;32m|\x1b[0m  "
bar_error = "\x1b[1;31m|\x1b[0m  "

def diff(word2):
    """Get the colors :: 2 - gray, 1 - yellow, 0 - green"""
    result = [2, 2, 2, 2, 2]
    word1 = list(answer)

    # Check for exact matches
    for i in range(5):
        if word2[i] == word1[i]:
            result[i] = 0
            word1[i] = ' '

    # Check for correct letters
    for i in range(5):
        if word2[i] in word1 and result[i] == 2:
            result[i] = 1
            word1.remove(word2[i])

    return result


print("\n   \x1b[1mWordle\x1b[0m\n\n", end='')
word_valid = True

for _ in range(6): print('|')
print("\x1b[6A\r", end='')

while True:
    bar = (bar_error, bar_new)[word_valid]
    guess = input(bar).lower()
    word_valid = False
    print(clear_prev, end='')

    if guess == answer:
        break

    if guess in (guesses + answers):
        word_valid = True
        print(bar_entered, end='')
        d = diff(guess)
        for i in range(5):
            print(colors[d[i]] + guess[i].upper(), end='')
        print(clear_color)

        atts += 1
        if atts == 6:
            break

raw_data = open('.wordlestats').read()
data = [int(i) for i in raw_data.split(':')]
data[atts] += (guess == answer)
data[6] += 1

msg = [f"\n   \x1b[1;31mUnfortunately, you didn't guess the word '{answer}'. Good luck next time!",
       f"\n   \x1b[1;32mCongratulations, you guessed the word '{answer}' in {atts+1} tries!"]

if guess == answer:
    data[7] += 1
else:
    data[7] = 0
data[8] = max(data[7], data[8])

open('.wordlestats', 'w').write(':'.join([str(i) for i in data]))

print(f"\x1b[{atts + 3}A\r", end='')
total_wins = sum(data[:6])
if data[6] == 0:
    win_percentage = 0
else:
    win_percentage = round(total_wins / data[6] * 100, 1)

print(f"\n\x1b[2K   \x1b[1mStats - ", end='')

print(f"{data[6]} games - ", end='')
print(f"{win_percentage}% wins - ", end='')
print(f"{total_wins} total wins - ", end='')
print(f"{data[7]} streak - ", end='')
print(f"{data[8]} max streak - ", end='')

print("\x1b[0m\n\x1b[2K\n", end='')

for i in range(6):
    if sum(data[:6]) == 0:
        percentage = 0
    else:
        percentage = round(data[i] / total_wins * 100, 1)
    print(f"\x1b[2K {i+1} ", end=bar_colors[i % 2])
    for j in range(barwidth):
        if (j * 100 / barwidth) >= percentage:
            print(clear_color, end='')
        print(end=' ')
    print(clear_color, end=f" {percentage}% ({data[i]})\n")

print(msg[guess == answer], end=clear_color + '\n\n')

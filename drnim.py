from random import randint

max_coins = 12
coins = max_coins
turn = 0
ai_move_history = []

# This function generates the file which contains the moves the AI makes. It also resets the file whenever it has too many or too few moves.
def generate_file():
    # Open the file in read only and get its content as a list. It has to be read only, otherwise accessing it resets the file.
    file = open('moves.txt', 'r')
    lines = file.readlines()
    file.close()

    # This checks if the length of the file is wrong. 
    # This could potentially happen by some error, but the most common case in which this is activated is what "max_coins" is adjusted.
    if len(lines) != max_coins - 1:
        # This time, the file is being written to, so we need to open it again.
        file = open('moves.txt', 'w')

        to_write = ''

        # We only need "max_coins" - 1 lines in the file, because the last coin (12 by default) is guaranteed to be taken by the human.
        for i in range(max_coins - 1):
            to_write += '123\n'

        file.write(to_write)
        file.close()

# This function displays the coins.
def display():
    for i in range(coins):
        print('O', end=' ')

    print()

# This prompts the user to see how many coins they want to take. 
def prompt():
    take = int(input('How many coins would you like to take? : '))

    # If the user chose something else other than 1, 2, or 3, prompt it again.
    # "take not in [1, 2, 3]" is a alternative way to see if a variable is one of a few things.
    # In my opinion, it is neater than writing "take == 1 or take == 2 or take == 3"
    if take not in [1, 2, 3]:
        print('Please take 1, 2, or 3 coins.')
        return prompt()

    return take;

# This function is where the AI decides how many coins it wants to take.
def ai():
    # Open the file and get the line which corresponds to the amount of coins we have. 
    # Remember, we're working with one line less, so we need to account for that.
    file = open('moves.txt', 'r')
    line = file.readlines()[coins - 1]
    file.close()

    # For that line in the file, choose a random number from it. 
    take = int(line[randint(0, len(line) - 2)])

    print(f'The AI took {take} coins.')

    ai_move_history.append([coins, take])

    return take

# If the AI won the game, it is rewarded.
def reward_ai():
    file = open('moves.txt', 'r')
    lines = file.readlines()
    file.close()

    # This part is a bit complex. Basically, it's going through the moves the AI made this game and adds two copies of it to the file.
    for move in ai_move_history:
        lines[move[0] - 1] = 2 * str(move[1]) + lines[move[0] - 1]

    file = open('moves.txt', 'w')
    file.write(''.join(lines))
    file.close()

# If the AI lost the game, it is punished.
def punish_ai():
    file = open('moves.txt', 'r')
    lines = file.readlines()
    file.close()

    # This part is also a bit complex. Essentially it is going through the moves the AI made and removes one copy of that option from the file.
    # Also, it checks if that line is empty afterwards, meaning there are no remaining options. If this is the case, that line gets reset.
    for move in ai_move_history:
        lines[move[0] - 1] = lines[move[0] - 1].replace(str(move[1]), '', 1)

        if lines[move[0] - 1] == '\n':
            lines[move[0] - 1] = '123\n'

    file = open('moves.txt', 'w')
    file.write(''.join(lines))
    file.close()
   
generate_file()

while coins > 0:
    turn += 1
    
    display()

    if turn % 2 == 1:
        coins -= prompt()
    else:
        coins -= ai()

    print()

if turn % 2 == 1:
    print('You win!')

    punish_ai()
else:
    print('The AI wins!')

    reward_ai()
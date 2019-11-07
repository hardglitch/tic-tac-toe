import random


RIGHTSTEPS = ('a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3')
fieldState = {x: ' ' for x in RIGHTSTEPS}
VICTORY_ALGORITHMS = (('a1', 'b1', 'c1'),
                      ('a2', 'b2', 'c2'),
                      ('a3', 'b3', 'c3'),
                      ('a1', 'a2', 'a3'),
                      ('b1', 'b2', 'b3'),
                      ('c1', 'c2', 'c3'),
                      ('a1', 'b2', 'c3'),
                      ('a3', 'b2', 'c1'),
                      )


def print_field():
    """
              A   B   C
          1     |   |     1
             -----------
          2   X |   | 0   2
             -----------
          3     |   |     3
              A   B   C

        Parameters: ' ', 'X', '0'
        field_size: x = 11, y = 5
    """
    for step in RIGHTSTEPS:
        if fieldState[step] not in (' ', 'X', '0'):
            raise SystemExit('Variable \'fieldState\' is not right.')

    print(f"   a   b   c \n"
          f"1  {fieldState['a1']} | {fieldState['b1']} | {fieldState['c1']} \n"
          f"  ---|---|---\n"
          f"2  {fieldState['a2']} | {fieldState['b2']} | {fieldState['c2']} \n"
          f"  ---|---|---\n"
          f"3  {fieldState['a3']} | {fieldState['b3']} | {fieldState['c3']} \n"
          )


def set_signs():
    while True:
        sign = input('Your sign (X or 0): ').upper()
        if sign in ('X', '0'):
            return sign, '0' if sign == 'X' else 'X'
        print('Wrong input')


def player_step():

    # True - OK, next step
    # False - STOP!

    while True:
        step = input('Your step (Examples: \'a3\', \'b2\'): ').lower()
        if step in RIGHTSTEPS and fieldState[step] not in [cpuSign, playerSign]:
            fieldState[step] = playerSign
            print_field()
            if not check_step('Player'):
                return False
            return True
        print('It\'s wrong. Try again.')


def cpu_step():

    # True - OK, next step
    # False - STOP!

    while True:
        step = cpu_logic()
        if step in RIGHTSTEPS and fieldState[step] not in [playerSign, cpuSign]:
            fieldState[step] = cpuSign
            break
    print(f'CPU step is {step}')
    print_field()
    if not check_step('CPU'):
        return False
    return True


def cpu_logic():

    for twoPasses in range(2):
        for combination in VICTORY_ALGORITHMS:

            # defense (first pass)
            # only double combinations
            if twoPasses == 0:
                # ps ps ' '
                if fieldState[combination[0]] == fieldState[combination[1]] == playerSign\
                        and fieldState[combination[2]] == ' ':
                    return combination[2]

                # ' ' ps ps
                elif fieldState[combination[1]] == fieldState[combination[2]] == playerSign\
                        and fieldState[combination[0]] == ' ':
                    return combination[0]

                # ps ' ' ps
                elif fieldState[combination[0]] == fieldState[combination[2]] == playerSign\
                        and fieldState[combination[1]] == ' ':
                    return combination[1]

            # attack (second pass)
            if twoPasses == 1:

                # double combinations

                # cs cs ' '
                if fieldState[combination[0]] == fieldState[combination[1]] == cpuSign\
                        and fieldState[combination[2]] == ' ':
                    return combination[2]

                # ' ' cs cs
                elif fieldState[combination[1]] == fieldState[combination[2]] == cpuSign\
                        and fieldState[combination[0]] == ' ':
                    return combination[0]

                # cs ' ' cs
                elif fieldState[combination[0]] == fieldState[combination[2]] == cpuSign\
                        and fieldState[combination[1]] == ' ':
                    return combination[1]

                # single combinations

                # cs ' ' ' '
                elif fieldState[combination[0]] == cpuSign\
                        and fieldState[combination[1]] == fieldState[combination[2]] == ' ':
                    return random.choice([combination[1], combination[2]])

                # ' ' cs ' '
                elif fieldState[combination[1]] == cpuSign\
                        and fieldState[combination[0]] == fieldState[combination[2]] == ' ':
                    return random.choice([combination[0], combination[2]])

                # ' ' ' ' cs
                elif fieldState[combination[2]] == cpuSign\
                        and fieldState[combination[0]] == fieldState[combination[1]] == ' ':
                    return random.choice([combination[0], combination[1]])

    return random.choice(RIGHTSTEPS)   # any step, unimportant (it's first step)


def is_win():

    # True - STOP! Victory!
    # False - OK, next step

    for combination in VICTORY_ALGORITHMS:
        # s s s
        if fieldState[combination[0]] == fieldState[combination[1]] == fieldState[combination[2]] != ' ':
            return True
    return False


def is_drawn_game():

    # True - STOP!
    # False - OK, next step

    for cell in RIGHTSTEPS:
        if fieldState[cell] == ' ':
            return False
    return True


def check_step(person):

    # True - OK, next step
    # False - STOP!

    if person in ('CPU', 'Player'):
        # -------------------------
        if is_win():
            print('You win!' if person == 'Player' else 'CPU win!')
            return False
        # -------------------------
        elif is_drawn_game():
            print('Drawn game!')
            return False
        # -------------------------
        return True


# ---------------------------------

# Game settings
playerSign, cpuSign = set_signs()

# Who makes the first step
if random.choice([True, False]):
    print_field()
    player_step()    # player
    cpu_step()
else:
    cpu_step()       # or cpu

# Base game
while player_step() and cpu_step():
    continue

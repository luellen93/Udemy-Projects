def start_playing():

    print("Welcome to TIC TAC TOE!")
    player_choice = input("Please choose X or O: ")
    player_options = ["X", "O"]

    while player_choice.upper() not in player_options:
        player_choice = input("Please choose X or O: ")

    return player_choice

def player_turn(num):

    if num % 2 ==0:
        print("Player 1(X) your turn")
    else:
        print("Player 2(O) your turn")
    

def display(x):

    
    print(" | ".join(x[0:3]))
    print("---------")
    print(" | ".join(x[3:6]))
    print("---------")
    print(" | ".join(x[6:9]))
    


def user_choice():

    choice = ""
    num_list = [str(n) for n in range(10)]

    while choice.isdigit() == False:
        choice = input("Choose a position: 1-9: ")
        if choice.isdigit() == False:
            print("What you entered is not valid.")
            continue
            
    while choice not in num_list:
        if choice not in num_list:
            print("The number you entered is not between 1 and 9.")
        choice = input("Please choice a position 1-9: ")
        
    return int(choice)

def replacement_value(x, position):
    
    if turn % 2 == 0:
        if x[position - 1] == " ":
            x[position - 1] = "X"
        else:
            print("This position is unavailable.")
            user_choice()
    else:
        if x[position - 1] == " ":
            x[position - 1] = "O"
        else:
            print("This position is unavailable.")
            user_choice()

    return x

def game_over():

    choice = False
    win_list = ["123", "456", "789", "147", "369", "159", "357", "258"] 


    for i in win_list:
        win = []
        for j in i:
            win.append(game_list[int(j) - 1])
            if "".join(win[0:3]) == "XXX" or "".join(win[0:3]) == "OOO":
                choice = True
                break

    return choice

    


turn = 0
game_list = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
continue_playing = False

start_playing()
display(game_list)
player_turn(turn)

while turn < 9 and continue_playing == False:

    position = user_choice()

    game_list = replacement_value(game_list, position)

    turn += 1

    display(game_list)

    continue_playing = game_over()

    player_turn(turn)
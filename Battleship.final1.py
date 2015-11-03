from random import randint

board_large = [] #cria um lista para o 1o board
board_small = [] #cria um lista para o 2o board
player_one = {
    "name": "Player 1",
    "wins": 0,
    "lose": 0
}
player_two = {
    "name": "Player 2",
    "wins": 0,
    "lose": 0
}
total_turns = 0
win_state_change = 0

def build_board_large(board): # cria a  do 1o jogador
    for item in range(9):
        board.append(["~"] * 9)

def build_board_small(board):
    for item in range(9):
        board.append(["~"] * 9)

def show_board(board_one, board_two): # cria a board do 2o jogador
    print ("Board One")
    for row in board_one:
        print (" ".join(row))
    print ("Board Two")
    for row in board_two:
        print (" ".join(row))

def random_row(board):
    rand_numb = randint(1, len(board[0])) # escolhe randomicamente a linha do barco
    return rand_numb

def random_col(board):
    rand_numb = randint(1, len(board)) # escolhe randomicamente a coluna do barco
    return rand_numb

def start_game(board_one, board_two):
    del board_one[:]
    del board_two[:]
    print ("Vamos jogar Battleship!")
    print ("Turn 1")
    build_board_large(board_large)
    build_board_small(board_small)
    show_board(board_one, board_two)
    ship_col_large = random_col(board_large) - 1 # escolhe randomicamente a linha do barco do 1o jogador
    ship_row_large = random_row(board_large) - 1 # escolhe randomicamente a coluna do barco do 1o jogador
    ship_col_small = random_col(board_small) - 1 # escolhe randomicamente a linha do barco do 2o jogador
    ship_row_small = random_row(board_small) - 1 # escolhe randomicamente a coluna do barco do 2o jogador
#    print (ship_row_large) # mostra a linha do barco 1o jogador 
#    print (ship_col_large) # mostra a coluna do barco do 1o jogador
#    print (ship_row_small) # mostra a linha do barco 2o jogador
#    print (ship_row_small) # mostra a coluna do barco do 2o jogador
    return {'ship_col_large': ship_col_large, 'ship_row_large': ship_row_large, 'ship_col_small': ship_col_small, 'ship_row_small': ship_row_small}

ship_points = start_game(board_large, board_small)

def best_out_of(win_state, total_turns=0, player=player_one): #funcao para definir o vencedor do jogo
    play_again = ""
    if player["wins"] >= 2:
        print ("%s win best out of 3" % (player["name"])) # Caso No de vitorias for >=2 jogador 1/2 ganha por melhor de 3
    elif player["lose"] >= 2:
        print ("%s lost best out of 3" % (player["name"])) # Caso No de derrotas  for >= 2 jogador 1/2 perde por melhor de 3
    elif win_state == 1:
        print ("%s wins this game!" % (player["name"])) # imprimi que jogador 1/2 vence o jogo
        play_again = str(input("Voce quer jogar novamente ?(yes/no)")) # pergunta se quer recomecar o jogo
    elif win_state == 0 and total_turns == 6:
        play_again = str(input("Este jogo foi empate. Voce quer jogar novamente ?(yes/no) ")) #fala q o jogo foi empate e sugere comecar ele novamente
    elif win_state != 6 and total_turns == 6:
        play_again = str(input("Voce quer jogar novamente ?(yes/no")) # pergunta se quer comecar um novo jogo
    if play_again == "yes":
        return play_again
    else:
        exit()

def input_check(ship_row, ship_col, player, board, win_state): #funcao para checar o chute de linha e coluna
    while True:
        try:
            guess_row = int(input("Guess Row:")) #pega o chute de linha
            guess_col = int(input("Guess Col:")) # pega o chute de coluna
        except ValueError:
            print ("entre apenas um No.") #avisa para digitar apenas 1 No
            continue
        else:
            break
    if guess_row == ship_row and guess_col == ship_col:
        global ship_points
        win_state = 1  
        player["wins"] += 1  
        print ("Parabens! voce afundou meu navio") # caso o chute de linha e de coluna for igual as posicoes randomicamente geradas da vitoria ao jogador
        if best_out_of(win_state) == "yes":
            ship_points = start_game(board_large, board_small)
            return ship_points
    elif player == player_two:  
        if (guess_row < 0 or guess_row >= 9) or (guess_col < 0 or guess_col >= 9): # caso os chutes estejam fora das boundries avisa o jogador
            print("Oops, isso ai nem eh no oceano.")
        elif board[guess_row - 1][guess_col - 1] == "X": # caso o jogador repita tentativas de chute avisa ou fala que errou o navio
            print ("ja tentou aqui.")
        else:
            print ("errou meu navio!")
            board[guess_row - 1][guess_col - 1] = "X"
        show_board(board_large, board_small)
    elif player == player_one:  
        if (guess_row < 0 or guess_row >= 9) or (guess_col < 0 or guess_col >= 9): 
            print ("Oops, isso ai nem eh no oceano.")
        elif board[guess_row - 1][guess_col - 1] == "X": # caso o jogador repita tentativas de chute avisa ou fala que errou o navio
            print ("ja tentou aqui.")
        else:
            print ("errou meu navio!")
            board[guess_row - 1][guess_col - 1] = "X"
            win_state = 0
        show_board(board_large, board_small)
    return win_state

def player_turns(total_turns): # muda os turnos dos jogadores
    if total_turns % 2 == 0: 
        player_turn = player_two
        return player_turn
    else:
        player_turn = player_one
        return player_turn


for games in range(3): #define o No de turnos a serem jogados
    games += 1  
    for turns in range(6): 
        total_turns += 1
        if player_turns(total_turns) == player_one: # fala que eh vez do jogador 1
            print ("It's player Ones's turn")
            input_check(ship_points['ship_row_large'], ship_points['ship_col_large'], player_one, board_large, win_state_change)
        elif player_turns(total_turns) == player_two: #fala que eh a vez do jogador 2
            print ("It's player Two's turn")
            input_check(ship_points['ship_row_small'], ship_points['ship_col_small'], player_two, board_small, win_state_change)
        if total_turns == 6:
            if best_out_of(win_state_change, total_turns) == "yes":
                ship_points = start_game(board_large, board_small)
                continue
            else:
                break
    if games == 6:
            print ("O Jogo acabou") # termina o jogo apos todos os turnos
        
            exit()
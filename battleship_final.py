"""
Created on Mon Sep 16 21:06:20 2015

@author: Nathan """


from random import randint

board_large = []
board_small = []
player_one = {
    "nome": "Jogador  1",
    "vitorias": 0,
    "derrotas": 0
}
player_two = {
    "nome": "jogador 2",
    "vitorias": 0,
    "derrotas": 0
}
total_turns = 0
win_state_change = 0


def build_board_large(board):
    """crie um tabuleiro 5x5"""
    for item in range(5):
        board.append(["O"] * 5)


def build_board_small(board):   
    """crie um tabuleiro 5x5"""
    for item in range(5):
        board.append(["O"] * 5)


def show_board(board_one, board_two):
    """fazer com que a lista pareca um tabuleiro de batalha naval"""
    print ("Board One")
    for row in board_one:
        print (" ".join(row))
    print ("Board Two")
    for row in board_two:
        print (" ".join(row))


def load_game(board_one, board_two):
    """cada vez que o jogador decide comecar a jogar, o loop renicia"""
    print ("Vamos jogar batalha naval!")
    print ("rodada 1")
    del board_one[:]
    del board_two[:]
    build_board_large(board_one)
    build_board_small(board_two)
    show_board(board_one, board_two)
    ship_col_large = (lambda x: randint(1, len(x)))(board_one)
    ship_row_large = (lambda x: randint(1, len(x[0])))(board_one)
    ship_col_small = (lambda x: randint(1, len(x)))(board_two)
    ship_row_small = (lambda x: randint(1, len(x[0])))(board_two)
    #print ("Board 1 ship column: " + str(ship_row_large)) #mostra em qual coluna esta o barco na board 1
    #print ("Board 1 ship row: " + str(ship_col_large))  #mostra em qual linha esta o barco na board 1
    #print ("Board 2 ship column: " + str(ship_row_small)) #mostra em qual coluna esta o barco na board 2
    #print ("Board 2 ship row: " + str(ship_col_small)) #mostra em qual linha esta o barco na board 2
    return {
        'ship_col_large': ship_col_large,
        'ship_row_large': ship_row_large,
        'ship_col_small': ship_col_small,
        'ship_row_small': ship_row_small
    }

ship_points = load_game(board_large, board_small)  # define o lugar do novo navio para o novo dicionario


def player_turns():
    """altera o jogador, checando atraves dos Nos impares"""
    if total_turns % 2 == 0:
        return player_two
    else:
        return player_one


def play_again():
    """Renicia o jogo caso o jogador queira"""
    global total_turns
    global ship_points
    answer = str(input("voce quer jogador de novo(yes/no)"))
    if answer == "yes":
        total_turns = 0    # reset/ comeca novamente a partir do Jogador 1 
        show_board(board_large, board_small)
        ship_points = load_game(board_large, board_small)
    else:
        exit()


def best_out_of(win_state, player):
    """checa os status do jogo"""
    global total_turns
    if win_state == 1 and player["wins"] < 2:  # checa se o Jogador 1 ainda esta no jogo
        print ("%s venceu o jogo!") % (player["name"])
        play_again()
    elif win_state == 0 and total_turns == 6:
        print ("esse jogo foi um empate")
        play_again()
    elif win_state != 0 and total_turns == 6:
        play_again()
    elif player["wins"] >= 2:     # cehca quem ganhou a melhor de 3
        print ("%s ganhou na melhor de 3") % (player["name"])
        play_again()
    elif player["lose"] >= 2:
        print ("%s perdeu na melhor de 3") % (player["name"])
        play_again()
    else:
        play_again()


def input_check(ship_row, ship_col, player, board):
    """checa os chutes dos jogadores"""
    global win_state_change
    guess_col = 0
    guess_row = 0
    while True:
        try:
            guess_row = int(input("chute a fila:")) - 1
            guess_col = int(input("chute a coluna:")) - 1
        except ValueError:
            print ("entre somente um No.")
            continue
        else:
            break
    match = guess_row == ship_row - 1 and guess_col == ship_col - 1
    not_on_small_board = (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4)
    not_on_large_board = (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4)

    if match:
        win_state_change = 1  # nota que alguem ganhou o atual jogo
        player["wins"] += 1
        print ("parabens! Voce afundou meu navio")
        best_out_of(win_state_change, player)
    elif not match and player == player_two:  
        if not_on_small_board:
            print ("Oops, isso nem eh no oceano.")
        elif board[guess_row][guess_col] == "X":
            print ("Voce ja chutou aqui.")
        else:
            print ("errou meu navio!")
            board[guess_row][guess_col] = "X"
        win_state_change = 0
        show_board(board_large, board_small)
    elif not match and player == player_one:
        if not_on_large_board:
            print ("Oops, isso nem eh no oceano..")
        elif board[guess_row][guess_col] == "X":
            print ("Voce ja chutou aqui.")
        else:
            print ("errou meu navio!")
            board[guess_row][guess_col] = "X"
        win_state_change = 0
        show_board(board_large, board_small)
    else:
        return win_state_change

"""Start the game logic"""
for games in range(3):
    games += 1  # total de 3 jogos
    for turns in range(6):  # 6 turnos totais = 3 turnos para cada jogador
        total_turns += 1
        if player_turns() == player_one:
            print ("Eh a vez do jogador 1")
            input_check(
                ship_points['ship_row_large'],
                ship_points['ship_col_large'],
                player_one, board_large
            )
        elif player_turns() == player_two:
            print ("Eh a vez do jogador 2")
            input_check(
                ship_points['ship_row_small'],
                ship_points['ship_col_small'],
                player_two, board_small
            )
        else:
            break
        if total_turns == 6 and player_turns() == player_one:
            best_out_of(win_state_change, player_one)
        elif total_turns == 6 and player_turns() == player_two:
            best_out_of(win_state_change, player_two)
        else:
            continue
    if games == 3:
            print ("O jogo acabou.")
        #   print "Wins: %s" % (player_one[entry])
            exit()
    else:
        continue

import random as r
import multiprocessing
import copy
import math as m
from termcolor import colored
import sys
import os


class color:
    PURPLE = '\033[1;35;48m'
    CYAN = '\033[1;36;48m'
    BOLD = '\033[1;37;48m'
    BLUE = '\033[1;34;48m'
    GREEN = '\033[1;32;48m'
    YELLOW = '\033[1;33;48m'
    RED = '\033[1;31;48m'
    BLACK = '\033[1;30;48m'
    UNDERLINE = '\033[4;37;48m'
    END = '\033[1;37;0m'


# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKCYAN = '\033[96m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_board(board, LAST, SWITCH):
    # SWITCH 0: CSAK A JELEKET ÍRJA KI
    #        1: CSAK A JELEKET ÉS 1-ESEKET ÍRJA KI
    #        2: MEZŐK TARTALMAIT IS KIÍRJA

    w = len(board[0])
    h = len(board)
    ### FEJLÉC
    print('   ', end='')
    for x in range(w):
        print(color.PURPLE + str(x).ljust(3, ' ') + color.END, end='')
    print('')
    for y in range(h):
        ### OSZLOP SZÁMOZÁS
        print(color.PURPLE + str(y).ljust(3, ' ') + color.END, end='')
        ### TARTALOM
        for x in range(w):
            if SWITCH == 0:
                if board[y][x] != 'x' and board[y][x] != 'o':
                    print('.', end='  ')
                else:
                    if LAST != 0:
                        if x == LAST[0] and y == LAST[1]:
                            print(colored(board[y][x], 'red'), end='  ')
                        else:
                            print(colored(board[y][x], 'cyan', attrs=['bold']), end='  ')
                    else:
                        print(colored(board[y][x], 'cyan', attrs=['bold']), end='  ')
            elif SWITCH == 1:
                if LAST != 0:
                    if x == LAST[0] and y == LAST[1]:
                        print(color.GREEN + str(board[y][x]) + color.END, end='  ')
                    elif board[y][x] == 'o' or board[y][x] == 'x':
                        print(color.CYAN + str(board[y][x]) + color.END, end='  ')
                    elif board[y][x] >= 1:
                        print(color.RED + str(int(board[y][x])) + color.END, end='  ')
                    else:
                        print('.', end='  ')
                else:
                    if board[y][x] == 'x':
                        print(color.CYAN + str(board[y][x]) + color.END, end='  ')
                    elif board[y][x] == 'o':
                        print(color.YELLOW + str(board[y][x]) + color.END, end='  ')
                    elif board[y][x] >= 1:
                        print(color.RED + str(int(board[y][x])) + color.END, end='  ')
                    else:
                        print('.', end='  ')
            elif SWITCH == 2:
                if LAST != 0:
                    if x == LAST[0] and y == LAST[1]:
                        print(colored(board[y][x], 'red', attrs=['bold']), end='  ')
                    elif board[y][x] == 'o' or board[y][x] == 'x':
                        print(colored(board[y][x], 'cyan', attrs=['bold']), end='  ')
                    elif board[y][x] == 1:
                        print('1', end='  ')
                    elif board[y][x] == 0:
                        print('0', end='  ')
                    else:
                        print(colored(board[y][x], 'red', attrs=['bold']), end='  ')
                else:
                    if board[y][x] == 'o' or board[y][x] == 'x':
                        print(colored(board[y][x], 'cyan', attrs=['bold']), end='  ')
                    elif board[y][x] == 1:
                        print('1', end='  ')
                    elif board[y][x] == 0:
                        print('0', end='  ')
                    else:
                        print(colored(board[y][x], 'red', attrs=['bold']), end='  ')
        ### OSZLOP SZÁMOZÁS
        print(color.PURPLE + str(y) + color.END)
    ### ALSÓ SZÁMOZOTT SOR
    print('   ', end='')
    for x in range(w):
        print(color.PURPLE + str(x).ljust(3, ' ') + color.END, end='')
    print('\n')


def print_possible_steps(board):
    possible_steps = 0
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 1:
                possible_steps += 1
    print('Lehetséges lépések száma:', possible_steps)


def take_cross(board):
    w = len(board[0])
    h = len(board)
    ### ### ELLENŐRZÉS, HOGY VAN-E LEHETŐSÉG, VAGYIS NINCS MINDENHOL 0
    s = 0
    for y in range(h):
        for x in range(w):
            if board[y][x] == 1:
                s += 1
    if s == 0:
        return 0
    ### ### SORSOLÁS
    OK = 0
    while OK != 1:
        posx = r.randint(0, w - 1)
        posy = r.randint(0, h - 1)
        if board[posy][posx] != 1:
            continue
        else:
            board[posy][posx] = 'x'
            OK = 1
    return (posx, posy)


def take_circle(board):
    w = len(board[0])
    h = len(board)
    ### ### ELLENŐRZÉS, HOGY VAN-E LEHETŐSÉG, VAGYIS NINCS MINDENHOL 0
    s = 0
    for y in range(h):
        for x in range(w):
            if board[y][x] == 1:
                s += 1
    if s == 0:
        return 0
    ### ### SORSOLÁS
    OK = 0
    while OK != 1:
        posx = r.randint(0, w - 1)
        posy = r.randint(0, h - 1)
        if board[posy][posx] != 1:
            continue
        else:
            board[posy][posx] = 'o'
            OK = 1
    return (posx, posy)


def take_fix(board, pos, SIGN):
    # FIX POZÍCIÓBA RAK EGY JELET
    board[pos[1]][pos[0]] = SIGN


def take_rand(board, SIGN):
    w = len(board[0])
    h = len(board)
    squares = []

    ### ### ELLENŐRZÉS, HOGY VAN-E LEHETŐSÉG, VAGYIS NINCS MINDENHOL 0
    for y in range(h):
        for x in range(w):
            if board[y][x] != 'o' and board[y][x] != 'x':
                if board[y][x] > 0:
                    squares.append(board[y][x])
    if len(squares) == 0:
        return 0

    ### ### SORSOLÁS
    k = choose_weighted(squares)

    ### ### BEÍRÁS
    s = 0
    for y in range(h):
        for x in range(w):
            if board[y][x] != 'o' and board[y][x] != 'x':
                if board[y][x] > 0:
                    if s == k:
                        board[y][x] = SIGN
                        return (x, y)
                    else:
                        s += 1


def choose_weighted(LIST):
    q = 10000
    s = 0
    w = 0
    for i in range(len(LIST)):
        w = w + int(LIST[i] * q)
    if w == 0:
        return -1
    x = r.randint(1, w)
    for i in range(len(LIST)):
        s = s + int(LIST[i] * q)
        if x <= s:
            return i


def if_end(board, SIGN, SWITCH):
    # NYERT-E VALAMELYIK: VISSZATÉRÉSI ÉRTÉKE A GYŐZTES JELE VAGY 0
    # SWITCH 0: NEM ÍR KI SEMMIT
    #        1: KIÍRJA A NYERŐ SOR ELSŐ JELÉNEK KOORDINÁTÁIT

    w = len(board[0])
    h = len(board)
    for y in range(h):
        for x in range(w):
            if board[y][x] == SIGN:
                ### ### ### HORIZONTÁLIS ELLENŐRZÉS ### ### ###
                win = [[x, y]]
                if x + 4 <= w - 1:
                    for k in range(1, 5):
                        if board[y][x + k] == SIGN:
                            win.append([x + k, y])
                    if len(win) == 5:
                        if SWITCH == 1:
                            clear_screen()
                            print_board(board, win, 0)
                        return SIGN

                ### ### ### VERTIKÁLIS ELLENŐRZÉS ### ### ###
                win = [[x, y]]
                if y + 4 <= h - 1:
                    for k in range(1, 5):
                        if board[y + k][x] == SIGN:
                            win.append([x, y + k])
                    if len(win) == 5:
                        if SWITCH == 1:
                            clear_screen()
                            print_board(board, win, 0)
                        return SIGN

                ### ### ### DIAGONÁLIS+ ELLENŐRZÉS ### ### ###
                win = [[x, y]]
                if x + 4 <= w - 1 and y + 4 <= h - 1:
                    for k in range(1, 5):
                        if board[y + k][x + k] == SIGN:
                            win.append([x + k, y + k])
                    if len(win) == 5:
                        if SWITCH == 1:
                            clear_screen()
                            print_board(board, win, 0)
                        return SIGN

                ### ### ### DIAGONÁLIS- ELLENŐRZÉS ### ### ###
                win = [[x, y]]
                if x - 4 >= 0 and y + 4 <= h - 1:
                    for k in range(1, 5):
                        if board[y + k][x - k] == SIGN:
                            win.append([x - k, y + k])
                    if len(win) == 5:
                        if SWITCH == 1:
                            clear_screen()
                            print_board(board, win, 0)
                        return SIGN

                # ### ### ### HORIZONTÁLIS ELLENŐRZÉS ### ### ###
                # for k in range(6):
                #     if x + k <= w - 1 and k != 5:
                #         if board[y][x + k] == SIGN:
                #             continue
                #         else:
                #             break
                #     elif k == 5:
                #         if SWITCH == 1:
                #             print('H', x + 1, y + 1)
                #         return SIGN
                #     elif x + k == w:
                #         break
                # ### ### ### VERTIKÁLIS ELLENŐRZÉS ### ### ###
                # for k in range(6):
                #     if y + k <= h - 1 and k != 5:
                #         if board[y + k][x] == SIGN:
                #             continue
                #         else:
                #             break
                #     elif k == 5:
                #         if SWITCH == 1:
                #             print('V', x + 1, y + 1)
                #         return SIGN
                #     elif y + k == h:
                #         break
                # ### ### ### DIAGONÁLIS+ ELLENŐRZÉS ### ### ###
                # for k in range(6):
                #     if y + k <= h - 1 and x + k <= w - 1 and k != 5:
                #         if board[y + k][x + k] == SIGN:
                #             continue
                #         else:
                #             break
                #     elif k == 5:
                #         if SWITCH == 1:
                #             print('D+', x + 1, y + 1)
                #         return SIGN
                #     elif y + k == h:
                #         break
                #     elif x + k == w:
                #         break
                # ### ### ### DIAGONÁLIS- ELLENŐRZÉS ### ### ###
                # for k in range(6):
                #     if y + k <= h - 1 and x - k >= 0 and k != 5:
                #         if board[y + k][x - k] == SIGN:
                #             continue
                #         else:
                #             break
                #     elif k == 5:
                #         if SWITCH == 1:
                #             print('D-', x + 1, y + 1)
                #         return SIGN
                #     elif y + k == h:
                #         break
                #     elif x - k == -1:
                #         break
    return 0


def trivial(board, SIGN):
    # VAN-E VALAMELYIKNEK 4-ESE, VAGYIS TRIVIÁLIS, HOGY HOVA KELL RAKNI
    # A KÉRDÉSES HELYEKET KITÖLTI 1-ESSEL

    w = len(board[0])
    h = len(board)
    triv_pos = set()
    for y in range(h):
        for x in range(w):
            if board[y][x] == SIGN:
                ### ### ### HORIZONTÁLIS ELLENŐRZÉS ### ### ###
                s = 1
                pos_tmp = ()
                for k in range(1, 5):
                    if x + k <= w - 1:
                        if board[y][x + k] == SIGN:
                            s += 1
                        elif board[y][x + k] != 'x' and board[y][x + k] != 'o':
                            pos_tmp = (x + k, y)
                    if s == 4 and k == 3:
                        if x - 1 >= 0:
                            if board[y][x - 1] != 'o' and board[y][x - 1] != 'x':
                                triv_pos.add((x - 1, y))
                        if x + 4 <= w - 1:
                            if board[y][x + 4] != 'o' and board[y][x + 4] != 'x':
                                triv_pos.add((x + 4, y))
                        break
                    if s == 4 and k == 4 and pos_tmp != ():
                        triv_pos.add(pos_tmp)

                ### ### ### VERTIKÁLIS ELLENŐRZÉS ### ### ###
                s = 1
                pos_tmp = ()
                for k in range(1, 5):
                    if y + k <= h - 1:
                        if board[y + k][x] == SIGN:
                            s += 1
                        elif board[y + k][x] != 'x' and board[y + k][x] != 'o':
                            pos_tmp = (x, y + k)
                    if s == 4 and k == 3:
                        if y - 1 >= 0:
                            if board[y - 1][x] != 'o' and board[y - 1][x] != 'x':
                                triv_pos.add((x, y - 1))
                        if y + 4 <= h - 1:
                            if board[y + 4][x] != 'o' and board[y + 4][x] != 'x':
                                triv_pos.add((x, y + 4))
                        break
                    if s == 4 and k == 4 and pos_tmp != ():
                        triv_pos.add(pos_tmp)

                ### ### ### DIAGONÁLIS+ ELLENŐRZÉS ### ### ###
                s = 1
                pos_tmp = ()
                for k in range(1, 5):
                    if y + k <= h - 1 and x + k <= w - 1:
                        if board[y + k][x + k] == SIGN:
                            s += 1
                        elif board[y + k][x + k] != 'x' and board[y + k][x + k] != 'o':
                            pos_tmp = (x + k, y + k)
                    if s == 4 and k == 3:
                        if x - 1 >= 0 and y - 1 >= 0:
                            if board[y - 1][x - 1] != 'o' and board[y - 1][x - 1] != 'x':
                                triv_pos.add((x - 1, y - 1))
                        if x + 4 <= w - 1 and y + 4 <= h - 1:
                            if board[y + 4][x + 4] != 'o' and board[y + 4][x + 4] != 'x':
                                triv_pos.add((x + 4, y + 4))
                        break
                    if s == 4 and k == 4 and pos_tmp != ():
                        triv_pos.add(pos_tmp)

                ### ### ### DIAGONÁLIS- ELLENŐRZÉS ### ### ###
                s = 1
                pos_tmp = ()
                for k in range(1, 5):
                    if y + k <= h - 1 and x - k >= 0:
                        if board[y + k][x - k] == SIGN:
                            s += 1
                        elif board[y + k][x - k] != 'x' and board[y + k][x - k] != 'o':
                            pos_tmp = (x - k, y + k)
                    if s == 4 and k == 3:
                        if x + 1 <= w - 1 and y - 1 >= 0:
                            if board[y - 1][x + 1] != 'o' and board[y - 1][x + 1] != 'x':
                                triv_pos.add((x + 1, y - 1))
                        if x - 4 >= 0 and y + 4 <= h - 1:
                            if board[y + 4][x - 4] != 'o' and board[y + 4][x - 4] != 'x':
                                triv_pos.add((x - 4, y + 4))
                        break
                    if s == 4 and k == 4 and pos_tmp != ():
                        triv_pos.add(pos_tmp)

    if triv_pos != set():
        fill_zero(board)
        for i in triv_pos:
            take_fix(board, i, 1)
        return 1
    else:
        return 0


def trivial2nd(board, SIGN, WHOSE):
    # TUD-E VALAKI NYITOTT 4-EST KIALAKÍTANI
    # A KÉRDÉSES HELYEKET KITÖLTI 1-ESSEL
    # HA NEM TÖRTÉNT ÍRÁS, AKKOR 0 A VISSZATÉRÉSI ÉRTÉKE

    all_sign = {'o', 'x'}
    w = len(board[0])
    h = len(board)
    triv2nd_pos = set()
    SUMM_FORM = 0
    for y in range(h):
        for x in range(w):
            if board[y][x] == SIGN:
                ### ### ### HORIZONTÁLIS ELLENŐRZÉS ### ### ###
                s = 1
                INCOMP = 0
                pos_tmp = ()
                for k in range(1, 4):
                    if x + k <= w - 1:
                        if board[y][x + k] == SIGN:
                            s += 1
                        else:
                            if s == 3:
                                pass
                            else:
                                if board[y][x + k] in all_sign:
                                    break
                                INCOMP = 1
                                pos_tmp = (x + k, y)
                ### ### 3 EGY SORBAN NYITOTT VÉGEKKEL
                if s == 3 and INCOMP == 0 and x + 3 <= w - 1 and x - 1 >= 0:
                    if board[y][x - 1] not in all_sign and board[y][x + 3] not in all_sign:
                        SUMM_FORM += 1
                        ### SAJÁTUNK FELŐL DONTÜNK
                        if WHOSE == 'OWN':
                            if x - 2 >= 0:
                                if board[y][x - 2] not in all_sign:
                                    triv2nd_pos.add((x - 1, y))
                            if x + 4 <= w - 1:
                                if board[y][x + 4] not in all_sign:
                                    triv2nd_pos.add((x + 3, y))
                        ### ELLENFÉLNEK KELL DÖNTENIE
                        elif WHOSE == 'ENEMY':
                            ### NINCS A SZÉLÉHEZ KÖZEL
                            if x - 2 >= 0 and x + 4 <= w - 1:
                                if board[y][x - 2] not in all_sign or board[y][x + 4] not in all_sign:
                                    triv2nd_pos.add((x - 1, y))
                                    triv2nd_pos.add((x + 3, y))
                            ### TÁBLA JOBB SZÉLÉHEZ VAN KÖZEL (MERT AZ ELSŐ ESET NEM TELJESÜLT)
                            elif x - 2 >= 0:
                                if board[y][x - 2] not in all_sign:
                                    triv2nd_pos.add((x - 1, y))
                                    triv2nd_pos.add((x + 3, y))
                            ### TÁBLA BAL SZÉLÉHEZ VAN KÖZEL
                            elif x + 4 <= w - 1:
                                if board[y][x + 4] not in all_sign:
                                    triv2nd_pos.add((x - 1, y))
                                    triv2nd_pos.add((x + 3, y))
                ### ### 4-BŐL VAN 3 ÉS NYITOTTAK A VÉGEK
                if s == 3 and INCOMP == 1 and x + 4 <= w - 1 and x - 1 >= 0:
                    if board[y][x - 1] not in all_sign and board[y][x + 4] not in all_sign:
                        SUMM_FORM += 1
                        if WHOSE == 'OWN':
                            triv2nd_pos.add(pos_tmp)
                        elif WHOSE == 'ENEMY':
                            triv2nd_pos.add(pos_tmp)
                            triv2nd_pos.add((x + 4, y))
                            triv2nd_pos.add((x - 1, y))

                ### ### ### VERTIKÁLIS ELLENŐRZÉS ### ### ###
                s = 1
                INCOMP = 0
                pos_tmp = ()
                for k in range(1, 4):
                    if y + k <= h - 1:
                        if board[y + k][x] == SIGN:
                            s += 1
                        else:
                            if s == 3:
                                pass
                            else:
                                if board[y + k][x] in all_sign:
                                    break
                                INCOMP = 1
                                pos_tmp = (x, y + k)
                ### ### 3 EGY SORBAN NYITOTT VÉGEKKEL
                if s == 3 and INCOMP == 0 and y + 3 <= h - 1 and y - 1 >= 0:
                    if board[y - 1][x] not in all_sign and board[y + 3][x] not in all_sign:
                        SUMM_FORM += 1
                        ### SAJÁTUNK FELŐL DONTÜNK
                        if WHOSE == 'OWN':
                            if y - 2 >= 0:
                                if board[y - 2][x] not in all_sign:
                                    triv2nd_pos.add((x, y - 1))
                            if y + 4 <= h - 1:
                                if board[y + 4][x] not in all_sign:
                                    triv2nd_pos.add((x, y + 3))
                        ### ELLENFÉLNEK KELL DÖNTENIE
                        elif WHOSE == 'ENEMY':
                            ### NINCS A SZÉLÉHEZ KÖZEL
                            if y - 2 >= 0 and y + 4 <= h - 1:
                                if board[y - 2][x] not in all_sign or board[y + 4][x] not in all_sign:
                                    triv2nd_pos.add((x, y - 1))
                                    triv2nd_pos.add((x, y + 3))
                            ### TÁBLA JOBB SZÉLÉHEZ VAN KÖZEL (MERT AZ ELSŐ ESET NEM TELJESÜLT)
                            elif y - 2 >= 0:
                                if board[y - 2][x] not in all_sign:
                                    triv2nd_pos.add((x, y - 1))
                                    triv2nd_pos.add((x, y + 3))
                            ### TÁBLA BAL SZÉLÉHEZ VAN KÖZEL
                            elif y + 4 <= h - 1:
                                if board[y + 4][x] not in all_sign:
                                    triv2nd_pos.add((x, y - 1))
                                    triv2nd_pos.add((x, y + 3))
                ### ### 4-BŐL VAN 3 ÉS NYITOTTAK A VÉGEK
                if s == 3 and INCOMP == 1 and y + 4 <= h - 1 and y - 1 >= 0:
                    if board[y - 1][x] not in all_sign and board[y + 4][x] not in all_sign:
                        SUMM_FORM += 1
                        if WHOSE == 'OWN':
                            triv2nd_pos.add(pos_tmp)
                        elif WHOSE == 'ENEMY':
                            triv2nd_pos.add(pos_tmp)
                            triv2nd_pos.add((x, y + 4))
                            triv2nd_pos.add((x, y - 1))

                ### ### ### DIAGONÁLIS+ ELLENŐRZÉS ### ### ###
                s = 1
                INCOMP = 0
                pos_tmp = ()
                for k in range(1, 4):
                    if x + k <= w - 1 and y + k <= h - 1:
                        if board[y + k][x + k] == SIGN:
                            s += 1
                        else:
                            if s == 3:
                                pass
                            else:
                                if board[y + k][x + k] in all_sign:
                                    break
                                INCOMP = 1
                                pos_tmp = (x + k, y + k)
                ### ### 3 EGY SORBAN NYITOTT VÉGEKKEL
                if s == 3 and INCOMP == 0 and y + 3 <= h - 1 and y - 1 >= 0 and x + 3 <= w - 1 and x - 1 >= 0:
                    if board[y - 1][x - 1] not in all_sign and board[y + 3][x + 3] not in all_sign:
                        SUMM_FORM += 1
                        ### SAJÁTUNK FELŐL DONTÜNK
                        if WHOSE == 'OWN':
                            if y - 2 >= 0 and x - 2 >= 0:
                                if board[y - 2][x - 2] not in all_sign:
                                    triv2nd_pos.add((x - 1, y - 1))
                            if y + 4 <= h - 1 and x + 4 <= w - 1:
                                if board[y + 4][x + 4] not in all_sign:
                                    triv2nd_pos.add((x + 3, y + 3))
                        ### ELLENFÉLNEK KELL DÖNTENIE
                        elif WHOSE == 'ENEMY':
                            ### NINCS A SZÉLÉHEZ KÖZEL
                            if y - 2 >= 0 and y + 4 <= h - 1 and x - 2 >= 0 and x + 4 <= w - 1:
                                if board[y - 2][x - 2] not in all_sign or board[y + 4][x + 4] not in all_sign:
                                    triv2nd_pos.add((x - 1, y - 1))
                                    triv2nd_pos.add((x + 3, y + 3))
                            ### TÁBLA JOBB SZÉLÉHEZ VAN KÖZEL (MERT AZ ELSŐ ESET NEM TELJESÜLT)
                            elif y - 2 >= 0 and x - 2 >= 0:
                                if board[y - 2][x - 2] not in all_sign:
                                    triv2nd_pos.add((x - 1, y - 1))
                                    triv2nd_pos.add((x + 3, y + 3))
                            ### TÁBLA BAL SZÉLÉHEZ VAN KÖZEL
                            elif y + 4 <= h - 1 and x + 4 <= w - 1:
                                if board[y + 4][x + 4] not in all_sign:
                                    triv2nd_pos.add((x - 1, y - 1))
                                    triv2nd_pos.add((x + 3, y + 3))
                ### ### 4-BŐL VAN 3 ÉS NYITOTTAK A VÉGEK
                if s == 3 and INCOMP == 1 and y + 4 <= h - 1 and y - 1 >= 0 and x + 4 <= w - 1 and x - 1 >= 0:
                    if board[y - 1][x - 1] not in all_sign and board[y + 4][x + 4] not in all_sign:
                        SUMM_FORM += 1
                        if WHOSE == 'OWN':
                            triv2nd_pos.add(pos_tmp)
                        elif WHOSE == 'ENEMY':
                            triv2nd_pos.add(pos_tmp)
                            triv2nd_pos.add((x + 4, y + 4))
                            triv2nd_pos.add((x - 1, y - 1))

                ### ### ### DIAGONÁLIS- ELLENŐRZÉS ### ### ###
                s = 1
                INCOMP = 0
                pos_tmp = ()
                for k in range(1, 4):
                    if x - k >= 0 and y + k <= h - 1:
                        if board[y + k][x - k] == SIGN:
                            s += 1
                        else:
                            if s == 3:
                                pass
                            else:
                                if board[y + k][x - k] in all_sign:
                                    break
                                INCOMP = 1
                                pos_tmp = (x - k, y + k)
                ### ### 3 EGY SORBAN NYITOTT VÉGEKKEL
                if s == 3 and INCOMP == 0 and y + 3 <= h - 1 and y - 1 >= 0 and x - 3 >= 0 and x + 1 <= w - 1:
                    if board[y - 1][x + 1] not in all_sign and board[y + 3][x - 3] not in all_sign:
                        SUMM_FORM += 1
                        ### SAJÁTUNK FELŐL DONTÜNK
                        if WHOSE == 'OWN':
                            if y - 2 >= 0 and x + 2 <= w - 1:
                                if board[y - 2][x + 2] not in all_sign:
                                    triv2nd_pos.add((x + 1, y - 1))
                            if y + 4 <= h - 1 and x - 4 >= 0:
                                if board[y + 4][x - 4] not in all_sign:
                                    triv2nd_pos.add((x - 3, y + 3))
                        ### ELLENFÉLNEK KELL DÖNTENIE
                        elif WHOSE == 'ENEMY':
                            ### NINCS A SZÉLÉHEZ KÖZEL
                            if y - 2 >= 0 and y + 4 <= h - 1 and x - 2 >= 0 and x + 4 <= w - 1:
                                if board[y - 2][x + 2] not in all_sign or board[y + 4][x - 4] not in all_sign:
                                    triv2nd_pos.add((x + 1, y - 1))
                                    triv2nd_pos.add((x - 3, y + 3))
                            ### TÁBLA JOBB SZÉLÉHEZ VAN KÖZEL (MERT AZ ELSŐ ESET NEM TELJESÜLT)
                            elif y - 2 >= 0 and x + 2 <= w - 1:
                                if board[y - 2][x + 2] not in all_sign:
                                    triv2nd_pos.add((x + 1, y - 1))
                                    triv2nd_pos.add((x - 3, y + 3))
                            ### TÁBLA BAL SZÉLÉHEZ VAN KÖZEL
                            elif y + 4 <= h - 1 and x - 4 >= 0:
                                if board[y + 4][x - 4] not in all_sign:
                                    triv2nd_pos.add((x + 1, y - 1))
                                    triv2nd_pos.add((x - 3, y + 3))
                ### ### 4-BŐL VAN 3 ÉS NYITOTTAK A VÉGEK
                if s == 3 and INCOMP == 1 and y + 4 <= h - 1 and y - 1 >= 0 and x - 4 >= 0 and x + 1 <= w - 1:
                    if board[y - 1][x + 1] not in all_sign and board[y + 4][x - 4] not in all_sign:
                        SUMM_FORM += 1
                        if WHOSE == 'OWN':
                            triv2nd_pos.add(pos_tmp)
                        elif WHOSE == 'ENEMY':
                            triv2nd_pos.add(pos_tmp)
                            triv2nd_pos.add((x - 4, y + 4))
                            triv2nd_pos.add((x + 1, y - 1))

    if triv2nd_pos != set():
        fill_zero(board)
        for i in triv2nd_pos:
            take_fix(board, i, 1)
    return SUMM_FORM


def force(board, SIGN, WHOSE):
    all_sign = {'o', 'x'}
    direction = {'h', 'v', 'd+', 'd-'}
    w = len(board[0])
    h = len(board)
    all_pos = []
    force_pos = set()
    for y in range(h):
        for x in range(w):
            if board[y][x] == 1:
                board[y][x] = SIGN
                direction = {'h', 'v', 'd+', 'd-'}
                all_pos.append(tuple(open3(board, direction, SIGN, 0)))
                all_pos.append(tuple(open3_incompl(board, direction, SIGN, 0)))
                all_pos.append(tuple(half_closed4(board, direction, SIGN, 0)))
                all_pos.append(tuple(closed4_incompl(board, direction, SIGN, 0)))
                if len(direction) < 3:
                    for i in range(len(all_pos)):
                        for j in range(i + 1, len(all_pos)):
                            for m in range(len(all_pos[i])):
                                # SAJÁT TÍPUSÚ NYERŐ ÁLLÁSOKON BELÜL KERES
                                if len(all_pos[i]) != 1 and m != len(all_pos[i]):
                                    for n in range(m + 1, len(all_pos[i])):
                                        for p in all_pos[i][m]:
                                            if p in all_pos[i][n]:
                                                force_pos.add(p)
                                # MÁS TÍPUSÚ NYERŐ ÁLLÁSOKKAL HASONLÍT ÖSSZE
                                for k in all_pos[j]:
                                    for p in all_pos[i][m]:
                                        if p in k:
                                            force_pos.add(p)
                board[y][x] = 1
                all_pos = []

    tmp = []
    for i in force_pos:
        if board[i[1]][i[0]] in all_sign:
            tmp.append(i)
    for i in range(len(tmp)):
        force_pos.remove(tmp[i])

    if WHOSE == 'OWN':
        if force_pos != set():
            fill_zero(board)
            for i in force_pos:
                take_fix(board, i, 1)
            return 1
        else:
            return 0

    elif WHOSE == 'ENEMY':
        def_pos = set()
        for i in force_pos:
            board[i[1]][i[0]] = SIGN
            tmp = open3(board, direction, SIGN, 1)
            if tmp != []:
                for j in range(len(tmp)):
                    def_pos = def_pos.union(tmp[j])

            tmp = open3_incompl(board, direction, SIGN, 1)
            if tmp != []:
                for j in range(len(tmp)):
                    def_pos = def_pos.union(tmp[j])

            tmp = half_closed4(board, direction, SIGN, 1)
            if tmp != []:
                for j in range(len(tmp)):
                    def_pos = def_pos.union(tmp[j])

            tmp = closed4_incompl(board, direction, SIGN, 1)
            if tmp != []:
                for j in range(len(tmp)):
                    def_pos = def_pos.union(tmp[j])
            board[i[1]][i[0]] = 1

        tmp = []
        for i in def_pos:
            if board[i[1]][i[0]] in all_sign:
                tmp.append(i)
        for i in range(len(tmp)):
            def_pos.remove(tmp[i])

        if def_pos != set():
            fill_zero(board)
            for i in def_pos:
                take_fix(board, i, 1)
            return 1
        else:
            return 0


def open3(board, direction, SIGN, IFDEFENCE):
    all_sign = {'o', 'x'}
    # all_sign.remove(SIGN)
    w = len(board[0])
    h = len(board)
    open3_pos = []
    for y in range(h):
        for x in range(w):
            if board[y][x] == SIGN:
                ### ### ### HORIZONTÁLIS ELLENŐRZÉS ### ### ###
                s = 1
                WRITTEN = 0
                ORIENTATION = 0
                if x + 2 <= w - 1:
                    for k in range(1, 3):
                        if board[y][x + k] == SIGN:
                            s += 1
                    ### ### 3 EGY SORBAN NYITOTT VÉGEKKEL
                    if s == 3 and x + 3 <= w - 1 and x - 1 >= 0:
                        if board[y][x - 1] not in all_sign and board[y][x + 3] not in all_sign:
                            ### TÁBLA BAL SZÉLÉN VAN
                            if x - 1 == 0:
                                if board[y][x + 4] not in all_sign:
                                    ORIENTATION = 'LEFT'
                            ### TÁBLA JOBB SZÉLÉN VAN
                            if x + 3 == w - 1:
                                if board[y][x - 2] not in all_sign:
                                    ORIENTATION = 'RIGHT'
                            ### TÁBLA KÖZEPÉN VAN
                            if x - 2 >= 0 and x + 4 <= w - 1:
                                # BALRÓL KORLÁTOS
                                if board[y][x - 2] in all_sign and board[y][x + 4] not in all_sign:
                                    ORIENTATION = 'LEFT'
                                # JOBBRÓL KORLÁTOS
                                if board[y][x - 2] not in all_sign and board[y][x + 4] in all_sign:
                                    ORIENTATION = 'RIGHT'
                                # TELJESEN NYITOTT MINDKÉT OLDALA
                                if board[y][x - 2] not in all_sign and board[y][x + 4] not in all_sign:
                                    ORIENTATION = 'MIDDLE'

                            if ORIENTATION == 'LEFT':
                                open3_pos.append({(x, y), (x + 1, y), (x + 2, y)})
                                if IFDEFENCE == 1:
                                    open3_pos[-1].add((x - 1, y))
                                    open3_pos[-1].add((x + 3, y))
                                    open3_pos[-1].add((x + 4, y))
                                WRITTEN = 1
                            elif ORIENTATION == 'RIGHT':
                                open3_pos.append({(x, y), (x + 1, y), (x + 2, y)})
                                if IFDEFENCE == 1:
                                    open3_pos[-1].add((x - 2, y))
                                    open3_pos[-1].add((x - 1, y))
                                    open3_pos[-1].add((x + 3, y))
                                WRITTEN = 1
                            elif ORIENTATION == 'MIDDLE':
                                open3_pos.append({(x, y), (x + 1, y), (x + 2, y)})
                                if IFDEFENCE == 1:
                                    open3_pos[-1].add((x - 1, y))
                                    open3_pos[-1].add((x + 3, y))
                                WRITTEN = 1

                            if WRITTEN == 1:
                                if 'h' in direction:
                                    direction.remove('h')

                ### ### ### VERTIKÁLIS ELLENŐRZÉS ### ### ###
                s = 1
                WRITTEN = 0
                ORIENTATION = 0
                if y + 2 <= h - 1:
                    for k in range(1, 3):
                        if board[y + k][x] == SIGN:
                            s += 1
                    ### ### 3 EGY SORBAN NYITOTT VÉGEKKEL
                    if s == 3 and y + 3 <= h - 1 and y - 1 >= 0:
                        if board[y - 1][x] not in all_sign and board[y + 3][x] not in all_sign:
                            ### TÁBLA TETEJÉN VAN
                            if y - 1 == 0:
                                if board[y + 4][x] not in all_sign:
                                    ORIENTATION = 'TOP'
                            ### TÁBLA ALJÁN VAN
                            if y + 3 == h - 1:
                                if board[y - 2][x] not in all_sign:
                                    ORIENTATION = 'BOTTOM'
                            ### TÁBLA KÖZEPÉN VAN
                            if y - 2 >= 0 and y + 4 <= h - 1:
                                # FELÜLRŐL KORLÁTOS
                                if board[y - 2][x] in all_sign and board[y + 4][x] not in all_sign:
                                    ORIENTATION = 'TOP'
                                # ALULRÓL KORLÁTOS
                                if board[y - 2][x] not in all_sign and board[y + 4][x] in all_sign:
                                    ORIENTATION = 'BOTTOM'
                                # TELJESEN NYITOTT MINDKÉT OLDALON
                                if board[y - 2][x] not in all_sign and board[y + 4][x] not in all_sign:
                                    ORIENTATION = 'MIDDLE'

                            if ORIENTATION == 'TOP':
                                open3_pos.append({(x, y), (x, y + 1), (x, y + 2)})
                                if IFDEFENCE == 1:
                                    open3_pos[-1].add((x, y - 1))
                                    open3_pos[-1].add((x, y + 3))
                                    open3_pos[-1].add((x, y + 4))
                                WRITTEN = 1
                            elif ORIENTATION == 'BOTTOM':
                                open3_pos.append({(x, y), (x, y + 1), (x, y + 2)})
                                if IFDEFENCE == 1:
                                    open3_pos[-1].add((x, y - 2))
                                    open3_pos[-1].add((x, y - 1))
                                    open3_pos[-1].add((x, y + 3))
                                WRITTEN = 1
                            elif ORIENTATION == 'MIDDLE':
                                open3_pos.append({(x, y), (x, y + 1), (x, y + 2)})
                                if IFDEFENCE == 1:
                                    open3_pos[-1].add((x, y - 1))
                                    open3_pos[-1].add((x, y + 3))
                                WRITTEN = 1

                            if WRITTEN == 1:
                                if 'v' in direction:
                                    direction.remove('v')

                ### ### ### DIAGONÁLIS+ ELLENŐRZÉS ### ### ###
                s = 1
                WRITTEN = 0
                ORIENTATION = 0
                if x + 2 <= w - 1 and y + 2 <= h - 1:
                    for k in range(1, 3):
                        if board[y + k][x + k] == SIGN:
                            s += 1
                    ### ### 3 EGY SORBAN NYITOTT VÉGEKKEL
                    if s == 3 and x - 1 >= 0 and x + 3 <= w - 1 and y + 3 <= h - 1 and y - 1 >= 0:
                        if board[y - 1][x - 1] not in all_sign and board[y + 3][x + 3] not in all_sign:
                            ### TÁBLA KORLÁTOZZA A BAL FELSŐ SARKÁT
                            if x - 1 == 0 and y - 1 == 0:
                                if board[y + 4][x + 4] not in all_sign:
                                    ORIENTATION = 'LEFT'
                            elif x - 1 == 0 and y + 4 <= h - 1:
                                if board[y + 4][x + 4] not in all_sign:
                                    ORIENTATION = 'LEFT'
                            elif y - 1 == 0 and x + 4 <= w - 1:
                                if board[y + 4][x + 4] not in all_sign:
                                    ORIENTATION = 'LEFT'
                            ### TÁBLA KORLÁTOZZA A JOBB ALSÓ SARKÁT
                            if x + 3 == w - 1 and y + 3 == h - 1:
                                if board[y - 2][x - 2] not in all_sign:
                                    ORIENTATION = 'RIGHT'
                            elif x + 3 == w - 1 and y - 2 >= 0:
                                if board[y - 2][x - 2] not in all_sign:
                                    ORIENTATION = 'RIGHT'
                            elif y + 3 == h - 1 and x - 2 >= 0:
                                if board[y - 2][x - 2] not in all_sign:
                                    ORIENTATION = 'RIGHT'
                            ### TÁBLA KÖZEPÉN VAN
                            if x - 2 >= 0 and x + 4 <= w - 1 and y - 2 >= 0 and y + 4 <= h - 1:
                                # BALRÓL KORLÁTOS
                                if board[y - 2][x - 2] in all_sign and board[y + 4][x + 4] not in all_sign:
                                    ORIENTATION = 'LEFT'
                                # JOBBRÓL KORLÁTOS
                                if board[y - 2][x - 2] not in all_sign and board[y + 4][x + 4] in all_sign:
                                    ORIENTATION = 'RIGHT'
                                # TELJESEN NYITOTT MINDKÉT SARKA
                                if board[y - 2][x - 2] not in all_sign and board[y + 4][x + 4] not in all_sign:
                                    ORIENTATION = 'MIDDLE'

                            if ORIENTATION == 'LEFT':
                                open3_pos.append({(x, y), (x + 1, y + 1), (x + 2, y + 2)})
                                if IFDEFENCE == 1:
                                    open3_pos[-1].add((x - 1, y - 1))
                                    open3_pos[-1].add((x + 3, y + 3))
                                    open3_pos[-1].add((x + 4, y + 4))
                                WRITTEN = 1
                            elif ORIENTATION == 'RIGHT':
                                open3_pos.append({(x, y), (x + 1, y + 1), (x + 2, y + 2)})
                                if IFDEFENCE == 1:
                                    open3_pos[-1].add((x - 2, y - 2))
                                    open3_pos[-1].add((x - 1, y - 1))
                                    open3_pos[-1].add((x + 3, y + 3))
                                WRITTEN = 1
                            elif ORIENTATION == 'MIDDLE':
                                open3_pos.append({(x, y), (x + 1, y + 1), (x + 2, y + 2)})
                                if IFDEFENCE == 1:
                                    open3_pos[-1].add((x - 1, y - 1))
                                    open3_pos[-1].add((x + 3, y + 3))
                                WRITTEN = 1

                        if WRITTEN == 1:
                            if 'd+' in direction:
                                direction.remove('d+')

                ### ### ### DIAGONÁLIS- ELLENŐRZÉS ### ### ###
                s = 1
                WRITTEN = 0
                ORIENTATION = 0
                if x - 2 >= 0 and y + 2 <= h - 1:
                    for k in range(1, 3):
                        if board[y + k][x - k] == SIGN:
                            s += 1
                    ### ### 3 EGY SORBAN NYITOTT VÉGEKKEL
                    if s == 3 and x + 1 <= w - 1 and x - 3 >= 0 and y + 3 <= h - 1 and y - 1 >= 0:
                        if board[y - 1][x + 1] not in all_sign and board[y + 3][x - 3] not in all_sign:
                            ### TÁBLA KORLÁTOZZA A JOBB FELSŐ SARKÁT
                            if x + 1 == w - 1 and y - 1 == 0:
                                if board[y + 4][x - 4] not in all_sign:
                                    ORIENTATION = 'RIGHT'
                            elif x + 1 == w - 1 and y + 4 <= h - 1:
                                if board[y + 4][x - 4] not in all_sign:
                                    ORIENTATION = 'RIGHT'
                            elif y - 1 == 0 and x - 4 >= 0:
                                if board[y + 4][x - 4] not in all_sign:
                                    ORIENTATION = 'RIGHT'
                            ### TÁBLA KORLÁTOZZA A BAL ALSÓ SARKÁT
                            if x - 3 == 0 and y + 3 == h - 1:
                                if board[y - 2][x + 2] not in all_sign:
                                    ORIENTATION = 'LEFT'
                            elif x - 3 == 0 and y - 2 >= 0:
                                if board[y - 2][x + 2] not in all_sign:
                                    ORIENTATION = 'LEFT'
                            elif y + 3 == h - 1 and x + 2 <= w - 1:
                                if board[y - 2][x + 2] not in all_sign:
                                    ORIENTATION = 'LEFT'
                            ### TÁBLA KÖZEPÉN VAN
                            if x + 2 <= w - 1 and x - 4 >= 0 and y - 2 >= 0 and y + 4 <= h - 1:
                                # JOBBRÓL KORLÁTOS
                                if board[y - 2][x + 2] in all_sign and board[y + 4][x - 4] not in all_sign:
                                    ORIENTATION = 'RIGHT'
                                # BALRÓL KORLÁTOS
                                if board[y - 2][x + 2] not in all_sign and board[y + 4][x - 4] in all_sign:
                                    ORIENTATION = 'LEFT'
                                # TELJESEN NYITOTT MINDKÉT SARKA
                                if board[y - 2][x + 2] not in all_sign and board[y + 4][x - 4] not in all_sign:
                                    ORIENTATION = 'MIDDLE'

                            if ORIENTATION == 'RIGHT':
                                open3_pos.append({(x, y), (x - 1, y + 1), (x - 2, y + 2)})
                                if IFDEFENCE == 1:
                                    open3_pos[-1].add((x + 1, y - 1))
                                    open3_pos[-1].add((x - 3, y + 3))
                                    open3_pos[-1].add((x - 4, y + 4))
                                WRITTEN = 1
                            elif ORIENTATION == 'LEFT':
                                open3_pos.append({(x, y), (x - 1, y + 1), (x - 2, y + 2)})
                                if IFDEFENCE == 1:
                                    open3_pos[-1].add((x + 2, y - 2))
                                    open3_pos[-1].add((x + 1, y - 1))
                                    open3_pos[-1].add((x - 3, y + 3))
                                WRITTEN = 1
                            elif ORIENTATION == 'MIDDLE':
                                open3_pos.append({(x, y), (x - 1, y + 1), (x - 2, y + 2)})
                                if IFDEFENCE == 1:
                                    open3_pos[-1].add((x + 1, y - 1))
                                    open3_pos[-1].add((x - 3, y + 3))
                                WRITTEN = 1

                        if WRITTEN == 1:
                            if 'd-' in direction:
                                direction.remove('d-')

    return open3_pos


def open3_incompl(board, direction, SIGN, IFDEFENCE):
    all_sign = {'o', 'x'}
    all_sign.remove(SIGN)
    w = len(board[0])
    h = len(board)
    open3_incompl_pos = []
    for y in range(h):
        for x in range(w):
            if board[y][x] == SIGN:
                ### ### ### HORIZONTÁLIS ELLENŐRZÉS ### ### ###
                s = 1
                pos_tmp = []
                void = 0
                if x + 3 <= w - 1:
                    for k in range(1, 4):
                        if board[y][x + k] == SIGN:
                            s += 1
                        elif board[y][x + k] not in all_sign and k != 3:
                            void = k
                    ### ### HIÁNYOS 3-AS
                    if s == 3 and void != 0 and x + 4 <= w - 1 and x - 1 >= 0:
                        if board[y][x - 1] not in all_sign and board[y][x + 4] not in all_sign:
                            pos_tmp.append((x, y))
                            pos_tmp.append((x + 1, y))
                            pos_tmp.append((x + 2, y))
                            pos_tmp.append((x + 3, y))
                            if IFDEFENCE == 0:
                                pos_tmp.pop(void)
                            else:
                                pos_tmp.append((x - 1, y))
                                pos_tmp.append((x + 4, y))
                            open3_incompl_pos.append(pos_tmp)
                            if 'h' in direction:
                                direction.remove('h')

                ### ### ### VERTIKÁLIS ELLENŐRZÉS ### ### ###
                s = 1
                pos_tmp = []
                void = 0
                if y + 3 <= h - 1:
                    for k in range(1, 4):
                        if board[y + k][x] == SIGN:
                            s += 1
                        elif board[y + k][x] not in all_sign and k != 3:
                            void = k
                    ### ### HIÁNYOS 3-AS
                    if s == 3 and void != 0 and y + 4 <= h - 1 and y - 1 >= 0:
                        if board[y - 1][x] not in all_sign and board[y + 4][x] not in all_sign:
                            pos_tmp.append((x, y))
                            pos_tmp.append((x, y + 1))
                            pos_tmp.append((x, y + 2))
                            pos_tmp.append((x, y + 3))
                            if IFDEFENCE == 0:
                                pos_tmp.pop(void)
                            else:
                                pos_tmp.append((x, y - 1))
                                pos_tmp.append((x, y + 4))
                            open3_incompl_pos.append(pos_tmp)
                            if 'v' in direction:
                                direction.remove('v')

                ### ### ### DIAGONÁLIS+ ELLENŐRZÉS ### ### ###
                s = 1
                pos_tmp = []
                void = 0
                if x + 3 <= w - 1 and y + 3 <= h - 1:
                    for k in range(1, 4):
                        if board[y + k][x + k] == SIGN:
                            s += 1
                        elif board[y + k][x + k] not in all_sign and k != 3:
                            void = k
                    ### ### HIÁNYOS 3-AS
                    if s == 3 and void != 0 and x + 4 <= w - 1 and x - 1 >= 0 and y + 4 <= h - 1 and y - 1 >= 0:
                        if board[y - 1][x - 1] not in all_sign and board[y + 4][x + 4] not in all_sign:
                            pos_tmp.append((x, y))
                            pos_tmp.append((x + 1, y + 1))
                            pos_tmp.append((x + 2, y + 2))
                            pos_tmp.append((x + 3, y + 3))
                            if IFDEFENCE == 0:
                                pos_tmp.pop(void)
                            else:
                                pos_tmp.append((x - 1, y - 1))
                                pos_tmp.append((x + 4, y + 4))
                            open3_incompl_pos.append(pos_tmp)
                            if 'd+' in direction:
                                direction.remove('d+')

                ### ### ### DIAGONÁLIS- ELLENŐRZÉS ### ### ###
                s = 1
                pos_tmp = []
                void = 0
                if x - 3 >= 0 and y + 3 <= h - 1:
                    for k in range(1, 4):
                        if board[y + k][x - k] == SIGN:
                            s += 1
                        elif board[y + k][x - k] not in all_sign and k != 3:
                            void = k
                    ### ### HIÁNYOS 3-AS
                    if s == 3 and void != 0 and x - 4 >= 0 and x + 1 <= w - 1 and y + 4 <= h - 1 and y - 1 >= 0:
                        if board[y - 1][x + 1] not in all_sign and board[y + 4][x - 4] not in all_sign:
                            pos_tmp.append((x, y))
                            pos_tmp.append((x - 1, y + 1))
                            pos_tmp.append((x - 2, y + 2))
                            pos_tmp.append((x - 3, y + 3))
                            if IFDEFENCE == 0:
                                pos_tmp.pop(void)
                            else:
                                pos_tmp.append((x + 1, y - 1))
                                pos_tmp.append((x - 4, y + 4))
                            open3_incompl_pos.append(pos_tmp)
                            if 'd-' in direction:
                                direction.remove('d-')

    for i in range(len(open3_incompl_pos)):
        open3_incompl_pos[i] = set(open3_incompl_pos[i])
    return open3_incompl_pos


def half_closed4(board, direction, SIGN, IFDEFENCE):
    all_sign = {'o', 'x'}
    w = len(board[0])
    h = len(board)
    half_closed4_pos = []
    for y in range(h):
        for x in range(w):
            if board[y][x] == SIGN:
                ### ### ### HORIZONTÁLIS ELLENŐRZÉS ### ### ###
                if x + 3 <= w - 1:
                    s = 1
                    WRITTEN = 0
                    for k in range(1, 4):
                        if board[y][x + k] == SIGN:
                            s += 1
                    if s == 4:
                        ### ### 4 EGY SORBAN LEGFELJEBB EGYIK VÉGE ZÁRT
                        if x + 4 <= w - 1 and x - 1 >= 0:
                            if board[y][x - 1] not in all_sign or board[y][x + 4] not in all_sign:
                                half_closed4_pos.append({(x, y), (x + 1, y), (x + 2, y), (x + 3, y)})
                                if IFDEFENCE == 1:
                                    if board[y][x - 1] not in all_sign:
                                        half_closed4_pos[-1].add((x - 1, y))
                                    else:
                                        half_closed4_pos[-1].add((x + 4, y))
                                WRITTEN = 1
                        elif x - 1 == -1:
                            if board[y][x + 4] not in all_sign:
                                half_closed4_pos.append({(x, y), (x + 1, y), (x + 2, y), (x + 3, y)})
                                if IFDEFENCE == 1:
                                    half_closed4_pos[-1].add((x + 4, y))
                                WRITTEN = 1
                        elif x + 4 == w:
                            if board[y][x - 1] not in all_sign:
                                half_closed4_pos.append({(x, y), (x + 1, y), (x + 2, y), (x + 3, y)})
                                if IFDEFENCE == 1:
                                    half_closed4_pos[-1].add((x - 1, y))
                                WRITTEN = 1
                        if WRITTEN == 1:
                            if 'h' in direction:
                                direction.remove('h')

                ### ### ### VERTIKÁLIS ELLENŐRZÉS ### ### ###
                if y + 3 <= h - 1:
                    s = 1
                    WRITTEN = 0
                    for k in range(1, 4):
                        if board[y + k][x] == SIGN:
                            s += 1
                    if s == 4:
                        ### ### 4 EGY SORBAN LEGFELJEBB EGYIK VÉGE ZÁRT
                        if y + 4 <= h - 1 and y - 1 >= 0:
                            if board[y - 1][x] not in all_sign or board[y + 4][x] not in all_sign:
                                half_closed4_pos.append({(x, y), (x, y + 1), (x, y + 2), (x, y + 3)})
                                if IFDEFENCE == 1:
                                    if board[y - 1][x] not in all_sign:
                                        half_closed4_pos[-1].add((x, y - 1))
                                    else:
                                        half_closed4_pos[-1].add((x, y + 4))
                                WRITTEN = 1
                        elif y - 1 == -1:
                            if board[y + 4][x] not in all_sign:
                                half_closed4_pos.append({(x, y), (x, y + 1), (x, y + 2), (x, y + 3)})
                                if IFDEFENCE == 1:
                                    half_closed4_pos[-1].add((x, y + 4))
                                WRITTEN = 1
                        elif y + 4 == h:
                            if board[y - 1][x] not in all_sign:
                                half_closed4_pos.append({(x, y), (x, y + 1), (x, y + 2), (x, y + 3)})
                                if IFDEFENCE == 1:
                                    half_closed4_pos[-1].add((x, y - 1))
                                WRITTEN = 1
                        if WRITTEN == 1:
                            if 'v' in direction:
                                direction.remove('v')

                ### ### ### DIAGONÁLIS+ ELLENŐRZÉS ### ### ###
                if x + 3 <= w - 1 and y + 3 <= h - 1:
                    s = 1
                    WRITTEN = 0
                    for k in range(1, 4):
                        if board[y + k][x + k] == SIGN:
                            s += 1
                    if s == 4:
                        ### ### 4 EGY SORBAN LEGFELJEBB EGYIK VÉGE ZÁRT
                        if x + 4 <= w - 1 and x - 1 >= 0 and y + 4 <= h - 1 and y - 1 >= 0:
                            if board[y - 1][x - 1] not in all_sign or board[y + 4][x + 4] not in all_sign:
                                half_closed4_pos.append({(x, y), (x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)})
                                if IFDEFENCE == 1:
                                    if board[y - 1][x - 1] not in all_sign:
                                        half_closed4_pos[-1].add((x - 1, y - 1))
                                    else:
                                        half_closed4_pos[-1].add((x + 4, y + 4))
                                WRITTEN = 1
                        elif (x - 1 == -1 and y + 4 <= h - 1) or (y - 1 == -1 and x + 4 <= w - 1):
                            if board[y + 4][x + 4] not in all_sign:
                                half_closed4_pos.append({(x, y), (x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)})
                                if IFDEFENCE == 1:
                                    half_closed4_pos[-1].add((x + 4, y + 4))
                                WRITTEN = 1
                        elif (x + 4 == w and y - 1 >= 0) or (y + 4 == h and x - 1 >= 0):
                            if board[y - 1][x - 1] not in all_sign:
                                half_closed4_pos.append({(x, y), (x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)})
                                if IFDEFENCE == 1:
                                    half_closed4_pos[-1].add((x - 1, y - 1))
                                WRITTEN = 1
                        if WRITTEN == 1:
                            if 'd+' in direction:
                                direction.remove('d+')

                ### ### ### DIAGONÁLIS- ELLENŐRZÉS ### ### ###
                if x - 3 >= 0 and y + 3 <= h - 1:
                    s = 1
                    WRITTEN = 0
                    for k in range(1, 4):
                        if board[y + k][x - k] == SIGN:
                            s += 1
                    if s == 4:
                        ### ### 4 EGY SORBAN LEGFELJEBB EGYIK VÉGE ZÁRT
                        if x - 4 >= 0 and x + 1 <= w - 1 and y + 4 <= h - 1 and y - 1 >= 0:
                            if board[y - 1][x + 1] not in all_sign or board[y + 4][x - 4] not in all_sign:
                                half_closed4_pos.append({(x, y), (x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)})
                                if IFDEFENCE == 1:
                                    if board[y - 1][x + 1] not in all_sign:
                                        half_closed4_pos[-1].add((x + 1, y - 1))
                                    else:
                                        half_closed4_pos[-1].add((x - 4, y + 4))
                                WRITTEN = 1
                        elif (x + 1 == w and y + 4 <= h - 1) or (y - 1 == -1 and x - 4 >= 0):
                            if board[y + 4][x - 4] not in all_sign:
                                half_closed4_pos.append({(x, y), (x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)})
                                if IFDEFENCE == 1:
                                    half_closed4_pos[-1].add((x - 4, y + 4))
                                WRITTEN = 1
                        elif (x - 4 == -1 and y - 1 >= 0) or (y + 4 == h and x + 1 <= w - 1):
                            if board[y - 1][x + 1] not in all_sign:
                                half_closed4_pos.append({(x, y), (x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)})
                                if IFDEFENCE == 1:
                                    half_closed4_pos[-1].add((x + 1, y - 1))
                                WRITTEN = 1
                        if WRITTEN == 1:
                            if 'd-' in direction:
                                direction.remove('d-')
    return half_closed4_pos


def closed4_incompl(board, direction, SIGN, IFDEFENCE):
    all_sign = {'o', 'x'}
    w = len(board[0])
    h = len(board)
    closed4_incompl_pos = []
    for y in range(h):
        for x in range(w):
            if board[y][x] == SIGN:
                ### ### ### HORIZONTÁLIS ELLENŐRZÉS ### ### ###
                s = 1
                pos_tmp = []
                void = 0
                if x + 4 <= w - 1:
                    for k in range(1, 5):
                        if board[y][x + k] == SIGN:
                            s += 1
                        elif board[y][x + k] not in all_sign and k != 4:
                            void = k
                    ### ### HIÁNYOS 4-ES, MINDEGY, HOGY MI VAN A SZÉLEIN
                    if s == 4 and void != 0:
                        pos_tmp.append((x, y))
                        pos_tmp.append((x + 1, y))
                        pos_tmp.append((x + 2, y))
                        pos_tmp.append((x + 3, y))
                        pos_tmp.append((x + 4, y))
                        if IFDEFENCE == 0:
                            pos_tmp.pop(void)
                        closed4_incompl_pos.append(pos_tmp)
                        if 'h' in direction:
                            direction.remove('h')

                ### ### ### VERTIKÁLIS ELLENŐRZÉS ### ### ###
                s = 1
                pos_tmp = []
                void = 0
                if y + 4 <= h - 1:
                    for k in range(1, 5):
                        if board[y + k][x] == SIGN:
                            s += 1
                        elif board[y + k][x] not in all_sign and k != 4:
                            void = k
                    ### ### HIÁNYOS 4-ES, MINDEGY, HOGY MI VAN A SZÉLEIN
                    if s == 4 and void != 0:
                        pos_tmp.append((x, y))
                        pos_tmp.append((x, y + 1))
                        pos_tmp.append((x, y + 2))
                        pos_tmp.append((x, y + 3))
                        pos_tmp.append((x, y + 4))
                        if IFDEFENCE == 0:
                            pos_tmp.pop(void)
                        closed4_incompl_pos.append(pos_tmp)
                        if 'v' in direction:
                            direction.remove('v')

                ### ### ### DIAGONÁLIS+ ELLENŐRZÉS ### ### ###
                s = 1
                pos_tmp = []
                void = 0
                if x + 4 <= w - 1 and y + 4 <= h - 1:
                    for k in range(1, 5):
                        if board[y + k][x + k] == SIGN:
                            s += 1
                        elif board[y + k][x + k] not in all_sign and k != 4:
                            void = k
                    ### ### HIÁNYOS 4-ES, MINDEGY, HOGY MI VAN A SZÉLEIN
                    if s == 4 and void != 0:
                        pos_tmp.append((x, y))
                        pos_tmp.append((x + 1, y + 1))
                        pos_tmp.append((x + 2, y + 2))
                        pos_tmp.append((x + 3, y + 3))
                        pos_tmp.append((x + 4, y + 4))
                        if IFDEFENCE == 0:
                            pos_tmp.pop(void)
                        closed4_incompl_pos.append(pos_tmp)
                        if 'd+' in direction:
                            direction.remove('d+')

                ### ### ### DIAGONÁLIS- ELLENŐRZÉS ### ### ###
                s = 1
                pos_tmp = []
                void = 0
                if x - 4 >= 0 and y + 4 <= h - 1:
                    for k in range(1, 5):
                        if board[y + k][x - k] == SIGN:
                            s += 1
                        elif board[y + k][x - k] not in all_sign and k != 4:
                            void = k
                    ### ### HIÁNYOS 4-ES, MINDEGY, HOGY MI VAN A SZÉLEIN
                    if s == 4 and void != 0:
                        pos_tmp.append((x, y))
                        pos_tmp.append((x - 1, y + 1))
                        pos_tmp.append((x - 2, y + 2))
                        pos_tmp.append((x - 3, y + 3))
                        pos_tmp.append((x - 4, y + 4))
                        if IFDEFENCE == 0:
                            pos_tmp.pop(void)
                        closed4_incompl_pos.append(pos_tmp)
                        if 'd-' in direction:
                            direction.remove('d-')

    for i in range(len(closed4_incompl_pos)):
        closed4_incompl_pos[i] = set(closed4_incompl_pos[i])
    return closed4_incompl_pos


def double4_inline(board, SIGN, IFDEFENCE):
    all_sign = {'o', 'x'}
    w = len(board[0])
    h = len(board)
    double4_inline_pos = set()
    for y in range(h):
        for x in range(w):
            if board[y][x] == SIGN:
                ### ### ### HORIZONTÁLIS ELLENŐRZÉS ### ### ###
                s = 0
                void = ()
                if x + 6 <= w - 1:
                    if board[y][x + 6] == SIGN and board[y][x + 1] not in all_sign and board[y][x + 5] not in all_sign:
                        for k in (2, 3, 4):
                            if board[y][x + k] == SIGN:
                                s += 1
                            elif board[y][x + k] not in all_sign:
                                void = (x + k, y)
                        if s == 2 and void != ():
                            double4_inline_pos.add(void)
                            if IFDEFENCE == 1:
                                double4_inline_pos.add((x + 1, y))
                                double4_inline_pos.add((x + 5, y))

                ### ### ### VERTIKÁLIS ELLENŐRZÉS ### ### ###
                s = 0
                void = ()
                if y + 6 <= h - 1:
                    if board[y + 6][x] == SIGN and board[y + 1][x] not in all_sign and board[y + 5][x] not in all_sign:
                        for k in (2, 3, 4):
                            if board[y + k][x] == SIGN:
                                s += 1
                            elif board[y + k][x] not in all_sign:
                                void = (x, y + k)
                        if s == 2 and void != ():
                            double4_inline_pos.add(void)
                            if IFDEFENCE == 1:
                                double4_inline_pos.add((x, y + 1))
                                double4_inline_pos.add((x, y + 5))

                ### ### ### DIAGONÁLIS+ ELLENŐRZÉS ### ### ###
                s = 0
                void = ()
                if x + 6 <= w - 1 and y + 6 <= h - 1:
                    if board[y + 6][x + 6] == SIGN and board[y + 1][x + 1] not in all_sign and board[y + 5][
                        x + 5] not in all_sign:
                        for k in (2, 3, 4):
                            if board[y + k][x + k] == SIGN:
                                s += 1
                            elif board[y + k][x + k] not in all_sign:
                                void = (x + k, y + k)
                        if s == 2 and void != ():
                            double4_inline_pos.add(void)
                            if IFDEFENCE == 1:
                                double4_inline_pos.add((x + 1, y + 1))
                                double4_inline_pos.add((x + 5, y + 5))

                ### ### ### DIAGONÁLIS- ELLENŐRZÉS ### ### ###
                s = 0
                void = ()
                if x - 6 >= 0 and y + 6 <= h - 1:
                    if board[y + 6][x - 6] == SIGN and board[y + 1][x - 1] not in all_sign and board[y + 5][
                        x - 5] not in all_sign:
                        for k in (2, 3, 4):
                            if board[y + k][x - k] == SIGN:
                                s += 1
                            elif board[y + k][x - k] not in all_sign:
                                void = (x - k, y + k)
                        if s == 2 and void != ():
                            double4_inline_pos.add(void)
                            if IFDEFENCE == 1:
                                double4_inline_pos.add((x - 1, y + 1))
                                double4_inline_pos.add((x - 5, y + 5))
    return double4_inline_pos


def force_new(board, SIGN, WHOSE, LEVEL):
    all_sign = {'o', 'x'}
    direction = {'h', 'v', 'd+', 'd-'}
    w = len(board[0])
    h = len(board)
    force_pos = set()
    for y in range(h):
        for x in range(w):
            if str(board[y][x]).isalpha() == False:
                if board[y][x] > 0:
                    FORCE4_tmp = 0
                    tmp = board[y][x]
                    board[y][x] = SIGN
                    direction = {'h', 'v', 'd+', 'd-'}
                    open3(board, direction, SIGN, 0)
                    open3_incompl(board, direction, SIGN, 0)
                    if half_closed4(board, direction, SIGN, 0) != []:
                        FORCE4_tmp = 1
                    if closed4_incompl(board, direction, SIGN, 0) != []:
                        FORCE4_tmp = 1
                    if len(direction) < 3:
                        if LEVEL == 'STRONG':
                            if FORCE4_tmp == 1:
                                force_pos.add((x, y))
                        elif LEVEL == 'WEAK':
                            force_pos.add((x, y))
                    board[y][x] = tmp

    if force_pos != set() and WHOSE == 'ENEMY':
        force_pos_tmp = set()
        for i in force_pos:
            take_fix(board, i, SIGN)

            pos_tmp = open3(board, direction, SIGN, 1)
            for j in pos_tmp:
                force_pos_tmp = force_pos_tmp.union(j)

            pos_tmp = open3_incompl(board, direction, SIGN, 1)
            for j in pos_tmp:
                force_pos_tmp = force_pos_tmp.union(j)

            pos_tmp = half_closed4(board, direction, SIGN, 1)
            for j in pos_tmp:
                force_pos_tmp = force_pos_tmp.union(j)

            pos_tmp = closed4_incompl(board, direction, SIGN, 1)
            for j in pos_tmp:
                force_pos_tmp = force_pos_tmp.union(j)

            take_fix(board, i, 1)
        force_pos = force_pos.union(force_pos_tmp)

    if WHOSE == 'OWN':
        force_pos = force_pos.union(double4_inline(board, SIGN, 0))
    else:
        force_pos = force_pos.union(double4_inline(board, SIGN, 1))

    if force_pos != set():
        fill_zero(board)
        for i in force_pos:
            if board[i[1]][i[0]] not in all_sign:
                take_fix(board, i, 1)
        return 1
    else:
        return 0


def mini_force(board, SIGN, WHOSE):
    all_sign = {'o', 'x'}
    for i in all_sign:
        if i != SIGN:
            ENEMY = i
    w = len(board[0])
    h = len(board)
    mini_force_pos = set()
    for y in range(h):
        for x in range(w):
            if board[y][x] == SIGN:
                ### ### ### HORIZONTÁLIS ELLENŐRZÉS ### ### ###
                s = 1
                void = []
                for k in range(1, 5):
                    if x + k <= w - 1:
                        if board[y][x + k] == SIGN:
                            s += 1
                        elif board[y][x + k] == ENEMY:
                            s = 0
                            break
                        else:
                            void.append((x + k, y))
                        if s == 3:
                            break
                if s == 3:
                    # l1 : BALRA ELSŐ MEZŐ VIZSGÁLATÁHOZ
                    # l2 : BALRA MÁSODIK MEZŐ VIZSGÁLATÁHOZ
                    # r1 : JOBBRA ELSŐ MEZŐ VIZSGÁLATÁHOZ
                    # r2 : JOBBRA MÁSODIK MEZŐ VIZSGÁLATÁHOZ
                    if len(void) == 2:
                        mini_force_pos.add(void[0])
                        mini_force_pos.add(void[1])
                    elif len(void) == 1:
                        l1 = 0
                        r1 = 0
                        if x - 1 >= 0:
                            l1 = 1
                        if x + 4 <= w - 1:
                            r1 = 1

                        if l1 == 1:
                            if board[y][x - 1] not in all_sign:
                                mini_force_pos.add(void[0])
                                mini_force_pos.add((x - 1, y))
                        if r1 == 1:
                            if board[y][x + 4] not in all_sign:
                                mini_force_pos.add(void[0])
                                mini_force_pos.add((x + 4, y))
                    elif len(void) == 0:
                        l1 = 0
                        l2 = 0
                        r1 = 0
                        r2 = 0
                        if x - 2 >= 0:
                            l1 = 1
                            l2 = 1
                        elif x - 1 >= 0:
                            l1 = 1
                        if x + 4 <= w - 1:
                            r1 = 1
                            r2 = 1
                        elif x + 3 <= w - 1:
                            r1 = 1

                        if l2 == 1:
                            if board[y][x - 1] not in all_sign and board[y][x - 2] not in all_sign:
                                mini_force_pos.add((x - 1, y))
                                mini_force_pos.add((x - 2, y))

                        if l1 == 1 and r1 == 1:
                            if board[y][x - 1] not in all_sign and board[y][x + 3] not in all_sign:
                                mini_force_pos.add((x - 1, y))
                                mini_force_pos.add((x + 3, y))

                        if r2 == 1:
                            if board[y][x + 3] not in all_sign and board[y][x + 4] not in all_sign:
                                mini_force_pos.add((x + 3, y))
                                mini_force_pos.add((x + 4, y))

                ### ### ### VERTIKÁLIS ELLENŐRZÉS ### ### ###
                s = 1
                void = []
                for k in range(1, 5):
                    if y + k <= h - 1:
                        if board[y + k][x] == SIGN:
                            s += 1
                        elif board[y + k][x] == ENEMY:
                            s = 0
                            break
                        else:
                            void.append((x, y + k))
                        if s == 3:
                            break
                if s == 3:
                    # l1 : BALRA ELSŐ MEZŐ VIZSGÁLATÁHOZ
                    # l2 : BALRA MÁSODIK MEZŐ VIZSGÁLATÁHOZ
                    # r1 : JOBBRA ELSŐ MEZŐ VIZSGÁLATÁHOZ
                    # r2 : JOBBRA MÁSODIK MEZŐ VIZSGÁLATÁHOZ
                    if len(void) == 2:
                        mini_force_pos.add(void[0])
                        mini_force_pos.add(void[1])
                    elif len(void) == 1:
                        l1 = 0
                        r1 = 0
                        if y - 1 >= 0:
                            l1 = 1
                        if y + 4 <= h - 1:
                            r1 = 1

                        if l1 == 1:
                            if board[y - 1][x] not in all_sign:
                                mini_force_pos.add(void[0])
                                mini_force_pos.add((x, y - 1))
                        if r1 == 1:
                            if board[y + 4][x] not in all_sign:
                                mini_force_pos.add(void[0])
                                mini_force_pos.add((x, y + 4))
                    elif len(void) == 0:
                        l1 = 0
                        l2 = 0
                        r1 = 0
                        r2 = 0
                        if y - 2 >= 0:
                            l1 = 1
                            l2 = 1
                        elif y - 1 >= 0:
                            l1 = 1
                        if y + 4 <= h - 1:
                            r1 = 1
                            r2 = 1
                        elif y + 3 <= h - 1:
                            r1 = 1

                        if l2 == 1:
                            if board[y - 1][x] not in all_sign and board[y - 2][x] not in all_sign:
                                mini_force_pos.add((x, y - 1))
                                mini_force_pos.add((x, y - 2))

                        if l1 == 1 and r1 == 1:
                            if board[y - 1][x] not in all_sign and board[y + 3][x] not in all_sign:
                                mini_force_pos.add((x, y - 1))
                                mini_force_pos.add((x, y + 3))

                        if r2 == 1:
                            if board[y + 3][x] not in all_sign and board[y + 4][x] not in all_sign:
                                mini_force_pos.add((x, y + 3))
                                mini_force_pos.add((x, y + 4))

                ### ### ### DIAGONÁLIS+ ELLENŐRZÉS ### ### ###
                s = 1
                void = []
                for k in range(1, 5):
                    if x + k <= w - 1 and y + k <= h - 1:
                        if board[y + k][x + k] == SIGN:
                            s += 1
                        elif board[y + k][x + k] == ENEMY:
                            s = 0
                            break
                        else:
                            void.append((x + k, y + k))
                        if s == 3:
                            break
                if s == 3:
                    # l1 : BALRA ELSŐ MEZŐ VIZSGÁLATÁHOZ
                    # l2 : BALRA MÁSODIK MEZŐ VIZSGÁLATÁHOZ
                    # r1 : JOBBRA ELSŐ MEZŐ VIZSGÁLATÁHOZ
                    # r2 : JOBBRA MÁSODIK MEZŐ VIZSGÁLATÁHOZ
                    if len(void) == 2:
                        mini_force_pos.add(void[0])
                        mini_force_pos.add(void[1])
                    elif len(void) == 1:
                        l1 = 0
                        r1 = 0
                        if x - 1 >= 0 and y - 1 >= 0:
                            l1 = 1
                        if x + 4 <= w - 1 and y + 4 <= h - 1:
                            r1 = 1

                        if l1 == 1:
                            if board[y - 1][x - 1] not in all_sign:
                                mini_force_pos.add(void[0])
                                mini_force_pos.add((x - 1, y - 1))
                        if r1 == 1:
                            if board[y + 4][x + 4] not in all_sign:
                                mini_force_pos.add(void[0])
                                mini_force_pos.add((x + 4, y + 4))
                    elif len(void) == 0:
                        l1 = 0
                        l2 = 0
                        r1 = 0
                        r2 = 0
                        if x - 2 >= 0 and y - 2 >= 0:
                            l1 = 1
                            l2 = 1
                        elif x - 1 >= 0 and y - 1 >= 0:
                            l1 = 1
                        if x + 4 <= w - 1 and y + 4 <= h - 1:
                            r1 = 1
                            r2 = 1
                        elif x + 3 <= w - 1 and y + 3 <= h - 1:
                            r1 = 1

                        if l2 == 1:
                            if board[y - 1][x - 1] not in all_sign and board[y - 2][x - 2] not in all_sign:
                                mini_force_pos.add((x - 1, y - 1))
                                mini_force_pos.add((x - 2, y - 2))

                        if l1 == 1 and r1 == 1:
                            if board[y - 1][x - 1] not in all_sign and board[y + 3][x + 3] not in all_sign:
                                mini_force_pos.add((x - 1, y - 1))
                                mini_force_pos.add((x + 3, y + 3))

                        if r2 == 1:
                            if board[y + 3][x + 3] not in all_sign and board[y + 4][x + 4] not in all_sign:
                                mini_force_pos.add((x + 3, y + 3))
                                mini_force_pos.add((x + 4, y + 4))

                ### ### ### DIAGONÁLIS- ELLENŐRZÉS ### ### ###
                s = 1
                void = []
                for k in range(1, 5):
                    if x - k >= 0 and y + k <= h - 1:
                        if board[y + k][x - k] == SIGN:
                            s += 1
                        elif board[y + k][x - k] == ENEMY:
                            s = 0
                            break
                        else:
                            void.append((x - k, y + k))
                        if s == 3:
                            break
                if s == 3:
                    # l1 : BALRA ELSŐ MEZŐ VIZSGÁLATÁHOZ
                    # l2 : BALRA MÁSODIK MEZŐ VIZSGÁLATÁHOZ
                    # r1 : JOBBRA ELSŐ MEZŐ VIZSGÁLATÁHOZ
                    # r2 : JOBBRA MÁSODIK MEZŐ VIZSGÁLATÁHOZ
                    if len(void) == 2:
                        mini_force_pos.add(void[0])
                        mini_force_pos.add(void[1])
                    elif len(void) == 1:
                        l1 = 0
                        r1 = 0
                        if x + 1 <= w - 1 and y - 1 >= 0:
                            l1 = 1
                        if x - 4 >= 0 and y + 4 <= h - 1:
                            r1 = 1

                        if l1 == 1:
                            if board[y - 1][x + 1] not in all_sign:
                                mini_force_pos.add(void[0])
                                mini_force_pos.add((x + 1, y - 1))
                        if r1 == 1:
                            if board[y + 4][x - 4] not in all_sign:
                                mini_force_pos.add(void[0])
                                mini_force_pos.add((x - 4, y + 4))
                    elif len(void) == 0:
                        l1 = 0
                        l2 = 0
                        r1 = 0
                        r2 = 0
                        if x + 2 <= w - 1 and y - 2 >= 0:
                            l1 = 1
                            l2 = 1
                        elif x + 1 <= w - 1 and y - 1 >= 0:
                            l1 = 1
                        if x - 4 >= 0 and y + 4 <= h - 1:
                            r1 = 1
                            r2 = 1
                        elif x - 3 >= 0 and y + 3 <= h - 1:
                            r1 = 1

                        if l2 == 1:
                            if board[y - 1][x + 1] not in all_sign and board[y - 2][x + 2] not in all_sign:
                                mini_force_pos.add((x + 1, y - 1))
                                mini_force_pos.add((x + 2, y - 2))

                        if l1 == 1 and r1 == 1:
                            if board[y - 1][x + 1] not in all_sign and board[y + 3][x - 3] not in all_sign:
                                mini_force_pos.add((x + 1, y - 1))
                                mini_force_pos.add((x - 3, y + 3))

                        if r2 == 1:
                            if board[y + 3][x - 3] not in all_sign and board[y + 4][x - 4] not in all_sign:
                                mini_force_pos.add((x - 3, y + 3))
                                mini_force_pos.add((x - 4, y + 4))
    if mini_force_pos != set():
        fill_zero(board)
        for i in mini_force_pos:
            take_fix(board, i, 1)
        return 1
    else:
        return 0


def prog_step(board, steps, k, SIGN, forbidden_pos, SWITCH):
    # SWITCH 0: CSAK JÁTSZIK
    #        1: LÉPTETVE JÁTSZIK

    ### AKKOR KELLHET, HA SZERETNÉNK VISSZALÉPÉST IS
    # circle = 0
    # for y in range(len(board)):
    #     for x in range(len(board[y])):
    #         if board[y][x] == 'o':
    #             circle += 1
    #         elif board[y][x] == 'x':
    #             circle -= 1
    # if circle == 1:
    #     SIGN = 'x'
    # else:
    #     SIGN = 'o'
    if SWITCH == 1:
        clear_screen()
        print_board(board, steps[-1], 0)
        print('Következő:', SIGN)
        print_possible_steps(board)

    ENEMY_set = {'o', 'x'}
    ENEMY_set.remove(SIGN)
    h = len(board)
    w = len(board[0])
    orig = (int(w / 2), int(h / 2))
    for i in ENEMY_set:
        ENEMY = i

    # 1-ESEK INCIALIZÁLÁSA
    if k == 1:
        fill_one(board, 1)
    else:
        fill_one(board, 1.5)

    if trivial(board, SIGN) == 1:
        if SWITCH == 1:
            input()
            clear_screen()
            print_board(board, steps[-1], 1)
            print('Következő:', SIGN)
            print_possible_steps(board)
            input()
        # learnt_zeroing(board, k, forbidden_pos, outfile)
        weighting(board, SIGN)
        steps.append(take_rand(board, SIGN))

    elif trivial(board, ENEMY) == 1:
        if SWITCH == 1:
            input()
            clear_screen()
            print_board(board, steps[-1], 1)
            print('Következő:', SIGN)
            print_possible_steps(board)
            input()
        # learnt_zeroing(board, k, forbidden_pos, outfile)
        weighting(board, SIGN)
        steps.append(take_rand(board, SIGN))

    elif trivial2nd(board, SIGN, 'OWN') == 1:
        if SWITCH == 1:
            input()
            clear_screen()
            print_board(board, steps[-1], 1)
            print('Következő:', SIGN)
            print_possible_steps(board)
            input()
        # learnt_zeroing(board, k, forbidden_pos, outfile)
        weighting(board, SIGN)
        steps.append(take_rand(board, SIGN))

    else:
        triv_enemy = trivial2nd(board, ENEMY, 'ENEMY')

        ###AZ ELLENFÉLNEK CSAK 1 ALAKZATA VAN, TEHÁT 1 LÉPPÉSSEL LEHET VÉDEKEZNI ELLENE
        if triv_enemy == 1:
            if SWITCH == 1:
                input()
                clear_screen()
                print_board(board, steps[-1], 1)
                print('Következő:', SIGN)
                print_possible_steps(board)
                input()
            # learnt_zeroing(board, k, forbidden_pos, outfile)
            weighting(board, SIGN)
            steps.append(take_rand(board, SIGN))

        elif triv_enemy > 1:
            if force_new(board, SIGN, 'OWN', 'STRONG') == 1:
                if SWITCH == 1:
                    input()
                    clear_screen()
                    print_board(board, steps[-1], 1)
                    print('Következő:', SIGN)
                    print_possible_steps(board)
                    input()
                # learnt_zeroing(board, k, forbidden_pos, outfile)
                weighting(board, SIGN)
                steps.append(take_rand(board, SIGN))
            else:
                if SWITCH == 1:
                    input()
                    clear_screen()
                    print_board(board, steps[-1], 1)
                    print('Következő:', SIGN)
                    print_possible_steps(board)
                    input()
                mini_force(board, SIGN)
                # learnt_zeroing(board, k, forbidden_pos, outfile)
                weighting(board, SIGN)
                steps.append(take_rand(board, SIGN))

        if triv_enemy == 0:
            if force_new(board, SIGN, 'OWN', 'WEAK') == 1:
                if SWITCH == 1:
                    input()
                    clear_screen()
                    print_board(board, steps[-1], 1)
                    print('Következő:', SIGN)
                    print_possible_steps(board)
                    input()
                # learnt_zeroing(board, k, forbidden_pos, outfile)
                weighting(board, SIGN)
                steps.append(take_rand(board, SIGN))
            elif force(board, ENEMY, 'ENEMY') == 1:
                if SWITCH == 1:
                    input()
                    clear_screen()
                    print_board(board, steps[-1], 1)
                    print('Következő:', SIGN)
                    print_possible_steps(board)
                    input()
                # learnt_zeroing(board, k, forbidden_pos, outfile)
                weighting(board, SIGN)
                steps.append(take_rand(board, SIGN))
            elif k == 0:
                take_fix(board, orig, SIGN)
                steps.append(orig)
            else:
                if SWITCH == 1:
                    clear_screen()
                    print_board(board, steps[-1], 0)
                    print('Következő:', SIGN)
                    print_possible_steps(board)
                    input()
                # learnt_zeroing(board, k, forbidden_pos, outfile)
                weighting(board, SIGN)
                steps.append(take_rand(board, SIGN))
    if steps[-1] == 0:
        return 0
    else:
        return 1


def step(board, steps, k, SIGN, forbidden_pos, SWITCH):
    # SWITCH 0: CSAK JÁTSZIK
    #        1: LÉPTETVE JÁTSZIK

    ### AKKOR KELLHET, HA SZERETNÉNK VISSZALÉPÉST IS
    # circle = 0
    # for y in range(len(board)):
    #     for x in range(len(board[y])):
    #         if board[y][x] == 'o':
    #             circle += 1
    #         elif board[y][x] == 'x':
    #             circle -= 1
    # if circle == 1:
    #     SIGN = 'x'
    # else:
    #     SIGN = 'o'
    if SWITCH == 1:
        clear_screen()
        print_board(board, steps[-1], 0)
        print('Következő:', SIGN)
        print_possible_steps(board)

    ENEMY_set = {'o', 'x'}
    ENEMY_set.remove(SIGN)
    h = len(board)
    w = len(board[0])
    orig = (int(w / 2), int(h / 2))
    for i in ENEMY_set:
        ENEMY = i

    if trivial(board, SIGN) == 1:
        if SWITCH == 1:
            input()
            clear_screen()
            print_board(board, steps[-1], 1)
            print('Következő:', SIGN)
            print_possible_steps(board)
            input()
        steps.append(take_rand(board, SIGN))

    elif trivial(board, ENEMY) == 1:
        if SWITCH == 1:
            input()
            clear_screen()
            print_board(board, steps[-1], 1)
            print('Következő:', SIGN)
            print_possible_steps(board)
            input()
        steps.append(take_rand(board, SIGN))

    elif trivial2nd(board, SIGN, 'OWN') == 1:
        if SWITCH == 1:
            input()
            clear_screen()
            print_board(board, steps[-1], 1)
            print('Következő:', SIGN)
            print_possible_steps(board)
            input()
        steps.append(take_rand(board, SIGN))

    else:
        triv_enemy = trivial2nd(board, ENEMY, 'ENEMY')

        ###AZ ELLENFÉLNEK CSAK 1 ALAKZATA VAN, TEHÁT 1 LÉPPÉSSEL LEHET VÉDEKEZNI ELLENE
        if triv_enemy == 1:
            if SWITCH == 1:
                input()
                clear_screen()
                print_board(board, steps[-1], 1)
                print('Következő:', SIGN)
                print_possible_steps(board)
                input()
            steps.append(take_rand(board, SIGN))

        elif triv_enemy > 1:
            if force(board, SIGN, 'OWN') == 1:
                if SWITCH == 1:
                    input()
                    clear_screen()
                    print_board(board, steps[-1], 1)
                    print('Következő:', SIGN)
                    print_possible_steps(board)
                    input()
                steps.append(take_rand(board, SIGN))
            else:
                if SWITCH == 1:
                    input()
                    clear_screen()
                    print_board(board, steps[-1], 1)
                    print('Következő:', SIGN)
                    print_possible_steps(board)
                    input()
                steps.append(take_rand(board, SIGN))

    if triv_enemy == 0:
        if force(board, SIGN, 'OWN') == 1:
            if SWITCH == 1:
                input()
                clear_screen()
                print_board(board, steps[-1], 1)
                print('Következő:', SIGN)
                print_possible_steps(board)
                input()
            steps.append(take_rand(board, SIGN))
        elif force(board, ENEMY, 'ENEMY') == 1:
            print('ittt 2')
            if SWITCH == 1:
                input()
                clear_screen()
                print_board(board, steps[-1], 1)
                print('Következő:', SIGN)
                print_possible_steps(board)
                input()
            steps.append(take_rand(board, SIGN))
        elif k == 0:
            take_fix(board, orig, SIGN)
            steps.append(orig)
            fill_one(board, 1)
        else:
            if SWITCH == 1:
                clear_screen()
                print_board(board, steps[-1], 0)
                print('Következő:', SIGN)
                print_possible_steps(board)
                input()
            weighting(board, SIGN)
            steps.append(take_rand(board, SIGN))
    if steps[-1] == 0:
        return 0
    else:
        return 1


def weighting3(board, SIGN, WRITTEN):
    w = len(board[0])
    h = len(board)
    all_sign = {'x', 'o'}
    if SIGN == 'x':
        ENEMY = 'o'
    else:
        ENEMY = 'x'

    for x in range(w):
        for y in range(h):
            if board[y][x] == SIGN:
                ### ### HORIZONTÁLIS ELLENŐRZÉS
                s = 1
                l = 1
                void = []
                coords = [[x, y]]
                for k in range(1, 5):
                    if x + k <= w - 1:
                        if board[y][x + k] == SIGN:
                            s += 1
                            coords.append([x + k, y])
                        elif board[y][x + k] == ENEMY:
                            break
                        else:
                            void.append([x + k, y])
                        if s == 3:
                            break
                if s == 3 and k < 4:
                    step = 0
                    for i in range(1, 5 - k):
                        if x - i >= 0:
                            if board[y][x - i] not in all_sign:
                                void.append([x - i, y])
                                step += 1
                            else:
                                break
                    for i in range(1, 5 - k):
                        if x + k + i <= w - 1:
                            if board[y][x + k + i] not in all_sign:
                                void.append([x + k + i, y])
                                step += 1
                            else:
                                break
                    if len(void) >= 2:
                        for i in void:
                            board[i[1]][i[0]] += 3
                        for i in coords:
                            WRITTEN.append(i)
                            WRITTEN[-1].append('h')
                elif s == 3 and k == 4:
                    for i in void:
                        board[i[1]][i[0]] += 3
                    for i in coords:
                        WRITTEN.append(i)
                        WRITTEN[-1].append('h')

                ### ### VERTIKÁLIS ELLENŐRZÉS
                s = 1
                void = []
                coords = [[x, y]]
                for k in range(1, 5):
                    if y + k <= h - 1:
                        if board[y + k][x] == SIGN:
                            s += 1
                            coords.append([x, y + k])
                        elif board[y + k][x] == ENEMY:
                            break
                        else:
                            void.append([x, y + k])
                        if s == 3:
                            break
                if s == 3 and k < 4:
                    step = 0
                    for i in range(1, 5 - k):
                        if y - i >= 0:
                            if board[y - i][x] not in all_sign:
                                void.append([x, y - i])
                                step += 1
                            else:
                                break
                    for i in range(1, 5 - k):
                        if y + k + i <= h - 1:
                            if board[y + k + i][x] not in all_sign:
                                void.append([x, y + k + i])
                                step += 1
                            else:
                                break
                    if len(void) >= 2:
                        for i in void:
                            board[i[1]][i[0]] += 3
                        for i in coords:
                            WRITTEN.append(i)
                            WRITTEN[-1].append('v')
                elif s == 3 and k == 4:
                    for i in void:
                        board[i[1]][i[0]] += 3
                    for i in coords:
                        WRITTEN.append(i)
                        WRITTEN[-1].append('v')

                ### ### DIAGONÁLIS+ ELLENŐRZÉS
                s = 1
                void = []
                coords = [[x, y]]
                for k in range(1, 5):
                    if x + k <= w - 1 and y + k <= h - 1:
                        if board[y + k][x + k] == SIGN:
                            s += 1
                            coords.append([x + k, y + k])
                        elif board[y + k][x + k] == ENEMY:
                            break
                        else:
                            void.append([x + k, y + k])
                        if s == 3:
                            break
                if s == 3 and k < 4:
                    step = 0
                    for i in range(1, 5 - k):
                        if x - i >= 0 and y - i >= 0:
                            if board[y - i][x - i] not in all_sign:
                                void.append([x - i, y - i])
                                step += 1
                            else:
                                break
                    for i in range(1, 5 - k):
                        if x + k + i <= w - 1 and y + k + i <= h - 1:
                            if board[y + k + i][x + k + i] not in all_sign:
                                void.append([x + k + i, y + k + i])
                                step += 1
                            else:
                                break
                    if len(void) >= 2:
                        for i in void:
                            board[i[1]][i[0]] += 3
                        for i in coords:
                            WRITTEN.append(i)
                            WRITTEN[-1].append('d+')
                elif s == 3 and k == 4:
                    for i in void:
                        board[i[1]][i[0]] += 3
                    for i in coords:
                        WRITTEN.append(i)
                        WRITTEN[-1].append('d+')

                ### ### DIAGONÁLIS- ELLENŐRZÉS
                s = 1
                void = []
                coords = [[x, y]]
                for k in range(1, 5):
                    if x - k >= 0 and y + k <= h - 1:
                        if board[y + k][x - k] == SIGN:
                            s += 1
                            coords.append([x - k, y + k])
                        elif board[y + k][x - k] == ENEMY:
                            break
                        else:
                            void.append([x - k, y + k])
                        if s == 3:
                            break
                if s == 3 and k < 4:
                    step = 0
                    for i in range(1, 5 - k):
                        if x + i <= w - 1 and y - i >= 0:
                            if board[y - i][x + i] not in all_sign:
                                void.append([x + i, y - i])
                                step += 1
                            else:
                                break
                    for i in range(1, 5 - k):
                        if x - k - i >= 0 and y + k + i <= h - 1:
                            if board[y + k + i][x - k - i] not in all_sign:
                                void.append([x - k - i, y + k + i])
                                step += 1
                            else:
                                break
                    if len(void) >= 2:
                        for i in void:
                            board[i[1]][i[0]] += 3
                        for i in coords:
                            WRITTEN.append(i)
                            WRITTEN[-1].append('d-')
                elif s == 3 and k == 4:
                    for i in void:
                        board[i[1]][i[0]] += 3
                    for i in coords:
                        WRITTEN.append(i)
                        WRITTEN[-1].append('d-')


def weighting2(board, SIGN, WRITTEN):
    w = len(board[0])
    h = len(board)
    WEIGHT1 = 3
    WEIGHT2 = 3
    WEIGHT3 = 1
    all_sign = {'x', 'o'}
    if SIGN == 'x':
        ENEMY = 'o'
    else:
        ENEMY = 'x'

    for x in range(w):
        for y in range(h):
            if board[y][x] == SIGN:
                ### ### HORIZONTÁLIS ELLENŐRZÉS
                SKIPP = 0
                if WRITTEN != []:
                    for i in WRITTEN:
                        if i[2] == 'h':
                            if i[0] == x and i[1] == y:
                                SKIPP = 1
                s = 1
                void = []
                void_p = []
                void_m = []
                for k in range(1, 5):
                    if x + k <= w - 1:
                        if board[y][x + k] == SIGN:
                            s += 1
                        elif board[y][x + k] == ENEMY:
                            break
                        else:
                            void.append([x + k, y])
                        if s == 2:
                            break
                    else:
                        break
                if s == 2:
                    for i in range(1, 5 - k):
                        if x - i >= 0:
                            if board[y][x - i] not in all_sign:
                                void_m.append([x - i, y])
                            else:
                                break
                        else:
                            break
                    for i in range(1, 5 - k):
                        if x + k + i <= w - 1:
                            if board[y][x + k + i] not in all_sign:
                                void_p.append([x + k + i, y])
                            else:
                                break
                        else:
                            break
                    if len(void) + len(void_m) + len(void_p) >= 3:
                        for i in void:
                            board[i[1]][i[0]] += WEIGHT1
                        NUM = 0
                        for i in void_m:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] += WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] += WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] += WEIGHT3
                        NUM = 0
                        for i in void_p:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] += WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] += WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] += WEIGHT3

                ### ### VERTIKÁLIS ELLENŐRZÉS
                SKIPP = 0
                if WRITTEN != []:
                    for i in WRITTEN:
                        if i[2] == 'v':
                            if i[0] == x and i[1] == y:
                                SKIPP = 1
                s = 1
                void = []
                void_p = []
                void_m = []
                for k in range(1, 5):
                    if y + k <= h - 1:
                        if board[y + k][x] == SIGN:
                            s += 1
                        elif board[y + k][x] == ENEMY:
                            break
                        else:
                            void.append([x, y + k])
                        if s == 2:
                            break
                    else:
                        break
                if s == 2:
                    for i in range(1, 5 - k):
                        if y - i >= 0:
                            if board[y - i][x] not in all_sign:
                                void_m.append([x, y - i])
                            else:
                                break
                        else:
                            break
                    for i in range(1, 5 - k):
                        if y + k + i <= h - 1:
                            if board[y + k + i][x] not in all_sign:
                                void_p.append([x, y + k + i])
                            else:
                                break
                        else:
                            break
                    if len(void) + len(void_m) + len(void_p) >= 3:
                        for i in void:
                            board[i[1]][i[0]] += WEIGHT1
                        NUM = 0
                        for i in void_m:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] += WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] += WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] += WEIGHT3
                        NUM = 0
                        for i in void_p:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] += WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] += WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] += WEIGHT3

                ### ### DIAGONÁLIS+ ELLENŐRZÉS
                SKIPP = 0
                if WRITTEN != []:
                    for i in WRITTEN:
                        if i[2] == 'd+':
                            if i[0] == x and i[1] == y:
                                SKIPP = 1
                s = 1
                void = []
                void_p = []
                void_m = []
                for k in range(1, 5):
                    if x + k <= w - 1 and y + k <= h - 1:
                        if board[y + k][x + k] == SIGN:
                            s += 1
                        elif board[y + k][x + k] == ENEMY:
                            break
                        else:
                            void.append([x + k, y + k])
                        if s == 2:
                            break
                    else:
                        break
                if s == 2:
                    for i in range(1, 5 - k):
                        if x - i >= 0 and y - i >= 0:
                            if board[y - i][x - i] not in all_sign:
                                void_m.append([x - i, y - i])
                            else:
                                break
                        else:
                            break
                    for i in range(1, 5 - k):
                        if x + k + i <= w - 1 and y + k + i <= h - 1:
                            if board[y + k + i][x + k + i] not in all_sign:
                                void_p.append([x + k + i, y + k + i])
                            else:
                                break
                        else:
                            break
                    if len(void) + len(void_m) + len(void_p) >= 3:
                        for i in void:
                            board[i[1]][i[0]] += WEIGHT1
                        NUM = 0
                        for i in void_m:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] += WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] += WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] += WEIGHT3
                        NUM = 0
                        for i in void_p:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] += WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] += WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] += WEIGHT3

                ### ### DIAGONÁLIS- ELLENŐRZÉS
                SKIPP = 0
                if WRITTEN != []:
                    for i in WRITTEN:
                        if i[2] == 'd-':
                            if i[0] == x and i[1] == y:
                                SKIPP = 1
                s = 1
                void = []
                void_p = []
                void_m = []
                for k in range(1, 5):
                    if x - k >= 0 and y + k <= h - 1:
                        if board[y + k][x - k] == SIGN:
                            s += 1
                        elif board[y + k][x - k] == ENEMY:
                            break
                        else:
                            void.append([x - k, y + k])
                        if s == 2:
                            break
                    else:
                        break
                if s == 2:
                    for i in range(1, 5 - k):
                        if x + i <= w - 1 and y - i >= 0:
                            if board[y - i][x + i] not in all_sign:
                                void_m.append([x + i, y - i])
                            else:
                                break
                        else:
                            break
                    for i in range(1, 5 - k):
                        if x - k - i >= 0 and y + k + i <= h - 1:
                            if board[y + k + i][x - k - i] not in all_sign:
                                void_p.append([x - k - i, y + k + i])
                            else:
                                break
                        else:
                            break
                    if len(void) + len(void_m) + len(void_p) >= 3:
                        for i in void:
                            board[i[1]][i[0]] += WEIGHT1
                        NUM = 0
                        for i in void_m:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] += WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] += WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] += WEIGHT3
                        NUM = 0
                        for i in void_p:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] += WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] += WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] += WEIGHT3


def weighting(board, SIGN):
    WRITTEN = []
    weighting3(board, SIGN, WRITTEN)
    weighting2(board, SIGN, WRITTEN)


def fill_one(board, RANGE):
    # RANGENEK MEGFELELŐEN KITÖLTI MINDEN JEL KÖRÜLI ÜRES MEZŐKET
    w = len(board[0])
    h = len(board)

    if RANGE == 1.5:
        # 1 TÁVOLSÁGBAN A NÉGYZETET KITÖLTI 1-ESEKKEL
        # SARKOKBA 0.5 (HA 2 ILYEN SAROK EGYBEESIK AKKOR 1 LESZ)
        # KÖZVETLENÜL A JEL ALATT ÉS MELLETT LÉVŐ 2 TÁVOLSÁGBAN EGY-EGY MEZŐT 1-ESSEL KITÖLT
        for y in range(h):
            for x in range(w):
                if board[y][x] == 'x' or board[y][x] == 'o':
                    ### ### RANGE == 1 KITÖLTÉS
                    for i in range(-1, 1 + 1):
                        for j in range(-1, 1 + 1):
                            if x + i >= 0 and x + i < w and y + j >= 0 and y + j < h:
                                if board[y + j][x + i] == 0 or board[y + j][x + i] == 0.5:
                                    board[y + j][x + i] = 1

                    ### ### SARKOK KITÖLTÉSE +0.5
                    for i in (-2, 2):
                        for j in (-2, 2):
                            if x + i >= 0 and x + i < w and y + j >= 0 and y + j < h:
                                if board[y + j][x + i] == 0 or board[y + j][x + i] == 0.5:
                                    board[y + j][x + i] += 0.5

                    ### ### 2 TÁVOLSÁGRA LÉVŐ ÉLEK KITÖLTÉSE
                    for i in (-2, 2):
                        if x + i >= 0 and x + i < w:
                            if board[y][x + i] == 0 or board[y][x + i] == 0.5:
                                board[y][x + i] = 1
                        if y + i >= 0 and y + i < h:
                            if board[y + i][x] == 0 or board[y + i][x] == 0.5:
                                board[y + i][x] = 1
        ### ### 0.5-KET 0-RA ÁLLÍTJUK
        for y in range(h):
            for x in range(w):
                if board[y][x] == 0.5:
                    board[y][x] = 0

    elif RANGE == 1 or RANGE == 2:
        for y in range(h):
            for x in range(w):
                if board[y][x] == 'x' or board[y][x] == 'o':
                    for i in range(-RANGE, RANGE + 1):
                        for j in range(-RANGE, RANGE + 1):
                            if x + i >= 0 and x + i < w and y + j >= 0 and y + j < h:
                                if board[y + j][x + i] == 0:
                                    board[y + j][x + i] = 1


def fill_zero(board):
    w = len(board[0])
    h = len(board)
    for y in range(h):
        for x in range(w):
            if board[y][x] != 'x' and board[y][x] != 'o':
                board[y][x] = 0


def str2set(str_set, set_fin):
    i = 0
    while i < len(str_set):
        if str_set[i] == '(':
            x = ''
            y = ''
            j = i + 1
            while str_set[j] != ',':
                x += str_set[j]
                j += 1
            j += 1

            while str_set[j] != ')':
                y += str_set[j]
                j += 1
            i = j + 1
            set_fin.add((int(x), int(y)))
        i += 1


def pos_rec(board, STEPS):
    # A KIALAKULT POZÍCIÓHOZ RENDELÜNK EGY KARAKTERSORT
    # AMIT ANNAK MEGFELELŐEN, HOGY HOGY NÉZÜNK RÁ 8 FÉLEKÉPPEN TEHETÜNK MEG
    #
    # A POZÍCIÓ KÖRÉ ÍRHATÓ TÉGLALAP SARKAIBAN ELKÉPZELVE EGY-EGY KOORDINÁTARENDSZERT
    # X-TENGELY ÓRAMUTATÓ JÁRÁSÁNAK ELLENKEZŐEN ÁLL:
    #       POS 1 : BAL ALSÓ SAROK
    #       POS 2 : JOBB ALSÓ SAROK
    #       POS 3 : JOBB FELSŐ SAROK
    #       POS 4 : BAL BAL FELSŐ SAROK
    # X-TENGELY ÓRAMUTATÓ JÁRÁSÁNAK MEGFELELŐEN ÁLL:
    #       POS 5 : BAL ALSÓ SAROK
    #       POS 6 : JOBB ALSÓ SAROK
    #       POS 7 : JOBB FELSŐ SAROK
    #       POS 8 : BAL BAL FELSŐ SAROK

    w = len(board[0])
    h = len(board)
    xmin = xmax = 0
    ymin = ymax = 0
    k = 0  # JELEKET SZÁMLÁLJA

    # MINDEGYIK LEHETSÉGES POZÍCIÓHOZ FOG TARTOZNI EGY KULCS ÉS A NEKI MEGFELELŐ KARAKTERSOR ÉRTÉKKÉNT
    record = {}

    ### ### CSAK 1 JEL VAN VAGY 0
    if STEPS == 1:
        for y in range(h):
            for x in range(w):
                if board[y][x] == 'x' or board[y][x] == 'o':
                    pos = '0000' + str(board[y][x])
                    record['pos1'] = pos
                    return record
    elif STEPS == 0:
        return record

    ### ### A KIALAKULT POZÍCIÓ KÖRÉ ÍRHATÓ TÉGLALAP KÉT ÁTLÓS SARKÁNAK KOORDINÁTÁINAK MEGHATÁROZÁSA
    for y in range(h):
        for x in range(w):
            if board[y][x] == 'x' or board[y][x] == 'o':
                k += 1
                if k == 1:
                    ymin = y
                    xmin = x
                    xmax = x
                elif k == STEPS:
                    ymax = y
                    if x < xmin:
                        xmin = x
                    if x > xmax:
                        xmax = x
                else:
                    if x < xmin:
                        xmin = x
                    if x > xmax:
                        xmax = x

    ### CSAK AZ X-TENGELLYEL PÁRHUZAMOSAN VANNAK A JELEK
    if ymin == ymax:
        pos1 = ''
        for x in range(xmin, xmax + 1):
            if board[ymin][x] == 'x':
                if x - xmin < 10:
                    pos1 += '0' + str(x - xmin)
                else:
                    pos1 += str(x - xmin)
                pos1 += '00x'
            elif board[ymin][x] == 'o':
                if x - xmin < 10:
                    pos1 += '0' + str(x - xmin)
                else:
                    pos1 += str(x - xmin)
                pos1 += '00o'
        record['pos1'] = pos1

        pos2 = ''
        for x in range(xmax, xmin - 1, -1):
            if board[ymin][x] == 'x':
                if xmax - x < 10:
                    pos2 += '0' + str(xmax - x)
                else:
                    pos2 += str(xmax - x)
                pos2 += '00x'
            elif board[ymin][x] == 'o':
                if xmax - x < 10:
                    pos2 += '0' + str(xmax - x)
                else:
                    pos2 += str(xmax - x)
                pos2 += '00o'
        record['pos2'] = pos2

    ### CSAK AZ Y-TENGELLYEL PÁRHUZAMOSAN VANNAK A JELEK
    elif xmin == xmax:
        pos1 = ''
        for y in range(ymin, ymax + 1):
            if board[y][xmin] == 'x':
                if y - ymin < 10:
                    pos1 += '0' + str(y - ymin)
                else:
                    pos1 += str(y - ymin)
                pos1 += '00x'
            elif board[y][xmin] == 'o':
                if y - ymin < 10:
                    pos1 += '0' + str(y - ymin)
                else:
                    pos1 += str(y - ymin)
                pos1 += '00o'
        record['pos1'] = pos1

        pos2 = ''
        for y in range(ymax, ymin - 1, -1):
            if board[y][xmin] == 'x':
                if ymax - y < 10:
                    pos2 += '0' + str(ymax - y)
                else:
                    pos2 += str(ymax - y)
                pos2 += '00x'
            elif board[y][xmin] == 'o':
                if ymax - y < 10:
                    pos2 += '0' + str(ymax - y)
                else:
                    pos2 += str(ymax - y)
                pos2 += '00o'
        record['pos2'] = pos2

    ### VAN RENDES TÉGLALAP, AMI A KIALAKULT HELYZET KÖRÉ ÍRHATÓ
    else:
        pos1 = ''
        for y in range(ymax, ymin - 1, -1):
            for x in range(xmin, xmax + 1):
                if board[y][x] == 'x':
                    if x - xmin < 10:
                        pos1 += '0' + str(x - xmin)
                    else:
                        pos1 += str(x - xmin)
                    if ymax - y < 10:
                        pos1 += '0' + str(ymax - y)
                    else:
                        pos1 += str(ymax - y)
                    pos1 += 'x'
                elif board[y][x] == 'o':
                    if x - xmin < 10:
                        pos1 += '0' + str(x - xmin)
                    else:
                        pos1 += str(x - xmin)
                    if ymax - y < 10:
                        pos1 += '0' + str(ymax - y)
                    else:
                        pos1 += str(ymax - y)
                    pos1 += 'o'
        record['pos1'] = pos1

        pos2 = ''
        for x in range(xmax, xmin - 1, -1):
            for y in range(ymax, ymin - 1, -1):
                if board[y][x] == 'x':
                    if ymax - y < 10:
                        pos2 += '0' + str(ymax - y)
                    else:
                        pos2 += str(ymax - y)
                    if xmax - x < 10:
                        pos2 += '0' + str(xmax - x)
                    else:
                        pos2 += str(xmax - x)
                    pos2 += 'x'
                elif board[y][x] == 'o':
                    if ymax - y < 10:
                        pos2 += '0' + str(ymax - y)
                    else:
                        pos2 += str(ymax - y)
                    if xmax - x < 10:
                        pos2 += '0' + str(xmax - x)
                    else:
                        pos2 += str(xmax - x)
                    pos2 += 'o'
        record['pos2'] = pos2

        pos3 = ''
        for y in range(ymin, ymax + 1):
            for x in range(xmax, xmin - 1, -1):
                if board[y][x] == 'x':
                    if xmax - x < 10:
                        pos3 += '0' + str(xmax - x)
                    else:
                        pos3 += str(xmax - x)
                    if y - ymin < 10:
                        pos3 += '0' + str(y - ymin)
                    else:
                        pos3 += str(y - ymin)
                    pos3 += 'x'
                elif board[y][x] == 'o':
                    if xmax - x < 10:
                        pos3 += '0' + str(xmax - x)
                    else:
                        pos3 += str(xmax - x)
                    if y - ymin < 10:
                        pos3 += '0' + str(y - ymin)
                    else:
                        pos3 += str(y - ymin)
                    pos3 += 'o'
        record['pos3'] = pos3

        pos4 = ''
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                if board[y][x] == 'x':
                    if y - ymin < 10:
                        pos4 += '0' + str(y - ymin)
                    else:
                        pos4 += str(y - ymin)
                    if x - xmin < 10:
                        pos4 += '0' + str(x - xmin)
                    else:
                        pos4 += str(x - xmin)
                    pos4 += 'x'
                elif board[y][x] == 'o':
                    if y - ymin < 10:
                        pos4 += '0' + str(y - ymin)
                    else:
                        pos4 += str(y - ymin)
                    if x - xmin < 10:
                        pos4 += '0' + str(x - xmin)
                    else:
                        pos4 += str(x - xmin)
                    pos4 += 'o'
        record['pos4'] = pos4

        pos5 = ''
        for x in range(xmin, xmax + 1):
            for y in range(ymax, ymin - 1, -1):
                if board[y][x] == 'x':
                    if ymax - y < 10:
                        pos5 += '0' + str(ymax - y)
                    else:
                        pos5 += str(ymax - y)
                    if x - xmin < 10:
                        pos5 += '0' + str(x - xmin)
                    else:
                        pos5 += str(x - xmin)
                    pos5 += 'x'
                elif board[y][x] == 'o':
                    if ymax - y < 10:
                        pos5 += '0' + str(ymax - y)
                    else:
                        pos5 += str(ymax - y)
                    if x - xmin < 10:
                        pos5 += '0' + str(x - xmin)
                    else:
                        pos5 += str(x - xmin)
                    pos5 += 'o'
        record['pos5'] = pos5

        pos6 = ''
        for y in range(ymax, ymin - 1, -1):
            for x in range(xmax, xmin - 1, -1):
                if board[y][x] == 'x':
                    if xmax - x < 10:
                        pos6 += '0' + str(xmax - x)
                    else:
                        pos6 += str(xmax - x)
                    if ymax - y < 10:
                        pos6 += '0' + str(ymax - y)
                    else:
                        pos6 += str(ymax - y)
                    pos6 += 'x'
                elif board[y][x] == 'o':
                    if xmax - x < 10:
                        pos6 += '0' + str(xmax - x)
                    else:
                        pos6 += str(xmax - x)
                    if ymax - y < 10:
                        pos6 += '0' + str(ymax - y)
                    else:
                        pos6 += str(ymax - y)
                    pos6 += 'o'
        record['pos6'] = pos6

        pos7 = ''
        for x in range(xmax, xmin - 1, -1):
            for y in range(ymin, ymax + 1):
                if board[y][x] == 'x':
                    if y - ymin < 10:
                        pos7 += '0' + str(y - ymin)
                    else:
                        pos7 += str(y - ymin)
                    if xmax - x < 10:
                        pos7 += '0' + str(xmax - x)
                    else:
                        pos7 += str(xmax - x)
                    pos7 += 'x'
                elif board[y][x] == 'o':
                    if y - ymin < 10:
                        pos7 += '0' + str(y - ymin)
                    else:
                        pos7 += str(y - ymin)
                    if xmax - x < 10:
                        pos7 += '0' + str(xmax - x)
                    else:
                        pos7 += str(xmax - x)
                    pos7 += 'o'
        record['pos7'] = pos7

        pos8 = ''
        for y in range(ymin, ymax + 1):
            for x in range(xmin, xmax + 1):
                if board[y][x] == 'x':
                    if x - xmin < 10:
                        pos8 += '0' + str(x - xmin)
                    else:
                        pos8 += str(x - xmin)
                    if y - ymin < 10:
                        pos8 += '0' + str(y - ymin)
                    else:
                        pos8 += str(y - ymin)
                    pos8 += 'x'
                elif board[y][x] == 'o':
                    if x - xmin < 10:
                        pos8 += '0' + str(x - xmin)
                    else:
                        pos8 += str(x - xmin)
                    if y - ymin < 10:
                        pos8 += '0' + str(y - ymin)
                    else:
                        pos8 += str(y - ymin)
                    pos8 += 'o'
        record['pos8'] = pos8

    return record


def rectangle_corner(board, STEPS):
    w = len(board[0])
    h = len(board)
    k = 0
    for y in range(h):
        for x in range(w):
            if board[y][x] == 'x' or board[y][x] == 'o':
                k += 1
                if k == 1:
                    ymin = y
                    xmin = x
                    ymax = y
                    xmax = x
                elif k == STEPS:
                    ymax = y
                    if x < xmin:
                        xmin = x
                    if x > xmax:
                        xmax = x
                else:
                    if x < xmin:
                        xmin = x
                    if x > xmax:
                        xmax = x
    return (xmin, ymin, xmax, ymax)

# OLD
def learnt_zero(board, STEPS, POS_NUM, POS):
    w = len(board[0])
    h = len(board)
    xmin = xmax = 0
    ymin = ymax = 0
    k = 0  # JELEKET SZÁMLÁLJA
    tmp = [0, 0]  # ÁTMENETILEG TÁROLJUK BENNE A KONVERTÁLT KOORDINÁTÁKAT

    ### ### A KIALAKULT POZÍCIÓ KÖRÉ ÍRHATÓ TÉGLALAP KÉT ÁTLÓS SARKÁNAK KOORDINÁTÁIT HATÁROZZUK MEG
    for y in range(h):
        for x in range(w):
            if board[y][x] == 'x' or board[y][x] == 'o':
                k += 1
                if k == 1:
                    ymin = y
                    xmin = x
                elif k == STEPS:
                    ymax = y
                    if x < xmin:
                        xmin = x
                    if x > xmax:
                        xmax = x
                else:
                    if x < xmin:
                        xmin = x
                    if x > xmax:
                        xmax = x

    ### CSAK AZ X-TENGELLYEL PÁRHUZAMOSAN VANNAK A JELEK
    if ymin == ymax:
        if POS_NUM == 'pos1':
            for i in POS:
                tmp[0] = i[0] + xmin
                tmp[1] = ymax
                if tmp[0] >= 0 and tmp[0] <= w - 1:
                    board[tmp[1]][tmp[0]] = 0
        elif POS_NUM == 'pos2':
            for i in POS:
                tmp[0] = xmax - i[0]
                tmp[1] = ymax
                if tmp[0] >= 0 and tmp[0] <= w - 1:
                    board[tmp[1]][tmp[0]] = 0

    ### CSAK AZ Y-TENGELLYEL PÁRHUZAMOSAN VANNAK A JELEK
    elif xmin == xmax:
        if POS_NUM == 'pos1':
            for i in POS:
                tmp[0] = xmax
                tmp[1] = i[1] + ymin
                if tmp[0] >= 0 and tmp[0] <= w - 1:
                    board[tmp[1]][tmp[0]] = 0
        elif POS_NUM == 'pos2':
            for i in POS:
                tmp[0] = xmax
                tmp[1] = ymax - i[1]
                if tmp[1] >= 0 and tmp[1] <= h - 1:
                    board[tmp[1]][tmp[0]] = 0

    ### VAN RENDES TÉGLALAP, AMI A KIALAKULT HELYZET KÖRÉ ÍRHATÓ
    else:
        if POS_NUM == 'pos1':
            for i in POS:
                tmp[0] = i[0] + xmin
                tmp[1] = ymax - i[1]
                if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                    board[tmp[1]][tmp[0]] = 0

        elif POS_NUM == 'pos2':
            for i in POS:
                tmp[0] = xmax - i[1]
                tmp[1] = ymax - i[0]
                if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                    board[tmp[1]][tmp[0]] = 0

        elif POS_NUM == 'pos3':
            for i in POS:
                tmp[0] = xmax - i[0]
                tmp[1] = i[1] + ymin
                if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                    board[tmp[1]][tmp[0]] = 0

        elif POS_NUM == 'pos4':
            for i in POS:
                tmp[0] = i[1] + xmin
                tmp[1] = i[0] + ymin
                if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                    board[tmp[1]][tmp[0]] = 0

        elif POS_NUM == 'pos5':
            for i in POS:
                tmp[0] = i[1] + xmin
                tmp[1] = ymax - i[0]
                if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                    board[tmp[1]][tmp[0]] = 0

        elif POS_NUM == 'pos6':
            for i in POS:
                tmp[0] = xmax - i[0]
                tmp[1] = ymax - i[1]
                if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                    board[tmp[1]][tmp[0]] = 0

        elif POS_NUM == 'pos7':
            for i in POS:
                tmp[0] = xmax - i[1]
                tmp[1] = i[0] + ymin
                if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                    board[tmp[1]][tmp[0]] = 0

        elif POS_NUM == 'pos8':
            for i in POS:
                tmp[0] = i[0] + xmin
                tmp[1] = i[1] + ymin
                if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                    board[tmp[1]][tmp[0]] = 0


# NEW
def learn(board, STEPS, LAST_STEPS, FORBIDDEN_POS):
    # STEPS: LÉPÉSEK SZÁMA
    # LAST_STEPS: LÉPÉSEK LISTÁJA
    # FORBIDDEN_POS: IDE MENTJÜK A TILTOTT LÉPÉSEKET
    # print('LEARN BEGIN!')
    w = len(board[0])
    h = len(board)
    xmin = xmax = 0  # TÉGLALAP KOORDINÁTÁI
    ymin = ymax = 0
    last = [0, 0]  # UTOLSÓ LÉPÉS
    tmp = [0, 0]  # ÁTMENETILEG TÁROLJUK BENNE A KONVERTÁLT KOORDINÁTÁKAT
    fin_coord = [[0, 0], 0]  #
    OK = 0  # INDIKÁTORA, HOGY TALÁLTUNK-E PASSZOLÓ ÁLLÁST

    ### ### AZ UTOLSÓ LÉPÉSEKET VISSZAVONJUK ÉS AZT AZ ÁLLÁST VIZSGÁLJUK
    if LAST_STEPS[-1] != 'break':
        if LAST_STEPS[-1] == 0:
            LAST_STEPS.pop(-1)

        # UTOLSÓ (NYERŐ) LÉPÉS VISSZAVONÁSA
        last = LAST_STEPS[-1]
        take_fix(board, last, 1)
        STEPS -= 1

        for rev in range(2, len(LAST_STEPS)):
            # LÉPÉSEK VISSZAVONÁSA 1-ESÉVEL
            last = LAST_STEPS[-rev]
            take_fix(board, last, 1)
            STEPS -= 1

            # POZÍCIÓK MEGHATÁROZÁSA
            pos_fin = pos_rec(board, STEPS)
            s = 0  # JELEKET SZÁMLÁLJA

            ### ### A KIALAKULT POZÍCIÓ KÖRÉ ÍRHATÓ TÉGLALAP KÉT ÁTLÓS SARKÁNAK KOORDINÁTÁINAK MEGHATÁROZÁSA
            corners = rectangle_corner(board, STEPS)
            xmin = corners[0]
            ymin = corners[1]
            xmax = corners[2]
            ymax = corners[3]

            ### CSAK 1 JEL VAN, VAGYIS KEZDŐÁLLÁSNÁL VAGYUNK
            if STEPS == 1:
                for i in pos_fin:
                    if pos_fin[i] in FORBIDDEN_POS:
                        if i == 'pos1':
                            fin_coord[0][0] = last[0] - xmax
                            fin_coord[0][1] = last[1] - ymax
                            ### MELLÉ RAKOTT ELSŐRE X
                            if fin_coord[0][0] == 0 or fin_coord[0][1] == 0:
                                fin_coord[0][0] = 1
                                fin_coord[0][1] = 0
                            ### ÁTLÓSAN RAKOTT ELSŐRE X
                            else:
                                fin_coord[0][0] = 1
                                fin_coord[0][1] = 1
                            if rev == 2:
                                fin_coord[1] = 'z'
                            else:
                                if rev % 2 == 1:
                                    fin_coord[1] = 1
                                else:
                                    fin_coord[1] = -1

                            SEARCH = 0
                            for k in FORBIDDEN_POS[pos_fin[i]]:
                                if k[0] == fin_coord[0]:
                                    if fin_coord[1] == 'z':
                                        k[1] = 'z'
                                    else:
                                        k[1] += fin_coord[1]
                                    SEARCH = 1
                                    break
                            if SEARCH == 0:
                                FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                                FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                            OK = 1
                            break
                if OK == 0:
                    fin_coord[0][0] = last[0] - xmax
                    fin_coord[0][1] = last[1] - ymax
                    ### MELLÉ RAKOTT ELSŐRE X
                    if fin_coord[0][0] == 0 or fin_coord[0][1] == 0:
                        fin_coord[0][0] = 1
                        fin_coord[0][1] = 0
                    ### ÁTLÓSAN RAKOTT ELSŐRE X
                    else:
                        fin_coord[0][0] = 1
                        fin_coord[0][1] = 1
                    if rev == 2:
                        fin_coord[1] = 'z'
                    else:
                        if rev % 2 == 1:
                            fin_coord[1] = 1
                        else:
                            fin_coord[1] = -1
                    FORBIDDEN_POS[pos_fin['pos1']] = [[[0, 0], 0]]
                    FORBIDDEN_POS[pos_fin['pos1']][-1] = copy.deepcopy(fin_coord)

            ### CSAK AZ X-TENGELLYEL PÁRHUZAMOSAN VANNAK A JELEK
            elif ymin == ymax:
                for i in pos_fin:
                    if pos_fin[i] in FORBIDDEN_POS:
                        if i == 'pos1':
                            tmp[0] = last[0] - xmin
                            tmp[1] = 0
                            fin_coord[0][0] = tmp[0]
                            fin_coord[0][1] = tmp[1]
                            if rev == 2:
                                fin_coord[1] = 'z'
                            else:
                                if rev % 2 == 1:
                                    fin_coord[1] = 1
                                else:
                                    fin_coord[1] = -1

                            SEARCH = 0
                            for k in FORBIDDEN_POS[pos_fin[i]]:
                                if k[0] == fin_coord[0]:
                                    if fin_coord[1] == 'z':
                                        k[1] = 'z'
                                    else:
                                        k[1] += fin_coord[1]
                                    SEARCH = 1
                                    break
                            if SEARCH == 0:
                                FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                                FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                            OK = 1
                            break
                        elif i == 'pos2':
                            tmp[0] = xmax - last[0]
                            tmp[1] = 0
                            fin_coord[0][0] = tmp[0]
                            fin_coord[0][1] = tmp[1]
                            if rev == 2:
                                fin_coord[1] = 'z'
                            else:
                                if rev % 2 == 1:
                                    fin_coord[1] = 1
                                else:
                                    fin_coord[1] = -1

                            SEARCH = 0
                            for k in FORBIDDEN_POS[pos_fin[i]]:
                                if k[0] == fin_coord[0]:
                                    if fin_coord[1] == 'z':
                                        k[1] = 'z'
                                    else:
                                        k[1] += fin_coord[1]
                                    SEARCH = 1
                                    break
                            if SEARCH == 0:
                                FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                                FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                            OK = 1
                            break
                if OK == 0:
                    tmp[0] = last[0] - xmin
                    tmp[1] = 0
                    fin_coord[0][0] = tmp[0]
                    fin_coord[0][1] = tmp[1]
                    if rev == 2:
                        fin_coord[1] = 'z'
                    else:
                        if rev % 2 == 1:
                            fin_coord[1] = 1
                        else:
                            fin_coord[1] = -1
                    FORBIDDEN_POS[pos_fin['pos1']] = [[[0, 0], 0]]
                    FORBIDDEN_POS[pos_fin['pos1']][-1] = copy.deepcopy(fin_coord)

            ### CSAK AZ Y-TENGELLYEL PÁRHUZAMOSAN VANNAK A JELEK
            elif xmin == xmax:
                for i in pos_fin:
                    if pos_fin[i] in FORBIDDEN_POS:
                        if i == 'pos1':
                            tmp[0] = 0
                            tmp[1] = last[1] - ymin
                            fin_coord[0][0] = tmp[0]
                            fin_coord[0][1] = tmp[1]
                            if rev == 2:
                                fin_coord[1] = 'z'
                            else:
                                if rev % 2 == 1:
                                    fin_coord[1] = 1
                                else:
                                    fin_coord[1] = -1

                            SEARCH = 0
                            for k in FORBIDDEN_POS[pos_fin[i]]:
                                if k[0] == fin_coord[0]:
                                    if fin_coord[1] == 'z':
                                        k[1] = 'z'
                                    else:
                                        k[1] += fin_coord[1]
                                    SEARCH = 1
                                    break
                            if SEARCH == 0:
                                FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                                FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                            OK = 1
                            break
                        elif i == 'pos2':
                            tmp[0] = 0
                            tmp[1] = ymax - last[1]
                            fin_coord[0][0] = tmp[0]
                            fin_coord[0][1] = tmp[1]
                            if rev == 2:
                                fin_coord[1] = 'z'
                            else:
                                if rev % 2 == 1:
                                    fin_coord[1] = 1
                                else:
                                    fin_coord[1] = -1

                            SEARCH = 0
                            for k in FORBIDDEN_POS[pos_fin[i]]:
                                if k[0] == fin_coord[0]:
                                    if fin_coord[1] == 'z':
                                        k[1] = 'z'
                                    else:
                                        k[1] += fin_coord[1]
                                    SEARCH = 1
                                    break
                            if SEARCH == 0:
                                FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                                FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                            OK = 1
                            break
                if OK == 0:
                    tmp[0] = 0
                    tmp[1] = last[1] - ymin
                    fin_coord[0][0] = tmp[0]
                    fin_coord[0][1] = tmp[1]
                    if rev == 2:
                        fin_coord[1] = 'z'
                    else:
                        if rev % 2 == 1:
                            fin_coord[1] = 1
                        else:
                            fin_coord[1] = -1
                    FORBIDDEN_POS[pos_fin['pos1']] = [[[0, 0], 0]]
                    FORBIDDEN_POS[pos_fin['pos1']][-1] = copy.deepcopy(fin_coord)

            ### VAN RENDES TÉGLALAP, AMI A KIALAKULT HELYZET KÖRÉ ÍRHATÓ
            else:
                for i in pos_fin:
                    if pos_fin[i] in FORBIDDEN_POS:
                        if i == 'pos1':
                            tmp[0] = last[0] - xmin
                            tmp[1] = ymax - last[1]
                            fin_coord[0][0] = tmp[0]
                            fin_coord[0][1] = tmp[1]
                            if rev == 2:
                                fin_coord[1] = 'z'
                            else:
                                if rev % 2 == 1:
                                    fin_coord[1] = 1
                                else:
                                    fin_coord[1] = -1

                            SEARCH = 0
                            for k in FORBIDDEN_POS[pos_fin[i]]:
                                if k[0] == fin_coord[0]:
                                    if fin_coord[1] == 'z':
                                        k[1] = 'z'
                                    else:
                                        k[1] += fin_coord[1]
                                    SEARCH = 1
                                    break
                            if SEARCH == 0:
                                FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                                FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                            OK = 1
                            break
                        elif i == 'pos2':
                            tmp[0] = ymax - last[1]
                            tmp[1] = xmax - last[0]
                            fin_coord[0][0] = tmp[0]
                            fin_coord[0][1] = tmp[1]
                            if rev == 2:
                                fin_coord[1] = 'z'
                            else:
                                if rev % 2 == 1:
                                    fin_coord[1] = 1
                                else:
                                    fin_coord[1] = -1

                            SEARCH = 0
                            for k in FORBIDDEN_POS[pos_fin[i]]:
                                if k[0] == fin_coord[0]:
                                    if fin_coord[1] == 'z':
                                        k[1] = 'z'
                                    else:
                                        k[1] += fin_coord[1]
                                    SEARCH = 1
                                    break
                            if SEARCH == 0:
                                FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                                FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                            OK = 1
                            break
                        elif i == 'pos3':
                            tmp[0] = xmax - last[0]
                            tmp[1] = last[1] - ymin
                            fin_coord[0][0] = tmp[0]
                            fin_coord[0][1] = tmp[1]
                            if rev == 2:
                                fin_coord[1] = 'z'
                            else:
                                if rev % 2 == 1:
                                    fin_coord[1] = 1
                                else:
                                    fin_coord[1] = -1

                            SEARCH = 0
                            for k in FORBIDDEN_POS[pos_fin[i]]:
                                if k[0] == fin_coord[0]:
                                    if fin_coord[1] == 'z':
                                        k[1] = 'z'
                                    else:
                                        k[1] += fin_coord[1]
                                    SEARCH = 1
                                    break
                            if SEARCH == 0:
                                FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                                FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                            OK = 1
                            break
                        elif i == 'pos4':
                            tmp[0] = last[1] - ymin
                            tmp[1] = last[0] - xmin
                            fin_coord[0][0] = tmp[0]
                            fin_coord[0][1] = tmp[1]
                            if rev == 2:
                                fin_coord[1] = 'z'
                            else:
                                if rev % 2 == 1:
                                    fin_coord[1] = 1
                                else:
                                    fin_coord[1] = -1

                            SEARCH = 0
                            for k in FORBIDDEN_POS[pos_fin[i]]:
                                if k[0] == fin_coord[0]:
                                    if fin_coord[1] == 'z':
                                        k[1] = 'z'
                                    else:
                                        k[1] += fin_coord[1]
                                    SEARCH = 1
                                    break
                            if SEARCH == 0:
                                FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                                FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                            OK = 1
                            break
                        elif i == 'pos5':
                            tmp[0] = ymax - last[1]
                            tmp[1] = last[0] - xmin
                            fin_coord[0][0] = tmp[0]
                            fin_coord[0][1] = tmp[1]
                            if rev == 2:
                                fin_coord[1] = 'z'
                            else:
                                if rev % 2 == 1:
                                    fin_coord[1] = 1
                                else:
                                    fin_coord[1] = -1

                            SEARCH = 0
                            for k in FORBIDDEN_POS[pos_fin[i]]:
                                if k[0] == fin_coord[0]:
                                    if fin_coord[1] == 'z':
                                        k[1] = 'z'
                                    else:
                                        k[1] += fin_coord[1]
                                    SEARCH = 1
                                    break
                            if SEARCH == 0:
                                FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                                FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                            OK = 1
                            break
                        elif i == 'pos6':
                            tmp[0] = xmax - last[0]
                            tmp[1] = ymax - last[1]
                            fin_coord[0][0] = tmp[0]
                            fin_coord[0][1] = tmp[1]
                            if rev == 2:
                                fin_coord[1] = 'z'
                            else:
                                if rev % 2 == 1:
                                    fin_coord[1] = 1
                                else:
                                    fin_coord[1] = -1

                            SEARCH = 0
                            for k in FORBIDDEN_POS[pos_fin[i]]:
                                if k[0] == fin_coord[0]:
                                    if fin_coord[1] == 'z':
                                        k[1] = 'z'
                                    else:
                                        k[1] += fin_coord[1]
                                    SEARCH = 1
                                    break
                            if SEARCH == 0:
                                FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                                FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                            OK = 1
                            break
                        elif i == 'pos7':
                            tmp[0] = last[1] - ymin
                            tmp[1] = xmax - last[0]
                            fin_coord[0][0] = tmp[0]
                            fin_coord[0][1] = tmp[1]
                            if rev == 2:
                                fin_coord[1] = 'z'
                            else:
                                if rev % 2 == 1:
                                    fin_coord[1] = 1
                                else:
                                    fin_coord[1] = -1

                            SEARCH = 0
                            for k in FORBIDDEN_POS[pos_fin[i]]:
                                if k[0] == fin_coord[0]:
                                    if fin_coord[1] == 'z':
                                        k[1] = 'z'
                                    else:
                                        k[1] += fin_coord[1]
                                    SEARCH = 1
                                    break
                            if SEARCH == 0:
                                FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                                FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                            OK = 1
                            break
                        elif i == 'pos8':
                            tmp[0] = last[0] - xmin
                            tmp[1] = last[1] - ymin
                            fin_coord[0][0] = tmp[0]
                            fin_coord[0][1] = tmp[1]
                            if rev == 2:
                                fin_coord[1] = 'z'
                            else:
                                if rev % 2 == 1:
                                    fin_coord[1] = 1
                                else:
                                    fin_coord[1] = -1

                            SEARCH = 0
                            for k in FORBIDDEN_POS[pos_fin[i]]:
                                if k[0] == fin_coord[0]:
                                    if fin_coord[1] == 'z':
                                        k[1] = 'z'
                                    else:
                                        k[1] += fin_coord[1]
                                    SEARCH = 1
                                    break
                            if SEARCH == 0:
                                FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                                FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                            OK = 1
                            break
                if OK == 0:
                    tmp[0] = last[0] - xmin
                    tmp[1] = ymax - last[1]
                    fin_coord[0][0] = tmp[0]
                    fin_coord[0][1] = tmp[1]
                    if rev == 2:
                        fin_coord[1] = 'z'
                    else:
                        if rev % 2 == 1:
                            fin_coord[1] = 1
                        else:
                            fin_coord[1] = -1
                    FORBIDDEN_POS[pos_fin['pos1']] = [[[0, 0], 0]]
                    FORBIDDEN_POS[pos_fin['pos1']][-1] = copy.deepcopy(fin_coord)


def learnt_zeroing(board, STEPS, FORBIDDEN_POS):
    # STEPS: LÉPÉSEK SZÁMA
    # FORBIDDEN_POS: TILTOTT POZÍCIÓK, AMIKET KI KELL NULLÁZNI

    # POZITÍV EXPONENCIÁIS PARAMÉTEREI      // f(x) = AP - BP * CP^(-x) //
    AP = 30  # LIMES
    BP = AP - 1
    CP = 1.02  # EXP. ALAPJA: GÖRBE ALAKJA

    # NEGATÍV EXPONENCIÁLIS PARAMÉTEREI     // f(x) = AM^(-BM * x) //
    AM = 1.03  # EXP. ALAPJA: GÖRBE ALAKJA
    BM = 1.5  # EXP. KITEVŐJE: GÖRBE ALAKJA

    w = len(board[0])
    h = len(board)
    xmin = xmax = 0  # TÉGLALAP KOORDINÁTÁI
    ymin = ymax = 0
    k = 0  # JELEKET SZÁMLÁLJA
    tmp = [0, 0]  # ÁTMENETILEG TÁROLJUK BENNE A KONVERTÁLT KOORDINÁTÁKAT

    ### ### ACTUÁLIS POZÍCIÓ, AMIT VIZSGÁLUNK
    act_pos = pos_rec(board, STEPS)

    ### ### A KIALAKULT POZÍCIÓ KÖRÉ ÍRHATÓ TÉGLALAP KÉT ÁTLÓS SARKÁNAK KOORDINÁTÁINAK MEGHATÁROZÁSA
    corners = rectangle_corner(board, STEPS)
    xmin = corners[0]
    ymin = corners[1]
    xmax = corners[2]
    ymax = corners[3]

    ### CSAK 1 JEL VAN, VAGYIS KEZDŐÁLLÁSNÁL VAGYUNK (XMIN = YMIN = XMAX = YMAX)
    if STEPS == 1:
        for i in act_pos:
            if act_pos[i] in FORBIDDEN_POS:
                for j in FORBIDDEN_POS[act_pos[i]]:
                    ### ELSŐ ESET: KEZDŐ JELHEZ KÉPEST SAROK MEZŐK VIZSG.
                    if j[0][1] == 1:
                        # ELŐRE MEGHATÁROZZUK A BEÍRANDÓ ÉRTÉKEKET
                        if j[1] == 'z':
                            VALUE = 0
                        else:
                            if j[1] > 0:
                                VALUE = AP - BP * CP ** (-j[1])
                            else:
                                VALUE = AM ** (BM * j[1])
                        # SZIMMETRIA MIATT
                        for k in (-1, 1):
                            for l in (-1, 1):
                                tmp[0] = xmax + k
                                tmp[1] = ymax + l
                                if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                                    if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                        print('IN ZEROING PROBLEM: 1 JEL, SAROK')
                                        print('POS:', tmp)
                                    board[tmp[1]][tmp[0]] = VALUE

                    ### MÁSODIK ESET: KEZDŐ JELHEZ KÉPEST KÖZVETLEN SZOMSZÉDOS MEZŐK VIZSG.
                    if j[0][1] == 0:
                        # ELŐRE MEGHATÁROZZUK A BEÍRANDÓ ÉRTÉKEKET
                        if j[1] == 'z':
                            VALUE = 0
                        else:
                            if j[1] > 0:
                                VALUE = AP - BP * CP ** (-j[1])
                            else:
                                VALUE = AM ** (BM * j[1])
                        # SZIMMETRIA MIATT
                        for k in (-1, 1):
                            tmp[0] = xmax + k
                            tmp[1] = ymax
                            if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                                if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                    print('IN ZEROING PROBLEM: 1 JEL, SZOMSZÉD1')
                                    print('POS:', tmp)
                                board[tmp[1]][tmp[0]] = VALUE
                            tmp[0] = xmax
                            tmp[1] = ymax + k
                            if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                                if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                    print('IN ZEROING PROBLEM: 1 JEL, SZOMSZÉD2')
                                    print('POS:', tmp)
                                board[tmp[1]][tmp[0]] = VALUE

    ### CSAK AZ X-TENGELLYEL PÁRHUZAMOSAN VANNAK A JELEK
    elif ymin == ymax:
        for i in act_pos:
            if act_pos[i] in FORBIDDEN_POS:
                for j in FORBIDDEN_POS[act_pos[i]]:
                    if i == 'pos1':
                        tmp[0] = xmin + j[0][0]
                        tmp[1] = ymax + j[0][1]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('\n\nIN ZEROING PROBLEM: X-TENGELY1.1')
                                print('POS:', tmp)
                                print_board(board, 0, 0)
                                print(act_pos)
                                print(j)
                                print('\n')
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

                        # TENGELYRE SZIMMETRIA MIATT
                        tmp[1] = ymax - j[0][1]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('\n\nIN ZEROING PROBLEM: X-TENGELY1.2')
                                print('POS:', tmp)
                                print_board(board, 0, 0)
                                print(act_pos)
                                print(j)
                                print('\n')
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

                    elif i == 'pos2':
                        tmp[0] = xmax - j[0][0]
                        tmp[1] = ymax + j[0][1]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('\n\nIN ZEROING PROBLEM: X-TENGELY2.1')
                                print('POS:', tmp)
                                print_board(board, 0, 0)
                                print(act_pos)
                                print(j)
                                print('\n')
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

                        # TENGELYRE SZIMMETRIA MIATT
                        tmp[1] = ymax - j[0][1]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('\n\nIN ZEROING PROBLEM: X-TENGELY2.2')
                                print('POS:', tmp)
                                print_board(board, 0, 0)
                                print(act_pos)
                                print(j)
                                print('\n')
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

    ### CSAK AZ Y-TENGELLYEL PÁRHUZAMOSAN VANNAK A JELEK
    elif xmin == xmax:
        for i in act_pos:
            if act_pos[i] in FORBIDDEN_POS:
                for j in FORBIDDEN_POS[act_pos[i]]:
                    if i == 'pos1':
                        tmp[0] = xmax + j[0][1]
                        tmp[1] = ymin + j[0][0]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('\n\nIN ZEROING PROBLEM: Y-TENGELY1.1')
                                print('POS:', tmp)
                                print_board(board, 0, 0)
                                print(act_pos)
                                print(j)
                                print('\n')
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

                        # TENGELYRE SZIMMETRIA MIATT
                        tmp[0] = xmax - j[0][1]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('\n\nIN ZEROING PROBLEM: Y-TENGELY1.2')
                                print('POS:', tmp)
                                print_board(board, 0, 0)
                                print(act_pos)
                                print(j)
                                print('\n')
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

                    elif i == 'pos2':
                        tmp[0] = xmax + j[0][1]
                        tmp[1] = ymax - j[0][0]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('\n\nIN ZEROING PROBLEM: Y-TENGELY2.1')
                                print('POS:', tmp)
                                print_board(board, 0, 0)
                                print(act_pos)
                                print(j)
                                print('\n')
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

                        # TENGELYRE SZIMMETRIA MIATT
                        tmp[0] = xmax - j[0][1]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('\n\nIN ZEROING PROBLEM: Y-TENGELY2.2')
                                print('POS:', tmp)
                                print_board(board, 0, 0)
                                print(act_pos)
                                print(j)
                                print('\n')
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

    ### VAN RENDES TÉGLALAP, AMI A KIALAKULT HELYZET KÖRÉ ÍRHATÓ
    else:
        for i in act_pos:
            if act_pos[i] in FORBIDDEN_POS:
                for j in FORBIDDEN_POS[act_pos[i]]:
                    if i == 'pos1':
                        tmp[0] = j[0][0] + xmin
                        tmp[1] = ymax - j[0][1]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('IN ZEROING PROBLEM: NORM1')
                                print('POS:', tmp)
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

                    elif i == 'pos2':
                        tmp[0] = xmax - j[0][1]
                        tmp[1] = ymax - j[0][0]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('IN ZEROING PROBLEM: NORM2')
                                print('POS:', tmp)
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

                    elif i == 'pos3':
                        tmp[0] = xmax - j[0][0]
                        tmp[1] = j[0][1] + ymin
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('IN ZEROING PROBLEM: NORM3')
                                print('POS:', tmp)
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

                    elif i == 'pos4':
                        tmp[0] = j[0][1] + xmin
                        tmp[1] = j[0][0] + ymin
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('IN ZEROING PROBLEM: NORM4')
                                print('POS:', tmp)
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

                    elif i == 'pos5':
                        tmp[0] = j[0][1] + xmin
                        tmp[1] = ymax - j[0][0]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('IN ZEROING PROBLEM: NORM5')
                                print('POS:', tmp)
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

                    elif i == 'pos6':
                        tmp[0] = xmax - j[0][0]
                        tmp[1] = ymax - j[0][1]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('IN ZEROING PROBLEM: NORM6')
                                print('POS:', tmp)
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

                    elif i == 'pos7':
                        tmp[0] = xmax - j[0][1]
                        tmp[1] = j[0][0] + ymin
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('IN ZEROING PROBLEM: NORM7')
                                print('POS:', tmp)
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])

                    elif i == 'pos8':
                        tmp[0] = j[0][0] + xmin
                        tmp[1] = j[0][1] + ymin
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            if board[tmp[1]][tmp[0]] == 'x' or board[tmp[1]][tmp[0]] == 'o':
                                print('IN ZEROING PROBLEM: NORM8')
                                print('POS:', tmp)
                            if j[1] == 'z':
                                board[tmp[1]][tmp[0]] = 0
                            else:
                                if j[1] > 0:
                                    board[tmp[1]][tmp[0]] = AP - BP * CP ** (-j[1])
                                else:
                                    board[tmp[1]][tmp[0]] = AM ** (BM * j[1])


def learn_coord_maker(RECTANGLE, COORD, POS, INVERZ):
    XMIN = RECTANGLE[0]
    YMIN = RECTANGLE[1]
    XMAX = RECTANGLE[2]
    YMAX = RECTANGLE[3]
    tmp = [0, 0]
    if INVERZ == 0:
        ### VAN RENDES TÉGLALAP
        if POS == 'pos1':
            tmp[0] = COORD[0] - XMIN
            tmp[1] = YMAX - COORD[1]
        elif POS == 'pos2':
            tmp[0] = YMAX - COORD[1]
            tmp[1] = XMAX - COORD[0]
        elif POS == 'pos3':
            tmp[0] = XMAX - COORD[0]
            tmp[1] = COORD[1] - YMIN
        elif POS == 'pos4':
            tmp[0] = COORD[1] - YMIN
            tmp[1] = COORD[0] - XMIN
        elif POS == 'pos5':
            tmp[0] = YMAX - COORD[1]
            tmp[1] = COORD[0] - XMIN
        elif POS == 'pos6':
            tmp[0] = XMAX - COORD[0]
            tmp[1] = YMAX - COORD[1]
        elif POS == 'pos7':
            tmp[0] = COORD[1] - YMIN
            tmp[1] = XMAX - COORD[0]
        elif POS == 'pos8':
            tmp[0] = COORD[0] - XMIN
            tmp[1] = COORD[1] - YMIN

        ### X-TENGELLYEL PÁRHUZAMOS
        elif POS == 'pos1x':
            tmp[0] = COORD[0] - XMIN
            if YMAX > COORD[1]:
                tmp[1] = YMAX - COORD[1]
            else:
                tmp[1] = COORD[1] - YMAX
        elif POS == 'pos2x':
            tmp[0] = XMAX - COORD[0]
            if YMAX > COORD[1]:
                tmp[1] = YMAX - COORD[1]
            else:
                tmp[1] = COORD[1] - YMAX

        ### Y-TENGELLYEL PÁRHUZAMOS
        elif POS == 'pos1y':
            tmp[0] = COORD[1] - YMIN
            if COORD[0] > XMIN:
                tmp[1] = COORD[0] - XMIN
            else:
                tmp[1] = XMIN - COORD[0]
        elif POS == 'pos2y':
            tmp[0] = YMAX - COORD[1]
            if XMAX > COORD[0]:
                tmp[1] = XMAX - COORD[0]
            else:
                tmp[1] = COORD[0] - XMAX

    if INVERZ == 1:
        if POS == 'pos1':
            tmp[0] = COORD[0] + XMIN
            tmp[1] = YMAX - COORD[1]
        elif POS == 'pos2':
            tmp[0] = XMAX - COORD[1]
            tmp[1] = YMAX - COORD[0]
        elif POS == 'pos3':
            tmp[0] = XMAX - COORD[0]
            tmp[1] = COORD[1] + YMIN
        elif POS == 'pos4':
            tmp[0] = COORD[1] + XMIN
            tmp[1] = COORD[0] + YMIN
        elif POS == 'pos5':
            tmp[0] = COORD[1] + XMIN
            tmp[1] = YMAX - COORD[0]
        elif POS == 'pos6':
            tmp[0] = XMAX - COORD[0]
            tmp[1] = YMAX - COORD[1]
        elif POS == 'pos7':
            tmp[0] = XMAX - COORD[1]
            tmp[1] = COORD[0] + YMIN
        elif POS == 'pos8':
            tmp[0] = COORD[0] + XMIN
            tmp[1] = COORD[1] + YMIN

    return tmp


def learn_debug(board, STEPS, LAST_STEPS, FORBIDDEN_POS):
    w = len(board[0])
    h = len(board)
    xmin = xmax = 0  # TÉGLALAP KOORDINÁTÁI
    ymin = ymax = 0
    last = [0, 0]  # UTOLSÓ LÉPÉS
    tmp = [0, 0]  # ÁTMENETILEG TÁROLJUK BENNE A KONVERTÁLT KOORDINÁTÁKAT
    fin_coord = [[0, 0], 0]  #
    OK = 0  # INDIKÁTORA, HOGY TALÁLTUNK-E PASSZOLÓ ÁLLÁST

    # UTOLSÓ LÉPÉS (VISSZA LETT MÁR VONVA, DE VIZSGÁLJUK, HOGY MELYIK HELYZETBEN LETT LÉPVE)
    last = LAST_STEPS[-1]

    # POZÍCIÓK MEGHATÁROZÁSA
    pos_fin = pos_rec(board, STEPS)
    written = []
    s = 0       # JELEKET SZÁMLÁLJA
    rev = 2

    ### SZIMMETRIA VIZSGÁLAT
    # ÖSSZES SZIMMETRIA PÁR LISTÁBAN ÉS HALMAZOKBAN
    simmetry_tmp = []
    for i in pos_fin:
        for j in pos_fin:
            if i != j and pos_fin[i] == pos_fin[j]:
                simmetry_tmp.append({i, j})

    # HALMAZOK ÖSSZEFŰZÉSE
    simmetry = []
    set_tmp = set()
    CONTAIN = 0
    for seti in simmetry_tmp:
        set_tmp = seti
        for setj in simmetry_tmp:
            if seti & setj != set():
                set_tmp = set_tmp | seti | setj
        for k in simmetry:
            if k == set_tmp:
                CONTAIN = 1
        if CONTAIN == 0:
            simmetry.append(set_tmp)
        CONTAIN = 0

    ### BEÍRANDÓ ÉRTÉK MEGHATÁROZÁSA (fin_coord[1])
    if rev == 2:
        VALUE = 'z'
    else:
        if rev % 2 == 1:
            VALUE = 1
        else:
            VALUE = -1

    ### ### A KIALAKULT POZÍCIÓ KÖRÉ ÍRHATÓ TÉGLALAP KÉT ÁTLÓS SARKÁNAK KOORDINÁTÁINAK MEGHATÁROZÁSA
    for y in range(h):
        for x in range(w):
            if board[y][x] == 'x' or board[y][x] == 'o':
                s += 1
                if s == 1:
                    ymin = y
                    xmin = x
                    xmax = x
                    ymax = y
                elif s == STEPS:
                    ymax = y
                    if x < xmin:
                        xmin = x
                    if x > xmax:
                        xmax = x
                else:
                    if x < xmin:
                        xmin = x
                    if x > xmax:
                        xmax = x

    print('1. ELLENŐRZÉS: TÉGLALAP KOORD:', xmin, ymin, xmax, ymax)
    ### X VAGY Y TENGELYEKKEL PÁRHUZAMOSAN VANNAK A JELEK
    if ymin == ymax or xmin == xmax:
        if len(simmetry) == 2:
            if ymin == ymax:
                simmetry = {'pos1x', 'pos2x'}
            elif xmin == xmax:
                simmetry = {'pos1y', 'pos2y'}
            for i in pos_fin:
                if pos_fin[i] in FORBIDDEN_POS:
                    for p in simmetry:
                        fin_coord[0] = learn_coord_maker(xmin, ymin, xmax, ymax, last, p)
                        fin_coord[1] = VALUE

                        SEARCH = 0
                        WRITE = 1
                        for k in FORBIDDEN_POS[pos_fin[i]]:
                            if k[0] == fin_coord[0]:
                                SEARCH = 1
                                for q in written:
                                    if q[0] == fin_coord[0]:
                                        WRITE = 0
                                if WRITE == 1:
                                    if fin_coord[1] == 'z':
                                        k[1] = 'z'
                                    else:
                                        k[1] += fin_coord[1]

                                    ### AMELYIK KOORDINÁTÁT MÁR ÍRTUK, AZT ELMENTJÜK
                                    WAS = 0
                                    for t in written:
                                        if t[0] == fin_coord[0]:
                                            WAS = 1
                                    if WAS == 0:
                                        written.append(fin_coord)
                                break

                        if SEARCH == 0:
                            FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                            FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                    OK = 1
            if OK == 0:
                a = 0
                for p in simmetry:
                    a += 1
                    fin_coord[0] = learn_coord_maker(xmin, ymin, xmax, ymax, last, p)
                    fin_coord[1] = VALUE
                    if a == 1:
                        FORBIDDEN_POS[pos_fin['pos1']] = [[[0, 0], 0]]
                        FORBIDDEN_POS[pos_fin['pos1']][-1] = copy.deepcopy(fin_coord)
                    else:
                        if FORBIDDEN_POS[pos_fin['pos1']][-1] != fin_coord:
                            FORBIDDEN_POS[pos_fin['pos1']].append([[0, 0], 0])
                            FORBIDDEN_POS[pos_fin['pos1']][-1] = copy.deepcopy(fin_coord)
        else:
            if ymin == ymax:
                pxy = ['pos1x', 'pos2x']
            elif xmin == xmax:
                pxy = ['pos1y', 'pos2y']
            for i in pos_fin:
                if pos_fin[i] in FORBIDDEN_POS:
                    if i == 'pos1':
                        fin_coord[0] = learn_coord_maker(xmin, ymin, xmax, ymax, last, pxy[0])
                        fin_coord[1] = VALUE

                        SEARCH = 0
                        for k in FORBIDDEN_POS[pos_fin[i]]:
                            if k[0] == fin_coord[0]:
                                if fin_coord[1] == 'z':
                                    k[1] = 'z'
                                else:
                                    k[1] += fin_coord[1]
                                SEARCH = 1
                                break
                        if SEARCH == 0:
                            FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                            FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                        OK = 1
                        break
                    elif i == 'pos2':
                        fin_coord[0] = learn_coord_maker(xmin, ymin, xmax, ymax, last, pxy[1])
                        fin_coord[1] = VALUE

                        SEARCH = 0
                        for k in FORBIDDEN_POS[pos_fin[i]]:
                            if k[0] == fin_coord[0]:
                                if fin_coord[1] == 'z':
                                    k[1] = 'z'
                                else:
                                    k[1] += fin_coord[1]
                                SEARCH = 1
                                break
                        if SEARCH == 0:
                            FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                            FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                        OK = 1
                        break
            if OK == 0:
                fin_coord[0] = learn_coord_maker(xmin, ymin, xmax, ymax, last, pxy[0])
                fin_coord[1] = VALUE
                FORBIDDEN_POS[pos_fin['pos1']] = [[[0, 0], 0]]
                FORBIDDEN_POS[pos_fin['pos1']][-1] = copy.deepcopy(fin_coord)

    ### VAN RENDES TÉGLALAP
    else:
        for i in pos_fin:
            if pos_fin[i] in FORBIDDEN_POS:
                if simmetry != []:
                    for psets in simmetry:
                        if i in psets:
                            for p in psets:
                                fin_coord[0] = learn_coord_maker(xmin, ymin, xmax, ymax, last, p)
                                fin_coord[1] = VALUE
                                SEARCH = 0
                                for k in FORBIDDEN_POS[pos_fin[i]]:
                                    if k[0] == fin_coord[0]:
                                        SEARCH = 1
                                        for q in written:
                                            if q[0] == fin_coord[0]:
                                                WRITE = 0
                                        if WRITE == 1:
                                            if fin_coord[1] == 'z':
                                                k[1] = 'z'
                                            else:
                                                k[1] += fin_coord[1]

                                            ### AMELYIK KOORDINÁTÁT MÁR ÍRTUK, AZT ELMENTJÜK
                                            WAS = 0
                                            for t in written:
                                                if t[0] == fin_coord[0]:
                                                    WAS = 1
                                            if WAS == 0:
                                                written.append(fin_coord)
                                        break
                                if SEARCH == 0:
                                    FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                                    FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                                OK = 1
                else:
                    fin_coord[0] = learn_coord_maker(xmin, ymin, xmax, ymax, last, i)
                    fin_coord[1] = VALUE
                    SEARCH = 0
                    for k in FORBIDDEN_POS[pos_fin[i]]:
                        if k[0] == fin_coord[0]:
                            if fin_coord[1] == 'z':
                                k[1] = 'z'
                            else:
                                k[1] += fin_coord[1]
                            SEARCH = 1
                            break
                    if SEARCH == 0:
                        FORBIDDEN_POS[pos_fin[i]].append([[0, 0], 0])
                        FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                    OK = 1
                break
        if OK == 0:
            if simmetry != []:
                s = 0
                for psets in simmetry:
                    if 'pos1' in psets:
                        for p in psets:
                            s += 1
                            fin_coord[0] = learn_coord_maker(xmin, ymin, xmax, ymax, last, p)
                            fin_coord[1] = VALUE
                            if s == 1:
                                FORBIDDEN_POS[pos_fin['pos1']] = [[[0, 0], 0]]
                                FORBIDDEN_POS[pos_fin['pos1']][-1] = copy.deepcopy(fin_coord)
                            else:
                                for t in FORBIDDEN_POS[pos_fin['pos1']]:
                                    if fin_coord[0] != t[0]:
                                        FORBIDDEN_POS[pos_fin['pos1']].append([[0, 0], 0])
                                        FORBIDDEN_POS[pos_fin['pos1']][-1] = copy.deepcopy(fin_coord)
            else:
                fin_coord[0] = learn_coord_maker(xmin, ymin, xmax, ymax, last, i)
                fin_coord[1] = VALUE
                FORBIDDEN_POS[pos_fin['pos1']] = [[[0, 0], 0]]
                FORBIDDEN_POS[pos_fin['pos1']][-1] = copy.deepcopy(fin_coord)

def put_patter(board, POSITION, ALIGN, PATTERN, DIRECTION):
    h = len(board)
    w = len(board[0])
    l = len(PATTERN)
    l2 = int(l / 2)
    l2 = 0
    # for x in range(len(board[0])):
    #     for y in range(len(board)):
    #         board[y][x] = 0

    ### MIDDLE
    if POSITION == 'm':
        x = int(w / 2)
        y = int(h / 2)
        ### HORIZONTÁLIS
        if ALIGN == 'h':
            x -= l2
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y][x + i] = 0
                    elif PATTERN[i] == 1:
                        board[y][x + i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y][x + i] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y][x + i - 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y][x + i - 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y][x + i - 1] = 'o'
        ### VERTIKÁLIS
        elif ALIGN == 'v':
            y -= l2
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y + i][x] = 0
                    elif PATTERN[i] == 1:
                        board[y + i][x] = 'x'
                    elif PATTERN[i] == 2:
                        board[y + i][x] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y + i - 1][x] = 0
                    elif PATTERN[-i] == 1:
                        board[y + i - 1][x] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y + i - 1][x] = 'o'
        ### DIAGONÁLIS+
        elif ALIGN == 'd+':
            x -= l2
            y -= l2
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y + i][x + i] = 0
                    elif PATTERN[i] == 1:
                        board[y + i][x + i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y + i][x + i] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y + i - 1][x + i - 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y + i - 1][x + i - 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y + i - 1][x + i - 1] = 'o'
        ### DIAGONÁLIS-
        elif ALIGN == 'd-':
            x += l2
            y -= l2
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y + i][x - i] = 0
                    elif PATTERN[i] == 1:
                        board[y + i][x - i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y + i][x - i] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y + i - 1][x - i + 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y + i - 1][x - i + 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y + i - 1][x - i + 1] = 'o'

    ### ### TOP
    elif POSITION == 't':
        x = int(w / 2)
        y = 0
        ### HORIZONTÁLIS
        if ALIGN == 'h':
            x -= l2
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y][x + i] = 0
                    elif PATTERN[i] == 1:
                        board[y][x + i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y][x + i] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y][x + i - 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y][x + i - 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y][x + i - 1] = 'o'
        ### VERTIKÁLIS
        elif ALIGN == 'v':
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y + i][x] = 0
                    elif PATTERN[i] == 1:
                        board[y + i][x] = 'x'
                    elif PATTERN[i] == 2:
                        board[y + i][x] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y + i - 1][x] = 0
                    elif PATTERN[-i] == 1:
                        board[y + i - 1][x] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y + i - 1][x] = 'o'
        ### DIAGONÁLIS+
        elif ALIGN == 'd+':
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y + i][x + i] = 0
                    elif PATTERN[i] == 1:
                        board[y + i][x + i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y + i][x + i] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y + i - 1][x + i - 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y + i - 1][x + i - 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y + i - 1][x + i - 1] = 'o'
        ### DIAGONÁLIS-
        elif ALIGN == 'd-':
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y + i][x - i] = 0
                    elif PATTERN[i] == 1:
                        board[y + i][x - i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y + i][x - i] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y + i - 1][x - i + 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y + i - 1][x - i + 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y + i - 1][x - i + 1] = 'o'

    ### ### RIGHT
    elif POSITION == 'r':
        x = w - 1
        y = int(h / 2)
        ### HORIZONTÁLIS
        if ALIGN == 'h':
            if DIRECTION == 'F':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y][x - i + 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y][x - i + 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y][x - i + 1] = 'o'
            elif DIRECTION == 'B':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y][x - i] = 0
                    elif PATTERN[i] == 1:
                        board[y][x - i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y][x - i] = 'o'
        elif ALIGN == 'v':
            y -= l2
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y + i][x] = 0
                    elif PATTERN[i] == 1:
                        board[y + i][x] = 'x'
                    elif PATTERN[i] == 2:
                        board[y + i][x] = 'o'
            if DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y + i - 1][x] = 0
                    elif PATTERN[-i] == 1:
                        board[y + i - 1][x] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y + i - 1][x] = 'o'
        elif ALIGN == 'd+':
            if DIRECTION == 'F':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y - i + 1][x - i + 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y - i + 1][x - i + 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y - i + 1][x - i + 1] = 'o'
            elif DIRECTION == 'B':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y - i][x - i] = 0
                    elif PATTERN[i] == 1:
                        board[y - i][x - i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y - i][x - i] = 'o'
        elif ALIGN == 'd-':
            if DIRECTION == 'F':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y + i - 1][x - i + 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y + i - 1][x - i + 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y + i - 1][x - i + 1] = 'o'
            elif DIRECTION == 'B':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y + i][x - i] = 0
                    elif PATTERN[i] == 1:
                        board[y + i][x - i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y + i][x - i] = 'o'

    ### ### LEFT
    elif POSITION == 'l':
        x = 0
        y = int(h / 2)
        ### HORIZONTÁLIS
        if ALIGN == 'h':
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y][x + i] = 0
                    elif PATTERN[i] == 1:
                        board[y][x + i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y][x + i] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y][x + i - 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y][x + i - 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y][x + i - 1] = 'o'
        ### VERTIKÁLIS
        elif ALIGN == 'v':
            y -= l2
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y + i][x] = 0
                    elif PATTERN[i] == 1:
                        board[y + i][x] = 'x'
                    elif PATTERN[i] == 2:
                        board[y + i][x] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y + i - 1][x] = 0
                    elif PATTERN[-i] == 1:
                        board[y + i - 1][x] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y + i - 1][x] = 'o'
        ### DIAGONÁLIS+
        elif ALIGN == 'd+':
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y + i][x + i] = 0
                    elif PATTERN[i] == 1:
                        board[y + i][x + i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y + i][x + i] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y + i - 1][x + i - 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y + i - 1][x + i - 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y + i - 1][x + i - 1] = 'o'
        ### DIAGONÁLIS-
        elif ALIGN == 'd-':
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y - i][x + i] = 0
                    elif PATTERN[i] == 1:
                        board[y - i][x + i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y - i][x + i] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y - i + 1][x + i - 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y - i + 1][x + i - 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y - i + 1][x + i - 1] = 'o'

    ### ### BOTTOM
    elif POSITION == 'b':
        x = int(w / 2)
        y = h - 1
        ### HORIZONTÁLIS
        if ALIGN == 'h':
            x -= l2
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y][x + i] = 0
                    elif PATTERN[i] == 1:
                        board[y][x + i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y][x + i] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y][x + i - 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y][x + i - 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y][x + i - 1] = 'o'
        ### VERTIKÁLIS
        elif ALIGN == 'v':
            if DIRECTION == 'F':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y - i + 1][x] = 0
                    elif PATTERN[-i] == 1:
                        board[y - i + 1][x] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y - i + 1][x] = 'o'
            elif DIRECTION == 'B':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y - i][x] = 0
                    elif PATTERN[i] == 1:
                        board[y - i][x] = 'x'
                    elif PATTERN[i] == 2:
                        board[y - i][x] = 'o'
        ### DIAGONÁLIS+
        elif ALIGN == 'd+':
            if DIRECTION == 'F':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y - i + 1][x - i] = 0
                    elif PATTERN[-i] == 1:
                        board[y - i + 1][x - i] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y - i + 1][x - i] = 'o'
            elif DIRECTION == 'B':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y - i][x - i] = 0
                    elif PATTERN[i] == 1:
                        board[y - i][x - i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y - i][x - i] = 'o'
        ### DIAGONÁLIS-
        elif ALIGN == 'd-':
            if DIRECTION == 'F':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y - i + 1][x + i] = 0
                    elif PATTERN[-i] == 1:
                        board[y - i + 1][x + i] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y - i + 1][x + i] = 'o'
            elif DIRECTION == 'B':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y - i][x + i] = 0
                    elif PATTERN[i] == 1:
                        board[y - i][x + i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y - i][x + i] = 'o'

    ### ### TOP LEFT
    elif POSITION == 'tl':
        x = 0
        y = 0
        ### HORIZONTÁLIS
        if ALIGN == 'h':
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y][x + i] = 0
                    elif PATTERN[i] == 1:
                        board[y][x + i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y][x + i] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y][x + i - 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y][x + i - 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y][x + i - 1] = 'o'
        ### VERTIKÁLIS
        elif ALIGN == 'v':
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y + i][x] = 0
                    elif PATTERN[i] == 1:
                        board[y + i][x] = 'x'
                    elif PATTERN[i] == 2:
                        board[y + i][x] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y + i - 1][x] = 0
                    elif PATTERN[-i] == 1:
                        board[y + i - 1][x] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y + i - 1][x] = 'o'
        ### DIAGONÁLIS+
        elif ALIGN == 'd+':
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y + i][x + i] = 0
                    elif PATTERN[i] == 1:
                        board[y + i][x + i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y + i][x + i] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y + i - 1][x + i - 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y + i - 1][x + i - 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y + i - 1][x + i - 1] = 'o'
        ### DIAGONÁLIS-
        elif ALIGN == 'd-':
            pass

    ### ### TOP RIGHT
    elif POSITION == 'tr':
        x = w - 1
        y = 0
        ### HORIZONTÁLIS
        if ALIGN == 'h':
            if DIRECTION == 'F':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y][x - i + 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y][x - i + 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y][x - i + 1] = 'o'
            elif DIRECTION == 'B':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y][x - i] = 0
                    elif PATTERN[i] == 1:
                        board[y][x - i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y][x - i] = 'o'
        elif ALIGN == 'v':
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y + i][x] = 0
                    elif PATTERN[i] == 1:
                        board[y + i][x] = 'x'
                    elif PATTERN[i] == 2:
                        board[y + i][x] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y + i - 1][x] = 0
                    elif PATTERN[-i] == 1:
                        board[y + i - 1][x] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y + i - 1][x] = 'o'
        elif ALIGN == 'd+':
            pass
        elif ALIGN == 'd-':
            if DIRECTION == 'F':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y + i - 1][x - i + 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y + i - 1][x - i + 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y + i - 1][x - i + 1] = 'o'
            elif DIRECTION == 'B':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y + i][x - i] = 0
                    elif PATTERN[i] == 1:
                        board[y + i][x - i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y + i][x - i] = 'o'

    ### ### BOTTOM LEFT
    elif POSITION == 'bl':
        x = 0
        y = h - 1
        ### HORIZONTÁLIS
        if ALIGN == 'h':
            if DIRECTION == 'F':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y][x + i] = 0
                    elif PATTERN[i] == 1:
                        board[y][x + i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y][x + i] = 'o'
            elif DIRECTION == 'B':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y][x + i - 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y][x + i - 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y][x + i - 1] = 'o'
        ### VERTIKÁLIS
        elif ALIGN == 'v':
            if DIRECTION == 'F':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y - i + 1][x] = 0
                    elif PATTERN[-i] == 1:
                        board[y - i + 1][x] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y - i + 1][x] = 'o'
            elif DIRECTION == 'B':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y - i][x] = 0
                    elif PATTERN[i] == 1:
                        board[y - i][x] = 'x'
                    elif PATTERN[i] == 2:
                        board[y - i][x] = 'o'
        ### DIAGONÁLIS+
        elif ALIGN == 'd+':
            pass
        ### DIAGONÁLIS-
        elif ALIGN == 'd-':
            if DIRECTION == 'F':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y - i + 1][x + i - 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y - i + 1][x + i - 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y - i + 1][x + i - 1] = 'o'
            elif DIRECTION == 'B':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y - i][x + i] = 0
                    elif PATTERN[i] == 1:
                        board[y - i][x + i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y - i][x + i] = 'o'

    ### ### BOTTOM RIGHT
    elif POSITION == 'br':
        x = w - 1
        y = h - 1
        ### HORIZONTÁLIS
        if ALIGN == 'h':
            if DIRECTION == 'F':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y][x - i + 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y][x - i + 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y][x - i + 1] = 'o'
            elif DIRECTION == 'B':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y][x - i] = 0
                    elif PATTERN[i] == 1:
                        board[y][x - i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y][x - i] = 'o'
        ### VERTIKÁLIS
        elif ALIGN == 'v':
            if DIRECTION == 'F':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y - i + 1][x] = 0
                    elif PATTERN[-i] == 1:
                        board[y - i + 1][x] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y - i + 1][x] = 'o'
            elif DIRECTION == 'B':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y - i][x] = 0
                    elif PATTERN[i] == 1:
                        board[y - i][x] = 'x'
                    elif PATTERN[i] == 2:
                        board[y - i][x] = 'o'
        ### DIAGONÁLIS+
        elif ALIGN == 'd+':
            if DIRECTION == 'F':
                for i in range(1, len(PATTERN) + 1):
                    if PATTERN[-i] == 0:
                        board[y - i + 1][x - i + 1] = 0
                    elif PATTERN[-i] == 1:
                        board[y - i + 1][x - i + 1] = 'x'
                    elif PATTERN[-i] == 2:
                        board[y - i + 1][x - i + 1] = 'o'
            elif DIRECTION == 'B':
                for i in range(len(PATTERN)):
                    if PATTERN[i] == 0:
                        board[y - i][x - i] = 0
                    elif PATTERN[i] == 1:
                        board[y - i][x - i] = 'x'
                    elif PATTERN[i] == 2:
                        board[y - i][x - i] = 'o'
        ### DIAGONÁLIS-
        elif ALIGN == 'd-':
            pass



def draw_pos(board, POS):
    height = len(board)
    width = len(board[0])
    steps = len(POS) // 5
    tmp_board = list(range(height))
    for y in range(len(tmp_board)):
        tmp_board[y] = list(range(width))
        for x in range(len(tmp_board[y])):
            tmp_board[y][x] = 0

    for k in range(steps):
        x = int(POS[5 * k] + POS[5 * k + 1])
        y = int(POS[5 * k + 2] + POS[5 * k + 3])
        y = height - 1 - y
        SIGN = POS[5 * k + 4]

        take_fix(tmp_board, (x, y), SIGN)

    print_board(tmp_board, 0, 1)

def if_simmetry(board, POS):
    height = len(board)
    width = len(board[0])
    steps = len(POS) // 5
    tmp_board = list(range(height))
    for y in range(len(tmp_board)):
        tmp_board[y] = list(range(width))
        for x in range(len(tmp_board[y])):
            tmp_board[y][x] = 0

    for k in range(steps):
        x = int(POS[5 * k] + POS[5 * k + 1])
        y = int(POS[5 * k + 2] + POS[5 * k + 3])
        SIGN = POS[5 * k + 4]

        take_fix(tmp_board, (x, y), SIGN)

    pos_fin = pos_rec(tmp_board, steps)

    ### SZIMMETRIA VIZSGÁLAT
    # ÖSSZES POZICIÓT BELETESSZÜK EGY HALMAZBA, HA VAN EGYFORMA, AKKOR NEM DUPLIKÁLÓDNAK
    simmetry = set()
    for i in pos_fin:
        simmetry.add(pos_fin[i])

    return simmetry

def pos_expand(w, h, POS):
    steps = len(POS) // 5
    tmp_board = list(range(h))
    expanded = [tuple(), dict()]
    for y in range(len(tmp_board)):
        tmp_board[y] = list(range(w))
        for x in range(len(tmp_board[y])):
            tmp_board[y][x] = 0

    for k in range(steps):
        x = int(POS[5 * k] + POS[5 * k + 1])
        y = int(POS[5 * k + 2] + POS[5 * k + 3])
        y = h - 1 - y
        SIGN = POS[5 * k + 4]

        take_fix(tmp_board, (x, y), SIGN)

    expanded[0] = rectangle_corner(tmp_board, steps)
    expanded[1] = pos_rec(tmp_board, steps)

    return expanded


def merge_2pos(w, h, FORBIDDEN_POS1, FORBIDDEN_POS2):
    ### FORBIDDEN_POS1 = FORBIDDEN_POS1 + FORBIDDEN_POS2
    for pos2 in FORBIDDEN_POS2:
        # POS2 KIBONTÁSA -> ÖSSZES LEHETSÉGES LEÍRÁSA AZ ÁLLÁSNAK
        pos2_all = pos_expand(w, h, pos2)

        ### NEM X-TENGELLYEL PÁRHUZAMOS ALAKZATRÓL VAN SZÓ
            ### 'VAGY' RÉSZ A KEZDŐÁLLÁS MIATT KELL, MERT AZT IS ITT VIZSGÁLJUK
        if pos2_all[0][1] != pos2_all[0][3] or pos2_all[0][0] == pos2_all[0][2]:

            ### AZ ADOTT POZÍCIÓ NINCS AZZAL A KONKRÉT KARAKTERSOROZATTAL A FORBIDDEN_POS1-BEN
            if pos2 not in FORBIDDEN_POS1:
                # KERESÉS, HOGY BENNE VAN-E VALAMELYIK POS2_ALL A FORBIDDEN_POS1-BEN
                pos1 = ''
                for p in pos2_all[1]:
                    if pos2_all[1][p] in FORBIDDEN_POS1:
                        pos_mutual = p
                        pos1 = pos2_all[1][p]
                        break

                # VAN TALÁLAT
                if pos1 != '':
                    # POS2 KOORDINÁTÁINAK KONVERTÁLÁSA -> ABS -> POS_MUTUAL
                    for data2 in FORBIDDEN_POS2[pos2]:
                        coord_abs = learn_coord_maker(pos2_all[0], data2[0], 'pos1', 1)
                        coord1_calc = learn_coord_maker(pos2_all[0], coord_abs, pos_mutual, 0)

                        # MINDEN KOORDINÁTÁN LÉVŐ ADATOKAT ÖSSZEADUNK VAGY HOZZÁÍRJUK
                        ADD = 0
                        for data1 in FORBIDDEN_POS1[pos1]:
                            if coord1_calc == data1[0]:
                                if data2[1][0] == 'z' and data1[1][0] != 'z':
                                    data1[1][0] = 'z'
                                elif data2[1][0] != 'z' and data1[1][0] != 'z':
                                    data1[1][0] += data2[1][0]
                                data1[1][1] += data2[1][1]
                                ADD = 0
                                break
                            else:
                                ADD = 1
                        if ADD == 1:
                            FORBIDDEN_POS1[pos1].append([[0, 0], [0, 0]])
                            FORBIDDEN_POS1[pos1][-1][0] = copy.deepcopy(coord1_calc)
                            FORBIDDEN_POS1[pos1][-1][1] = copy.deepcopy(data2[1])
                # NINCS TALÁLAT
                else:
                    FORBIDDEN_POS1[pos2] = FORBIDDEN_POS2[pos2]

            ### AZ ADOTT POZÍCIÓ MINDKÉT SZÓTÁRBAN UGYANAZZAL A KARAKTERSOROZATTAL SZEREPEL
            else:
                ADD = 0
                for data2 in FORBIDDEN_POS2[pos2]:
                    for data1 in FORBIDDEN_POS1[pos2]:
                        if data1[0] == data2[0]:
                            if data2[1][0] == 'z' and data1[1][0] != 'z':
                                data1[1][0] = 'z'
                            elif data2[1][0] != 'z' and data1[1][0] != 'z':
                                data1[1][0] += data2[1][0]
                            data1[1][1] += data2[1][1]
                            ADD = 0
                            break
                        else:
                            ADD = 1
                    if ADD == 1:
                        FORBIDDEN_POS1[pos2].append([[0, 0], [0, 0]])
                        FORBIDDEN_POS1[pos2][-1] = copy.deepcopy(data2)

        ### X-TENGELLYEL PÁRHUZAMOS ALAKZATRÓL VAN SZÓ
        else:
            ### MEGVIZSGÁLJUK, HOGY SZEREPEL-E AZ ALAKZAT 2 KARAKTERSOROZATA VALAMELYIKE A FORBIDDEN_POS1-BEN
            pos = ''
            if pos2_all[1]['pos1'] in FORBIDDEN_POS1:
                pos = pos2_all[1]['pos1']
            elif pos2_all[1]['pos2'] in FORBIDDEN_POS1:
                pos = pos2_all[1]['pos2']

            if pos != '':
                INV = 0
                if pos2 != pos:
                    x_delta = pos2_all[0][2] - pos2_all[0][0]
                    INV = 1
                ADD = 0

                for data2 in FORBIDDEN_POS2[pos2]:
                    data2_tmp1 = copy.deepcopy(data2)
                    data2_tmp2 = copy.deepcopy(data2)
                    data2_tmp2[0][1] *= -1
                    if INV == 1:
                        data2_tmp1[0][0] = x_delta - data2_tmp1[0][0]
                        data2_tmp2[0][0] = x_delta - data2_tmp2[0][0]

                    for data1 in FORBIDDEN_POS1[pos]:
                        if data2_tmp1[0] == data1[0] or data2_tmp2[0] == data1[0]:
                            if data2[1][0] == 'z' and data1[1][0] != 'z':
                                data1[1][0] = 'z'
                            elif data2[1][0] != 'z' and data1[1][0] != 'z':
                                data1[1][0] += data2[1][0]
                            data1[1][1] += data2[1][1]
                            ADD = 0
                            break
                        else:
                            ADD = 1
                    if ADD == 1:
                        FORBIDDEN_POS1[pos].append([[0, 0], [0, 0]])
                        FORBIDDEN_POS1[pos][-1] = copy.deepcopy(data2_tmp1)
            else:
                FORBIDDEN_POS1[pos2] = FORBIDDEN_POS2[pos2]


def main():
    s = 'v'
    # s = input('Melyik legyen?\n')
    if s == 'd-':
        board = ([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 'x', 0, 0, 0, 'x', 0],
                 [0, 0, 0, 0, 0, 0, 0, 'x', 0, 0, 0, 'x', 0, 0],
                 [0, 0, 0, 0, 0, 0, 'x', 0, 0, 0, 'x', 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 'x', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 'x', 0, 0, 0, 'o', 0, 0, 0, 0, 0, 'x', 0],
                 [0, 'x', 0, 0, 0, 0, 0, 0, 0, 0, 0, 'x', 0, 0],
                 [0, 0, 0, 0, 'x', 0, 0, 0, 0, 0, 'x', 0, 0, 0],
                 [0, 0, 0, 'x', 0, 0, 'x', 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 'x', 0, 0, 'x', 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 'x', 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


    elif s == 'd+':
        #          0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19
        board = ([ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],  # 0
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],  # 1
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],  # 2
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],  # 3
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],  # 4
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],  # 5
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],  # 6
                 [ 0 , 0 , 0 , 0 , 0 ,'x','x','o', 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],  # 7
                 [ 0 , 0 , 0 , 0 ,'o','o', 0 ,'x', 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],  # 8
                 [ 0 , 0 , 0 , 0 , 0 ,'x','o','x', 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],  # 9
                 [ 0 , 0 , 0 , 0 ,'x', 0 ,'o', 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],  # 10
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],  # 11
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ])  # 12

    elif s == 'v':
        board = ([ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 ,'o', 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ])

    elif s == 'h':
        board = ([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    elif s == 'r':
        board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 'x', 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 'o', 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 'o', 'x', 0, 0, 0, 0],
                 [0, 0, 'x', 0, 0, 0, 'o', 0, 0, 0, 0],
                 [0, 'x', 'o', 'o', 'o', 'o', 'x', 'o', 0, 0, 0],
                 [0, 0, 0, 0, 'x', 'o', 'x', 0, 'x', 0, 0],
                 [0, 0, 0, 0, 0, 0, 'o', 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 ]

    h = len(board)
    w = len(board[0])
    all_sign = {'o', 'x'}
    direction = {'h', 'v', 'd+', 'd-'}
    steps = []
    #forbidden_pos = {'0000x0200o0101x0201o0301x0002o0102o0302x0103x0203x0303o':[[3,-1]]}
    forbidden_pos1 = {}
    forbidden_pos2 = {}
    k = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'o' or board[i][j] == 'x':
                k += 1
                steps.append([j, i])
            else:
                board[i][j] = 1


    pos_all = pos_rec(board, k)
    pos_exp = pos_expand(w, h, pos_all['pos1'])
    print(pos_expand(w, h, pos_all['pos1']))
    print(pos_exp[0][1])
    print(pos_exp[0][3])
    print(pos_exp[1]['pos1'])
    print(pos_exp[1]['pos2'])
    return 0
    forbidden_pos1[pos_all['pos1']] = [[[-1, 1], [1, 1]]]
    forbidden_pos2[pos_all['pos2']] = [[[4, 1], [2, 2]]]
    print('Pos1:')
    draw_pos(board, pos_all['pos1'])
    print('Pos2:')
    draw_pos(board, pos_all['pos2'])

    print('Merge előtt:')
    print('Forbidden1:', forbidden_pos1)
    print('Forbidden2:', forbidden_pos2)
    merge_2pos(w, h, forbidden_pos1, forbidden_pos2)
    print('Merge után:')
    print('Forbidden1:', forbidden_pos1)
    print('Forbidden2:', forbidden_pos2)

    return 0
    print_board(board, 0, 0)

    print()
    pos_orig = pos_rec(board, k)

    pos1 = pos_orig['pos1']
    coord1 = [[2,3], [1, 1]]

    pos2 = pos_orig['pos2']
    coord2 = [[3,5], [1,1]]
    print('Pos1')
    draw_pos(board, pos1)
    print('Pos2')
    draw_pos(board, pos2)

    # I.
    pos1_all = pos_expand(w, h, pos1)
    pos2_all = pos_expand(w, h, pos2)
    # print(pos_rec(board, k))
    # print(pos1_all[1])
    # print(pos2_all[1])


    # II.
    pos2_all_inv = dict([(value, key) for key, value in pos2_all[1].items()])

    # III.
    for i in pos2_all_inv:
        if i == pos1:
            pos_mutual = pos2_all_inv[i]

    # IV.
    #learn_coord_maker(XMIN, YMIN, XMAX, YMAX, COORD, POS, INVERZ)
    coord_abs = learn_coord_maker(pos2_all[0][0], pos2_all[0][1], pos2_all[0][2], pos2_all[0][3], coord2[0], 'pos1', 1)

    # V.
    coord1_calc = learn_coord_maker(pos2_all[0][0], pos2_all[0][1], pos2_all[0][2], pos2_all[0][3], coord_abs, pos_mutual,0)
    print('Coord2 orig:\t', coord2[0])
    print('Coord_abs:  \t', coord_abs)
    print('Coord1 orig:\t', coord1[0])
    print('Coord1 calc:\t', coord1_calc)

    return 0
    print('\nPOS:')
    infile = open(r'Ocvist_pos.txt', 'r')
    i = 0
    for line in infile:
        if i % 2 == 0:
            pos = line
            pos = pos.replace("\n", "")
            if len(pos) == 5:
                print(i)
                print(pos)
        else:
            coord_list_tmp = []
            coord = line
            coord = coord.replace("\n", "")
        i += 1
    infile.close()

    return 0


    # TEST

    steps.append([7, 6])
    print_board(board, 0, 1)
    print(steps[-1])
    learn_debug(board, k, steps, forbidden_pos)
    for i in forbidden_pos:
        print(i)
        print(forbidden_pos[i])
        print()


    return 0

    pos = pos_rec(board, k)
    print_board(board, 0, 1)
    learn_debug(board, k, steps, forbidden_pos)
    print(forbidden_pos)
    return 0

    # print_board(board, 0, 1)
    # force_new(board, 'x', 'ENEMY', 1)
    # # force_pos_tmp = set()
    # # pos_tmp = open3(board, direction, 'x', 1)
    # # for j in pos_tmp:
    # #     force_pos_tmp = force_pos_tmp.union(j)
    # # print(force_pos_tmp)
    # print_board(board, 0, 1)
    # return 0

    # print_board(board, 0, 1)
    # # step(board, steps, k, 'o', forbidden_pos, 0)
    # # # force(board, 'o', 'OWN')
    # # print_board(board, 0, 1)
    # # force_new(board, 'x', 'OWN', 'STRONG')
    # # print('tirv2nd:', trivial2nd(board, 'x', 'OWN'))
    # print(open3(board, direction, 'x', 0))
    # print_board(board, 0, 1)
    # return 0

    SIGN = 'x'

    poss = ['m', 't', 'l', 'r', 'b', 'tr', 'tl', 'bl', 'br']
    align1 = ['h', 'v', 'd+', 'd-']
    align2 = ['h', 'v', 'd+', 'd-']
    alignh = ['h']
    backnforth = ['F']

    PATTS_TRIV2ND = [[0, 0, 1, 1, 1, 0, 0], [0, 1, 1, 0, 1, 0]]
    PATTS_MINI_FORCE = [[0, 0, 1, 1, 1, 0, 0], [0, 1, 1, 0, 1, 0], [0, 1, 0, 1, 1, 0], [0, 1, 1, 0, 0, 1],
                        [0, 1, 0, 1, 0, 1], [0, 1, 0, 0, 1, 1]]
    PATTS_MINI_FORCE2 = [[2, 0, 1, 1, 1, 0, 0], [0, 1, 1, 2, 1, 0], [0, 1, 2, 1, 1, 0], [0, 1, 1, 0, 2, 1, 0],
                         [2, 1, 0, 1, 0, 1, 2], [2, 1, 0, 0, 1, 1, 2]]

    for x in range(len(board[0])):
        for y in range(len(board)):
            board[y][x] = 1

    for pattern in PATTS_MINI_FORCE2:
        for ali in align1:
            put_patter(board, 'm', ali, pattern, 'F')
            mini_force(board, 'x', 'OWN')
            print_board(board, 0, 1)

            for x in range(len(board[0])):
                for y in range(len(board)):
                    board[y][x] = 1

    return 0

    PATTS3 = [[0, 0, 1, 1, 1, 2], [0, 1, 0, 1, 1, 2], [1, 0, 0, 1, 1, 2], [0, 1, 1, 0, 1, 2], [1, 0, 1, 0, 1, 2],
              [1, 1, 0, 0, 1, 2], [0, 1, 1, 1, 0, 2], [1, 0, 1, 1, 0, 2], [1, 1, 0, 1, 0, 2], [1, 1, 1, 0, 0, 2]]

    PATTS2 = [[0, 0, 0, 1, 1, 2], [0, 0, 1, 0, 1, 2], [0, 1, 0, 0, 1, 2], [1, 0, 0, 0, 1, 2], [0, 0, 1, 1, 0, 2],
              [0, 1, 0, 1, 0, 2], [1, 0, 0, 1, 0, 2], [0, 1, 1, 0, 0, 2], [1, 0, 1, 0, 0, 2], [1, 1, 0, 0, 0, 2]]

    PATTS1 = [[[1, 1, 0], [1, 1, 0], 4, 5], [[1, 1, 0], [1, 0, 1, 0], 4, 6], [[1, 1, 0], [1, 1, 0, 0], 4, 6],
              [[1, 1, 0], [2, 1, 1, 1, 0], 5, 4], [[1, 0, 1, 0], [1, 1, 0], 4, 6], [[1, 0, 1, 0], [1, 0, 1, 0], 4, 7],
              [[1, 0, 1, 0], [1, 1, 0, 0], 4, 7], [[1, 0, 1, 0], [2, 1, 1, 1, 0], 5, 5],
              [[1, 1, 0, 0], [1, 1, 0], 4, 6], [[1, 1, 0, 0], [1, 1, 0, 0], 4, 7], [[1, 1, 0, 0], [1, 0, 1, 0], 4, 7],
              [[1, 1, 0, 0], [2, 1, 1, 1, 0], 5, 5], [[2, 1, 1, 1, 0], [1, 1, 0], 5, 4],
              [[2, 1, 1, 1, 0], [1, 1, 0, 0], 5, 5],
              [[2, 1, 1, 1, 0], [1, 0, 1, 0], 5, 5], [[2, 1, 1, 1, 0], [2, 1, 1, 1, 0], 6, 3]]
    WHOSE = 2
    if WHOSE == 1:
        WHOSE = 'OWN'
    else:
        WHOSE = 'ENEMY'
    elem = 4
    ones = 3

    all_poss = 0
    test = []

    for i in range(len(board)):
        for j in range(len(board[0])):
            board[i][j] = 1

    sum = 0
    for pattern in PATTS1:
        elem = pattern[2]
        ones = pattern[3]
        for p in poss:
            if all_poss == 1 or p == 'm':
                for ali1 in align1:
                    for ali2 in align2:
                        for bf in backnforth:
                            if ali1 != ali2:
                                if bf == 'F':
                                    if ali1 == 'h':
                                        print('POSITION:', p)
                                    print('\nAlign: ', ali1)
                                if bf == 'F':
                                    print('forth')
                                else:
                                    print('back')
                                put_patter(board, p, ali1, pattern[0], 'B')
                                put_patter(board, p, ali2, pattern[1], 'B')
                                for i in range(len(board)):
                                    for j in range(len(board[0])):
                                        if board[i][j] == 'o' or board[i][j] == 'x':
                                            pass
                                        else:
                                            board[i][j] = 1
                                # test = open3(board, direction, SIGN, 1)
                                # test = open3_incompl(board, direction, SIGN, 1)
                                # test = half_closed4(board, direction, SIGN, 1)
                                # test = closed4_incompl(board, direction, SIGN, 0)
                                # test = double4_inline(board, 'x', 0)
                                # print('OPEN3:', test)

                                # if test != []:
                                #     for i in test[0]:
                                #         if board[i[1]][i[0]] != SIGN and board[i[1]][i[0]] != 0:
                                #             print('PROBLEM!\t', 'xy: (%d, %d)' % (i[0], i[1]), '\tval.:', board[i[1]][i[0]])
                                #     if len(test[0]) != 3:
                                #         print('PROBLEM! LEN\t', len(test[0]))

                                s = 0
                                prob = 0
                                for x in range(len(board[0])):
                                    for y in range(len(board)):
                                        if board[y][x] == 'x':
                                            s += 1
                                if s != elem:
                                    print('PROBLEM: ELEM SZÁM!', s)
                                    prob = 1

                                if prob == 0:
                                    force_new(board, 'x', WHOSE, 'STRONG')
                                    sum += 1

                                s = 0
                                for x in range(len(board[0])):
                                    for y in range(len(board)):
                                        if board[y][x] == 'x':
                                            s += 1
                                if s != elem:
                                    print('PROBLEM: ELEM SZÁM ELLENŐRZÉSNÉL!', s)

                                s = 0
                                for x in range(len(board[0])):
                                    for y in range(len(board)):
                                        if board[y][x] == 1:
                                            s += 1
                                if s != ones and s != 1:
                                    print('PROBLEM: EGYESEK SZÁMA!', s)

                                print_board(board, 0, 1)
                                for x in range(len(board[0])):
                                    for y in range(len(board)):
                                        board[y][x] = 1
                    print('\n\n')
    print('SUM', sum)
    if sum != 12:
        print('PROBLEM: SUM!', sum)

    return 0

    tmp = [1, 1, 1, 1, 100, 1, 1, 100, 100, 1, 1, 1]
    e = list(range(len(tmp)))
    print(len(tmp))
    for i in range(100000):
        x = choose_weighted(tmp)
        e[x] += 1
    print(e)

    return 0




main()
import random as r
import multiprocessing
import sys
import os
import time as t
import copy
from termcolor import colored


# PRINT PYTHON SIGN: print('\U0001F40D')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_board(board, LAST, SWITCH):
    # SWITCH 0: CSAK A JELEKET ÍRJA KI
    #        1: MEZŐK TARTALMAIT IS KIÍRJA

    w = len(board[0])
    h = len(board)
    ### FEJLÉC
    print('   ', end='')
    for x in range(w):
        print(colored(str(x + 1).ljust(3, ' '), 'magenta'), end='')
    print('')
    for y in range(h):
        ### OSZLOP SZÁMOZÁS
        print(colored(str(y + 1).ljust(3, ' '), 'magenta'), end='')
        ### TARTALOM
        for x in range(w):
            PRINT = 0
            if SWITCH == 0:
                if LAST != 0:
                    for i in LAST:
                        if (x, y) == i or [x, y] == i:
                            print(colored(board[y][x], 'red', attrs=['bold']), end='  ')
                            PRINT = 1
                    if PRINT == 0:
                        if board[y][x] == 'o' or board[y][x] == 'x':
                            print(colored(board[y][x], 'cyan', attrs=['bold']), end='  ')
                        else:
                            print('.', end='  ')
                else:
                    if board[y][x] == 'o' or board[y][x] == 'x':
                        print(colored(board[y][x], 'cyan', attrs=['bold']), end='  ')
                    else:
                        print('.', end='  ')
            elif SWITCH == 1:
                if LAST != 0:
                    for i in LAST:
                        if (x, y) == i or [x, y] == i:
                            print(colored(board[y][x], 'red', attrs=['bold']), end='  ')
                            PRINT = 1
                    if PRINT == 0:
                        if board[y][x] == 'o' or board[y][x] == 'x':
                            print(colored(board[y][x], 'cyan', attrs=['bold']), end='  ')
                        elif board[y][x] == 1:
                            print('1', end='  ')
                        elif board[y][x] == 0:
                            print('.', end='  ')
                else:
                    if board[y][x] == 'o' or board[y][x] == 'x':
                        print(colored(board[y][x], 'cyan', attrs=['bold']), end='  ')
                    elif board[y][x] == 1:
                        print('1', end='  ')
                    elif board[y][x] == 0:
                        print('.', end='  ')
        ### OSZLOP SZÁMOZÁS
        print(colored(y + 1, 'magenta'))
    ### ALSÓ SZÁMOZOTT SOR
    print('   ', end='')
    for x in range(w):
        print(colored(str(x + 1).ljust(3, ' '), 'magenta'), end='')
    print('\n')

def print_possible_steps(board):
    possible_steps = 0
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 1:
                possible_steps += 1
    print('Lehetséges lépések száma:', possible_steps)

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

def take_fix(board, pos, SIGN):
    # FIX POZÍCIÓBA RAK EGY JELET
    board[pos[1]][pos[0]] = SIGN


def choose_weighted(LIST):
    q = 100000
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
    # MINDEN MEZŐT, AHOL NINCS JEL KINULLÁZ
    w = len(board[0])
    h = len(board)
    for y in range(h):
        for x in range(w):
            if board[y][x] != 'x' and board[y][x] != 'o':
                board[y][x] = 0


def end(board, SIGN, SWITCH):
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
    # VALAKI 1 LÉPÉSRE VAN-E A GYŐZELEMTŐL
    # A KÉRDÉSES HELYEKET KITÖLTI 1-ESSEL
    # HA NEM TÖRTÉNT ÍRÁS, AKKOR 0 AZ ÉRTÉKE

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
    # HA NEM TÖRTÉNT ÍRÁS, AKKOR 0 AZ ÉRTÉKE

    all_sign = {'o', 'x'}
    w = len(board[0])
    h = len(board)
    triv2nd_pos = set()
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
                                    half_closed4_pos[-1].add((x - 1, y))
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
                                    half_closed4_pos[-1].add((x, y - 1))
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
                                    half_closed4_pos[-1].add((x - 1, y - 1))
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
                                    half_closed4_pos[-1].add((x + 1, y - 1))
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

def mini_force(board, SIGN):
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


def weighting3(board, SIGN, WRITTEN, DEFENSIVE):
    w = len(board[0])
    h = len(board)
    all_sign = {'x', 'o'}
    if DEFENSIVE == 1:
        WEIGHT = 5
    else:
        WEIGHT = 7

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
                            board[i[1]][i[0]] *= WEIGHT
                        for i in coords:
                            WRITTEN.append(i)
                            WRITTEN[-1].append('h')
                elif s == 3 and k == 4:
                    for i in void:
                        board[i[1]][i[0]] *= WEIGHT
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
                            board[i[1]][i[0]] *= WEIGHT
                        for i in coords:
                            WRITTEN.append(i)
                            WRITTEN[-1].append('v')
                elif s == 3 and k == 4:
                    for i in void:
                        board[i[1]][i[0]] *= WEIGHT
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
                            board[i[1]][i[0]] *= WEIGHT
                        for i in coords:
                            WRITTEN.append(i)
                            WRITTEN[-1].append('d+')
                elif s == 3 and k == 4:
                    for i in void:
                        board[i[1]][i[0]] *= WEIGHT
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
                            board[i[1]][i[0]] *= WEIGHT
                        for i in coords:
                            WRITTEN.append(i)
                            WRITTEN[-1].append('d-')
                elif s == 3 and k == 4:
                    for i in void:
                        board[i[1]][i[0]] *= WEIGHT
                    for i in coords:
                        WRITTEN.append(i)
                        WRITTEN[-1].append('d-')

def weighting2(board, SIGN, WRITTEN, DEFENSIVE):
    w = len(board[0])
    h = len(board)
    all_sign = {'x', 'o'}
    if DEFENSIVE == 1:
        WEIGHT1 = 3
        WEIGHT2 = 3
        WEIGHT3 = 1
    else:
        WEIGHT1 = 5
        WEIGHT2 = 5
        WEIGHT3 = 2

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
                            board[i[1]][i[0]] *= WEIGHT1
                        NUM = 0
                        for i in void_m:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] *= WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] *= WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] *= WEIGHT3
                        NUM = 0
                        for i in void_p:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] *= WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] *= WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] *= WEIGHT3

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
                            board[i[1]][i[0]] *= WEIGHT1
                        NUM = 0
                        for i in void_m:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] *= WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] *= WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] *= WEIGHT3
                        NUM = 0
                        for i in void_p:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] *= WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] *= WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] *= WEIGHT3

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
                            board[i[1]][i[0]] *= WEIGHT1
                        NUM = 0
                        for i in void_m:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] *= WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] *= WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] *= WEIGHT3
                        NUM = 0
                        for i in void_p:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] *= WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] *= WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] *= WEIGHT3

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
                            board[i[1]][i[0]] *= WEIGHT1
                        NUM = 0
                        for i in void_m:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] *= WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] *= WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] *= WEIGHT3
                        NUM = 0
                        for i in void_p:
                            NUM += 1
                            if NUM == 1:
                                board[i[1]][i[0]] *= WEIGHT1
                            if NUM == 2:
                                board[i[1]][i[0]] *= WEIGHT2
                            if NUM == 3 and SKIPP != 1:
                                board[i[1]][i[0]] *= WEIGHT3

def weighting(board, SIGN):
    pass
    # if SIGN == 'x':
    #     ENEMY = 'o'
    # else:
    #     ENEMY = 'x'

    # WRITTEN = []
    # weighting3(board, SIGN, WRITTEN, 0)
    # weighting2(board, SIGN, WRITTEN, 0)

    # weighting3(board, ENEMY, WRITTEN, 1)
    # weighting2(board, ENEMY, WRITTEN, 1)


def prog_step(board, steps, k, SIGN, forbidden_pos, RAWDATA, SWITCH):
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
        learnt_zeroing(board, k, forbidden_pos, RAWDATA)
        # weighting(board, SIGN)
        steps.append(take_rand(board, SIGN))

    elif trivial(board, ENEMY) == 1:
        if SWITCH == 1:
            input()
            clear_screen()
            print_board(board, steps[-1], 1)
            print('Következő:', SIGN)
            print_possible_steps(board)
            input()
        learnt_zeroing(board, k, forbidden_pos, RAWDATA)
        # weighting(board, SIGN)
        steps.append(take_rand(board, SIGN))

    elif trivial2nd(board, SIGN, 'OWN') == 1:
        if SWITCH == 1:
            input()
            clear_screen()
            print_board(board, steps[-1], 1)
            print('Következő:', SIGN)
            print_possible_steps(board)
            input()
        learnt_zeroing(board, k, forbidden_pos, RAWDATA)
        # weighting(board, SIGN)
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
            learnt_zeroing(board, k, forbidden_pos, RAWDATA)
            # weighting(board, SIGN)
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
                learnt_zeroing(board, k, forbidden_pos, RAWDATA)
                # weighting(board, SIGN)
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
                learnt_zeroing(board, k, forbidden_pos, RAWDATA)
                # weighting(board, SIGN)
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
                learnt_zeroing(board, k, forbidden_pos, RAWDATA)
                # weighting(board, SIGN)
                steps.append(take_rand(board, SIGN))
            elif force(board, ENEMY, 'ENEMY') == 1:
                if SWITCH == 1:
                    input()
                    clear_screen()
                    print_board(board, steps[-1], 1)
                    print('Következő:', SIGN)
                    print_possible_steps(board)
                    input()
                learnt_zeroing(board, k, forbidden_pos, RAWDATA)
                # weighting(board, SIGN)
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
                learnt_zeroing(board, k, forbidden_pos, RAWDATA)
                # weighting(board, SIGN)
                steps.append(take_rand(board, SIGN))
    if steps[-1] == 0:
        return 0
    else:
        return 1

def human_step(board, steps, k, PLAY, SIGN):
    w = len(board[0])
    h = len(board)
    clear_screen()
    print_board(board, [steps[-1]], 0)
    print()

    # KOORDINÁTÁK BEKÉRÉSE
    a = 0
    while a == 0:
        x = input('x coord: ')
        try:
            x = int(x) - 1
        except:
            if x == '-print_all 1':
                clear_screen()
                print_board(board, [steps[-1]], 1)
            elif x == '-back':
                steps.pop(-1)
                steps.pop(-1)
                k -= 2
            print('Nem érvényes szám! \nÚjra:')
            continue
        y = input('y coord: ')
        try:
            y = int(y) - 1
        except:
            if y == '-print_all 1':
                clear_screen()
                print_board(board, [steps[-1]], 1)
            elif y == '-back':
                steps.pop(-1)
                steps.pop(-1)
                k -= 2
            print('Nem érvényes szám! \nÚjra:')
            continue
            y = int(y) - 1
            if x >= 0 and x <= w - 1 and y >= 0 and y <= h - 1:
                if board[y][x] != 'x' and board[y][x] != 'o':
                    a = 1
                    steps.append((x, y))
                    take_fix(board, [x, y], SIGN)
                    k += 1
                    if end(board, SIGN, 0) == SIGN:
                        PLAY = 0
                else:
                    print('\nOtt már van jel! \nÚjra:')
            else:
                print('\nNem érvényes pozíció! \nÚjra:')


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
        # record = {'pos1': '...', 'pos2': '...', ..., 'pos8': '...'}
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

def str2list(str_list, list_fin):
    i = 3
    while i < len(str_list):
        x = ''
        y = ''
        val = ''
        k = ''
        ### X BEOLVASÁSA
        while str_list[i] != ',':
            x += str_list[i]
            i += 1
        i += 2

        ### Y BEOLVASÁSA
        while str_list[i] != ']':
            y += str_list[i]
            i += 1
        i += 4

        ### ÉRTÉK (VAL) BEOLVASÁSA
        while str_list[i] != ',':
            val += str_list[i]
            i += 1
        if val != '\'z\'':
            val = int(val)
        else:
            val = 'z'
        i += 2

        ### PARTIK SZÁMA
        while str_list[i] != ']':
            k += str_list[i]
            i += 1
        i += 6

        list_fin.append([[int(x), int(y)], [val, int(k)]])


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
        elif POS == 'pos1x1':
            tmp[0] = COORD[0] - XMIN
            tmp[1] = COORD[1] - YMAX

            # TENGELYRE SZIMMETRIA MIATT
        elif POS == 'pos1x2':
            tmp[0] = COORD[0] - XMIN
            tmp[1] = YMAX - COORD[1]

        elif POS == 'pos2x1':
            tmp[0] = XMAX - COORD[0]
            tmp[1] = COORD[1] - YMAX

            # TENGELYRE SZIMMETRIA MIATT
        elif POS == 'pos2x1':
            tmp[0] = XMAX - COORD[0]
            tmp[1] = YMAX - COORD[1]

    if INVERZ == 1:
        ### VAN RENDES TÉGLALAP
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

        ### X-TENGELLYEL PÁRHUZAMOS
        elif POS == 'pos1x1':
            tmp[0] = COORD[0] + XMIN
            tmp[1] = COORD[1] + YMAX

            # TENGELYRE SZIMMETRIA MIATT
        elif POS == 'pos1x2':
            tmp[0] = COORD[0] + XMIN
            tmp[1] = YMAX - COORD[1]

        elif POS == 'pos2x1':
            tmp[0] = XMAX - COORD[0]
            tmp[1] = COORD[1] + YMAX

            # TENGELYRE SZIMMETRIA MIATT
        elif POS == 'pos2x1':
            tmp[0] = XMAX - COORD[0]
            tmp[1] = YMAX - COORD[1]

    return tmp

def learn(board, STEPS, LAST_STEPS, FORBIDDEN_POS):
    #print('\n\nLEARN!!!')
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
    fin_coord = [[0, 0], [0, 1]]  #

    ### ### AZ UTOLSÓ LÉPÉSEKET VISSZAVONJUK ÉS AZT AZ ÁLLÁST VIZSGÁLJUK
    if LAST_STEPS[-1] != 'break':
        if LAST_STEPS[-1] == 0:
            LAST_STEPS.pop(-1)

        #print_board(board, LAST_STEPS[-1], 1)
        # UTOLSÓ (NYERŐ) LÉPÉS VISSZAVONÁSA
        last = LAST_STEPS[-1]
        take_fix(board, last, 1)
        STEPS -= 1

        for rev in range(2, len(LAST_STEPS)):
            written = []  # TALÁLATOT MENTJÜK BELE
            OK = 0  # INDIKÁTORA, HOGY TALÁLTUNK-E PASSZOLÓ ÁLLÁST
            k = 0  # JELEKET SZÁMLÁLJA

            #print_board(board, LAST_STEPS[-rev], 1)
            # LÉPÉSEK VISSZAVONÁSA 1-ESÉVEL
            last = LAST_STEPS[-rev]
            take_fix(board, last, 1)
            STEPS -= 1

            # POZÍCIÓK MEGHATÁROZÁSA
            pos_fin = pos_rec(board, STEPS)
            if pos_fin['pos1'] == '0000x' or pos_fin['pos1'] == '0100x' or pos_fin['pos1'] == '0001x':
                print('ITT A HIBA')
                print('LÉPÉSEK:', STEPS)
                print_board(board, 0, 0)

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
                for s in simmetry:
                    if s == set_tmp:
                        CONTAIN = 1
                if CONTAIN == 0:
                    simmetry.append(set_tmp)
                CONTAIN = 0

            ### A KIALAKULT POZÍCIÓ KÖRÉ ÍRHATÓ TÉGLALAP KÉT ÁTLÓS SARKÁNAK KOORDINÁTÁINAK MEGHATÁROZÁSA
            rectangle = rectangle_corner(board, STEPS)
            xmin = rectangle[0]
            ymin = rectangle[1]
            xmax = rectangle[2]
            ymax = rectangle[3]

            ### BEÍRANDÓ ÉRTÉK MEGHATÁROZÁSA (fin_coord[1][0])
            if rev == 2:
                VALUE = 'z'
            else:
                if rev % 2 == 1:
                    VALUE = 1
                else:
                    VALUE = 0

            ### CSAK 1 JEL VAN, VAGYIS KEZDŐÁLLÁSNÁL VAGYUNK
            if STEPS == 1:
                for i in pos_fin:
                    if pos_fin[i] in FORBIDDEN_POS:
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
                        fin_coord[1][0] = VALUE

                        SEARCH = 0
                        for k in FORBIDDEN_POS[pos_fin[i]]:
                            if k[0] == fin_coord[0]:
                                if fin_coord[1][0] == 'z':
                                    k[1][0] = 'z'
                                    k[1][1] += 1
                                else:
                                    k[1][0] += fin_coord[1][0]
                                    k[1][1] += 1
                                SEARCH = 1
                                break
                        if SEARCH == 0:
                            FORBIDDEN_POS[pos_fin[i]].append([[0, 0], [0, 0]])
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
                    fin_coord[1][0] = VALUE
                    FORBIDDEN_POS[pos_fin['pos1']] = [[[0, 0], [0, 0]]]
                    FORBIDDEN_POS[pos_fin['pos1']][-1] = copy.deepcopy(fin_coord)

            ### X TENGELLYEL PÁRHUZAMOSAN VANNAK A JELEK
            elif ymin == ymax:
                fin_coord = [[0, 0], [0, 1, 'pos1']]
                fin_coord_tmp = []  # ÖSSZES LÉPÉSNEK MEGFELELŐ JÓ KOORDINÁTÁT BELEÍRJUK, MAJD VÁLASZTUNK EGYET
                for i in pos_fin:
                    if pos_fin[i] in FORBIDDEN_POS:
                        if i == 'pos1':
                            tmp[0] = last[0] - xmin
                            tmp[1] = last[1] - ymax
                            fin_coord[0] = copy.deepcopy(tmp)
                            fin_coord[1][0] = VALUE
                            fin_coord[1][2] = 'pos1'
                            fin_coord_tmp.append([[0, 0], [0, 1, 'pos1']])
                            fin_coord_tmp[-1] = copy.deepcopy(fin_coord)

                            # TENGELYRE SZIMMETRIA MIATT
                            tmp[1] = ymax - last[1]
                            fin_coord[0] = copy.deepcopy(tmp)
                            fin_coord_tmp.append([[0, 0], [0, 1, 'pos1']])
                            fin_coord_tmp[-1] = copy.deepcopy(fin_coord)

                        elif i == 'pos2':
                            tmp[0] = xmax - last[0]
                            tmp[1] = last[1] - ymax
                            fin_coord[0] = copy.deepcopy(tmp)
                            fin_coord[1][0] = VALUE
                            fin_coord[1][2] = 'pos2'
                            fin_coord_tmp.append([[0, 0], [0, 1, 'pos1']])
                            fin_coord_tmp[-1] = copy.deepcopy(fin_coord)

                            # TENGELYRE SZIMMETRIA MIATT
                            tmp[1] = ymax - last[1]
                            fin_coord[0] = copy.deepcopy(tmp)
                            fin_coord_tmp.append([[0, 0], [0, 1, 'pos1']])
                            fin_coord_tmp[-1] = copy.deepcopy(fin_coord)
                        OK = 1

                if OK == 0:
                    fin_coord = [[0, 0], [0, 1]]
                    tmp[0] = last[0] - xmin
                    tmp[1] = last[1] - ymax
                    fin_coord[0] = copy.deepcopy(tmp)
                    fin_coord[1][0] = VALUE
                    FORBIDDEN_POS[pos_fin['pos1']] = [[[0, 0], [0, 0]]]
                    FORBIDDEN_POS[pos_fin['pos1']][-1] = copy.deepcopy(fin_coord)
                else:
                    SEARCH = 0
                    for f in fin_coord_tmp:
                        for k in FORBIDDEN_POS[pos_fin[f[1][2]]]:
                            if k[0] == f[0]:
                                if f[1][0] == 'z':
                                    k[1][0] = 'z'
                                    k[1][1] += 1
                                else:
                                    try:
                                        k[1][0] += f[1][0]
                                    except:
                                        print('HIBA X-TENGELYES!!!')
                                        print('POS:', pos_fin[f[1][2]])
                                        print('K[1][0]: {}\tf[1][0]: {}'.format(k[1][0], f[1][0]))
                                    k[1][0] += f[1][0]
                                    k[1][1] += 1
                                SEARCH = 1
                                break
                        if SEARCH == 1:
                            break
                    if SEARCH == 0:
                        fin_coord = fin_coord_tmp[0]
                        pos_tmp = fin_coord[1][2]
                        fin_coord[1].pop(2)
                        FORBIDDEN_POS[pos_fin[pos_tmp]].append([[[0, 0], [0, 0]]])
                        FORBIDDEN_POS[pos_fin[pos_tmp]][-1] = copy.deepcopy(fin_coord)

            ### Y TENGELLYEL PÁRHUZAMOSAN VANNAK A JELEK
            elif xmin == xmax:
                fin_coord = [[0, 0], [0, 1, 'pos1']]
                fin_coord_tmp = []  # ÖSSZES LÉPÉSNEK MEGFELELŐ JÓ KOORDINÁTÁT BELEÍRJUK, MAJD VÁLASZTUNK EGYET
                for i in pos_fin:
                    if pos_fin[i] in FORBIDDEN_POS:
                        if i == 'pos1':
                            tmp[0] = last[1] - ymin
                            tmp[1] = last[0] - xmin
                            fin_coord[0] = copy.deepcopy(tmp)
                            fin_coord[1][0] = VALUE
                            fin_coord[1][2] = 'pos1'
                            fin_coord_tmp.append([[0, 0], [0, 1, 'pos1']])
                            fin_coord_tmp[-1] = copy.deepcopy(fin_coord)

                            # TENGELYRE SZIMMETRIA MIATT
                            tmp[1] = xmin - last[0]
                            fin_coord[0] = copy.deepcopy(tmp)
                            fin_coord_tmp.append([[0, 0], [0, 1, 'pos1']])
                            fin_coord_tmp[-1] = copy.deepcopy(fin_coord)

                        elif i == 'pos2':
                            tmp[0] = ymax - last[1]
                            tmp[1] = last[0] - xmax
                            fin_coord[0] = copy.deepcopy(tmp)
                            fin_coord[1][0] = VALUE
                            fin_coord[1][2] = 'pos2'
                            fin_coord_tmp.append([[0, 0], [0, 1, 'pos1']])
                            fin_coord_tmp[-1] = copy.deepcopy(fin_coord)

                            # TENGELYRE SZIMMETRIA MIATT
                            tmp[1] = xmax - last[0]
                            fin_coord[0] = copy.deepcopy(tmp)
                            fin_coord_tmp.append([[0, 0], [0, 1, 'pos1']])
                            fin_coord_tmp[-1] = copy.deepcopy(fin_coord)
                        OK = 1

                if OK == 0:
                    fin_coord = [[0, 0], [0, 1]]
                    tmp[0] = last[1] - ymin
                    tmp[1] = last[0] - xmin
                    fin_coord[0] = copy.deepcopy(tmp)
                    fin_coord[1][0] = VALUE
                    FORBIDDEN_POS[pos_fin['pos1']] = [[[0, 0], [0, 0]]]
                    FORBIDDEN_POS[pos_fin['pos1']][-1] = copy.deepcopy(fin_coord)
                else:
                    SEARCH = 0
                    for f in fin_coord_tmp:
                        for k in FORBIDDEN_POS[pos_fin[f[1][2]]]:
                            if k[0] == f[0]:
                                if f[1][0] == 'z':
                                    k[1][0] = 'z'
                                    k[1][1] += 1
                                else:
                                    try:
                                        k[1][0] += f[1][0]
                                    except:
                                        print('HIBA Y-TENGELYES!!!')
                                        print('POS:', pos_fin[f[1][2]])
                                        print('K[1][0]: {}\tf[1][0]: {}'.format(k[1][0], f[1][0]))
                                    k[1][0] += f[1][0]
                                    k[1][1] += 1
                                SEARCH = 1
                                break
                        if SEARCH == 1:
                            break
                    if SEARCH == 0:
                        fin_coord = fin_coord_tmp[0]
                        pos_tmp = fin_coord[1][2]
                        fin_coord[1].pop(2)
                        FORBIDDEN_POS[pos_fin[pos_tmp]].append([[[0, 0], [0, 0]]])
                        FORBIDDEN_POS[pos_fin[pos_tmp]][-1] = copy.deepcopy(fin_coord)

            ### VAN RENDES TÉGLALAP, AMI A KIALAKULT HELYZET KÖRÉ ÍRHATÓ
            else:
                fin_coord = [[0, 0], [0, 1, 'pos1']]
                fin_coord_tmp = []
                if simmetry == []:
                    simmetry = [{'pos1'}, {'pos2'}, {'pos3'}, {'pos4'}, {'pos5'}, {'pos6'}, {'pos7'}, {'pos8'}]
                BREAK = 0
                for i in pos_fin:
                    if pos_fin[i] in FORBIDDEN_POS:
                        for sim in simmetry:
                            if i in sim:
                                for p in sim:
                                    fin_coord[0] = learn_coord_maker(rectangle, last, p, 0)
                                    fin_coord[1][0] = VALUE
                                    fin_coord[1][2] = p
                                    fin_coord_tmp.append([[0, 0], [0, 1, 'pos1']])
                                    fin_coord_tmp[-1] = copy.deepcopy(fin_coord)
                                SEARCH = 0
                                for f in fin_coord_tmp:
                                    for k in FORBIDDEN_POS[pos_fin[f[1][2]]]:
                                        if k[0] == f[0]:
                                            if f[1][0] == 'z':
                                                k[1][0] = 'z'
                                                k[1][1] += 1
                                            else:
                                                try:
                                                    k[1][0] += f[1][0]
                                                except:
                                                    print('HIBA TÉGLALAPOS!!!')
                                                    print('POS:', pos_fin[f[1][2]])
                                                    print('K[1][0]: {}\tf[1][0]: {}'.format(k[1][0], f[1][0]))
                                                k[1][0] += f[1][0]
                                                k[1][1] += 1
                                            BREAK = 1
                                            SEARCH = 1
                                            break
                                    if BREAK == 1:
                                        break
                                if SEARCH == 0:
                                    FORBIDDEN_POS[pos_fin[fin_coord_tmp[0][1][2]]].append([[0, 0], [0, 0]])
                                    fin_coord = fin_coord_tmp[0]
                                    fin_coord[1].pop(2)
                                    FORBIDDEN_POS[pos_fin[i]][-1] = copy.deepcopy(fin_coord)
                                OK = 1
                                break
                        break
                if OK == 0:
                    fin_coord[0] = learn_coord_maker(rectangle, last, 'pos1', 0)
                    fin_coord[1][0] = VALUE
                    fin_coord[1].pop(2)
                    FORBIDDEN_POS[pos_fin['pos1']] = [[[0, 0], [0, 0]]]
                    FORBIDDEN_POS[pos_fin['pos1']][-1] = copy.deepcopy(fin_coord)

def learnt_zeroing(board, STEPS, FORBIDDEN_POS, RAWDATA):
    # STEPS: LÉPÉSEK SZÁMA
    # FORBIDDEN_POS: TILTOTT POZÍCIÓK, AMIKET KI KELL NULLÁZNI

    # POZITÍV EXPONENCIÁIS PARAMÉTEREI      // f(x) = AP - BP * CP^(-x) //
    AP = 30  # LIMES
    BP = AP - 1
    CP = 1.02  # EXP. ALAPJA: GÖRBE ALAKJA

    # NEGATÍV EXPONENCIÁLIS PARAMÉTEREI     // f(x) = 0.9999 * AM^(-BM * x) + 0.0001//
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

    ### SZIMMETRIA VIZSGÁLAT
    # ÖSSZES SZIMMETRIA PÁR LISTÁBAN ÉS HALMAZOKBAN
    simmetry_tmp = []
    for i in act_pos:
        for j in act_pos:
            if i != j and act_pos[i] == act_pos[j]:
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
        for s in simmetry:
            if s == set_tmp:
                CONTAIN = 1
        if CONTAIN == 0:
            simmetry.append(set_tmp)
        CONTAIN = 0

    ### ### A KIALAKULT POZÍCIÓ KÖRÉ ÍRHATÓ TÉGLALAP KÉT ÁTLÓS SARKÁNAK KOORDINÁTÁINAK MEGHATÁROZÁSA
    rectangle = rectangle_corner(board, STEPS)
    xmin = rectangle[0]
    ymin = rectangle[1]
    xmax = rectangle[2]
    ymax = rectangle[3]

    ### CSAK 1 JEL VAN, VAGYIS KEZDŐÁLLÁSNÁL VAGYUNK (XMIN = YMIN = XMAX = YMAX)
    if STEPS == 1:
        for i in act_pos:
            if act_pos[i] in FORBIDDEN_POS:
                for j in FORBIDDEN_POS[act_pos[i]]:
                    # ELŐRE MEGHATÁROZZUK A BEÍRANDÓ ÉRTÉKEKET
                    if j[1][0] == 'z':
                        VALUE = 0
                    else:
                        if RAWDATA == 1:
                            VALUE = 1
                        else:
                            if j[1][0] > 0:
                                VALUE = AP - BP * CP ** (-j[1][0])
                            else:
                                VALUE = 0.9999 * AM ** (BM * j[1][0]) + 0.0001

                    ### ELSŐ ESET: KEZDŐ JELHEZ KÉPEST SAROK MEZŐK VIZSG.
                    if j[0][1] == 1:
                        # SZIMMETRIA MIATT
                        for k in (-1, 1):
                            for l in (-1, 1):
                                tmp[0] = xmax + k
                                tmp[1] = ymax + l
                                if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                                    board[tmp[1]][tmp[0]] = VALUE

                    ### MÁSODIK ESET: KEZDŐ JELHEZ KÉPEST KÖZVETLEN SZOMSZÉDOS MEZŐK VIZSG.
                    if j[0][1] == 0:
                        # SZIMMETRIA MIATT
                        for k in (-1, 1):
                            tmp[0] = xmax + k
                            tmp[1] = ymax
                            if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                                board[tmp[1]][tmp[0]] = VALUE
                            tmp[0] = xmax
                            tmp[1] = ymax + k
                            if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                                board[tmp[1]][tmp[0]] = VALUE

    ### CSAK AZ X-TENGELLYEL PÁRHUZAMOSAN VANNAK A JELEK
    elif ymin == ymax:
        for i in act_pos:
            if act_pos[i] in FORBIDDEN_POS:
                for j in FORBIDDEN_POS[act_pos[i]]:
                    # ELŐRE MEGHATÁROZZUK A BEÍRANDÓ ÉRTÉKEKET
                    if j[1][0] == 'z':
                        VALUE = 0
                    else:
                        if RAWDATA == 1:
                            VALUE = 1
                        else:
                            if j[1][0] > 0:
                                VALUE = AP - BP * CP ** (-j[1][0])
                            else:
                                VALUE = 0.9999 * AM ** (BM * j[1][0]) + 0.0001

                    if i == 'pos1':
                        tmp[0] = xmin + j[0][0]
                        tmp[1] = ymax + j[0][1]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            board[tmp[1]][tmp[0]] = VALUE

                        # TENGELYRE SZIMMETRIA MIATT
                        tmp[1] = ymax - j[0][1]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            board[tmp[1]][tmp[0]] = VALUE

                    elif i == 'pos2':
                        tmp[0] = xmax - j[0][0]
                        tmp[1] = ymax + j[0][1]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            board[tmp[1]][tmp[0]] = VALUE

                        # TENGELYRE SZIMMETRIA MIATT
                        tmp[1] = ymax - j[0][1]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            board[tmp[1]][tmp[0]] = VALUE

    ### CSAK AZ Y-TENGELLYEL PÁRHUZAMOSAN VANNAK A JELEK
    elif xmin == xmax:
        for i in act_pos:
            if act_pos[i] in FORBIDDEN_POS:
                for j in FORBIDDEN_POS[act_pos[i]]:
                    # ELŐRE MEGHATÁROZZUK A BEÍRANDÓ ÉRTÉKEKET
                    if j[1][0] == 'z':
                        VALUE = 0
                    else:
                        if RAWDATA == 1:
                            VALUE = 1
                        else:
                            if j[1][0] > 0:
                                VALUE = AP - BP * CP ** (-j[1][0])
                            else:
                                VALUE = 0.9999 * AM ** (BM * j[1][0]) + 0.0001

                    if i == 'pos1':
                        tmp[0] = xmax + j[0][1]
                        tmp[1] = ymin + j[0][0]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            board[tmp[1]][tmp[0]] = VALUE

                        # TENGELYRE SZIMMETRIA MIATT
                        tmp[0] = xmax - j[0][1]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            board[tmp[1]][tmp[0]] = VALUE

                    elif i == 'pos2':
                        tmp[0] = xmax + j[0][1]
                        tmp[1] = ymax - j[0][0]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            board[tmp[1]][tmp[0]] = VALUE

                        # TENGELYRE SZIMMETRIA MIATT
                        tmp[0] = xmax - j[0][1]
                        if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                            board[tmp[1]][tmp[0]] = VALUE

    ### VAN RENDES TÉGLALAP, AMI A KIALAKULT HELYZET KÖRÉ ÍRHATÓ
    else:
        if simmetry == []:
            simmetry = [{'pos1'}, {'pos2'}, {'pos3'}, {'pos4'}, {'pos5'}, {'pos6'}, {'pos7'}, {'pos8'}]
        for i in act_pos:
            if act_pos[i] in FORBIDDEN_POS:
                for sim in simmetry:
                    if i in sim:
                        for p in sim:
                            for j in FORBIDDEN_POS[act_pos[p]]:
                                # MEGHATÁROZZUK A BEÍRANDÓ ÉRTÉKEKET
                                if j[1][0] == 'z':
                                    VALUE = 0
                                else:
                                    if RAWDATA == 1:
                                        VALUE = 1
                                    else:
                                        if j[1][0] > 0:
                                            VALUE = AP - BP * CP ** (-j[1][0])
                                        else:
                                            VALUE = 0.9999 * AM ** (BM * j[1][0]) + 0.0001

                                tmp = learn_coord_maker(rectangle, j[0], p, 1)
                                if tmp[0] >= 0 and tmp[0] <= w - 1 and tmp[1] >= 0 and tmp[1] <= h - 1:
                                    board[tmp[1]][tmp[0]] = VALUE
                        break
            break

def cleardat(FORBIDDEN_POS):
    forbidden_pos_tmp = {}
    for i in FORBIDDEN_POS:
        if len(FORBIDDEN_POS[i]) > 1 or FORBIDDEN_POS[i][0][1][0] == 'z':
            forbidden_pos_tmp[i] = FORBIDDEN_POS[i]
    return forbidden_pos_tmp

def cleardat_file(INFILE, OUTFILE):
    ### ELLENŐRZÉS, HOGY ".txt" KITERJESZTÉSŰEK-E A MEGADOTT FILENEVEK
    iftxtin_tmp = ''
    iftxtout_tmp = ''
    for i in (-4, -3, -2, -1):
        iftxtin_tmp += INFILE[i]
        iftxtout_tmp += OUTFILE[i]
    # HA NEM, AKKOR KIEGÉSZÍTI
    if iftxtin_tmp != '.txt':
        INFILE += '.txt'
    if iftxtout_tmp != '.txt':
        OUTFILE += '.txt'

    infile = open(INFILE, 'r')
    outfile = open(OUTFILE, 'w')

    i = 0
    for line in infile:
        if i % 2 == 0:
            pos = line
        else:
            coord_list_tmp = []
            coord = line
            coord = coord.replace("\n", "")
            str2list(coord, coord_list_tmp)
            if len(coord_list_tmp) > 1 or coord_list_tmp[0][1][0] == 'z':
                outfile.write(str(pos))
                outfile.write(str(coord_list_tmp))
                outfile.write('\n')
        i += 1

    infile.close()
    outfile.close()

def conclusion(FORBIDDEN_POS):
    for i in FORBIDDEN_POS:
        if len(FORBIDDEN_POS[i]) > 2:
            s = 0
            percent_list = []
            mean_percent = 0

            maxv_percent = 0
            minv_percent = 1
            index = 0
            for j in FORBIDDEN_POS[i]:
                if j[1][0] != 'z' and j[1][1] >= 40:
                    s += 1
                    percent_list.append([j[1][0] / j[1][1], index])
                    mean_percent += percent_list[-1][0]
                    if percent_list[-1][0] > maxv_percent:
                        maxv_percent = percent_list[-1][0]
                    if percent_list[-1][0] < minv_percent:
                        minv_percent = percent_list[-1][0]
                index += 1
            if s > 2:
                mean_percent /= s
                ### VÁLTOZÁS FELTÉTELE
                if maxv_percent - minv_percent > 0.1:
                    for j in percent_list:
                        ### NULLÁZÁS FELTÉTELE
                        if j[0] < mean_percent:
                            FORBIDDEN_POS[i][j[1]][1][0] = 'z'

            elif s == 2:
                mean_percent /= s
                ### VÁLTOZÁS FELTÉTELE
                if maxv_percent - minv_percent > 0.3:
                    for j in percent_list:
                        ### NULLÁZÁS FELTÉTELE
                        if j[0] < mean_percent:
                            FORBIDDEN_POS[i][j[1]][1][0] = 'z'

        elif len(FORBIDDEN_POS[i]) == 2:
            if FORBIDDEN_POS[i][0][1][0] != 'z' and FORBIDDEN_POS[i][1][1][0] != 'z' and FORBIDDEN_POS[i][0][1][1] >= 30 and FORBIDDEN_POS[i][1][1][1] >= 30:
                percent1 = FORBIDDEN_POS[i][0][1][0] / FORBIDDEN_POS[i][0][1][1]
                percent2 = FORBIDDEN_POS[i][1][1][0] / FORBIDDEN_POS[i][1][1][1]
                ### NULLÁZÁS FELTÉTELE
                if percent1 - percent2 >= 0.3:
                    FORBIDDEN_POS[i][1][1][0] = 'z'
                elif percent2 - percent1 >= 0.3:
                    FORBIDDEN_POS[i][0][1][0] = 'z'

def conclusion_file(INFILE, OUTFILE):
    ### ELLENŐRZÉS, HOGY ".txt" KITERJESZTÉSŰEK-E A MEGADOTT FILENEVEK
    iftxtin_tmp = ''
    iftxtout_tmp = ''
    for i in (-4, -3, -2, -1):
        iftxtin_tmp += INFILE[i]
        iftxtout_tmp += OUTFILE[i]
    # HA NEM, AKKOR KIEGÉSZÍTI
    if iftxtin_tmp != '.txt':
        INFILE += '.txt'
    if iftxtout_tmp != '.txt':
        OUTFILE += '.txt'

    infile = open(INFILE, 'r')
    outfile = open(OUTFILE, 'w')

    i = 0
    for line in infile:
        if i % 2 == 0:
            pos = line
        else:
            coord_list_tmp = []
            coord = line
            coord = coord.replace("\n", "")
            str2list(coord, coord_list_tmp)

            s = 0
            percent_list = []
            mean_percent = 0
            ### VIZSGÁLAT FELTÉTELE
            if len(coord_list_tmp) > 2:
                maxv_percent = 0
                minv_percent = 1
                index = 0
                for j in coord_list_tmp:
                    if j[1][0] != 'z' and j[1][1] >= 40:
                        s += 1
                        percent_list.append([j[1][0]/j[1][1], index])
                        mean_percent += percent_list[-1][0]
                        if percent_list[-1][0] > maxv_percent:
                            maxv_percent = percent_list[-1][0]
                        if percent_list[-1][0] < minv_percent:
                            minv_percent = percent_list[-1][0]
                    index += 1
                if s > 2:
                    mean_percent /= s
                    ### VÁLTOZÁS FELTÉTELE
                    if maxv_percent - minv_percent > 0.1:
                        for j in percent_list:
                            ### NULLÁZÁS FELTÉTELE
                            if j[0] < mean_percent:
                                coord_list_tmp[j[1]][1][0] = 'z'

                elif s == 2:
                    mean_percent /= s
                    ### VÁLTOZÁS FELTÉTELE
                    if maxv_percent - minv_percent > 0.3:
                        for j in percent_list:
                            ### NULLÁZÁS FELTÉTELE
                            if j[0] < mean_percent:
                                coord_list_tmp[j[1]][1][0] = 'z'

            elif len(coord_list_tmp) == 2:
                if coord_list_tmp[0][1][0] != 'z' and coord_list_tmp[1][1][0] != 'z' and coord_list_tmp[0][1][1] >= 30 and coord_list_tmp[1][1][1] >= 30:
                    percent1 = coord_list_tmp[0][1][0] / coord_list_tmp[0][1][1]
                    percent2 = coord_list_tmp[1][1][0] / coord_list_tmp[1][1][1]
                    ### NULLÁZÁS FELTÉTELE
                    if percent1 - percent2 >= 0.3:
                        coord_list_tmp[1][1][0] = 'z'
                    elif percent2 - percent1 >= 0.3:
                        coord_list_tmp[0][1][0] = 'z'

            outfile.write(str(pos))
            outfile.write(str(coord_list_tmp))
            outfile.write('\n')
        i += 1

    infile.close()
    outfile.close()

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

def merge_all(w, h, *FORBIDDEN_POSES):
    for i in range(1, len(FORBIDDEN_POSES)):
        merge_2pos(w, h, FORBIDDEN_POSES[0], FORBIDDEN_POSES[i])

def dict_diff(FORBIDDEN_POS_NEW, FORBIDDEN_POS_OLD):
    ### FORBIDDEN_POS_NEW = FORBIDDEN_POS_NEW - FORBIDDEN_POS_OLD
    for pos_old in FORBIDDEN_POS_OLD:
        for data_old in FORBIDDEN_POS_OLD[pos_old]:
            for data_new in FORBIDDEN_POS_NEW[pos_old]:
                ### HA A KOORDINÁTÁK MEGEGYEZNEK
                if data_new[0] == data_old[0]:
                    if data_new[1][0] != 'z' and data_old[1][0] != 'z':
                        data_new[1][0] -= data_old[1][0]
                        data_new[1][1] -= data_old[1][1]
                    elif data_new[1][0] == 'z':
                        data_new[1][1] -= data_old[1][1]
                    break
            tmp = []
            for data_new in FORBIDDEN_POS_NEW[pos_old]:
                if data_new[1][1] != 0:
                    tmp.append(data_new)
            if tmp != []:
                FORBIDDEN_POS_NEW[pos_old] = copy.deepcopy(tmp)
            else:
                FORBIDDEN_POS_NEW.pop(pos_old)

def print_time(s):
    s = int(s)
    part_h = int(s/60/60)
    s -= part_h*3600
    part_min = int(s/60)
    s -= part_min*60
    print('%dh %dm %ds' %(part_h, part_min, s))

def draw_pos(board, POS):
    height = len(board)
    width = len(board[0])
    tmp_board = list(range(height))
    for y in range(len(tmp_board)):
        tmp_board[y] = list(range(width))
        for x in range(len(tmp_board[y])):
            tmp_board[y][x] = 0

    for k in range(len(POS) // 5):
        x = int(POS[5 * k] + POS[5 * k + 1])
        y = int(POS[5 * k + 2] + POS[5 * k + 3])
        SIGN = POS[5 * k + 4]

        take_fix(tmp_board, (x, y), SIGN)

    print_board(tmp_board, 0, 1)

def Quartz_Mountain(W, H, FORBIDDEN_POS, INDEX, LEARN, HUMAN, MAX, PRINT):
    ### TÁBLA KÉSZÍTÉSE
    board = list(range(H))
    for y in range(len(board)):
        board[y] = list(range(W))
        for x in range(len(board[y])):
            board[y][x] = 0

    ### A PROGRAM A LÉPÉSEINÉL AZ EGYES LÉPÉSEKET SÚLYOZZA-E
    if HUMAN == 0:
        RAWDATA = 1
    else:
        RAWDATA = 0

    GAMES = 0
    ksum = 0
    kmin = 100

    forbidden_pos = {}
    if len(FORBIDDEN_POS[INDEX]) != 0:
        forbidden_pos = copy.deepcopy(FORBIDDEN_POS[INDEX])
    FORBIDDEN_POS[INDEX].clear()

    if HUMAN == 0:
        print('Process %d start!' % (INDEX))
        sys.stdout.flush()

    ### AMŐBÁZÁSOK
    while GAMES < MAX:
        GAMES += 1
        # if GAMES % (MAX / 100) == 0:
        #     print('\r Percent (%):', int(GAMES / (MAX / 100)), end='')
        #     sys.stdout.flush()

        if HUMAN == 0 and INDEX == 0 and PRINT == 1:
            print('Process 0 game %d/%d:' % (GAMES, MAX))
            sys.stdout.flush()

        ### EGY GAME
        for y in range(H):
            for x in range(W):
                board[y][x] = 0
        SWITCH4STEP = 0
        k = 0  # LÉPÉSEK SZÁMLÁLÓJA
        steps = []  # MEGTETT LÉPÉSEKET TARTALMAZZA
        PLAY = 1

        if HUMAN == 1:
            a = 0
            while a == 0:
                HUMAN = input('o vagy x szeretnél lenni (kör kezd)? \n(o/x): ')
                if HUMAN == 'x' or HUMAN == 'o':
                    a = 1
                else:
                    print('\nNem jó jelet adtál meg!')

        while PLAY == 1:
            # O LÉPÉSE
            if k % 2 == 0:
                if PLAY == 0:
                    break
                if HUMAN == 'o':
                    human_step(board, steps, k, PLAY, HUMAN)
                else:
                    if prog_step(board, steps, k, 'o', forbidden_pos, RAWDATA, SWITCH4STEP) == 0:
                        break
                    k += 1
                    if end(board, 'o', 0) == 'o':
                        break
            #print_board(board, steps[-1], 0)


            # X LÉPÉSE
            if k % 2 == 1:
                if PLAY == 0:
                    break
                if HUMAN == 'x':
                    human_step(board, steps, k, PLAY, HUMAN)
                else:
                    if prog_step(board, steps, k, 'x', forbidden_pos, RAWDATA, SWITCH4STEP) == 0:
                        break
                    k += 1
                    if end(board, 'x', 0) == 'x':
                        break

                if HUMAN == 0:
                    if k > 70:
                        steps[-1] = 'break'
                        GAMES -= 1
                        BREAK = 1
                        if INDEX == 0 and PRINT == 1:
                            print('break')
                        break
            #print_board(board, steps[-1], 0)

        # VÉGE EGY PARTINAK
        if HUMAN == 0 and INDEX == 0 and PRINT == 1:
            print('  Steps:', k)

        ### VÉGSŐ ÁLLÁS ÉRTÉKELÉSE
        if k < kmin:
            kmin = k
        ksum += k

        if LEARN == 1:
            learn(board, k, steps, forbidden_pos)

        if HUMAN == 1:
            clear_screen()
            print_board(board, 0, 0)
            if k % 2 == 0:
                end(board, 'x', 1)
            else:
                end(board, 'o', 1)
            print('Lépések száma: ', k)

        if HUMAN == 1:
            a = 0
            ans = input('Folytatás? (i/n): ')
            while a == 0:
                if ans == 'i' or ans == 'n':
                    a = 1
                else:
                    ans = input('Folytatás? (i/n): ')
            if ans == 'n':
                break
            else:
                a = 0
                while a == 0:
                    HUMAN = input('o vagy x szeretnél lenni (kör kezd)? \n(o/x): ')
                    if HUMAN == 'x' or HUMAN == 'o':
                        a = 1
                        GAMES -= 1
                    else:
                        print('\nNem jó jelet adtál meg!')

    ### ADATOK TISZTÍTÁSA
    forbidden_pos = cleardat(forbidden_pos)

    ### ADATOK MÁSOLÁSA
    FORBIDDEN_POS[INDEX] = copy.deepcopy(forbidden_pos)

    ### RÉSZEREDMÉNY
    print('Process %d end.' % (INDEX))


if __name__ == '__main__':
    ### TÁBLA MÉRETEI FŐ FÜGGVÉNYNEK
    w = 15
    h = 15

    ### KAPCSOLÓK
    CONTINUE = 0    # FOLYTASSA-E AZ OCVIST_POS.TXT FILEBÓL
    LEARN = 1
    HUMAN = 0
    MAX = 30        # MINDEN EGYES SZÁL ENNYI GAMET JÁTSZIK EGYSZERRE, MAJD ÉRTÉKELÉS PART SZÁMSZOR
    PART = 4        # HÁNYSZOR MAX-NYI KÖRT JÁTSZON MINDEGYIK SZÁLON
    PRINT = 1

    ### HASZNÁLATOS OBJEKTUMOK
    forbidden_pos_all = {}
    process_num = multiprocessing.cpu_count()
    manager = multiprocessing.Manager()
    forbidden_poses = manager.list([manager.dict() for _ in range(process_num)])

    ### HA KORÁBBI ÁLLÁST FOLYTATNA
    if CONTINUE == 1:
        infile = open(r'Ocvist_pos.txt', 'r')
        i = 0
        for line in infile:
            if i % 2 == 0:
                pos = line
                pos = pos.replace("\n", "")
            else:
                coord_list_tmp = []
                coord = line
                coord = coord.replace("\n", "")
                str2list(coord, coord_list_tmp)
                forbidden_pos_all[pos] = coord_list_tmp
            i += 1
        infile.close()


    ### MULTIPROCESS SZÁMÍTÁSOK
    orig_time = t.perf_counter()
    for p in range(PART):
        print('PART:', p + 1)
        before = t.perf_counter()
        for i in range(process_num):
            forbidden_poses[i] = copy.deepcopy(forbidden_pos_all)
        processes = []
        for i in range(process_num):
            # the_ocvist(FORBIDDEN_POS, INDEX, LEARN, HUMAN, MAX, PART, PRINT)
            process = multiprocessing.Process(target=Quartz_Mountain, args=(w, h, forbidden_poses, i, LEARN, HUMAN, MAX, PRINT))
            processes.append(process)
            process.start()
        for proc in processes:
            proc.join()
        print('\nMultiprocess rész ideje:', end=' ')
        print_time(t.perf_counter() - before)
        print()

        ### EREDMÉNYEK ÖSSZEÍRÁSA RES_TMP[0]-BA
        res_tmp = []
        for i in range(len(forbidden_poses)):
            res_tmp.append({})
            res_tmp[-1] = copy.deepcopy(forbidden_poses[i])
            dict_diff(res_tmp[-1], forbidden_pos_all)
        merge_all(w, h, *res_tmp)
        merge_2pos(w, h, forbidden_pos_all, res_tmp[0])
        res_tmp = []

        ### KONKLÚZIÓ
        conclusion(forbidden_pos_all)

        if LEARN == 1:
            print('File írása!')
            if p < PART - 1:
                ### RÉSZEREDMÉNYEK MENTÉSE
                savefile = open(r'Ocvist_pos_save.txt', 'w')
                for i in forbidden_pos_all:
                    savefile.write(str(i))
                    savefile.write('\n')
                    savefile.write(str(forbidden_pos_all[i]))
                    savefile.write('\n')
                savefile.close()

                ### RÉSZEREDMÉNYEK VISSZAMÁSOLÁSA
                for i in range(len(forbidden_poses)):
                    forbidden_poses[i] = copy.deepcopy(forbidden_pos_all)
                print('Save file kész!\n\n')
            else:
                ### VÉGSŐ EREDMÉNY KIÍRÁSA
                outfile = open(r'Ocvist_pos.txt', 'w')
                for i in forbidden_pos_all:
                    outfile.write(str(i))
                    outfile.write('\n')
                    outfile.write(str(forbidden_pos_all[i]))
                    outfile.write('\n')
                outfile.close()
                print('Végső pos file kész!')
                print('\nTeljes idő:', end=' ')
                print_time(t.perf_counter() - orig_time)
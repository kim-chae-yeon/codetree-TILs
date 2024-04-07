from copy import deepcopy
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def gisa_move(gisa, dir):
    r, c, h, w = map(int, gisa_dict[gisa][:4])
    if 0 <= r + dx[dir] + h - 1 < L and 0 <= c + dy[dir] + w - 1 < L:
        check_chess = sum([chess_board[x][c + dy[dir]: c + dy[dir] + w] for x in range(r + dx[dir], r + dx[dir] + h)], [])
        if not 2 in check_chess:
            move_location = [gisa_board[x][c + dy[dir]: c + dy[dir] + w] for x in range(r + dx[dir], r + dx[dir] + h)]
            move_dict[gisa] = (r + dx[dir], c + dy[dir])

            for m in set(sum(move_location, [])):
                if m != 0 and not m in move_dict:
                    if not gisa_move(m, dir):
                        break
            else:
                for x in range(r, r + h):
                    for y in range(c, c + w):
                        board[x][y] = 0

                if gisa == i or (gisa != i and gisa_dict[gisa][4] > damage_dict[gisa] + check_chess.count(1)):
                    for x in range(r + dx[dir], r + dx[dir] + h):
                        for y in range(c + dy[dir], c + dy[dir] + w):
                            board[x][y] = gisa

                    if gisa != i:
                        tmp_damage[gisa] += check_chess.count(1)
                else:
                    delete_gisa.append(gisa)
                return True

    return False

if __name__ == "__main__":
    L, N, Q = map(int, input().split())
    chess_board = [list(map(int, input().split())) for _ in range(L)]
    gisa_dict = dict()
    gisa_board = [[0] * L for _ in range(L)]
    for n in range(1, N + 1):
        gisa_dict[n] = list(map(int, input().split()))
        gisa_dict[n][0] -= 1
        gisa_dict[n][1] -= 1
        for r in range(gisa_dict[n][0], gisa_dict[n][0] + gisa_dict[n][2]):
            for c in range(gisa_dict[n][1], gisa_dict[n][1] + gisa_dict[n][3]):
                gisa_board[r][c] = n

    damage_dict = dict({n: 0 for n in range(1, N + 1)})
    for _ in range(Q):
        i, d = map(int, input().split())
        if i in gisa_dict:
            move_dict = dict()
            board = deepcopy(gisa_board)
            delete_gisa = []
            tmp_damage = [0] * (N + 1)
            if gisa_move(i, d):
                gisa_board = board
                for d in delete_gisa:
                    del move_dict[d]
                    del damage_dict[d]
                    del gisa_dict[d]

                for move_gisa in move_dict:
                    damage_dict[move_gisa] += tmp_damage[move_gisa]
                    gisa_dict[move_gisa][0] = move_dict[move_gisa][0]
                    gisa_dict[move_gisa][1] = move_dict[move_gisa][1]
    print(sum(damage_dict.values()))
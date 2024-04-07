dx = [-1, 0, 1, 0, -1, -1, 1, 1]
dy = [0, 1, 0, -1, -1, 1, -1, 1]

def close_santa_find_and_move():
    global rudolf
    close_santa, dist, r, c = 0, 5001, -1, -1
    for s, loc in santa_dict.items():
        d = (rudolf[0] - loc[0]) ** 2 + (rudolf[1] - loc[1]) ** 2
        if d < dist or (d == dist and (loc[0] > r or (loc[0] == r and loc[1] > c))):
            close_santa, dist, r, c = s, d, loc[0], loc[1]

    dir, dis = -1, 5001
    for d in range(8):
        next_rudolf_x, next_rudolf_y = rudolf[0] + dx[d], rudolf[1] + dy[d]
        if 0 <= next_rudolf_x < N and 0 <= next_rudolf_y < N and dis > (next_rudolf_x - r) ** 2 + (next_rudolf_y - c) ** 2:
            dir, dis = d, (next_rudolf_x - r) ** 2 + (next_rudolf_y - c) ** 2

    if dis == 0:
        gijul_santa[close_santa] = 2
        rudolf_kick_santa(dir)
    else:
        rudolf = [rudolf[0] + dx[dir], rudolf[1] + dy[dir]]

def rudolf_kick_santa(dir):
    global rudolf
    santa = game_map[rudolf[0] + dx[dir]][rudolf[1] + dy[dir]]
    rudolf = list(santa_dict[santa])
    game_map[rudolf[0]][rudolf[1]] = 0

    santa_score[santa] += C
    move_santa = (santa_dict[santa][0] + C * dx[dir], santa_dict[santa][1] + C * dy[dir])

    if not (0 <= move_santa[0] < N and 0 <= move_santa[1] < N):
        del santa_dict[santa]

    elif not game_map[move_santa[0]][move_santa[1]]:
        santa_dict[santa] = move_santa
        game_map[move_santa[0]][move_santa[1]] = santa

    else:
        santa_kick_santa(santa, game_map[move_santa[0]][move_santa[1]], dir)

def santa_kick_santa(from_santa, to_santa, dir):
    game_map[santa_dict[to_santa][0]][santa_dict[to_santa][1]] = 0
    santa_dict[from_santa] = santa_dict[to_santa]
    game_map[santa_dict[from_santa][0]][santa_dict[from_santa][1]] = from_santa

    move_santa = (santa_dict[to_santa][0] + dx[dir], santa_dict[to_santa][1] + dy[dir])
    if not (0 <= move_santa[0] < N and 0 <= move_santa[1] < N):
        del santa_dict[to_santa]

    elif rudolf == [move_santa[0], move_santa[1]]:
        dir = dir + 2 if dir < 2 else dir - 2
        santa_kick_rudolf(to_santa, dir)

    elif not game_map[move_santa[0]][move_santa[1]]:
        santa_dict[to_santa] = (move_santa[0], move_santa[1])
        game_map[move_santa[0]][move_santa[1]] = to_santa

    else:
        santa_kick_santa(to_santa, game_map[move_santa[0]][move_santa[1]], dir)

def santa_move(santa):
    dir, min_dist = -1, (santa_dict[santa][0] - rudolf[0]) ** 2 + (santa_dict[santa][1] - rudolf[1]) ** 2
    for d in range(4):
        next_x, next_y = santa_dict[santa][0] + dx[d], santa_dict[santa][1] + dy[d]
        if 0 <= next_x < N and 0 <= next_y < N and not game_map[next_x][next_y] and min_dist > (next_x - rudolf[0]) ** 2 + (next_y - rudolf[1]) ** 2:
            dir, min_dist = d, (next_x - rudolf[0]) ** 2 + (next_y - rudolf[1]) ** 2

    if dir != -1:
        game_map[santa_dict[santa][0]][santa_dict[santa][1]] = 0
        next_x, next_y = santa_dict[santa][0] + dx[dir], santa_dict[santa][1] + dy[dir]
        if rudolf == [next_x, next_y]:
            dir = dir + 2 if dir < 2 else dir - 2
            santa_kick_rudolf(santa, dir)
        else:
            game_map[next_x][next_y] = santa
            santa_dict[santa] = (next_x, next_y)

def santa_kick_rudolf(santa, dir):
    next_x, next_y = rudolf[0] + D * dx[dir], rudolf[1] + D * dy[dir]
    santa_score[santa] += D
    gijul_santa[santa] = 2

    if not (0 <= next_x < N and 0 <= next_y < N):
        del santa_dict[santa]

    elif not game_map[next_x][next_y]:
        santa_dict[santa] = (next_x, next_y)
        game_map[next_x][next_y] = santa

    else:
        santa_kick_santa(santa, game_map[next_x][next_y], dir)

if __name__ == "__main__":
    N, M, P, C, D = map(int, input().split())
    game_map = [[0] * N for _ in range(N)]

    global rudolf
    rudolf = list(int(x) - 1 for x in input().split())
    santa_dict = dict()
    for _ in range(P):
        n, r, c = map(int, input().split())
        santa_dict[n] = (r - 1, c - 1)
        game_map[r - 1][c - 1] = n

    santa_dict = dict(sorted(santa_dict.items(), key=lambda x: x[0]))
    santa_score = dict({x: 0 for x in range(1, P + 1)})
    gijul_santa = dict()

    for _ in range(M):
        close_santa_find_and_move()
        if not santa_dict:
            break

        for s in range(1, P + 1):
            if s in santa_dict and not s in gijul_santa:
                santa_move(s)
        if not santa_dict:
            break

        tmp = []
        for s, v in gijul_santa.items():
            if v == 1:
                tmp.append(s)
                continue
            gijul_santa[s] -= 1
        for s in tmp:
            del gijul_santa[s]

        for s in santa_dict:
            santa_score[s] += 1
    print(" ".join(list(map(str, santa_score.values()))))
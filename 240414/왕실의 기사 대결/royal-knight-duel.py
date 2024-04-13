# (1, 1)로 시작
# 빈칸 / 함정 / 벽
L, N, Q = map(int, input().split())

chess = []
chess_knight = [[0]*L for i in range(L)]
knight = [] # [1,2,2,1,5]
order = []
# 체력 = knight[i][4], #기사-1 = i

for _ in range(L):
    tmp = list(map(int, input().split()))
    chess.append(tmp)

for i in range(1, N+1):
    tmp = list(map(int, input().split()))
    tmp.append(0) #[5], 죽었는지 살았는지
    tmp.append(i) #[6] [[1,2,2,1,5, 0, 1(=몇번 기사인지)], ...]
    knight.append(tmp)

for _ in range(Q):
    tmp = list(map(int, input().split()))
    order.append(tmp) #[[1,2],[2,1],[3,3]]

dir = [[-1, 0], [0, 1], [1, 0], [0, -1]]
before_knight = [row[:] for row in knight] #damage 계산을 위함

def first_update_chess_knight(knight): #knight 정보로 chess_knight 업데이트함.
    for i in range(len(knight)):
        if knight[i][5] != -1:
            knight_num = knight[i][6]
            r = knight[i][0]
            c = knight[i][1]
            for j in range(knight[i][2]): #세로 (2)
                for k in range(knight[i][3]): #가로 (1)
                    chess_knight[r+j-1][c+k-1] = knight_num #r,c = 1, 2 / 2, 2

first_update_chess_knight(knight)

def find_knight(chess_knight_num): #ex. find_knight(1)
    lst = []
    for i in range(L):
        for j in range(L):
            if chess_knight[i][j] == chess_knight_num:
                lst.append([i, j])
    return lst #[[r, c]]


def check_knight(knightnum, move): #1, [1,0] > 몇번째 기사를 이동해라. 이동 불가하면 return 0
    check = 0
    movingarr = []
    knight_arr = find_knight(knightnum) # [[0,1],[1,1]]
    for i in range(len(knight_arr)):
        nr = knight_arr[i][0] + move[0]
        nc = knight_arr[i][1] + move[1]
        if nr>L-1 or nr<0 or nc>L-1 or nc<0: #체스판 벗어남
            return False
        elif chess[nr][nc] == 2: #벽을 만남
            return False
        elif chess_knight[nr][nc] != knightnum and chess_knight[nr][nc] != 0: # 다른 기사
            othernum = chess_knight[nr][nc]
            tmp = check_knight(othernum, move)
            if tmp == 0:
                return False
            else:
                for i in range(len(tmp)):
                    movingarr.append(tmp[i])
        else: #이동 가능
            check += 1
    if check == len(knight_arr):
        movingarr.append(knightnum)
        return movingarr #몇번째 기사들 이동하면 되는지
    movingarr.append(knightnum)
    return movingarr

for i in range(len(order)):
    tmp_chess = [[0]*L for i in range(L)]
    knightnum = order[i][0] # 1
    move = dir[order[i][1]] #[1, 0], 아래로 이동
    if knight[knightnum-1][5] == -1:# 기사가 죽었으면 pass
        continue
    if check_knight(knightnum, move) != 0: # 기사 이동이 가능함
        movingknightnum = check_knight(knightnum, move) #[1, 2, 3] 이동할 기사들 번호
        movingknightnum.reverse() # 역순으로 해서 이동해도 괜찮게끔 ---- !!! return값 없음
        for j in movingknightnum: # j번째 기사 이동
            knight_arr = find_knight(j)  # [[0,1],[1,1]]
            for k in range(len(knight_arr)):
                r = knight_arr[k][0]
                c = knight_arr[k][1]
                nr = knight_arr[k][0] + move[0]
                nc = knight_arr[k][1] + move[1]
                tmp_chess[nr][nc] = j

        # 죽어서 없는 놈 빼고 살아있고 안움직인 놈 다시 업데이트
        for i in range(1, N):
            pos=[]
            if i not in movingknightnum:
                if knight[i-1][5] == -1:
                    continue
                else:
                    pos=find_knight(i)
            for j in range(len(pos)):
                r = pos[j][0]
                c = pos[j][1]
                tmp_chess[r][c] = i

        chess_knight = tmp_chess

        for j in movingknightnum: # 기사 모두 이동 후, 데미지
            count = 0
            knight_arr = find_knight(j)
            for k in range(len(knight_arr)):
                r = knight_arr[k][0]
                c = knight_arr[k][1]
                if chess[r][c] == 1:
                    count += 1
            if knightnum != j: # 명령을 받은 기사는 데미지 x
                knight[j-1][4] -= count
                if knight[j-1][4] <= 0:
                    knight[j-1][5] = -1
                    for k in range(len(knight_arr)):
                        r = knight_arr[k][0]
                        c = knight_arr[k][1]
                        chess_knight[r][c] = 0 # chess_knight 판에서 지움
# 남은 체력 계산
hp = []
for i in range(len(knight)):
    if knight[i][5] == -1:
        continue
    else:
        hp.append(before_knight[i][4] - knight[i][4])
print(sum(hp))
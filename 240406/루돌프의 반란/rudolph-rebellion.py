N, M, P, C, D = list(map(int, input().split()))

# N x N metric, position = (r, c)
# M turns, 매 턴마다 루돌프 한번 움직인 뒤 1번부터 p번 산타 움직임.
# 루돌프는 가장 가까운 산타한테 8방향 돌진, if r >  이후 if c >
# 산타는 1번부터 P번까지 순서대로, 루돌프에게 가장 가까운 4방향으로 움직임. 위 아래 좌 우 순서 우선
# 움직일 수 있는 칸이 있는지 check && 루돌프에게 가까워질 수 있는지 check
# 
# 산타와 루돌프가 같은 칸이면 충돌 - 루돌프가 움직인 경우
# C만큼 점수 얻고 산타가 루돌프가 이동해온 방향으로 C만큼 밀려남
# - 산타가 움직인 경우 D만큼 점수 얻고 산타가 이동해온 방향으로 D만큼 밀려남. 밀려날떄는 충돌 x
# 밀려난게 게임판 밖이면 산타는 탈락
# 밀려난 칸에 다른 산타가 있으면 다른 산타가 1칸 해당 방향으로 밀려남.
# 그 옆에 산타가 있으면 연쇄적으로 1칸씩 밀려남. 게임판 밖으로 밀린 산타는 탈락.
# 루돌프와 충돌한 후 산타는 k번째 턴인경우 K+1턴까지 기절. K+2부턴 정상.  << state
# 루돌프는 기절한 산타를 돌진 대상으로 선택할 수 있음.
# M번에 걸쳐 루돌프, 산타가 순서대로 움직인 이후 게임 종료. P명의 산타가 모두 탈락하면 즉시 게임종료.
# 매 턴 이후 탈락하지 않은 산타 +1점씩
# -- 각 산타가 얻은 최종 점수 return

# -- logic
# def 가까운 산타 찾기
# def 가까운 루돌프 찾기
# def 상호작용
# 점수용 count array
# 기절용 state array

Rr, Rc = map(int, input().split())
arr = [[0]*N for _ in range(N)]
arr[Rc-1][Rr-1] = 2 # 루돌프 = 2

p_arr = []
# 중요! 좌상단은 (1, 1)!! -1 해줘야할듯
for i in range(P):
    tmp = list(map(int, input().split()))
    p_arr.append(tmp)

# 이거 산타 위치 계산할 때 써야함
for i in range(len(p_arr)):
    Sr, Sc = p_arr[i][1], p_arr[i][2]
    arr[Sc-1][Sr-1] = 1 # 산타 = 1

count = [0]*P
state = [0]*P # state = 1 : 기절, -1 : 탈락

def posi_R(arr):
    for i in range(N):
        for j in range(N):
            if arr[i][j] == 2:
                R = [j, i]
    return R

def posi_S(arr):
    S = []
    for i in range(N):
        for j in range(N):
            if arr[i][j] == 1:
                S.append([j,i])
    return S

def shortest_S(R, S):
    dist_arr = []
    index_arr = [] # 중복 확인용
    for i in range(len(S)):
        dist = (R[0] - S[i][0])**2 + (R[1] - S[i][1])**2
        dist_arr.append(dist)
        if min(dist_arr) > dist:
            index_arr = []
            index_arr.append(i)
        elif min(dist_arr) == dist:
            index_arr.append(i)
    return index_arr

def move_R_and_checkCollision(R, S, shortest_S, C):
    def move_chain(a,b): # a,b = moved_c, moved_r
        if a<0 and a>N-1 and b<0 and b>N-1:
            for i in range(P):
                if S[i][0] == a and S[i][1] == b:
                    state[i] = -1
        while a>=0 and a<=N-1 and b>=0 and b<=N-1: # 튕겨져서 게임판 밖으로 나가면 break
            if arr[b][a] == 1:
                if arr[b+back_c][a+back_r] != 1:
                    arr[b+back_c][a+back_r] = 1
                elif arr[b+back_c][a+back_r] == 1:
                    move_chain(a+back_r, b+back_c)
            elif arr[b][a] != 1:
                arr[b][a] = 1
                break

    before_R = R[:] # 중요 !!!!!! 리스트는 mutable, 따라서 list를 [:]로 copy 후 할당해야 안변함.
    if len(shortest_S) == 1: # 산타가 하나만 있는경우
        i = shortest_S[0]
        if R[0] != S[i][0] and R[1] != S[i][1]: # 대각선인 경우
            if S[i][0] > R[0]:
                R[0] = R[0]+1
            if S[i][0] < R[0]:
                R[0] = R[0]-1
            if S[i][1] > R[1]:
                R[1] = R[1]+1
            if S[i][1] < R[1]:
                R[1] = R[1]-1
        elif R[0] == S[i][0]: # x값이 같으면 y값만 이동
            if S[i][1] > R[1]:
                R[1] = R[1]+1
            if S[i][1] < R[1]:
                R[1] = R[1]-1
        elif R[1] == S[i][1]:
            if S[i][0] > R[0]:
                R[0] = R[0]+1
            if S[i][0] < R[0]:
                R[0] = R[0]-1
        if R[0] == S[i][0] and R[1] == S[i][1]: # 충돌 발생
            count[i] += C
            state[i] = 2
            back_r, back_c = (R[0]-before_R[0]), (R[1]-before_R[1]) # 루돌프가 온 방향
            moved_r, moved_c = S[i][0] + back_r*C, S[i][1] + back_c*C # *C
            print("R, before R", R, before_R)
            print("back_r", back_r)
            print("back_c", back_c)
            print("C", C)
            print("S[i][0]", S[i][0])
            print("moved_r", moved_r)
            print("moved_c", moved_c)
            if moved_r > N-1 or moved_r < 0 or moved_c > N-1 or moved_c < 0: # out of range 발생
                arr[S[i][1]][S[i][0]] = 0
                state[i] = -1
            elif arr[moved_c][moved_r] == 1: # C만큼 날라간 곳에 산타 있으면 연쇄 이동
                move_chain(moved_r, moved_c)
            else:
                S[i][0] += back_r
                S[i][1] += back_c
    else: # 거리가 같은 산타가 두개이상 -> r, c 우선순위
        r_arr = []
        c_arr = []
        idx_arr = []
        for i in range(len(shortest_S)):
            idx = shortest_S[i]
            r_arr.append(S[idx][0])
            if max(r_arr) < S[idx][0]:
                idx_arr = []
                idx_arr.append(idx)
            elif S[idx][0] == max(r_arr):
                idx_arr.append(idx)
        if len(idx_arr) > 1:
            ans=[]
            for j in idx_arr:
                c_arr.append(S[j][1])
                ans.append(j)
                if c_arr[0] < S[j][1]:
                    ans=[]
                    ans.append(j)
            idx_arr = ans
        if len(idx_arr) == 1:
            # 기존 알고리즘
            i = idx_arr[0]
            if R[0] != S[i][0] and R[1] != S[i][1]: # 대각선인 경우
                if S[i][0] > R[0]:
                    R[0] = R[0]+1
                if S[i][0] < R[0]:
                    R[0] = R[0]-1
                if S[i][1] > R[1]:
                    R[1] = R[1]+1
                if S[i][1] < R[1]:
                    R[1] = R[1]-1
            elif R[0] == S[i][0]: # x값이 같으면 y값만 이동
                if S[i][1] > R[1]:
                    R[1] = R[1]+1
                if S[i][1] < R[1]:
                    R[1] = R[1]-1
            elif R[1] == S[i][1]: # y값이 같으면 x값만 이동
                if S[i][0] > R[0]:
                    R[0] = R[0]+1
                if S[i][0] < R[0]:
                    R[0] = R[0]-1
            if R[0] == S[i][0] and R[1] == S[i][1]: # 충돌 발생
                count[i] += C
                state[i] = 2
                back_r, back_c = (R[0]-before_R[0]), (R[1]-before_R[1]) # 루돌프가 온 방향 * C
                moved_r, moved_c = S[i][0] + back_r*C, S[i][1] + back_c*C
                print("R, before R", R, before_R)
                print("back_r", back_r)
                print("back_c", back_c)
                print("C", C)
                print("S[i][0]", S[i][0])
                print("moved_r", moved_r)
                print("moved_c", moved_c)
                if moved_r > N-1 or moved_r < 0 or moved_c > N-1 or moved_c < 0: # out of range 발생
                    arr[S[i][1]][S[i][0]] = 0
                    state[i] = -1
                elif arr[moved_c][moved_r] == 1:
                    move_chain(moved_r, moved_c)
                else:
                    S[i][0] += back_r
                    S[i][1] += back_c
    arr[before_R[1]][before_R[0]] = 0
    arr[R[1]][R[0]] = 2
    return R

def move_S_and_checkCollision(R, S, shortest_S, D):
    def move_chain(a,b): # a,b = moved_c, moved_r
        while a>=0 and a<=N-1 and b>=0 and b<=N-1: # 튕겨져서 게임판 밖으로 나가면 break
            if arr[b][a] == 1:
                if arr[b+back_c][a+back_r] != 1:
                    arr[b+back_c][a+back_r] = 1
                elif arr[b+back_c][a+back_r] == 1:
                    move_chain(a+back_r, b+back_c)
            elif arr[b][a] != 1:
                arr[b][a] = 1
                break

    before_S = S[:] # 중요 !!!!!! 리스트는 mutable, 따라서 list를 [:]로 copy 후 할당해야 안변함.
    for i in range(len(P)):
        if state[i] != -1:
            S[i]

    for i in range(P):
        if state
        Sr, Sc = S[i][0], S[i][1]
    

    if len(shortest_S) == 1: # 산타가 하나만 있는경우
        i = shortest_S[0]
        if R[0] != S[i][0] or R[1] != S[i][1]:
            if S[i][1] < R[1]:
                S[i][1] = S[i][1]+1
            elif S[i][0] < R[0]:
                S[i][0] = S[i][0]+1
            elif S[i][1] > R[1]:
                S[i][1] = S[i][1]-1
            elif S[i][0] > R[0]:
                S[i][0] = S[i][0]-1
       
        if R[0] == S[i][0] and R[1] == S[i][1]: # 충돌 발생
            count[i] += D
            state[i] += 2
            back_r, back_c = (R[0]-before_R[0]), (R[1]-before_R[1]) # 루돌프가 온 방향
            moved_r, moved_c = S[i][0] + back_r*C, S[i][1] + back_c*C # *C
            print("R, before R", R, before_R)
            print("back_r", back_r)
            print("back_c", back_c)
            print("C", C)
            print("S[i][0]", S[i][0])
            print("moved_r", moved_r)
            print("moved_c", moved_c)
            if moved_r > N-1 or moved_r < 0 or moved_c > N-1 or moved_c < 0: # out of range 발생
                arr[S[i][1]][S[i][0]] = 0
            elif arr[moved_c][moved_r] == 1: # C만큼 날라간 곳에 산타 있으면 연쇄 이동
                move_chain(moved_r, moved_c)
            else:
                S[i][0] += back_r
                S[i][1] += back_c
    else: # 거리가 같은 산타가 두개이상 -> r, c 우선순위
        r_arr = []
        c_arr = []
        idx_arr = []
        for i in range(len(shortest_S)):
            idx = shortest_S[i]
            r_arr.append(S[idx][0])
            if max(r_arr) < S[idx][0]:
                idx_arr = []
                idx_arr.append(idx)
            elif S[idx][0] == max(r_arr):
                idx_arr.append(idx)
        if len(idx_arr) > 1:
            ans=[]
            for j in idx_arr:
                c_arr.append(S[j][1])
                ans.append(j)
                if c_arr[0] < S[j][1]:
                    ans=[]
                    ans.append(j)
            idx_arr = ans
        if len(idx_arr) == 1:
            # 기존 알고리즘
            i = idx_arr[0]
            if R[0] != S[i][0] and R[1] != S[i][1]: # 대각선인 경우
                if S[i][0] > R[0]:
                    R[0] = R[0]+1
                if S[i][0] < R[0]:
                    R[0] = R[0]-1
                if S[i][1] > R[1]:
                    R[1] = R[1]+1
                if S[i][1] < R[1]:
                    R[1] = R[1]-1
            elif R[0] == S[i][0]: # x값이 같으면 y값만 이동
                if S[i][1] > R[1]:
                    R[1] = R[1]+1
                if S[i][1] < R[1]:
                    R[1] = R[1]-1
            elif R[1] == S[i][1]: #y값이 같으면 x값만 동
                if S[i][0] > R[0]:
                    R[0] = R[0]+1
                if S[i][0] < R[0]:
                    R[0] = R[0]-1
            if R[0] == S[i][0] and R[1] == S[i][1]: # 충돌 발생
                count[i] += C
                state[i] += 2
                back_r, back_c = (R[0]-before_R[0]), (R[1]-before_R[1]) # 루돌프가 온 방향 * C
                moved_r, moved_c = S[i][0] + back_r*C, S[i][1] + back_c*C
                print("R, before R", R, before_R)
                print("back_r", back_r)
                print("back_c", back_c)
                print("C", C)
                print("S[i][0]", S[i][0])
                print("moved_r", moved_r)
                print("moved_c", moved_c)
                if moved_r > N-1 or moved_r < 0 or moved_c > N-1 or moved_c < 0: # out of range 발생
                    arr[S[i][1]][S[i][0]] = 0
                elif arr[moved_c][moved_r] == 1:
                    move_chain(moved_r, moved_c)
                else:
                    S[i][0] += back_r
                    S[i][1] += back_c
    arr[before_R[1]][before_R[0]] = 0
    arr[R[1]][R[0]] = 2
    return R

print(arr)
R = posi_R(arr) # [Rr, Rc] (-1씩 된 좌표)
S = posi_S(arr) # [[Sr, Sc], [Sr, Sc], ...] (-1씩 된 좌표)
short_s = shortest_S(R, S) # [0, 1, 2]
print("0 try", R)
R1 = move_R_and_checkCollision(R, S, short_s, C)
S1 = posi_S(arr)
short_s1 = shortest_S(R1, S1)
print(arr)
print("1 try R ", R1)
print("1 try S ", S1)
print("1 try short_s", short_s1)
R2 = move_R_and_checkCollision(R1, S1, short_s1, C)
print("2 try", R2)
print(arr)
print(count)



# 여기까지 3h 55m, GG
# 미구현요소 : move_S_andcheckcollision
# 
# 패착 : lst a = b로 const하게 박아두고 history로 쓰려했는데, 리스트는 mutable이라 b가 바뀌면 a가 자동으로 계속 바뀌어서
# 디버깅하는데 오래 걸림. 또한 move_S_checkcollision 구현하면서 Santa array인 S와 state로 기절일 땐 pass하려했는데, 
# santa가 게임판에서 밀려나 없어졌을 때 S의 index와 state의 index를 동일하게 하는걸 못해서 헤맸음.
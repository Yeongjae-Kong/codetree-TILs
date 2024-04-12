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

Rc, Rr = map(int, input().split())
arr = [[0]*N for _ in range(N)]
arr[Rc-1][Rr-1] = 2 # 루돌프 = 2

p_arr = []
# 중요! 좌상단은 (1, 1)!! -1 해줘야할듯
for i in range(P):
    tmp = list(map(int, input().split()))
    tmp.append(0) # state
    tmp.append(0) # count
    p_arr.append(tmp)
    
# [[1,1,3,0,0], [2,3,5,0,0], [3,5,1,0,0], [4,4,4,0,0]]
p_arr.sort()
# 이거 산타 위치 계산할 때 써야함
# p_arr를 loop돌며 arr에 산타 위치=1로 변환
for i in range(len(p_arr)):
    Sc, Sr = p_arr[i][1], p_arr[i][2]
    arr[Sc-1][Sr-1] = 1 # 산타 = 1

def posi_R(arr):
    for i in range(N):
        for j in range(N):
            if arr[i][j] == 2:
                R = [j, i]
    return R

def posi_S(arr):
    # 이거 산타 위치 arr에 계산할 때 써야함
    # p_arr를 loop돌며 arr 산타 위치=1로 변환
    # 초기 p_arr = [[1,1,3,0,0], [2,3,5,0,0], [3,5,1,0,0], [4,4,4,0,0]]
    for i in range(len(p_arr)):
        if p_arr[i][3] != -1:
            Sc, Sr = p_arr[i][1], p_arr[i][2]
            p_arr[i][1] = Sr
            p_arr[i][2] = Sc
            arr[Sc-1][Sr-1] = 1 # 산타 = 1
    return p_arr

def shortest_S(R, S): # 거리가 짧은 index (혹은 index arr) return
    dist_arr = []
    index_arr = [] # 중복 확인용
    for i in range(len(S)):
        if S[i][3] != -1:
            dist = (R[0] - S[i][1]+1)**2 + (R[1] - S[i][2]+1)**2
            if len(dist_arr) < 1:
                dist_arr.append(dist)
            if min(dist_arr) > dist:
                dist_arr.append(dist)
                index_arr = []
                index_arr.append(i)
            elif min(dist_arr) == dist:
                index_arr.append(i)
    return index_arr

def move_R_and_checkCollision(R, S, shortest_index, C):
    def move_chain(a,b): # a,b = moved_c, moved_r (3, 3) / back_r, back_c = (1, 0)
        if a+back_r<0 or a+back_r>N-1 or b+back_c<0 or b+back_c>N-1: # 밀려나간게 게임판 밖이면
            for i in range(P):
                if S[i][1]-1 == a and S[i][2]-1 == b: # 기존에 있던 밀려난 놈을 찾아서
                    S[i][1] += back_r
                    S[i][2] += back_c # 날아간 거리만큼 좌표를 더해주고
                    S[i][3] = -1 # 죽었다고 표시
            return S
        elif arr[b+back_c][a+back_r] != 1: # 밀려나간게 게임판 안이고 산타가 없으면 해당 위치로 산타 옮김
            for i in range(P):
                if S[i][1]-1 == a and S[i][2]-1 == b: # 기존에 있던 밀려난 놈 찾음
                    S[i][1] += back_r
                    S[i][2] += back_c 
            return S
        elif arr[b+back_c][a+back_r] == 1: # 밀려나갔는데 또 산타있으면 재귀
            print("move R에서 또 재귀 발생")
            move_chain(a+back_r, b+back_c)
            for i in range(P):
                if S[i][1]-1 == a and S[i][2]-1 == b: # 기존에 있던 밀려난 놈을 찾아서
                    S[i][1] += back_r
                    S[i][2] += back_c
            return S

    before_R = R[:] # 중요 !!!!!! 리스트는 mutable, 따라서 list를 [:]로 copy 후 할당해야 안변함.

    if len(shortest_index) == 1: # 산타가 하나만 있는경우
        i = shortest_index[0]
        if R[0] != S[i][1]-1 and R[1] != S[i][2]-1: # 대각선인 경우
            if S[i][1]-1 > R[0]:
                R[0] = R[0]+1
            if S[i][1]-1 < R[0]:
                R[0] = R[0]-1
            if S[i][2]-1 > R[1]:
                R[1] = R[1]+1
            if S[i][2]-1 < R[1]:
                R[1] = R[1]-1
        elif R[0] == S[i][1]-1: # x값이 같으면 y값만 이동
            if S[i][2]-1 > R[1]:
                R[1] = R[1]+1
            if S[i][2]-1 < R[1]:
                R[1] = R[1]-1
        elif R[1] == S[i][2]-1:
            if S[i][1]-1 > R[0]:
                R[0] = R[0]+1
            if S[i][1]-1 < R[0]:
                R[0] = R[0]-1
        if R[0] == S[i][1]-1 and R[1] == S[i][2]-1: # 충돌 발생
            S[i][4] += C
            S[i][3] = 2
            back_r, back_c = (R[0]-before_R[0]), (R[1]-before_R[1]) # 루돌프가 온 방향
            moved_r, moved_c = S[i][1]-1 + back_r*C, S[i][2]-1 + back_c*C # *C
            if moved_r > N-1 or moved_r < 0 or moved_c > N-1 or moved_c < 0: # out of range 발생
                arr[S[i][2]-1][S[i][1]-1] = 0
                S[i][3] = -1
            elif arr[moved_c][moved_r] == 1: # C만큼 날라간 곳에 산타 있으면 연쇄 이동
                S = move_chain(moved_r, moved_c)
                S[i][1] += back_r*C
                S[i][2] += back_c*C
            else:
                S[i][1] += back_r*C
                S[i][2] += back_c*C
    else: # shortest_index가 두개이상 -> r, c 우선순위
        r_arr = [0]
        c_arr = [0]
        idx_arr = []
        for idx in shortest_index:
            if max(r_arr) < S[idx][2]:
                idx_arr = []
                idx_arr.append(idx)
                r_arr.append(S[idx][2])
            elif S[idx][2] == max(r_arr):
                idx_arr.append(idx)
        if len(idx_arr) > 1:
            ans=[]
            if S[idx_arr[0]][1] < S[idx_arr[1]][1]:
                ans.append(idx_arr[1])
            else:
                ans.append(idx_arr[0])
            idx_arr = ans
        if len(idx_arr) == 1:
            # 기존 알고리즘
            i=idx_arr[0]
            if R[0] != S[i][1]-1 and R[1] != S[i][2]-1: # 대각선인 경우
                if S[i][1]-1 > R[0]:
                    R[0] = R[0]+1
                if S[i][1]-1 < R[0]:
                    R[0] = R[0]-1
                if S[i][2]-1 > R[1]:
                    R[1] = R[1]+1
                if S[i][2]-1 < R[1]:
                    R[1] = R[1]-1
            elif R[0] == S[i][1]-1: # x값이 같으면 y값만 이동
                if S[i][2]-1 > R[1]:
                    R[1] = R[1]+1
                if S[i][2]-1 < R[1]:
                    R[1] = R[1]-1
            elif R[1] == S[i][2]-1:
                if S[i][1]-1 > R[0]:
                    R[0] = R[0]+1
                if S[i][1]-1 < R[0]:
                    R[0] = R[0]-1
            if R[0] == S[i][1]-1 and R[1] == S[i][2]-1: # 충돌 발생
                S[i][4] += C
                S[i][3] = 2
                back_r, back_c = (R[0]-before_R[0]), (R[1]-before_R[1]) # 루돌프가 온 방향
                moved_r, moved_c = S[i][1]-1 + back_r*C, S[i][2]-1 + back_c*C # *C
                if moved_r > N-1 or moved_r < 0 or moved_c > N-1 or moved_c < 0: # out of range 발생
                    arr[S[i][2]-1][S[i][1]-1] = 0
                    S[i][3] = -1
                elif arr[moved_c][moved_r] == 1: # C만큼 날라간 곳에 산타 있으면 연쇄 이동
                    S = move_chain(moved_r, moved_c)
                    S[i][1] += back_r*C
                    S[i][2] += back_c*C
                else:
                    S[i][1] += back_r*C
                    S[i][2] += back_c*C
    arr[before_R[1]][before_R[0]] = 0
    for i in range(P):
        if S[i][3] != -1:
            arr[S[i][2]-1][S[i][1]-1] = 1
    arr[R[1]][R[0]] = 2
    return R, S, arr

def move_S_and_checkCollision(R, S, shortest_index, D):
    # !!!!!!!!!!!!!!!!!!!! 재귀함수는 return이 있어야 함.
    def move_chain(a,b): # a,b = moved_c, moved_r (3, 3) / back_r, back_c = (1, 0)
        if a+back_r<0 or a+back_r>N-1 or b+back_c<0 or b+back_c>N-1: # 밀려나간게 게임판 밖이면
            for i in range(P):
                if S[i][1]-1 == a and S[i][2]-1 == b: # 기존에 있던 밀려난 놈을 찾아서
                    S[i][3] = -1 # 죽었다고 표시
            return S
        elif arr[b+back_c][a+back_r] != 1: # 밀려나간게 게임판 안이고 산타가 없으면 해당 위치로 산타 옮김
            for i in range(P):
                if S[i][1]-1 == a and S[i][2]-1 == b: # 기존에 있던 밀려난 놈 찾음
                    S[i][1] += back_r
                    S[i][2] += back_c 
            return S
        elif arr[b+back_c][a+back_r] == 1: # 밀려나갔는데 또 산타있으면 재귀
            print("move S에서 또 재귀 발생")
            print("arr ", arr)
            print("a, b, back_r, back_c ", a, b, back_r, back_c)
            move_chain(a+back_r, b+back_c)
            for i in range(P):
                if S[i][1]-1 == a and S[i][2]-1 == b: # 기존에 있던 밀려난 놈을 찾아서
                    S[i][1] += back_r
                    S[i][2] += back_c
            return S
            

    # before_S = S.copy() << 틀렸음! # 중요 !!!!!! 리스트는 mutable, 따라서 list를 [:]로 copy 후 할당해야 안변함. 안그러면 포인터처럼 같은 주소를 참조.
    # 더 중요!!!!!!!!! 이 케이스의 경우, S가 list 안에 list가 있기 때문에 이렇게 하면 배열 자체는 다르지만 내부 요소가 똑같음.
    # 따라서 deep copy를 수행해야 함.
    before_S = [row[:] for row in S] # !!!!!!!

    for i in range(P):
        if S[i][3] == -1:
            continue
        elif S[i][3] == 0: # state가 0이면 sante move
            dist=[(R[0]-S[i][1]+1)**2 + (R[1]-S[i][2]+1)**2]
            direction=[0, 0]
            for di, dj in ((-1,0),(0,1),(1,0),(0,-1)): # 좌 하 우 상 순서로 세팅 후 for 문으로
                if S[i][1]+di>N or S[i][1]+di<=0 or S[i][2]+dj>N or S[i][2]+dj<=0:
                    continue
                mov_r = S[i][1]+di
                mov_c = S[i][2]+dj
                if arr[mov_c-1][mov_r-1] == 1:
                    continue
                dist_i = (R[0]-S[i][1]-di+1)**2 + (R[1]-S[i][2]-dj+1)**2
                if min(dist)>=dist_i:
                    dist.append(dist_i)
                    direction = [di, dj] # 마지막 남는 놈
            mov_r = S[i][1]+direction[0]
            mov_c = S[i][2]+direction[1]
            if arr[mov_c-1][mov_r-1] == 1:
                continue
            S[i][1] = mov_r
            S[i][2] = mov_c
        elif S[i][3] > 0: # state가 2이상 (충돌로 인한 기절)인 경우 state 감소
            S[i][3] -= 1
            continue
       
        if R[0] == S[i][1]-1 and R[1] == S[i][2]-1: # 충돌 발생
            S[i][4] += D
            S[i][3] = 1
            back_r, back_c = (before_S[i][1]-S[i][1]), (before_S[i][2]-S[i][2]) # 산타가 온 방향
            moved_r, moved_c = S[i][1]-1 + (back_r*D), S[i][2]-1 + (back_c*D) # *C
            if (moved_r==before_S[i][1]-1) and (moved_c==before_S[i][2]-1):
                continue
            if moved_r > N-1 or moved_r < 0 or moved_c > N-1 or moved_c < 0: # out of range 발생
                arr[S[i][2]-1][S[i][1]-1] = 0
                S[i][3] = -1
            elif arr[moved_c][moved_r] == 1: # C만큼 날라간 곳에 산타 있으면 연쇄 이동
                S = move_chain(moved_r, moved_c)
                S[i][1] += back_r*D
                S[i][2] += back_c*D
            else:
                S[i][1] += back_r*D
                S[i][2] += back_c*D
        arr[before_S[i][2]-1][before_S[i][1]-1] = 0
        for i in range(P):
            if S[i][3] != -1:
                arr[S[i][2]-1][S[i][1]-1] = 1
        arr[R[1]][R[0]]=2

    # print('R', R)
    # print('after move S, arr ', arr)
    # print('S ', S)
    # print('before S', before_S)

    return R, S, arr

R = posi_R(arr) # [Rr, Rc] (-1씩 된 좌표)
S = posi_S(arr) # [1,1,3,0,0], [2,3,5,0,0], [3,5,1,0,0], [4,4,4,0,0] / arr = ([0 0 0 0 1], ...)
short_s = shortest_S(R, S) # [0, 1, 2]
for i in range(M):
    R, S, arr = move_R_and_checkCollision(R, S, short_s, C)
    short_s = shortest_S(R, S)
    R, S, arr = move_S_and_checkCollision(R, S, short_s, D)
    short_s = shortest_S(R, S)
    for j in range(P):
        if S[j][3] != -1: # 탈락하지 않은 산타 1점 추가
            S[j][4] += 1
    
for j in range(P):
    print(S[j][4], end=' ')
print('\n')



# 여기까지 3h 55m, GG
# 미구현요소 : move_S_andcheckcollision
# 
# 패착 : lst a = b로 const하게 박아두고 history로 쓰려했는데, 리스트는 mutable이라 b가 바뀌면 a가 자동으로 계속 바뀌어서
# 디버깅하는데 오래 걸림. 또한 move_S_checkcollision 구현하면서 Santa array인 S와 state로 기절일 땐 pass하려했는데, 
# santa가 게임판에서 밀려나 없어졌을 때 S의 index와 state의 index를 동일하게 하는걸 못해서 헤맸음.
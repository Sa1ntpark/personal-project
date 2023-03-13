import pygame
import numpy as np

pygame.init() #초기화(반드시 필요)

#화면 크기 설정
screen_width =800 # 가로크기
screen_height=800 # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("BADOOK") #게임이름



#이미지 불러오기
badook = pygame.image.load(r"C:\Users\dlstj\OneDrive\바탕 화면\WorldBest_Zollaman-Sa1ntpark-patch-1\WorldBest_Zollaman-Sa1ntpark-patch-1\badook\image\badook.png")
badook_size = badook.get_rect().size
badook_width = badook_size[0]
badook_height = badook_size[1]

black = pygame.image.load(r"C:\Users\dlstj\OneDrive\바탕 화면\WorldBest_Zollaman-Sa1ntpark-patch-1\WorldBest_Zollaman-Sa1ntpark-patch-1\badook\image\blackdol.png")
white = pygame.image.load(r"C:\Users\dlstj\OneDrive\바탕 화면\WorldBest_Zollaman-Sa1ntpark-patch-1\WorldBest_Zollaman-Sa1ntpark-patch-1\badook\image\whitedol.png")
dol_size = black.get_rect().size
dol_width = dol_size[0]
dol_height = dol_size[1]



# 바둑판 좌표
#matrix= [  [좌표 x, 좌표 y, 픽셀 좌표 x, 픽셀 좌표 y, 돌 상태, 득점판단변수, 돌 놓은 순서]   ]
#돌상태 = 0 : 빈 상태
#       = 1 : 흰돌
#       = 2 : 검은돌 
a = []
for i in range(19):
    a.append(25.098 + i*(41.568))
matrix = []
for y in range(19):
    for x in range(19):
        matrix.append([x,y,a[x],a[y],0,0,0])

        
#score
global white_score
global black_score
white_score = 0
black_score = 0
#
click_x = 0
click_y = 0

#돌 놓은 순서
dol_order = 0

#돌 상태
# 1 = 흰
# 2 = 검
dol_state = 2


#font
game_font = pygame.font.Font(None, 30)

#delete
delete1 = []
delete2 = []
delete3 = []
delete4 = []

def deleteFunc1(n):
    if n[5] == 1:
        delete1.append(1)
    if n[5] == 2:
        delete2.append(1)
    if n[5] == 3:
        delete3.append(1)
    if n[5] == 4:
        delete4.append(1)

def deleteFunc0(n):
    if n[5] == 1:
        delete1.append(0)
    if n[5] == 2:
        delete2.append(0)
    if n[5] == 3:
        delete3.append(0)
    if n[5] == 4:
        delete4.append(0)

def Clear():
    global white_score
    global black_score
    score = 0
    
    a = 1
    for i in delete1:
        a *= i
    if a == 1:
        for m in matrix:
            if m[5] == 1:
                m[4] = 0
                score += 1

    a = 1
    for i in delete2:
        a *= i
    if a == 1:
        for m in matrix:
            if m[5] == 2:
                m[4] = 0
                score += 1

    a = 1
    for i in delete3:
        a *= i
    if a == 1:
        for m in matrix:
            if m[5] == 3:
                m[4] = 0
                score += 1


    a = 1
    for i in delete4:
        a *= i
    if a == 1:
        for m in matrix:
            if m[5] == 4:
                m[4] = 0
                score += 1

    if dol_state == 1:
        white_score += score
    else:
        black_score += score

def carryfunc(delete,n,m):
    if m[5] != n[5]:
        if m[5] == 1:
            for i in delete1:
                delete.append(i)
            delete1.clear()
        elif m[5] == 2:
            for i in delete2:
                delete.append(i)
            delete2.clear()
        elif m[5] == 3:
            for i in delete3:
                delete.append(i)
            delete3.clear()
        elif m[5] == 4:
            for i in delete4:
                delete.append(i)
            delete4.clear()



def carrying(n,m):
    if n[5] == 1:
        carryfunc(delete1,n,m)
    elif n[5] == 2:
        carryfunc(delete2,n,m)
    elif n[5] == 3:
        carryfunc(delete3,n,m)
    elif n[5] == 4:
        carryfunc(delete4,n,m)


    

#퍼질까?
def spread(x_arr,y_arr,dol_state):
    # x_arr, y_arr 위치의 돌이 dol_state랑 같을 때 // 맨처음 동작
    for m in matrix:
        if m[0] == x_arr and m[1] == y_arr and m[4] == dol_state:
            for n in matrix: 
                if n[0] == x_arr+1 and n[1] == y_arr: # 오른쪽
                    if n[4] != dol_state and n[4] != 0 and n[5] == 0:
                        n[5] = 1
                        spread(x_arr + 1, y_arr, dol_state)

                if n[0] == x_arr-1 and n[1] == y_arr: # 왼쪽
                    if n[4] != dol_state and n[4] != 0 and n[5] == 0:
                        n[5] = 2
                        spread(x_arr - 1, y_arr, dol_state)

                if n[0] == x_arr and n[1] == y_arr + 1: # 아래
                    if n[4] != dol_state and n[4] != 0 and n[5] == 0:
                        n[5] = 3
                        spread(x_arr, y_arr + 1, dol_state)

                if n[0] == x_arr and n[1] == y_arr-1: # 위
                    if n[4] != dol_state and n[4] != 0 and n[5] == 0:
                        n[5] = 4
                        spread(x_arr, y_arr - 1, dol_state)


    # x_arr, y_arr 위치의 돌이 dol_state랑 다를 때 
    for n in matrix:
        if n[0] == x_arr and n[1] == y_arr and n[4] != dol_state:
            for m in matrix:
                if m[0] == x_arr+1 and m[1] == y_arr: #오른쪽 퍼지기

                    if m[5] != n[5] and m[5] != 0:
                        for i in matrix:
                            if i[5] == m[5]:
                                i[5] = n[5]
                        carrying(n,m)

                    elif m[4] != dol_state and m[4] != 0 and m[5] == 0: 
                        m[5] = n[5]
                        spread(x_arr+1, y_arr, dol_state)
                    elif m[4] == dol_state: 
                        deleteFunc1(n)
                    elif m[4] == 0:
                        deleteFunc0(n)

            


                if m[0] == x_arr-1 and m[1] == y_arr: #왼쪽 퍼지기 

                    if m[5] != n[5] and m[5] != 0:
                        for i in matrix:
                            if i[5] == m[5]:
                                i[5] = n[5]
                        carrying(n,m)

                    if m[4] != dol_state and m[4] != 0 and m[5] == 0: 
                        m[5] = n[5]
                        spread(x_arr-1, y_arr, dol_state)
                    elif m[4] == dol_state: 
                        deleteFunc1(n)
                    elif m[4] == 0:
                        deleteFunc0(n)

            


                if m[0] == x_arr and m[1] == y_arr+1: #아래 퍼지기

                    if m[5] != n[5] and m[5] != 0:
                        for i in matrix:
                            if i[5] == m[5]:
                                i[5] = n[5]
                        carrying(n,m)

                    if m[4] != dol_state and m[4] != 0 and m[5] == 0:
                        m[5] = n[5]
                        spread(x_arr, y_arr+1, dol_state)
                    elif m[4] == dol_state: 
                        deleteFunc1(n)
                    elif m[4] == 0:
                        deleteFunc0(n)
                
            

                if m[0] == x_arr and m[1] == y_arr-1: #위 퍼지기

                    if m[5] != n[5] and m[5] != 0:
                        for i in matrix:
                            if i[5] == m[5]:
                                i[5] = n[5]
                        carrying(n,m)

                    if m[4] != dol_state and m[4] != 0 and m[5] == 0: 
                        m[5] = n[5]
                        spread(x_arr, y_arr-1, dol_state)
                    elif m[4] == dol_state: 
                        deleteFunc1(n)
                    elif m[4] == 0:
                        deleteFunc0(n)

            

def decision(x_arr,y_arr,dol_state):

    spread(x_arr,y_arr,dol_state)
    Clear()
                
    for m in matrix:
        m[5] = 0

    delete1.clear()
    delete2.clear()
    delete3.clear()
    delete4.clear()

            


#이벤트 루프
running =True #게임이 진행중인가?
while running:
    for event in pygame.event.get():#무조건 작성해야 하는 부분  #어떤 이벤트가 발생하는가
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하였는가?
            running= False
            
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_x = event.pos[0]
            click_y = event.pos[1]
            
            for m in matrix:
                if np.power(((m[2]-click_x)**2 + (m[3]-click_y)**2), 0.5) <=20.784 and m[4] == 0:
                    m[4] = dol_state
                    x_arr = m[0]
                    y_arr = m[1]

                    dol_order += 1
                    m[6] = dol_order
                    

                    decision(x_arr,y_arr,dol_state)

                    if dol_state == 1:
                        dol_state = 2
                    elif dol_state == 2:
                        dol_state = 1
                    
                 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #ctrl+z
                for m in matrix:
                    if m[6] == dol_order:
                        m[4] = 0
                dol_order -= 1
                if dol_state == 1:
                    dol_state = 2
                elif dol_state == 2:
                    dol_state = 1
           # if event.key == pygame.K_RIGHT: #ctrl+ shift + z


                        
        

   
    #screen.fill((0,0,255)) # rgb 배경채우기
    screen.blit(badook,(0,0)) #배경그리기
    
    
    white_score_text = game_font.render(str(white_score), True, (255,255,255))
    black_score_text = game_font.render(str(black_score), True, (0,0,0))
    
    white_text = game_font.render("WHITE",True, (255,255,255))
    black_text = game_font.render("BLACK",True, (0,0,0))
    
    
    if dol_state == 1:
        screen.blit(white_text,(365,5))
    elif dol_state == 2:
        screen.blit(black_text,(365,5))

    screen.blit(white_score_text,(75,5))
    screen.blit(black_score_text,(700,5))

    for m in matrix:
        if m[4] == 1:
            screen.blit(white,(m[2] - dol_width/2 ,m[3]-dol_height/2))
        if m[4] == 2:
            screen.blit(black,(m[2] - dol_width/2 ,m[3]-dol_height/2))
    
    
    pygame.display.update() # 게임화면 다시 그리기!

# pygame 종료
pygame.quit()
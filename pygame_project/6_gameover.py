# 1. 모든 공을 없애면 게임 종료 => 성공
# 2. 캐릭터는 공에 닿으면 게임 종료 => 실패
# 3. 시간 제한 99 초 초과 시 게임 종료 => 실패

import os
import pygame
######################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 640  # 가로 크기
screen_height = 480 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("*** Pang pang ***")

# FPS 초당 프레임 수
clock = pygame.time.Clock()
######################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)    # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images")   # 현재 폴더 위치에 images 폴더 위치를 더해 이미지가 있는 위치 반환

# 배경화면 만들기
background = pygame.image.load(os.path.join(image_path, "t_bg.png"))  # image_path 경로의 background.png 파일을 불러오기

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]    # 스테이지의 높이 위에 캐릭터를 두기 위해 사용

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "robot.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동 방향
character_to_x_LEFT = 0
character_to_x_RIGHT = 0

# 캐릭터 이동 속도
character_speed = 5

# 무기아이템 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

# 공 만들기 (4개 크기에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

# 공 크기에 따른 최초 스피드 => x좌표는 변경x, y좌표만 상하위치가 변경됨
ball_speed_y = [-18, -15, -12, -9]  # 배열에 담긴 4개 공의 각각 index 0, 1, 2, 3에 해당하는 값

# 공 여러개를 담을 배열 변수 선언
balls = []

# 게임 최초 시작 시 발생하는 가장 큰 공 1개 추가
# 딕셔너리이므로 중괄호 {}, 값을 사용
balls.append({
    "pos_x" : 50,   # 스크린 좌측 상단 기준으로 x좌표
    "pos_y" : 50,    # 스크린 좌측 상단 기준으로 y좌표
    "img_idx" : 0,  # 공의 이미지 인덱스
    "to_x" : 3, # 공의 x축 이동방향. -3 => 왼쪽으로 / 3 => 오른쪽으로 이동
    "to_y" : -6,    # 공의 y축 이동방향. 맨처음 약간 올라갔다가 내려가도록 설정
    "init_spd_y" : ball_speed_y[0]  # y 최초 속도
})

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# font 정의
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks()   # 시작 시간 정의

# 게임 종료 메시지
# Time Over : 실패. 시간 초과
# Mission Complete : 성공
# Game Over : 실패. 캐릭터가 공에 맞음
game_result = "Game Over!"

running = True
while running:
    dt = clock.tick(30)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                character_to_x_LEFT -= character_speed
            elif event.key == pygame.K_RIGHT:   # 캐릭터를 오른쪽으로
                character_to_x_RIGHT += character_speed
            elif event.key == pygame.K_SPACE:   # 무기아이템 발사
                # pass  # 중간 확인
                # weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_x_pos = character_x_pos + (weapon_width / 2)
                weapon_y_pos = character_y_pos  # 플레이어의 머리 위쪽에서 발사되므로
                weapons.append([weapon_x_pos, weapon_y_pos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x_LEFT + character_to_x_RIGHT

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    # w[0] : x좌표 / w[1] : y좌표
    # ex> x = 100, y = 200 => x좌표는 그대로, y좌표만 줄어듦. 180, 160, 140, ...
    # ex> x = 500, y = 200 => x좌표는 그대로, y좌표만 줄어듦. 180, 160, 140, ...
    # 연속적으로 무기를 append하는 배열 weapons에서 하나씩 꺼내오는 w를 통해
    # 0번째 인덱스와 1번째 인덱스 - 무기 속도를 리스트에 한번 더 감싼다.
    # 위의 두 인덱스가 담긴 리스트를 weapons에 담아 반환
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]    # 무기 위치를 위로 올림

    # 천장에 닿은 무기 없애기
    # y좌표가 천장에 닿으면 사라지도록, 스크린 위로 벗어난다면? 안보여야하므로
    # y좌표가 천장에 닿기 전까지의 위치만 배열에 담는다.
    # 즉, y좌표가 천장에 닿으면 무기가 바로 사라지도록 설정
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls): # balls에서 인덱스와 값을 불러온다.
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 공이 스크린 밖으로 벗어나지 않도록 경계값 설정
        # 경계선에 닿은 경우, 반대방향으로 튕기도록 설정
        # 가로벽에 닿았을 때 공 이동 위치 변경(튕겨 나오는 효과)
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1    # switch => 이동방향 조정

        # 공 세로 위치
        # 스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:   # 그 외의 모든 경우에는 속도를 증가
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. 충돌 처리

    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    # 모든 공들에 대해 캐릭터와의 충돌이 있었는지 비교해야하므로 공 배열 불러옴
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx   # 해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx   # 해당 공 없애기 위한 값 설정

                # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                if ball_img_idx < 3:
                    # 현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 충돌 후 나눠진 공 정보
                    # 현재보다 더 작은 공을 담아야하므로 공이 담긴 배열에서 다음 순서 인덱스를 불러와 담는다.
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1,   # 공의 이미지 인덱스
                        "to_x" : -3, # 공의 x축 이동방향. -3 => 왼쪽으로 / 3 => 오른쪽으로 이동
                        "to_y" : -6,    # 공의 y축 이동방향. 맨처음 약간 올라갔다가 내려가도록 설정
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]  # y 최초 속도
                    })

                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1,   # 공의 이미지 인덱스
                        "to_x" : 3, # 공의 x축 이동방향. -3 => 왼쪽으로 / 3 => 오른쪽으로 이동
                        "to_y" : -6,    # 공의 y축 이동방향. 맨처음 약간 올라갔다가 내려가도록 설정
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]  # y 최초 속도
                    })
                break   # 충돌 시 탈출. 공, 무기 하나씩 없어지도록 설정할 것이므로

        else:   # 계속 게임을 진행
            continue    # 안쪽 for문 조건이 맞지 않으면 continue. 바깥 for문 계속 수행함
        break   # 안쪽 for문에서 break를 만나면 여기로 진입 가능. 2중 루프문을 한번에 탈출가능

#    for 바깥조건:
#        바깥동작
#        for 안쪽조건:
#            안쪽동작
#            if 충돌하면:
#                break
#        else:
#            continue
#        break

    # 충돌된 공 or 무기 없애기
    if ball_to_remove > -1: # 배열 인덱스는 0부터 시작하므로 음수(초기값 -1)보다 큰 수는 충돌한 경우에만 발생
        del balls[ball_to_remove]   # 충돌한 공 삭제
        ball_to_remove = -1 # 삭제후 새로 생성될 공 초기화

    if  weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앤 경우 게임 종료 => 성공
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    # 5. 화면에 그리기
    screen.blit(background, (0, 0)) # 배경
    # 무기 => 플레이어보다 먼저 그려야 플레이어 위로 겹치지 않는다.
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))   # 무대
    screen.blit(character, (character_x_pos, character_y_pos))  # 플레이어

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000   # ms => s = (현재 시간 - 시작 시간) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255)) # 흰색
    screen.blit(timer, (10, 10))

    # 시간 초과한 경우
    if total_time - elapsed_time < 0:
        game_result = "Time Over!"
        running = False

    pygame.display.update()

# 게임 오버 메시지
msg = game_font.render(game_result, True, (255, 255, 0))    # 노란색
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 2초 대기 후 게임창 닫기
pygame.time.delay(2000)

pygame.quit()
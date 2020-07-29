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
background = pygame.image.load(os.path.join(image_path, "background.png"))  # image_path 경로의 background.png 파일을 불러오기

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]    # 스테이지의 높이 위에 캐릭터를 두기 위해 사용

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동 방향
character_to_x = 0

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

running = True
while running:
    dt = clock.tick(30)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:   # 캐릭터를 오른쪽으로
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:   # 무기아이템 발사
                # pass  # 중간 확인
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos  # 플레이어의 머리 위쪽에서 발사되므로
                weapons.append([weapon_x_pos, weapon_y_pos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

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

    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(background, (0, 0)) # 배경
    # 무기 => 플레이어보다 먼저 그려야 플레이어 위로 겹치지 않는다.
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    screen.blit(stage, (0, screen_height - stage_height))   # 무대
    screen.blit(character, (character_x_pos, character_y_pos))  # 플레이어

    pygame.display.update()

pygame.quit()
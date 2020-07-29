import pygame

pygame.init()   # 초기화 (반드시 필요)

screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Game A")

# FPS 초당 프레임 수
clock = pygame.time.Clock()

background = pygame.image.load("C:/Python/pygame_basic/background.png")

# 캐릭터(스프라이트) 불러오기
character = pygame.image.load("C:/Python/pygame_basic/character.png")
character_size = character.get_rect().size  # 이미지 크기 구해옴
character_width = character_size[0] # 캐릭터 가로 크기
character_height = character_size[1]    # 캐릭터 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2)    # 화면 가로 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height  # 화면 세로 크기 가장 아래에 해당하는 곳에 위치

# 이동할 좌표
to_x = 0
to_y = 0

# 이동 속도
character_speed = 0.6

# 적(enemy) 캐릭터
enemy = pygame.image.load("C:/Python/pygame_basic/enemy.png")
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = (screen_width / 2) - (enemy_width / 2)
enemy_y_pos = (screen_height / 2) - (enemy_height / 2)

# 폰트 정의
game_font = pygame.font.Font(None, 40)  # 폰트 객체 생성 (폰트, 크기)

# 총 시간
total_time = 10

# 시작 시간 정보
start_ticks = pygame.time.get_ticks()   # 현재 tick을 받아옴

running = True
while running:
    dt = clock.tick(60) # 게임화면의 초당 프레임 수를 설정

    # print("fps : " + str(clock.get_fps()))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:    # 어떤 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT:  # 캐릭터를 왼쪽으로
                to_x -= character_speed   # to_x = to_x - 10
            elif event.key == pygame.K_RIGHT:   # 캐릭터를 오른쪽으로
                to_x += character_speed
            elif event.key == pygame.K_UP:  # 캐릭터를 위로
                to_y -= character_speed
            elif event.key == pygame.K_DOWN:    # 캐릭터를 아래로
                to_y += character_speed

        if event.type == pygame.KEYUP:  # 방향키를 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    character_x_pos += to_x * dt # 캐릭터 x좌표 / 속도조절을 위해 델타값을 곱함
    character_y_pos += to_y * dt # 캐릭터 y좌표

    # 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 세로 경계값 처리
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    # 충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos   # 초기값 대신 업데이트된 실제 좌표값으로 그려줌
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # 충돌 체크
    if character_rect.colliderect(enemy_rect): # 사각형 기준으로 충돌이 있었는지 확인하는 함수를 사용하여 적과 충돌이 있었는지 체크
        print("충돌! \n게임을 종료합니다.")
        running = False

    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    # 타이머 삽입
    # 경과 시간 계산 = (현재 시각 - 시작 시각) / 1000
    # 경과 시간(ms)을 1000으로 나누어 초(s) 단위로 표시
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    # 출력할 시간, True, 폰트 색상
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 시간이 0 이하일 경우 게임 종료
    if total_time - elapsed_time <= 0:
        print("***\t타임아웃\t***")
        running = False

    pygame.display.update()

# 게임 종료 전 2초 정도 대기 (ms)
pygame.time.delay(2000)

pygame.quit()
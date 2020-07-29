import pygame

pygame.init()   # 초기화 (반드시 필요)

screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Game A")

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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:    # 어떤 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT:  # 캐릭터를 왼쪽으로
                to_x -= 5   # to_x = to_x - 5
            elif event.key == pygame.K_RIGHT:   # 캐릭터를 오른쪽으로
                to_x += 5
            elif event.key == pygame.K_UP:  # 캐릭터를 위로
                to_y -= 5
            elif event.key == pygame.K_DOWN:    # 캐릭터를 아래로
                to_y += 5

        if event.type == pygame.KEYUP:  # 방향키를 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    character_x_pos += to_x # 캐릭터 x좌표
    character_y_pos += to_y # 캐릭터 y좌표

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

    screen.blit(background, (0, 0))

    screen.blit(character, (character_x_pos, character_y_pos))  # 캐릭터 그리기

    pygame.display.update()

pygame.quit()
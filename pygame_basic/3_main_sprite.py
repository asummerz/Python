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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    screen.blit(character, (character_x_pos, character_y_pos))  # 캐릭터 그리기

    pygame.display.update()

pygame.quit()
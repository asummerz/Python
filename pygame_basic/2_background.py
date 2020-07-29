import pygame

pygame.init()   # 초기화 (반드시 필요)

screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Game A")

# 배경 이미지 불러오기
background = pygame.image.load("C:/Python/pygame_basic/background.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # screen.fill((0, 0, 255))
    screen.blit(background, (0, 0)) # 배경 그리기

    pygame.display.update() # 게임 화면 다시 그리기

pygame.quit()
# Quiz) 하늘에서 떨어지는 꽃 피하기 게임을 만드시오.

# [게임 조건]
# 1. 캐릭터는 화면 가장 아래에 위치, 좌우로만 이동 가능
# 2. 꽃은 화면 가장 위에서 떨어짐. x 좌표는 매번 랜덤으로 설정
# 3. 캐릭터가 꽃을 피하면 다음 꽃이 다시 떨어짐
# 4. 캐릭터가 꽃과 충돌하면 게임 종료
# 5. FPS 는 30 으로 고정

# [게임 이미지]
# 1. 배경 : 640 * 480 (세로 가로) - background.png
# 2. 캐릭터 : 70 * 70 - character.png
# 3. 꽃 : 70 * 70 - enemy.png
######################################################
import random
import pygame
######################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 480  # 가로 크기
screen_height = 640 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("*** Avoid the flowers ***")

# FPS 초당 프레임 수
clock = pygame.time.Clock()
######################################################
# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)
# 배경화면 이미지
background_01 = pygame.image.load("C:/Python/pygame_basic/background_01.png")

# 캐릭터 이미지
char_01 = pygame.image.load("C:/Python/pygame_basic/char_01.png")
char_01_size = char_01.get_rect().size
char_01_width = char_01_size[0]
char_01_height = char_01_size[1]
char_01_xPos = (screen_width / 2) - (char_01_width / 2)
char_01_yPos = screen_height - char_01_height

# 꽃 이미지
flower_01 = pygame.image.load("C:/Python/pygame_basic/flower_01.png")
flower_01_size = flower_01.get_rect().size
flower_01_width = flower_01_size[0]
flower_01_height = flower_01_size[1]
flower_01_xPos = random.randint(0, screen_width - flower_01_width)
flower_01_yPos = 0

flower_02 = pygame.image.load("C:/Python/pygame_basic/flower_02.png")
flower_02_size = flower_02.get_rect().size
flower_02_width = flower_02_size[0]
flower_02_height = flower_02_size[1]
flower_02_xPos = random.randint(0, screen_width - flower_02_width)
flower_02_yPos = 0

thunder = pygame.image.load("C:/Python/pygame_basic/thunder.png")
thunder_size = thunder.get_rect().size
thunder_width = thunder_size[0]
thunder_height = thunder_size[1]
thunder_xPos = random.randint(0, screen_width - thunder_width)
thunder_yPos = 0

# 이동 위치
toX = 0
# toY = 0

# 속도
char_01_speed = 10  # 캐릭터 속도
flower_01_speed = 8 # 꽃 속도
flower_02_speed = 10 # 꽃 속도
thunder_speed = 18  # 번개 속도

# 폰트
font = pygame.font.Font(None, 50)
font_str = pygame.font.Font(None, 35)

# 시간
totalTime = 10  # 총 시간
startTime = pygame.time.get_ticks() # 시작 시간

running = True
while running:
    dt = clock.tick(30)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 키보드를 눌렀을때 좌표 이동
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                toX -= char_01_speed
            if event.key == pygame.K_RIGHT:
                toX += char_01_speed
            # if event.key == pygame.KEYUP or event.type == pygame.KEYDOWN:
            #     toY = 0
        # 키보드를 누르지 않았을때 방향 변화 없도록 설정
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                toX = 0

    # 3. 게임 캐릭터 위치 정의
    char_01_xPos += toX
    # char_01_yPos += toY

    # 캐릭터 x 좌표 경계값 설정
    if char_01_xPos < 0:
        char_01_xPos = 0
    elif char_01_xPos > screen_width - char_01_width:
        char_01_xPos = screen_width - char_01_width

    flower_01_yPos += flower_01_speed
    flower_02_yPos += flower_02_speed
    thunder_yPos += thunder_speed

    if flower_01_yPos > screen_height:
        flower_01_yPos = 0
        flower_01_xPos = random.randint(0, screen_width - flower_01_width)

    if flower_02_yPos > screen_height:
        flower_02_yPos = 0
        flower_02_xPos = random.randint(0, screen_width - flower_02_width)

    if thunder_yPos > screen_height:
        thunder_yPos = 0
        thunder_xPos = random.randint(0, screen_width - thunder_width)

    # 4. 충돌 처리
    char_01_rect = char_01.get_rect()
    char_01_rect.left = char_01_xPos
    char_01_rect.top = char_01_yPos

    flower_01_rect = flower_01.get_rect()
    flower_01_rect.left = flower_01_xPos
    flower_01_rect.top = flower_01_yPos

    flower_02_rect = flower_02.get_rect()
    flower_02_rect.left = flower_02_xPos
    flower_02_rect.top = flower_02_yPos

    thunder_rect = thunder.get_rect()
    thunder_rect.left = thunder_xPos
    thunder_rect.top = thunder_yPos

    if char_01_rect.colliderect(flower_01_rect) or char_01_rect.colliderect(flower_02_rect) or char_01_rect.colliderect(thunder_rect):
        print("! 충돌 !")
        running = False

    # 5. 화면에 그리기
    screen.blit(background_01, (0, 0))
    screen.blit(char_01, (char_01_xPos, char_01_yPos))
    screen.blit(flower_01, (flower_01_xPos, flower_01_yPos))
    screen.blit(flower_02, (flower_02_xPos, flower_02_yPos))
    screen.blit(thunder, (thunder_xPos, thunder_yPos))
    
    elapsedTime = (pygame.time.get_ticks() - startTime) / 1000  # 경과된 시간
    timer = font.render(str(int(totalTime - elapsedTime)), True, (255, 255, 255))   # 타이머(카운트)
    timer_str = font_str.render('Time', True, (255, 255, 255))
    
    screen.blit(timer_str, (15, 22))
    screen.blit(timer, (80, 15))

    if totalTime - elapsedTime <= 0:
        print("*** Time Out ***\n다시 도전하세요 :D")
        running = False

    pygame.display.update()
pygame.time.delay(2000)
pygame.quit()
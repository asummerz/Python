import turtle

# 꼭지점 개수
point = 5

# 각 변의 길이
side = 200

# 1씩 증가되는 변의 개수를 담는 변수
i = 1

turtle.penup()
turtle.goto(-100, 20)
turtle.down()

# 루프문 안에서 별을 그린다.
while i <= point:
    # 변의 길이만큼 앞으로 이동하며 그린다.
    turtle.forward(side)
    # 360 / 5 = 72 → 72 * 2 = 144
    # 144 + 36 = 180    각 꼭짓점 내각이 36도이므로
    # 현재 앞을 본 상태에서 화살표의 방향을 144도만큼 오른쪽으로 돌린다.
    turtle.right((360 / point) * 2)
    # 앞으로 그릴 변의 개수를 1씩 증가시킨다.
    i += 1
# 별이 완성되면 종료한다.
turtle.done()

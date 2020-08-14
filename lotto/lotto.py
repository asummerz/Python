# 플레이어가 원하는 횟수만큼 번호를 랜덤으로 출력한다.
# 단, 숫자만 입력가능
import random

cnt = 0
check = '예', 'y'

while True:
    try:
        cnt = int(input("구매할 수량 : "))
        print("---------- * ---------- * ----------")
        break
    except ValueError:
        print("\n숫자만 입력하십시오.\n")

for i in range(cnt):
    myLotto = random.sample(range(1, 46), 6)
    myLotto.sort()
    print(myLotto)

print("---------- * ---------- * ----------")
# check = input("다시 구매하시겠습니까?(예/y 또는 아니오/n) : ")
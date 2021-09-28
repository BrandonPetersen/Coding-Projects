from cs50 import get_int
import sys

number = -1

while number < 0:
    number = get_int("Number: ")

digits = len(str(number))


if digits != 13 and digits != 15 and digits != 16:
    print("INVALID")
    sys.exit()

card = str(number)
sum1 = 0
product = 0

if digits % 2 == 0:
    for i in range(digits):
        num = int(card[i])
        if i % 2 == 0:
            product = num * 2
            if product > 9:
                sum1 += product // 10
                sum1 += product % 10
            else:
                sum1 += product
        else:
            sum1 += num
else:
    for i in range(digits):
        num = int(card[i])
        if i % 2 == 0:
            sum1 += num
        else:
            product = num * 2
            if product > 9:
                sum1 += product // 10
                sum1 += product % 10
            else:
                sum1 += product

if sum1 % 10 != 0:
    print("INVALID")
    sys.exit()
    
if int(card[0]) == 5 and 0 < int(card[1]) < 6:
    print("MASTERCARD")
elif int(card[0]) == 3 and (int(card[1]) == 4 or int(card[1]) == 7):
    print("AMEX")
elif int(card[0]) == 4:
    print("VISA")
else:
    print("INVALID")
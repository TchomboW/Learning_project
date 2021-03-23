import random

lotto_numbers = set()
sampleSize = 6
answerSize = 0
while answerSize < sampleSize:
    r = random.randint(1,49)
    if r not in lotto_numbers:
        answerSize += 1
        lotto_numbers.add(r)

print(lotto_numbers)
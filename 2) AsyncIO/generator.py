from typing import List


def fib(n: int) -> List[int]:
	numbers = []
	current, nxt = 0, 1
	while len(numbers) < n:
		current, nxt = nxt, current + nxt
		numbers.append(current)
	return numbers

# print(fib(10))


def fib():
	current, nxt = 0, 1
	while True:
		current, nxt = nxt, current + nxt
		yield current

result = fib()

# (above) it'll give generator object
# where 'current is 1'
# whilst all the code below will
# operate within 'while True' loop

for n in result:
	print(n, end=', ')
	if n > 1000:
		break

print()
print('Done')

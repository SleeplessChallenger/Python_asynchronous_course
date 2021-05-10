import time
import threading


def main():
	threads = [
		threading.Thread(target=greeter, args=('Michael', 5), daemon=True),
		threading.Thread(target=greeter, args=('Sarah', 2), daemon=True),
		threading.Thread(target=greeter, args=('George', 1), daemon=True),
		threading.Thread(target=greeter, args=('Tom', 4), daemon=True)
	]
	
	[t.start() for t in threads]

	print(2*2)

	[t.join(timeout=0.9) for t in threads]

	print('Done')


def greeter(name: str, times: int):
	for n in range(0, times):
		print(f'Hello, there {n} {name}')
		time.sleep(1)


if __name__ == '__main__':
	main()

import datetime
import multiprocessing
from threading import Thread
import math_func


def main():
	math_func.do_math(1)

	print(f'Doing math on {multiprocessing.cpu_count()}')

	processor_count = multiprocessing.cpu_count()
	threads = []

	for n in range(1, processor_count + 1):
		threads.append(Thread(target=math_func.do_math,
							  args=(3_000_000 * (n - 1) / processor_count,
							  	    3_000_000 * n / processor_count),
							  daemon=True))

	[t.start() for t in threads]
	t0 = datetime.datetime.now()
	
	[t.join() for t in threads]

	dt = datetime.datetime.now() - t0
	print(f"Done in {dt.total_seconds()} sec.")


if __name__ == '__main__':
	main()

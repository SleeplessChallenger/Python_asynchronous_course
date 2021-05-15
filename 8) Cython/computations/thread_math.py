import datetime
import math
import multiprocessing
from threading import Thread


# multithreading usually runs in 5 secs
def main():
	do_math(1)

	t0 = datetime.datetime.now()

	print(f'Doing math on {multiprocessing.cpu_count()}')

	processor_count = multiprocessing.cpu_count()
	threads = []

	for n in range(1, processor_count + 1):
		threads.append(Thread(target=do_math,
							  args=(30000000 * (n - 1) / processor_count,
							  	    30000000 * n / processor_count),
							  daemon=True))

	[t.start() for t in threads]
	[t.join() for t in threads]

	dt = datetime.datetime.now() - t0
	print(f"Done in {dt.total_seconds()} sec.")

# sync version runs in roughly 7 secs
def main_old():
	do_math(1)

	t0 = datetime.datetime.now()

	do_math(num=30000000)

	dt = datetime.datetime.now() - t0
	print(f"Done in {dt.total_seconds()} sec.")

def do_math(start=0, num=10):
	pos = start
	k_sq = 1000 * 1000
	while pos < num:
		pos += 1
		dist = math.sqrt((pos - k_sq) * 
						  (pos - k_sq))


if __name__ == '__main__':
	main()

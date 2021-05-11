import math
import multiprocessing
import datetime


def main():
	do_math(1)

	t0 = datetime.datetime.now()
	print(f'Doing math on {multiprocessing.cpu_count()}')

	pool = multiprocessing.Pool()
	processor_count = multiprocessing.cpu_count()

	for n in range(1, processor_count + 1):
		pool.apply_async(do_math,
						args=(30000000 * (n - 1) / processor_count,
							  30000000 * n / processor_count))

	pool.close()
	pool.join()

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

**Threads**

Arrows (image below) are processes (3 of them) and dots denote waiting period. Second and third processes kick off at some moment and then first thread waits for the second and third to be completed, after that we proceed

![Alt text](/ImageRepo/Threads_first.png?raw=true)


All above mentioned three threads are part of one process with same memory. 

AsyncIO **is cleaner and easier** than Threads. But asyncIO can be used if only we have libraries for the desired system (like the ones mentioned at the end of `AsyncIO` chapter) -> Threads is our option. 

**How threads work:** there is one thread which at some moment waits for response, this thread will give out (release) GIL while it waits for that I/O operation and second thread will take it and start doing another work.

Look at `hello_threads.py`. If program at below state, then after it has printed ‘Done’, the greeter thread continues its operation

```bash
def main():
	t = threading.Thread(target=greeter, args=('Michael', 5), daemon=True)
	t.start()
	print('Done')

def greeter(name: str, times: int):
	for n in range(0, times):
		print(f'Hello, there {n} {name}')
		time.sleep(1)
```

By default threads are known as **foreground threads (non-Daemon)**. If there is main thread and another one which was kicked off by first one, if first thread ends, then second will continue its execution:

<ins>‘Daemon’ and ‘non-Daemon’ threads</ins>

**First one** gets killed when the main program terminates. So, it’s a thread which we don’t need to care about in regard to shutting down it. **(daemon=True) WITHOT JOIN()**
```bash
def main():
	t = threading.Thread(target=greeter, args=('Michael', 5))
	t.start()

	print('Done')

def greeter(name: str, times: int):
	for n in range(0, times):
		print(f'Hello, there {n} {name}')
		time.sleep(1)
```

**Second one** is a thread which will make main program wait till it’s done and only then allow main program to terminate itself **WITHOUT JOIN()**

But if we’ve started some work, but need to do some other work? We add `.join()` which will make our main thread waits till another one is done and after that allows main to end (**even with daemon=True**). It can be used if Daemon Thread cannot be killed due to some reasons

From docs: JOIN
Wait until the thread terminates. This blocks the calling thread until the thread whose `.join()` method is called terminates – either normally or through an unhandled exception – or until the optional timeout occurs.

![Alt text](/ImageRepo/Threads_second.png?raw=true)

<h3>But how to work with multiple threads?</h3>
1. Create list comprehension of threads
2. Iterate over created list to start them
3. Iterate over created one to join them

**Timeout** puts time restriction.<br>
<ins><i>Stands for float representing the number of seconds to wait for the thread to become inactive. As join() always returns None, we must call isAlive() after **join()** to decide whether a timeout happened - if the thread is still alive, the **join()** call timed out.</i></ins>

We call `.is_alive()` on thread which we `.join()` with timeout. If thread is still alive -> do something, like terminate or stuff like that. If not `is_alive()` -> thread has done all the actions. Look at the code snippet below. Timeout < time to sleep => Dameon node (d in our case) won’t print ‘Exiting’ as the join was timed out, and the daemon thread is still alive and sleep. The main thread and t exited before the daemon thread wakes up from its five second sleep.
=> if one of the functions is daemon node (d in example below), then with timeout smaller than sleep and another node that is not daemon, our daemon node will terminate.

[Helpful link about threading](https://www.bogotobogo.com/python/Multithread/python_multithreading_Daemon_join_method_threads.php)

```bash
def n():
    logging.debug('Starting')
    logging.debug('Exiting')

def d():
    logging.debug('Starting')
    time.sleep(5)
    logging.debug('Exiting')

if __name__ == '__main__':

    t = threading.Thread(name='non-daemon', target=n)
    d = threading.Thread(name='daemon', target=d)
    d.setDaemon(True)

    d.start()
    t.start()

    d.join(3.0)
    print 'd.isAlive()', d.isAlive()
    t.join()
```

There are issue with terminating threads from, for example, terminal window.

1. `daemon=True` is an option to make termination smoother with Ctrl + C
2. Another way is to create separate thread which will observe client’s actions 

In `thread_prod.py` there is a concept of timeout, if after two last lines in main() func (can be considered as main thread) there is one of the daemon threads alive -> kill them.

The very loop is a pattern that can be applied to many cases. We simply ask whether there is one of the threads alive and then give them a small timeout to perform their operations 

However, we can unite threading with multiprocessing to try to achieve better results. See `thread_CPU_attempt.py` for details. But doing computational stuff will make multiple CPU-busy threads fight for resources and slow down CPU itself. GIL prevents interpreter from operating on more than one instruction at a time. Although, it makes computation a little bit faster, **multiprocessing & Cython** is better

![Alt text](/ImageRepo/Threads_third.png?raw=true)

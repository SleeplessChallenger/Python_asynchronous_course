**Multiprocessing**

GIL prevents python code from scaling across multiple threads. Of course, if that code calls something to the network/makes DB request,<br>
then it’ll release the GIL, but computationally one python interpreter instruction gets to run at a time.

On the image in the left side there are 3 threads, but only one is allowed to go due to GIL.
That’s why we kick off a bunch of processes where each process will have it’s own GIL, but they don’t interfere with each other as actually they’re various programs (== processes)

![Alt text](/ImageRepo/Multiprocessing_first.png?raw=true)

By default **multiprocessing** will use number of cores on the machine, but if you want to specify, then use `multiprocessing.Pool()` to do so.

<h4>Core concepts:</h4>

1. Create subprocesses with specifying how much you want in Pool
2. Start processes
3. At first `close()` == no more work is coming and then `join()`

![Alt text](/ImageRepo/Multiprocessing_second.png?raw=true)


But `multiprocessing_compute.py` doesn’t give back some tangible result and what if we want such?

Attach loop to list and then in the end iterate over list to `.get()` values from it. Look at `multiprocessing_return.py` for details.<br>
Also, look at the image for example (note: things that can be pickled in Python can be returned via multiprocessing.<br>
Such things are lot of, but not all in Python: created and passed in or returned from functions)


<ins><i>Below are notes regarding various functions in multiprocessing:</i></ins> <br>
- `Pool.apply` and `Pool.map` are blocking, meaning when you are calling them, you have to wait until the processes are finished.
- `Pool.apply_async` and `Pool.map_async` are asynchronous. You don’t wait for them to return the executed processes’ results to you, but instead a temporary<br>
result (AsyncResult) immediately. But when they do finish, you can call `get()`, `ready()` and `successful()` on AsyncResult.

![Alt text](/ImageRepo/Multiprocessing_third.png?raw=true)

<h3>Unifying multiprocessing and threading</h3>

**File:** `unify_thread_process.py`

Unifying different APIs. Before we did either threading or multiprocessing, but it’d be better if we could make<br>
same API does at first one and then another thing. Even better if API could figure out which one of the mentioned above to use

We can use <ins><i>concurrent.futures.thread/process</i></ins> to make interchangeable programs. 
```bash
  import multiprocessing
	p = multiprocessing.current_process()

	print(f"Getting title from {url.replace('https://', '')} "
		  f"PID: {p.pid} ProcName: {p.name}”)
```

Code above used in threading shows that there is the same thread number (p.pid) and same thread name (p.name)
```
	# 'submit' schedules a function to be executed
	# and returns a 'future object'
	# 'future object' encapsulates execution of
	# our function and allows to check on it
	# after it has been scheduled
```


Using context_manager with `PoolExecutor()` will assign all the work at first, then leave inner for-loop and start do all the things, then leave context_manager (after work has been done)

Due to the fact that we assign `PoolExecutor` as alias then we can `from concurrent.futures.process import ProcessPoolExecutor as PoolExecutor` and with the written above monitoring<br>
feature (featuring multiprocessing) we see that now there are multiple processes and not the only one.


Look at the image. There is one context_manager that will take care of execution **start and end** <br>
And inside that context_manager you can do all the bunch of asynchronous work <br>
+ we don’t need to take care of various `.join()/.close()`

Multiprocessing and Multithreading APIs are very similar, but not the same.

![Alt text](/ImageRepo/Multiprocessing_fourth.png?raw=true)


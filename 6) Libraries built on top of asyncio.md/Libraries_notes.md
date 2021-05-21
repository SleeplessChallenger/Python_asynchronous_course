**Libraries built on top of asyncio**

**Unsync** and **Trio** are two frameworks built on top of asyncio which enable to do things in an easier way

<ins><i>Deficiencies of asyncio/thread/multiprocessing:</i></ins>

A **Future** represents an eventual result of an **asynchronous** operation. **Future** is an ‘awaitable’ object.<br>
Coroutines can await on **Future** objects until they either have a result or an exception set, or until they are cancelled.

1. Difficulty in moving asyncio event loop across project
2. asyncio.Future is not thread safe. Hence, if you want to use it with threads then it may cause some problems. AsyncIO doesn’t use threads, it’s an event on a single thread
3. concurrent.Future’s cannot be directly awaited
4. Future.result() is a blocking operation even within an event loop. Generally it’s good, but if we did it in an event loop then we can clog up the event loop
5. asyncio.Future.result() will throw an exception if the future isn’t done
6. async Functions (async def foo()) always execute in the asyncio loop (not thread or process backed). Also, such functions don’t run in threads or in multiprocessing mode. asyncIO has totally different operation and we cannot distribute work between it and threads or processes
7. Cancellation and timeouts are tricky in threads and processes
8. Thread local storage doesn’t work for asyncio concurrency
9. Testing concurrent code can be tricky


Let’s look at first two files: `noSync.py`  & `asyncOnly.py`

First file is just ordinary one, but if we look at the second, then things can become more interesting. 

Although all files have async before them, 2/4 have real benefit from it, others don’t

1. `compute_some()` doesn’t have anything that can be ‘awaited’
2. `download_some()` has something to be awaited + pertinent library
3. `download_some_more()` in our case, we image that it doesn’t have async API, hence cannot be used with asyncio (though in reality it can be used, here we did it on purpose to show deficiency of using only asyncio) 
4. `wait_some()` also has functionality to be awaited

Of course, second file will work faster compared to first one, but we don’t reach the limit and can do even better.<br>
So, one function does **computing** and another function **doesn’t have asyncio library** for implementing asyncio

Secondly, let’s analyze third file with **unsync** (`with_unsync.py`)

1. Remove `.get_event_loop()` as there will be one <ins><i>ambient hidden asyncio event loop</i></ins>
2. Remove `create_task()` and leave plan functions
3. As we want to wait till every task is done -> replace `.run_until_complete()` with `t.result() for t in tasks`. It’s a blocking call until its done, so that line will make everything wait
4. `@unsync()` decorator will create an ambient loop around the **async func**
5. **BUT:** if we have function <ins><i>async possible operations</i></ins> (no libraries, for example) then we can <ins><i>remove async before def</i></ins> which will make this function run on thread. Ex: `download_some_more()`
6. If we have cpu_bound operation -> `@unsync(cpu_bound=True)` and remove `async` before function. Unsync will run such a method with **multiprocessing**

<h3>Async method - async loop, regular method - thread, cpu_bound method - multiprocessing</h3>

![Alt text](/ImageRepo/Libraries_first.png?raw=true)

When we call functions with unsync, it’ll return Unfuture (specific type of Future for unsync)

Problems with implementation on the image:

1. Moving event_loop can be cumbersome in the overall architecture
2. We must .create_task() as those methods don’t return values, they return coroutines 
3. Some of the methods are for asyncio (like those green ones), others are better suited for thread & multiprocessing


<h3>How unsync solves above issue</h3>

![Alt text](/ImageRepo/Libraries_second.png?raw=true)

<h4>Trio</h4>

File: `trio_prod.py`

A framework that is built from ground up and it doesn’t actually use asyncio (it integrates with async/await) , but does stuff in parallel. That’s why we just `import trio`

<h2>Attention: .Queue was removed hence see file trio_prod_new.py that is below (in python file)</h2>

1. trio.Queue(capacity=).  Capacity means how much can you put before it’ll block when you call put 
2. Write async before methods and use nursery which takes care of children functions 
3. context_manager will run till either all of the children get completed or there is an error, in which case nursery will cancel all still running and exit
4. In the bottom we should write: 

```bash
if __name__ == '__main__':
	trio.run(main)
```

Instead of simple `main()`

<h3>Cancellation concept in trio</h3>

What if we want to put a limit on how much time does it take to perform all the task (== all the children including)? -> Use another layer of context_manager to do so: 

`with trio.move_on_after():` 

In brackets you need to put upper bound of time passed which trio will cancel all the remaining work. Even if children themselves behave as nursery in other functions and have children -> all will be cancelled

In other words, `trio.open_nursery()` <ins>context_manager</ins> blocks all the tasks within them till either a) all is done or b) you cancel them or c) there is an error

![Alt text](/ImageRepo/Libraries_third.png?raw=true)

**NOTE:** Trio creates its own loop as Trio was built from scratch and not related to AsyncIO. Hence, if you want to use aiohttp or some other library,<br>
use **trio-asyncio** to integrate those. Because Trio does’t have support for libraries like aiohttp and of that ilk.

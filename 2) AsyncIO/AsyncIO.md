**Async**

Type of concurrent programming that doesn’t involve any threads or processes<br>
Concurrency is wider than parallelism. Parallelism is a subclass of concurrency.

[Article that describes parallelism and concurrency](https://luminousmen.com/post/concurrency-and-parallelism-are-different)

<h3>Salient note:</h3>

- Thread uses <ins>**preemptive multitasking:**</ins> the operating system actually knows about each thread and can interrupt it at any time to start running a different thread

- Async uses <ins>**cooperative multitasking:**</ins> tasks must cooperate by announcing when they are ready to be switched out. That means that the code in the task has to change slightly to make this happen.

<ins><i>Conceptually about Async:</ins></i> take multiple long operations, break them in places where operations wait for something and start another operation. (Image below)

![Alt text](/ImageRepo/AsyncIO_first.png?raw=true)

<h2>Producer-Consumer pattern</h2>

Producer part does the work and Consumer part searches for the answer (work to be done by Producer).<br>
They both work asynchronously if we do so.

**prod_cons_async.py**
Steps to convert sync program to async:

1. Make special loop which will be some kind of environment for the coroutines/threads
2. Instead of simple list() use asyncio.Queue(). It has .put() not .append(), .get() not .pop(0) (but if you want to iterate, then use list() as .Queue() isn’t iterable)
3. With .create_task() kicks off a couple of coroutines which will behave like generator here: they don’t actually run, but wait to be kicked off.<br>
<ins>[when first defined it will make one loop and stop within loop, so next operation will start already within loop]</ins>
4. .gather() will convert those coroutines into single task
5. .run_until_complete() will run that task until completion

But with above code we tweaked only main function, however, two other functions also should be altered:

1. Add <i>async</i> before `def`
2. Define within functions places that will signify that function is waiting (one of them is async method like `.get(), .put()`)
3. To do it place <i>await</i> before such places. Await should be placed before **coroutines** 
4. Also, instead of time.sleep() use async.sleep()

So, **await** is a marker that will tell python to break up the whole code into slices (like in the image above)

**Takeaway:** find method that supports async. I.e. when speaking to DB 

![Alt text](/ImageRepo/AsyncIO_second.png?raw=true)


<h4>We can speed up ‘asyncio’ with ‘uvloop’:</h4>

[Link to the GitHUb repo of this uvloop](https://github.com/SleeplessChallenger/uvloop)

`asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())` is what should be written before main code

When doing asynchronous scraping, we’ll switch from `‘requests’` library to `‘aiohttp’`

1. Keep in mind that Queue in Asyncio: `Queue` object is not iterable
2. `aiohttp` is a library that supports ‘asyncio’
3. return await `resp.text()` will convert from coroutine to string

**Key thing to remember:** at first start all the work and only then start to process that work (look in ‘async_scrape.py’).<br>
Because when you make a web request, you’re waiting for the response from the server -> use it for concurrency.


(descr for image below)
1. First context manager is for ‘aiohttp’
2. Second context manager is to make an asynchronous web request
3. `.raise_for_status()` is to check that response code is not like 400ish etc

![Alt text](/ImageRepo/AsyncIO_third.png?raw=true)


To use other libraries with asyncio they should support asynchronous methods. 
Let’s look for 4 async libraries for 4 popular systems : `MongoDB, PostgresSQL, Redis, File I/O`

1. File I/O: aiofiles
2. MongoDB: umongo
3. PostgreSQL: asyncpg
4. Redis: asyncio-redis

**Start of the course**

Reasons for using asynchronous programming: 1) speed 2) scalability

From 2005 CPUs are not getting faster & SingleThreaded operations the same. Today we’re not making singly CPU core faster,<br>
but adding new cores `=>` some kind of multithreading/multicore code is essential to boost the performance 

- Upper bound for improvement when speaking about speed and async:

It’s practically impossible to make code run on all CPUs at the same time. We need to think: how much can be made concurrent and<br>
is it worthy at all?

Why there are yellow == non-parallel operations? Ex: when you buy a course, then at first credit card is charged, then a new entry in<br>
DB is made, then email is sent -> they’re to be done sequentially

![Alt text](ImageRepo/StartOne.png?raw=true)

**But about scalability?** 

Scalability isn’t how fast, but how much can it handle until performance degrades (ex. How much concurrent processes can it handle)


Still scalability. Take a look at synchronous & asynchronous operations
<ins><i>Example of synchronous operation:</ins><i>

![Alt text](ImageRepo/StartTwo.png?raw=true)

Green is how long request takes to perform and vertical yellow bars are amount of time request either takes time to execute<br>
(with first one) or takes time to wait for previous request (second and third)

Next, let’s zoom in:

Request takes long time not because some computations are going, but because **it waits a lot for DB response**

![Alt text](ImageRepo/StartThree.png?raw=true)


<ins>Below is an example of asynchronous operation:<ins>

![Alt text](ImageRepo/StartFour.png?raw=true)


Of course, 100% concurrency is impossible, but still we’ve managed to drop time execution.<br>
When request 1 is waiting, request 2 starts to run, then when request 2 is waiting, request 3 starts.


(Image below) Here we free python, when request 1 waits for DB, to deal with request 2<br>
`=>` leveraging wait time to ramp up scalability.

![Alt text](ImageRepo/StartFive.png?raw=true)



<h3>Async techniques</h3>

<ins><i>Do more at once:</ins></i> take advantage of wait periods
<ins><i>Do things faster:</ins></i> leverage cores (CPU)

![Alt text](ImageRepo/StartSix.png?raw=true)


- Threads in Python don’t add computational speed due to GIL (Global Interpreter Lock).<br>
- Only one thread/step of execution can run at the same time. GIL is a thread-safety feature for memory management

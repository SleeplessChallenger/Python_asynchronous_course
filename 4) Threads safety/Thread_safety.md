**Thread safety**

Errors in threading are extremely tricky as they may vary from hardware/timing/load on the system
Such bugs are called `heisenbug`

Let’s analyze a bunch of images.

<h3>Temporarily invalid state</h3>

1. There is function call (left part of the image) that puts program in invalid state (red is invalid and blue is valid). It’s normal for program to be in invalid state during this function call as eventually it’ll be returned in valid state. **BUT** 
2. <ins>**What if you have multiple programs running?**</ins> Issue will arise if another programs takes invalid condition of the first function -> threading bug
3. Those figures on the image are just representation of data structures
4. On the image below you can see that during function call sometimes there are invalid states of the program
5. On the down most image you can see that eventually function is in valid state 

`=>` task of thread safety is to disallow such condition. It can be implemented in a coarse-grained way when anything isn’t accepted for another thread to do or fine-grained when only parts are not allow (like don’t touch that red figure only)

![Alt text](/ImageRepo/Thread_safety_first.png?raw=true)

![Alt text](/ImageRepo/Threads_safety_second.png?raw=true)

![Alt text](/ImageRepo/Threads_safety_third.png?raw=true)


Next, let’s look at `unsafe_bank.py` The main issue is that a) multiple threads may use accounts that are in process now b) in the end there is ‘Everything is okay’ default statement returned which  is incorrect<br>
So, how to tweak the class?<br>
Use either `Lock or RLock`. Problem with former is that if you call Lock from a function and it through series of function calls ends up calling into that Lock again -> Deadlock. RLock means that thread itself can enter the lock many times as long as it exists as many times, but no other thread can enters 

#####
**From RealPython:**<br>
But if one thread acquires Lock and never gives it away - `Deadlock`. <br>
Reasons: 1. Implementation bug -> Generally context manager handles it 2. Design issue -> using ‘RLock’
#####

At first, coarse-grained improvement: put RLock to inhibit other threads to do any transferring as this thread will put things into temporarily invalid state<br>
(as that first thread does transfer itself). We can do it either with acquire/release or via context manager<br>
+ we need to bring that lock to every place where there is some interaction with accounts. In our case it’s `do_transfer, validate_bank`


Secondly, If we add `self.lock = RLock()` and two accounts are being transferred by one thread and two another accounts by another thread -> everything should be alright, but if we try to fine-tune our bank with 2 context managers blindly -> serious error. <br>
**Bad example:** 
```bash
                with from_account.lock:
				            with to_account.lock:
```
How can example above happen? Thread 1 transfers from Account A to account B and Thread 2 does vice versa -> Deadlock Each of the waits for lock 2 (inner) to be released, but no, it doesn’t happen

For details see `safe_bank_improved.py`
```bash
	lock1, lock2 = (
		(from_account.lock, to_account.lock)
		if id(from_account) < id(to_account)
		else (to_account.lock, from_account.lock)
	)

	with lock1:
		with lock2:
			from_account.balance -= amount
			time.sleep(.000)
			to_account.balance += amount
```
So, if you use 2 locks from 2 different things (in our case it’s 2 different accounts) then you should take them in the same order otherwise deadlock
1. Use `RLock` instead Lock as we can reenter that type of lock and it’s easier to use
2. That context_manager on the image is a potentially unsafe operations which we don’t want other locks to see. In that context_manager there can be <ins>temporarily invalid state</ins> (from the image in the beginning of the topic)
3. Every time (means various functions etc) where you interact with data structures (in our example it’s account), you’re to take the same lock (== take a lock at those places as well)

![Alt text](/ImageRepo/Threads_safety_fourth.png?raw=true)

**Parallelism in C with Python**

Cython is an optimized static compiler for the Python. It makes writing C extensions for Python as easy as Python itself.

In CPython the interpreter/runtime is written in C

![Alt text](/ImageRepo/Cython_second.png?raw=true)

To run code with Cython we need to create setup file, look in folder `starter_hello` and there in setup.py. Also, the function which will do the work would be with `.pyx` extension. 
After that, we cannot simply run our script, at first `python setup.py build_ext --inplace` should be executed in command line and then yo can start script as usual

Here is a quick delineation of how to write code with Cython

![Alt text](/ImageRepo/Cython_first.png?raw=true)

<h3>Next, how to use Cython and threads to speed up the CPU_bound executions?</h3>

Actually, if we take CPU heavy program and implement threads => practically the same as sync version. Because all the work is a series of interpreter instructions in CPython, hence GIL tells us that only one instruction can run at a time. 
And with Cython we can break from the GIL

We can analyze our code (like with PyCharm Pro-> Profile) to find out **hotspot**. It turns out that `do_math()` function is the actual hotspot where we spend most of our time.<br>
Hence <ins>this particular element</ins> in the whole program should be speeded up. Then we need to <ins>ask ourselves a question:</ins> can we tweak it by using Cython?

We remove math to separate file with `.pyx` extension.

- Running files in such a manner will make it faster than synchronous, but slower than multiprocessing. Why? Because GIL still operates under the hood. 
- Hence we’ll use Cython syntax to pinpoint where GIL is required and where is not (because in places where it’s not required we have C code which doesn’t need GIL)

1. Use nogil contet_manager to disable GIL at the below code
2. from libc.math cimport sqrt. Not simple import, but cimport as we used `libc.math` library
3. As we cannot interact with CPython objects we need to tweak them to be Cython objects. Look at the function below, we substitute all the integers with cython.int

```bash
def do_math(start: cython.int =0, num: cython.int =10):
	pos: cython.int = start
	k_sq: cython.int = 1000 * 1000
	with nogil:
		while pos < num:
			pos += 1
			dist = sqrt((pos - k_sq) * 
						(pos - k_sq))
```

4. When code enters nogil section, it’s all C 

**But** there is an issue with above: we use <ins>c integers</ins> that are 32 bits, hence they’re overflown very easily. That’s why switching to float may be an option

Eventually we see that <ins><i>threading paired with Cython</i></ins> and right implementation can make operations to be even instantaneous. 

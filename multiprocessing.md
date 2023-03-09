# The multiprocessing doc

The easiest way to create turn a synchronous for loop into a multiprocessing pool.

Original code:
```python
def explain_sum(a, b):
    return {"a": a, "b": b, "a+b": a+b}

as_ = [1, 2, 3]
bs_ = [4, 5, 6]
results = []
for a,b in zip(as_, bs_):
    results.append(explain_sum(a, b))
print(results)
# [{'a': 1, 'b': 4, 'a+b': 5}, {'a': 2, 'b': 5, 'a+b': 7}, {'a': 3, 'b': 6, 'a+b': 9}]
```
Note that the function `explain_sum` takes two positional arguments.

Parallel code:
```python
import multiprocessing as mp

def explain_sum(d):
    a, b = d["a"], d["b"]
    return {"a": a, "b": b, "a+b": a+b}
# args becomes a list of dictionaries
ds = [{"a": 1, "b": 4}, {"a": 2, "b": 5}, {"a": 3, "b": 6}]
results = []
with mp.Pool(processes=num_workers) as pool:
	for result in pool.imap(explain_sum, ds):
	    results.append(result)
print(results)
# [{'a': 1, 'b': 4, 'a+b': 5}, {'a': 2, 'b': 5, 'a+b': 7}, {'a': 3, 'b': 6, 'a+b': 9}] # maybe in different order
```
The easiest way to deal with multiple arguments is to pass them as `kwargs` and parse them at the start of the function. 

Note that it works just fine with classes too. Unfortunately pools **cannot access class attributes** (at least not without additional efforts, probably doable with pipes and stuff).

Original code:
```python
from time import time

class Adder:
	def __init__(self, as_, bs_):
		self.results = []
		self.times = []
		for a,b in zip(as_, bs_):
			self.results.append(self.explain_sum(a,b))
			
	def explain_sum(self, a, b):
		t0 = time()
		d = {"a": a, "b": b, "a+b": a+b}
		self.times.append(time()-t0)
		return d

as_ = [1, 2, 3]
bs_ = [4, 5, 6]
adder = Adder(as_, bs_)
print(adder.results)
# [{'a': 1, 'b': 4, 'a+b': 5}, {'a': 2, 'b': 5, 'a+b': 7}, {'a': 3, 'b': 6, 'a+b': 9}]

print(adder.times)
# [4.76837158203125e-07, 0.0, 2.384185791015625e-07]
```

Parallel code:
```python
import multiprocessing as mp
from time import time

class Adder:
	def __init__(self, as_, bs_):
		self.results = []
		self.times = []
		pool = mp.Pool(3)
		for result in pool.imap(self.explain_sum, [{"a": a, "b": b} for a,b in zip(as_, bs_)]):
			self.results.append(result)
		pool.close()
			
	def explain_sum(self, d):
		t0 = time()
		a, b = d["a"], d["b"]
		d1 = {"a": a, "b": b, "a+b": a+b}
		self.times.append(time()-t0)
		return d1

as_ = [1, 2, 3]
bs_ = [4, 5, 6]
adder = Adder(as_, bs_)
print(adder.results)
# [{'a': 1, 'b': 4, 'a+b': 5}, {'a': 2, 'b': 5, 'a+b': 7}, {'a': 3, 'b': 6, 'a+b': 9}]

print(adder.times)
# [] # /!\ class attributes were not updated :(
```





# Discussion 6
## Q2: Add This Many
def add(x, el, s):
    num = 0
    for i in s:
        if x == i:
            s.append(el)
    print (s)
    return s
s = [1, 2, 4, 2, 1]
add(1, 5, s)
## Q3: generator
def countdown(n):
    while n >0:
        yield n
        n -= 1
c1, c2 = countdown(5), countdown(5)
print(next(c1))
print(next(c1))
print(next(c2))

## Q4: Filter-Iter
def filter_iter(iterable, fn):
    for elem in iterable:
        if fn(elem):
            yield elem

is_even = lambda x: x % 2 == 0
s = filter_iter(range(4,10), is_even)
print(next(s))
print(next(s))

## Q5: Merge
def sequence(start, step):
        while True:
            yield start
            start += step

def merge(a, b):
    first_a, first_b = next(a), next(b)
    while True:
        if first_a == first_b:
            yield first_a
            first_a, first_b = next(a), next(b)
        elif first_a < first_b:
            yield first_a
            first_a = next(a)
        else:
            yield first_b
            first_b = next(b)

a = sequence(2, 3)
b = sequence(3, 2)
result = merge(a, b)
print([next(result) for _ in range(10)])

## Q6 Primes Generator
def is_prime(n):
    def helper(i):
        if i == n:
            return True
        elif n % i == 0:
            return False
        return helper(i +1)
    return helper(2)

def primes_gen(n):
    if n == 1:
        return
    if is_prime(n):
        yield n
    yield from primes_gen(n-1)
    

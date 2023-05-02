from timeit import default_timer as timer
import concurrent.futures

result = 3

def f(x):
    return x * x - x + 1

# sequential
start = timer()
for i in range(20):
    result = f(result)


print('Result is very large. Only printing the last 5 digits:', result % 100000)
print('Sequential took: %.2f seconds.' % (timer() - start))

# concurrent
def concurrent_f(x):
    # every thread spawned, waits for this variable to be processed
    # by the previous thread
    global result
    result = f(result)
    print(f'done {x}')

start = timer()
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as exector:
    futures = [exector.submit(concurrent_f, i) for i in range(20)]

    _ = concurrent.futures.as_completed(futures)

print('Result is very large. Only printing the last 5 digits:', result % 100000)
print('Sequential took: %.2f seconds.' % (timer() - start))

import threading

def display(message, num):
    for i in range(num):
        print(f"{message} {i + 1}")

t1= threading.Thread(target=display, args=("Thread 1", 5))
t2 = threading.Thread(target=display, args=("Thread 2", 3))

t1.start()
t2.start()

t1.join()
t2.join()
import threading, time, random

def func():
	print("Thread fired!")
	for i in range(20):
		time.sleep(random.random() * 2)
		print("Loco")
	print("Thread dead!")

if __name__ == "__main__":
	myThread = threading.Thread(target=func, args=())
	myThread.start()
	while True:
		X = input(">>>")
		time.sleep(1)
		if X == "exit":
			break
		else:
			print(X)



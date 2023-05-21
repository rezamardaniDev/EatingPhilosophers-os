import threading
import time
import random


class Philosopher(threading.Thread):
    def __init__(self, number, left_chopstick, right_chopstick):
        threading.Thread.__init__(self)
        self.number = number
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self):
        while True:
            # Wait for random amount of time before picking up first chopstick
            time.sleep(random.uniform(0, 1))

            # Acquire locks on both chopsticks
            if self.left_chopstick.acquire(timeout=1):
                if self.right_chopstick.acquire(timeout=1):
                    # Eat for random amount of time
                    print(f"Philosopher {self.number} is eating.")
                    time.sleep(random.uniform(0, 1))

                    # Release locks on both chopsticks
                    self.right_chopstick.release()
                else:
                    # Release lock on left chopstick if right chopstick is not available
                    self.left_chopstick.release()
            else:
                # If left chopstick is not available, try again later
                print(f"Philosopher {self.number} is hungry.")


if __name__ == "__main__":
    # Create 5 philosophers and 5 chopsticks
    philosophers = [Philosopher(i, threading.Lock(), threading.Lock()) for i in range(5)]

    # Start all philosophers
    for philosopher in philosophers:
        philosopher.start()

    # Wait for all philosophers to finish
    for philosopher in philosophers:
        philosopher.join()

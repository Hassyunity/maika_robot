import threading
import time
import random

lock = threading.Lock() #protect resources

resources = {
    "foo": 0,
    "bar": 0,
    "foobar": 0,
    "money": 0,
    "robots": 2
}

MAX_ROBOTS = 30

threads = []

def mine_foo():
    time.sleep(1)
    with lock:
        resources["foo"] += 1
        print(f"[+] created foo → {resources['foo']}")

def mine_bar():
    time.sleep(random.uniform(0.5, 2))
    with lock:
        resources["bar"] += 1
        print(f"[+] created bar → {resources['bar']}")

def assemble():
    with lock:
        if resources["foo"] >= 1 and resources["bar"] >= 1:
            resources["foo"] -= 1
            resources["bar"] -= 1
        else:
            return

    time.sleep(2)

    if random.random() < 0.6:
        with lock:
            resources["foobar"] += 1
            print(f"[✓] Assemble success → {resources['foobar']}")
    else:
        with lock:
            resources["bar"] += 1
            print("[x] Assemble fail (bar récupéré)")

def sell():
    time.sleep(10)
    with lock:
        sold = min(5, resources["foobar"])
        resources["foobar"] -= sold
        resources["money"] += sold
        print(f"[💰] Sold {sold} → money: {resources['money']}€")

def buy_robot():
    with lock:
        if resources["money"] >= 3 and resources["foo"] >= 6:
            resources["money"] -= 3
            resources["foo"] -= 6
        else:
            return

    time.sleep(1)

    with lock:
        resources["robots"] += 1
        new_id = resources["robots"]

    print(f"[🤖] New robot created → total: {new_id}")

    t = threading.Thread(target=robot_behavior, args=(new_id,))
    t.start()
    threads.append(t)

def move():
    time.sleep(5)

# ---------------- ROBOT ---------------- #
def robot_behavior(robot_id):
    while True:
        with lock:
            if resources["robots"] >= MAX_ROBOTS:
                break

            foo = resources["foo"]
            bar = resources["bar"]
            foobar = resources["foobar"]
            money = resources["money"]

        # achat robot prioritaire
        if money >= 3 and foo >= 6:
            action = buy_robot

        elif money >= 3 and foo < 6:
            action = mine_foo

        elif foo >= 1 and bar >= 1:
            action = assemble

        elif foobar >= 5:
            action = sell

        elif foo < bar:
            action = mine_foo
        else:
            action = mine_bar

        print(f"[Robot {robot_id}] → {action.__name__}")
        action()

    print(f"[Robot {robot_id}] stopped")

def main():
    print("🚀 Starting factory...\n")

    # lancer robots initiaux
    for i in range(resources["robots"]):
        t = threading.Thread(target=robot_behavior, args=(i + 1,))
        t.start()
        threads.append(t)

    # attendre la fin
    for t in threads:
        t.join()

    print("\n🏁 FINISHED")
    print("Final resources:", resources)

if __name__ == "__main__":
    main()

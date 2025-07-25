#!/usr/bin/python3

import time

start = time.perf_counter()
n = 10**5
while time.perf_counter() - start < 60:
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            break
    n += 1

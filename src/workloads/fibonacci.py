#!/usr/bin/python3

import time

start = time.perf_counter()
while time.perf_counter() - start < 60:
    a, b = 0, 1
    for _ in range(100000):
        a, b = b, a + b


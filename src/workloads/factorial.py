#!/usr/bin/python3

import time
import math

start = time.perf_counter()
while time.perf_counter() - start < 60:
    for i in range(1, 10000):
        math.factorial(i)


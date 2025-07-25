#!/usr/bin/python3

import time
import numpy as np

start = time.perf_counter()
A = np.random.rand(200, 200)
B = np.random.rand(200, 200)
while time.perf_counter() - start < 60:
    _ = A @ B


# task_scheduler

For full design look at **docs/design.md**

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

## Here is the usage for the program:

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    scheduler.py [-h] --file FILE [--validate] [--run]

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

## Sample input.txt file for the program:

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

$ cat input.txt
  
./workloads/prime_check.py, 60, []

./workloads/fibonacci.py, 60, [./workloads/prime_check.py]

./workloads/matrix_multiply.py, 60, [./workloads/prime_check.py]

./workloads/factorial.py, 60, [./workloads/fibonacci.py, ./workloads/matrix_multiply.py]


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

## Sample test with --validate option:

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

$ python3 scheduler.py --file input.txt --validate

[Info] Expected parallel runtime: 180.000000 seconds

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

## Sample test with --run option:

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

$ python3 scheduler.py --file input.txt --run

[PID 35207] Task './workloads/prime_check.py' starting

[PID 35208] Task './workloads/fibonacci.py' waiting on: ['./workloads/prime_check.py']

[PID 35209] Task './workloads/matrix_multiply.py' waiting on: ['./workloads/prime_check.py']

[PID 35211] Task './workloads/factorial.py' waiting on: ['./workloads/fibonacci.py', './workloads/matrix_multiply.py']

[PID 35207] Task './workloads/prime_check.py' finished

[PID 35209] Task './workloads/matrix_multiply.py' starting

[PID 35208] Task './workloads/fibonacci.py' starting

[PID 35208] Task './workloads/fibonacci.py' finished

[PID 35209] Task './workloads/matrix_multiply.py' finished

[PID 35211] Task './workloads/factorial.py' starting

[PID 35211] Task './workloads/factorial.py' finished

[Info] Expected parallel runtime: 180.000000 seconds

[Info] Actual parallel runtime: 30.056223 seconds

[Info] Difference between Actual and expected runtime: 149.943777 seconds

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

## So how do we verify that multiprocessing works?

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Monitoring using htop shows all 4 cores are used when there are no dependencies:

<img width="2140" height="1162" alt="htop_view" src="https://github.com/user-attachments/assets/b4017ba8-154c-48e6-93c8-c767a6f0ef84" />

Similarly, nmon also shows good amount of CPU utilization on all cores:

<img width="1307" height="603" alt="nmon_view" src="https://github.com/user-attachments/assets/0b484921-aac3-4d0b-af11-446794ec4ce3" />

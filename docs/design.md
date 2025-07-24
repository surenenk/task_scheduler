Design Document: Parallel Task Scheduler

File:		scheduler.py
Language:	Python 3
Model:      CPU load parallelization
Testing:	pytest

++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Requirements:
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
* Design and implement a task scheduler to schedule and execute list of tasks in parallel.
* Get the input as a text file with list of tasks in format "name, duration, [dep1 dep2 ...]".
* Option to calculate the expected task runtime without actually running the tasks.
* Option to calculate the expected task runtime and compares it with the actual runtime.
* Tasks should be executed only after their dependencies are completed.

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Data Structures:
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Task Class:
- name: unique task name
- duration: expected task runtime in seconds
- deps: list of dependency tasks

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Program flow:
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

+-----------------+
| Parse task file |
+--------+--------+
         |
         v
+---------------------+ no  +------------------------+
| Valid dep graph?    |---> |    Error not valid     |
+---------------------+     +------------------------+
         | yes
         v
+--------+--------+      +------------------------+
| Compute runtime |----->| Show --validate output |
+--------+--------+      +------------------------+
         |
         v
+--------------------------------------+
| Fork process for each Task and       |
| Wait on dependencies completion event|
+--------------------------------------+
         |
         v
+-------------------------+
| Measure actual runtime  |
| during process run      |
+-------------------------+
         |
         v
+------------------------------------+
| Run actual task after deps are done|
+------------------------------------+
         |
         v
+-----------------------------------+
| Measure difference between actual |
| runtime and expected runtimes.    |
+-----------------------------------+
         |
         v
+---------------------------------+
| Display results and exit program|
+---------------------------------+

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Key Functions:
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

* parse_tasks(tasks):
   - Check validity of input
   - Parses a list of strings into a Dictionary of task objects.

* validate_tasks(tasks):
   - Validates that all dependencies exist.
   - Detects cyclic dependencies using DFS.

* has_cycle(tasks):
   - Uses DFS and recursion stack to detect cycles in task dependencies.

* compute_expected_runtime(tasks):
   - Computes the expected total runtime using DFS to calculate the longest dependent path (critical path).

* task_runner(task, task_events, timeline, work_fn):
   - Waits for all dependencies to complete. Event() driven so do not have to poll. Task can start as soon as deps complete.
   - Executes the given work_fn().
   - Records start and end times to calculate actual runtime. We need to use clock time to calculate actual time.
   - Use timeline to store completion times of various tasks and task_events to store event() information.
     We can use python multiprocessing(event and dict) for IPC between tasks since we need to sync between them.

* run_tasks_parallel(tasks, work_fn):
   - Spawns a process for each task.
   - Uses multiprocessing to share state across processes.
   - Tracks task completion using shared event dict.
   - Returns actual vs expected runtime and a timeline of task execution.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Testing
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
* Functions can be tested individually by injecting input and extracting output
* Compatible with pytest for unit and integration testing.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
History
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
* 07/24/2025 - Initial design suren.eda@gmail.com

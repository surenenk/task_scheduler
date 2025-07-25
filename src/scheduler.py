# python3
###############################################################################################################
#                        Parallel Task Scheduler
###############################################################################################################

import argparse
from multiprocessing import Manager,Process,Event
import os
import sys
import time

# Basic class to store input components
class Task:
    def __init__(self,name,duration,deps):
        self.name = name
        self.duration = float(duration)
        self.deps = deps

# parse the input params and return the components
def input_parser():
    parser = argparse.ArgumentParser(description="Parallel task scheduler")
    parser.add_argument("--file", required=True, help="Input file with path is required")
    parser.add_argument("--validate", action="store_true", help="Only validate and show expected runtime")
    parser.add_argument("--run", action="store_true", help="Run tasks in parallel and show results")

    # This should give us values for all arguments
    args = parser.parse_args()

    if not args.validate and not args.run:
        parser.print_help()
        sys.exit(1)

    return args

# Parse the input file passed and get the list of tasks
def get_tasks(file):
    tasks = {}
    deps = []

    if not os.path.isfile(file):
        print(f"Error: File not found: {file}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(file) as f:
            for line in f:
                if not line.strip():
                    continue

                # Try to split the line and on failure, error out
                try:
                    name,duration,deps_str = line.strip().split(",",2)
                    deps_str = deps_str.strip()[1:-1]
                    deps = [d.strip() for d in deps_str.split(",") if d.strip()]
                    # Create a dictionary of Task objects with task name as key
                    tasks[name.strip()] = Task(name.strip(),duration.strip(),deps)
                except ValueError as e:
                    raise ValueError(f"Invalid format in line '{line.strip()}'. Error: {e}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    return tasks

# Check if there is cyclic dependency here. Use a stack and a visited set to keep track of
# task and visited deps. If more than one task in stack with same name, there is a cycle.
def is_dep_cyclic(tasks):
    visited = set()
    stack = set()

    def dfs(task_name):
        if not task_name:
            return False

        if task_name in stack:
            return True

        if task_name in visited:
            return False

        stack.add(task_name)

        for dep in tasks[task_name].deps:
            if dfs(dep):
                return True

        stack.remove(task_name)
        visited.add(task_name)

        return False

    for task_name in tasks:
        if dfs(task_name):
            return True

    return False

# Validate the tasks. Check if they are valid like does the dep task exist in list of tasks,
# does the task list create cyclical dependency. If so error out.
def validate_tasks(tasks):
    task_names = set(tasks.keys())

    for task in tasks.values():
        for dep in task.deps:
            if not dep:
                break

            if dep not in task_names:
                raise ValueError(f"Invalid dependency '{dep}' in task '{task.name}'")

    if is_dep_cyclic(tasks):
        raise ValueError("Cycle detected in task dependencies")

# Calculate the expected runtime of task including the dependencies. Again use DFS to find max
# time.
def compute_expected_runtime(tasks):
    if not tasks:
        return 0

    # Save the calculated runtime for all tasks. We will get the max from this.
    task_mem = {}

    def dfs(task_name):
        if not task_name:
            return 0

        if task_name in task_mem:
            return task_mem[task_name]

        task = tasks[task_name]

        if not task.deps:
            # If no dependencies, total time is just task's duration
            task_mem[task_name] = task.duration
        else:
            # Task duration + max time of all dependency chains
            dep_times = []

            for dep in task.deps:
                dep_runtime = dfs(dep)
                dep_times.append(dep_runtime)

            task_mem[task_name] = task.duration + max(dep_times)

        return task_mem[task_name]

    # find the max of all tasks in our list and use that.
    longest_path_runtime = max(dfs(name) for name in tasks.keys())

    print(f"[Info] Expected parallel runtime: {longest_path_runtime:.6f} seconds")

    return longest_path_runtime

# Run one task at a time but do event wait() for deps to do a set(). Until then
# the task is blocked.
def task_runner(task, task_events, timeline, work_fn):
    if task.deps:
        print(f"[PID {os.getpid()}] Task '{task.name}' waiting on: {task.deps}")

    for dep in task.deps:
        if not dep:
            continue

        task_events[dep].wait()

    print(f"[PID {os.getpid()}] Task '{task.name}' starting")
    start = time.time()
    work_fn()
    end = time.time()
    timeline[task.name] = (start, end)
    print(f"[PID {os.getpid()}] Task '{task.name}' finished")

    task_events[task.name].set()

# Run dep tasks in parallel for each task. Once process is done, do a process join which
# will wait for all processes to complete.
def run_parallel_tasks(tasks):
    with Manager() as manager:
        timeline = manager.dict()
        task_events = {name: Event() for name in tasks}
        processes = []

        start_time = time.time()
        for task in tasks.values():
            p = Process(target=task_runner, args=(task, task_events, timeline, dummy_work_fn))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        end_time = time.time()
        actual_runtime = end_time - start_time
        expected_runtime = compute_expected_runtime(tasks)
        runtime_diff = abs(actual_runtime - expected_runtime)

        print(f"[Info] Actual parallel runtime: {actual_runtime:.6f} seconds")
        print(f"[Info] Difference between Actual and expected runtime: {runtime_diff:.6f} seconds")

        return {
            "actual_runtime": actual_runtime,
            "expected_runtime": expected_runtime,
            "timeline": dict(timeline)
        }

# Dummy function for testing
def dummy_work_fn():
    time.sleep(10)

def main():
    inputs = input_parser()

    tasks = get_tasks(inputs.file)
    validate_tasks(tasks)

    if inputs.validate:
        compute_expected_runtime(tasks)

    if inputs.run:
        run_parallel_tasks(tasks)

if __name__ == "__main__":
    main()

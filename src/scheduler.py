# python3
###############################################################################################################
#                        Parallel Task Scheduler
###############################################################################################################

import argparse
import os
import sys

# Basic class to store input components
class Task:
    def __init__(self,name,duration,deps):
        self.name = name
        self.duration = duration
        self.deps = deps

# parse the input params and return the components
def input_parser():
    parser = argparse.ArgumentParser(description="Parallel task scheduler")
    parser.add_argument("--file", required=True, help="Input file with path is required")
    parser.add_argument("--validate", action="store_true", help="Only validate and show expected runtime")
    parser.add_argument("--run", action="store_true", help="Run tasks in parallel and show results")

    # This should give us values for all arguments
    args = parser.parse_args()
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
                    deps = deps_str.strip("[]").split()
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
            if dep not in task_names:
                raise ValueError(f"Invalid dependency '{dep}' in task '{task.name}'")

    if is_dep_cyclic(tasks):
        raise ValueError("Cycle detected in task dependencies")

if __name__ := "__main__":
    inputs = input_parser()
    tasks = get_tasks(inputs.file)
    validate_tasks(tasks)

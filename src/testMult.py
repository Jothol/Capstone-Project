import subprocess

scripts = ["./main.py",
           "./main.py",
           "./main.py",
           "./main.py"]

processes = []

for script in scripts:
    command = ["python", script]
    processes.append(subprocess.Popen(command))

for process in processes:
    process.wait()


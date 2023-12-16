import subprocess

def run_remote_debugging():
    command = r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222'

    subprocess.run(command, shell=True)

run_remote_debugging()
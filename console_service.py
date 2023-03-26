import subprocess
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
global output

app = Flask(__name__)
CORS(app)

import subprocess
import threading
import queue
import time

encoding = 'ISO-8859-1'
# Define a global variable to store the output
output = ""

# Define a queue to store commands to be executed
command_queue = queue.Queue()
process = subprocess.Popen("powershell", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Define a function to run a command on the console
def run_command(command):
    global output
    
    print(f"process : {process}")
    print(f"process stdin : {process.stdin}")
    while process.stdin is None:
        time.sleep(0.1)    
    # Send the command to the console
    process.stdin.write(command.encode(encoding) + b"\n")
    process.stdin.flush()
    
    # Wait for the output to be generated
    time.sleep(1.0)

run_command("cd ~\Documents\chatgpt_extensions")


def watch_output():
    global output
    print("Running output watcher")
    while True:
        # Read the output of the console and add it to the global variable
        stdout = process.stdout.readline().decode(encoding)
        if stdout:
            output += stdout
            print(stdout.strip())


# Define a function to execute the queued commands
def execute_commands():
    global output
    while True:
        command = command_queue.get()
        try:
            print(f"Executing command {command}")
            run_command(command)
            print(f"Command {command} executed")
        except Exception as ex:
            output += str(ex)
        command_queue.task_done()
        print(f"Waiting for next command")

# Start the thread to watch the console output
output_thread = threading.Thread(target=watch_output)
output_thread.daemon = True
output_thread.start()

# Start the thread to execute commands
execute_thread = threading.Thread(target=execute_commands)
execute_thread.daemon = True
execute_thread.start()

# Define the route to receive commands from the frontend
@app.route('/command', methods=['POST'])
def execute_command():
    global output
    command = request.json['command']
    print(f"Received command : {command}")

    # Add the command to the queue
    command_queue.put(command)

    print(f"Entries in queue : {command_queue.qsize()}")
    # Wait for a short period of time to allow the output to be captured
    time.sleep(1)

    # Send any pending stdout and stderr data
    output_lines = output.split('\n')
    output = ""
    return jsonify(output=output_lines)

@app.route('/console')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

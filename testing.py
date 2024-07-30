import os
import time
import inspect
from IPython.terminal.embed import InteractiveShellEmbed


class CustomInteractiveShell(InteractiveShellEmbed):
    def run_cell(self, raw_cell, store_history=True, silent=False, shell_futures=True):
        # Your custom pre-execution logic here
        print(f"Custom pre-execution: {raw_cell}")

        # Call the parent class's run_cell method
        result = super().run_cell(raw_cell, store_history, silent, shell_futures)

        # Your custom post-execution logic here
        print("Custom post-execution")
        
        return result

# Path to the current script file
script_path = __file__

# Read the initial version of the file
with open(script_path, 'r') as f:
    initial_lines = f.readlines()

# Save the initial modification time
initial_mtime = os.path.getmtime(script_path)

# Create the global IPython shell object
shell = CustomInteractiveShell.instance()

def embed(local_ns=None):
    # Launch shell
    shell(
        local_ns=local_ns,
        stack_depth=2,
    )

def example():
    x = 20
    y = 'hello'
    print("hello")
    z = "fucsk"
    
    embed(locals())

    shell.run_cell("print(\"hellorasd\")")

def monitor_changes():
    global initial_mtime, initial_lines, shell
    while True:
        current_mtime = os.path.getmtime(script_path)
        if current_mtime != initial_mtime:
            print("File changed, evaluating changes...")
            initial_mtime = current_mtime

            # Read the new version of the file
            with open(script_path, 'r') as f:
                new_lines = f.readlines()

            # Identify changed lines
            changed_lines = [new_line for line, new_line in zip(initial_lines, new_lines) if line != new_line]

            # Execute the changed lines in the IPython shell
            if changed_lines:
                # for line in changed_lines:
                #     print(f"Executing changed line: {line.strip()}") 
                #     shell.run_cell(line)
                shell.run_cell("print(\"file reloaded\")")

            initial_lines = new_lines

        time.sleep(1)

if __name__ == "__main__":
    import threading
    # Start monitoring file changes in a separate thread
    threading.Thread(target=monitor_changes, daemon=True).start()
    
    # Run the example function
    example()

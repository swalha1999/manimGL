import dearpygui.dearpygui as dpg
import subprocess
import os
import threading
import clipboard

# Shapes dictionary for easier selection
shapes = {
    "Circle": "Circle",
    "Square": "Square",
    "Triangle": "Triangle",
    "Rectangle": "Rectangle",
    "Dot": "Dot",
    "Line": "Line",
    # Add more shapes as needed
}

# Callback functions for buttons
def play_callback(sender, app_data):
    code = dpg.get_value("code_input")
    with open("temp_scene.py", "w") as file:
        file.write(code)

    def run_manim():
        try:
            process = subprocess.run(["manim", "-pql", "temp_scene.py", "MyScene"], capture_output=True, text=True)
            if process.returncode == 0:
                output_text = "Render successful!"
                image_path = "./media/images/temp_scene/MyScene/000.png"
                if os.path.exists(image_path):
                    dpg.window(tag="render_output", pmin=(0, 0), pmax=(600, 500),
                                   texture_id=dpg.load_texture_from_file(image_path))
                else:
                    dpg.set_value("error_output", "Render image not found.")
            else:
                output_text = process.stderr
            dpg.set_value("error_output", output_text)
        except Exception as e:
            dpg.set_value("error_output", str(e))

    threading.Thread(target=run_manim).start()


def pause_callback(sender, app_data):
    print("Pause button pressed")


def stop_callback(sender, app_data):
    print("Stop button pressed")


def clear_output_callback(sender, app_data):
    # Clear the error output text
    dpg.set_value("error_output", "")


def copy_code_callback(sender, app_data):
    # Get the code from the input text
    code = dpg.get_value("code_input")
    # Copy the code to the clipboard
    clipboard.copy(code)
    # Show a notification (optional)
    dpg.add_popup(message="Code copied!", modal=False)


# Function to insert the selected shape into the code
def insert_shape(sender, app_data, shape_name):
    # Get the current code
    code = dpg.get_value("code_input")
    # Add the selected shape to the code (you might need to adjust this based on Manim syntax)
    new_code = code + f"\nself.play(Create({shape_name}()))"
    # Update the code input text
    dpg.set_value("code_input", new_code)
    # Hide the popup window
    dpg.hide_item("add_drawing_window")


# Initialize Dear PyGui context
dpg.create_context()

# Create the "Add Drawing" window positioned to the left of the code section
with dpg.window(label="Add Drawing", width=120, height=800, no_close=True, pos=(0, 0)):
    for shape_name, display_name in shapes.items():
        dpg.add_button(label=display_name, callback=insert_shape, user_data=shape_name)

with dpg.window(label="Main Window", width=1000, height=800, pos=(120, 0)):
    # Component 1: Buttons
    with dpg.group(horizontal=True):
        dpg.add_button(label="Play", callback=play_callback)
        dpg.add_button(label="Pause", callback=pause_callback)
        dpg.add_button(label="Stop", callback=stop_callback)
        dpg.add_button(label="Clear Output", callback=clear_output_callback)
        dpg.add_button(label="Copy Code", callback=copy_code_callback)

    # Component 2: Code section and rendering screen
    with dpg.child_window(width=800, height=500):
        with dpg.group(horizontal=True):

            with dpg.group():
                dpg.add_input_text(tag="code_input", multiline=True, height=500, width=400,
                                   default_value="from manim import *\n\nclass MyScene(Scene):\n    def construct(self):\n        self.play(Write(Text('Hello, Manim!')))")
            with dpg.group():
                dpg.add_text("Rendering Screen")
                dpg.window(tag="render_output", width=500, height=500)


    # Component 3: Text output for errors
    with dpg.child_window(width=800, height=200):
        dpg.add_text("Error Output")
        dpg.add_input_text(tag="error_output", multiline=True, readonly=True, height=200, width=1000)

dpg.create_viewport(title='Manim GUI', width=1000, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
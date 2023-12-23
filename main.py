from flask import Flask
from flask_socketio import SocketIO, emit
import pyvjoystick
import eventlet
import os
import sys
import os

static_folder = getattr(sys, '_MEIPASS', os.path.abspath("."))  # Get path to bundled static folder
# Access index.html:
index_html_path = os.path.join(static_folder, "static", "index.html")
# Access style.css:
style_css_path = os.path.join(static_folder, "static", "style", "style.css")
# Use these paths to open, read, or serve the files as needed in your application's logic.

joystick = pyvjoystick.vjoy.VJoyDevice(1)
xAxis = pyvjoystick.vjoy.HID_USAGE.X

app = Flask(__name__,static_url_path="/static")
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")
    
@socketio.on("sliderchanged1")
def handle_slider_change(data):
    hex_value = data["sliderval"]
    joystick.set_axis(xAxis,hex_value)
    
toggle_checks = [False] * 7  # Store button states in a list

@socketio.on('checkbox_clicked')
def handle_checkbox_clicked(checkbox_id):
    global toggle_checks
    button_index = int(checkbox_id["_checkboxid"])
    toggle_checks[button_index] = not toggle_checks[button_index]
    joystick.set_button(button_index, toggle_checks[button_index])
    print(f"Checkbox {button_index} clicked")

#toggle_buttons = [False] * 13  # Store button states in a list
@socketio.on("button_clicked")
def handle_button_clicked(data):
    global toggle_buttons
    button_index = int(data["_buttonid"])
    #toggle_buttons[button_index] = not toggle_buttons[button_index]
    joystick.set_button(button_index, 1)
    eventlet.sleep(0.2)
    joystick.set_button(button_index, 0)
    print(button_index)



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=8000)  # Bind to all network interfaces

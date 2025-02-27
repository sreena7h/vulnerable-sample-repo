import sys
import traceback
import json
import logging
import linecache
from datetime import datetime

# Configuration
TELEMETRY_FILE = 'telemetry.json'
APP_DIR = "/Users/sreenath/concert/temp/crud_project"
IGNORED_FILE = "telemetry_agent.py"  # Ignore telemetry_agent.py stack entries

# Setup logging
logging.basicConfig(
    filename='telemetry_debug.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def telemetry_capture_stack():
    """Captures stack trace relevant to the application directory, including the source code line, while ignoring telemetry_agent.py."""
    stack = []
    for frame in traceback.extract_stack():
        if frame.filename.startswith(APP_DIR) and IGNORED_FILE not in frame.filename:
            # Use the frame's code line if available, otherwise fetch via linecache
            code_line = frame.line if frame.line is not None else linecache.getline(frame.filename, frame.lineno).strip()
            stack.append({
                "file": frame.filename,
                "lineno": frame.lineno,
                "function": frame.name,
                "code": code_line
            })
    logging.debug(f"Captured stack trace: {stack}")
    return stack

def telemetry_get_api_endpoint():
    """Derives an API-like identifier based on the first function in the stack trace."""
    stack = telemetry_capture_stack()
    if stack:
        endpoint = f"{stack[0]['file']}::{stack[0]['function']}"
        return endpoint
    logging.warning("No stack trace found, returning unknown_endpoint.")
    return "unknown_endpoint"

def telemetry_read_existing():
    """Reads the existing telemetry file and returns the data as a list."""
    try:
        with open(TELEMETRY_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.warning(f"Telemetry file issue: {e}, starting with an empty list.")
        return []

def telemetry_group_by_function(stack):
    """
    Groups the stack trace entries by function name.
    Stores the first occurrence's line number and code as the start,
    and updates the end line number with the most recent occurrence.
    """
    function_map = {}
    for entry in stack:
        func_name = entry["function"]
        if func_name not in function_map:
            function_map[func_name] = {
                "method": func_name,
                "file": entry["file"],
                "start_lineno": entry["lineno"],
                "start_line_code": entry["code"],
                # "end_lineno": entry["lineno"],
                "stack": [entry]
            }
        else:
            # Simply update the end_lineno to the current frame's lineno (last occurrence)
            function_map[func_name]["end_lineno"] = entry["lineno"]
            function_map[func_name]["stack"].append(entry)
    return list(function_map.values())

def telemetry_log_data(data):
    """Saves telemetry logs in the required structured format with updated location information."""
    telemetry_logs = telemetry_read_existing()
    
    for entry in telemetry_logs:
        if entry["url"] == data["url"]:
            entry["stacks"].extend(data["stacks"])  # Append new stacks
            # Recalculate location using all frames from every stack entry
            all_frames = []
            for stack_entry in entry["stacks"]:
                all_frames.extend(stack_entry.get("stack", []))
            entry["location"] = telemetry_group_by_function(all_frames)
            break
    else:
        telemetry_logs.append(data)  # New entry if URL not found

    try:
        with open(TELEMETRY_FILE, 'w') as f:
            json.dump(telemetry_logs, f, indent=4)
    except Exception as e:
        logging.error(f"Error writing telemetry data to file: {e}")

def telemetry_trace_calls(frame, event, arg):
    """Captures call events and logs telemetry."""
    if (event == 'call' and 
        frame.f_code.co_filename.startswith(APP_DIR) and 
        IGNORED_FILE not in frame.f_code.co_filename):
        stack_data = telemetry_capture_stack()
        telemetry_data = {
            "url": telemetry_get_api_endpoint(),
            "stacks": [{
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "function": frame.f_code.co_name,
                "file": frame.f_code.co_filename,
                "lineno": frame.f_lineno,
                "stack": stack_data
            }],
            "location": telemetry_group_by_function(stack_data)
        }
        telemetry_log_data(telemetry_data)
    return telemetry_trace_calls

def telemetry_initialize():
    """Initializes telemetry tracing if no debugger is active."""
    logging.info("Initializing telemetry tracing...")
    if sys.gettrace() is None:
        sys.settrace(telemetry_trace_calls)
        logging.info("Telemetry tracing enabled.")
    else:
        logging.warning("Debugger detected: telemetry tracing is disabled.")

# telemetry_initialize()
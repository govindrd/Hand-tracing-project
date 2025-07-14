# Placeholder for future drawing or saving functions

def save_trace_to_file(trace_data, filename="output/traces/trace.json"):
    import json
    with open(filename, 'w') as f:
        json.dump(trace_data, f, indent=2)

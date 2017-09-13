import json
import os
import errno

def value_or_callable(val, *args, **kwargs):
    if callable(val):
        return val(*args, **kwargs)
    return val

def create_path_if_needed(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            # TODO Python 3 accepts a exist_ok=True in the function below (so we don't need to check whether the path exists)
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def save_file(filename, content):
    create_path_if_needed(filename)
    with open(filename, 'w') as f:
        f.write(content)

def dump_json(filename, data, *args, **kwargs):
    create_path_if_needed(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, *args, **kwargs) 

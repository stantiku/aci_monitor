import json


def set_query_path(*argv):
    # Collect hierarchical json elements to access and return them as a list.
    query_path = []
    for arg in argv:
        query_path.append(arg)
    return query_path


def load_value(json_input, query_path):
    # Return the value get from json_input[query_path]
    value = json_input
    if isinstance(json_input, str):  # Convert string to json if json_input is string
        value = json.loads(json_input)
    for q in query_path:
        value = value[q]
    return value


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


def class_query(session, apic_ip, class_name):
# Purpose:  Return all objects in the specified class
# Input:    session: a sesison from requests library
#           class_name: name of the class to query
# Output:   A list of objects in the class
    CLASS_PATH = "/api/node/class/"
    output = []
    response_body = session.get(apic_ip
                    + CLASS_PATH 
                    + class_name 
                    + ".json"
                    , verify=False)
    # if apic return any errors, break
    if (response_body.status_code != 200):
        print ("REST call error: " + str(response_body.status_code))
    else:
        object_list = json.loads(response_body.text)["imdata"]
        for object in object_list:
            output.append(object[class_name]["attributes"]["dn"])
    return output


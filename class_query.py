import requests
import json
import urllib3
from aci_operation import query_utils as query_utils
from aci_operation import monitor as monitor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def class_query():
    with open('settings.json') as f:
      settings = json.load(f)
      aci_server = settings["aci_server"]
      aci_username = settings["aci_username"]
      aci_password = settings["aci_password"]
    credentials = '{ "aaaUser": { "attributes": { "name":"' + aci_username \
                  + '", "pwd":"' + aci_password + '"}}}'
    session = requests.Session()
    res_body = session.post(aci_server + '/api/aaaLogin.json' \
              , data=json.dumps(json.loads(credentials)), verify=False)
    query_path = query_utils.set_query_path("imdata", 0, "aaaLogin", "attributes", "token")
    token = query_utils.load_value(res_body.text, query_path)

    #############################################################
    # Example of how to list objects in the specified classes
    # Modify object_mapping.json file as needed
    with open("object_mapping.json") as f:
        object_mapping = json.load(f)
    for object_name in object_mapping:
        object_class = object_mapping.get(object_name).get("class")
        object_list = query_utils.class_query(session, aci_server, object_class)
        print ("Class: {}".format(object_class))
        for object in object_list:
            print ("* Obj:{}".format(object))

class_query()




import requests
import json
import urllib3
from aci_operation import query_utils as query_utils
from aci_operation import monitor as monitor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
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
    with open("intf_list.json") as f:
        port_list = json.load(f)
    monitor.show_port_stats(session, aci_server, port_list)    

if __name__ == "__main__":
    main()

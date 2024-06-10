#!/usr/bin/env python3
'''EdgePower trapper script.

Ubiquiti seems to have taken the stance of not providing all attributes via
SNMP. As such this script instead screen scrapes the status data via the web
interface.

It passes the data onto zabbix using zabbix sender (preferably built in
library vs the external executable).

CLI arguments:
1. Mode:
  * poll - Normal polling cycle
  * disc - Discovery run
1. Zabbix Hostname
2. IP / hostname
3. Username
4. Password

URL Paths:
* /api/v1/
    * statistics
        * CPU
        * RAM
        * Temp (board, power supplies)
        * Uptime
        * Power supplies
        * Power output
    * interfaces
        * IPs
        * PoE status
        * lldp status
    * services
        * ssh
        * web
        * syslog
        * ntp
        * lldp / cdp
        * SNMP
        * UNMS

Attributes to monitor:
* Hardware model
* Ping stats
* Serial #
* Software Version
* Batteries
    * Battery Count
    * Battery Replacement Indicator
    * Charge Level
    * Charging Status
    * Last Replace
    * Operational Status
    * Status
    * Temp
    * Time Remaining
    * Voltage
* Power Supply / Outputs:
    * Current
    * Voltage
    * Power
* PSUs:
    * Battery Count
    * Type

Notes:
* How to do low-level discovery using external scripts?
* Template parts to setup / create:
    * items
    * low-level discovery of modules + interfaces
    * triggers
    * graphs
    * dashboards?

'''

# System imports
import pprint
import sys
import urllib3

# External imports
import dotenv
import requests
import zappix.sender



def fetch_data(hostname: str, username: str, password: str) -> dict:
    '''Fetch data from an edgepower.

    '''
    sess = requests.Session()
    res = sess.post(
        f'https://{hostname}/api/v1.0/user/login',
        json={'username': username, 'password': password},
        verify=False,
    )
    # pprint.pprint(res.json())
    x_auth_token = res.headers['x-auth-token']

    data = {}
    for curr_section in ['device','interfaces','services','statistics','system']:
        res = sess.get(
            f'https://{hostname}/api/v1.0/{curr_section}',
            verify=False,
            headers={
                'x-auth-token': x_auth_token,
            }
        )
        data[curr_section] = res.json()

    return data

def main() -> None:
    '''Main
    '''
    #config = dotenv.dotenv_values('.env')
    config = {
        'ZBX_HOSTNAME': sys.argv[1],
        'DEV_HOSTNAME': sys.argv[2],
        'DEV_USERNAME': sys.argv[3],
        'DEV_PASSWORD': sys.argv[4],
    }

    dev_data = fetch_data(
        config['DEV_HOSTNAME'],
        config['DEV_USERNAME'],
        config['DEV_PASSWORD'],
    )

    pprint.pprint(dev_data)

    host_items = {
        'state': dev_data['statistics'][0]['device']['state'],
    }

    trapper_data = []
    for key, value in host_items.items():
        trapper_data.append(zappix.sender.SenderData(
            host  = config['ZBX_HOSTNAME'],
            key   = key,
            value = value,
        ))

    pprint.pprint(trapper_data)
    sender = zappix.sender.Sender('127.0.0.1')
    result = sender.send_bulk(trapper_data)
    # pprint.pprint(result)
    if result.total != result.processed:
        print(f"Error result: {result} -> {trapper_data}")



if __name__ == '__main__':
    urllib3.disable_warnings()
    main()

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

'''

# System imports

# External imports
import requests


def main() -> None:
    '''
    '''

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# coding: utf-8
#

from pyzabbix import ZabbixAPI
import json, sys
import click

################################################################

# PARAMETRIZAR ESSAS VARIAVEIS

URL_ZABBIX = "https://127.0.0.1/zabbix"
USER_ZABBIX = "admin"
PASS_ZABBIX = "passwd"

################################################################


@click.group()
def menu():
    pass

@menu.command()
def discovery():
    hostgroups = zapi.hostgroup.get(output=["name"])

    json_data = [{"{#GROUPID}": i['groupid'],"{#GROUPNAME}": i['name']} for i in hostgroups]

    print(json.dumps({"data": json_data}, indent=4))

@menu.command()
@click.option('--groupid',help='GroupID Zabbix', type=int, required=True)
def coleta(groupid):
        hostgroups = zapi.host.get(output=["name"],
                                groupids=groupid,
                                filter={"status":"0"},
                                countOutput=True)
        print(hostgroups)


if __name__ == "__main__":
    zapi = ZabbixAPI(URL_ZABBIX)
    zapi.login(USER_ZABBIX, PASS_ZABBIX)
    menu()



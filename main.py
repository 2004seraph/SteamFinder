#!/usr/bin/env python3

#This script requires wireshark (libpcap) and steam to be installed.
#In order to get any useful output, you must run this script, wait, then run
#and rerun Steam as many times as you want to sweep your network for clients.

#Made By seraph (https://github.com/Sammot)

import configparser
import pyshark
import os
import requests
from bs4 import BeautifulSoup

steamDiscoveryData = {}

columnSchema = '{:48} | {:18} | {:20} | {:17} | {:8} | {:24} | {:8}'

cls = lambda: os.system('cls' if os.name=='nt' else 'clear')

config = configparser.ConfigParser()
config.read('SteamFinder.ini')

def handle_packet(packet):
    #Dictionary prevents duplicate packet entries
    steamDiscoveryData[str(packet.eth.src)] = columnSchema.format(
        packet.steam_ihs_discovery.body_status_timestamp,
        packet.eth.src,
        packet.steam_ihs_discovery.body_status_hostname,
        packet.steam_ihs_discovery.body_status_user_steamid,
        packet.steam_ihs_discovery.body_status_euniverse,
        str(BeautifulSoup((requests.get('https://steamcommunity.com/profiles/' + str(packet.steam_ihs_discovery.body_status_user_steamid) + '/?xml=1')).content, "lxml-xml").find('steamID').string),
        packet.steam_ihs_discovery.body_status_gamesrunning
    )

    print_info()

def print_info():
    cls()
    print("You can force a refresh by restarting your Steam client, as it will send out another batch of discovery packets")
    print("")
    print(columnSchema.format("Timestamp", "Source MAC", "Hostname", "SteamID", "Universe", "Steam Name", "Playing?"))
    for p in steamDiscoveryData:
        print(steamDiscoveryData[p])

    print("")
    print("A tool by seraph :3")

os.system('mode con: cols=172 lines=40')

print("Waiting for Steam Discovery packets...")
print("")
print("You can force a refresh by restarting your Steam client, as it will send out another batch of discovery packets")

capture = pyshark.LiveCapture(interface=config['NETWORK']["Interface"], display_filter='steam_ihs_discovery.header_msg_type == 1')

#To test this script, uncomment the line below and comment out the line below that one.
#capture = pyshark.FileCapture(input_file='test-example.pcapng', display_filter='steam_ihs_discovery.header_msg_type == 1')
capture.sniff(timeout=50)

capture.apply_on_packets(handle_packet)

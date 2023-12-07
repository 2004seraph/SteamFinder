#!/usr/bin/env python3

"""
SteamFinder By seraph (https://github.com/2004seraph)
LICENSE: GPLv3

This script requires wireshark (libpcap) and steam to be installed.

Usage: You must run this script `python3 steam_lan_capture.py`, wait, then run and rerun
Steam as many times as you want to sweep your network for clients.
"""

from typing import Callable

import requests
from bs4 import BeautifulSoup
import pyshark


class SteamLANCapture:
    """
    Thin wrapper class around a pyshark.LiveCapture instance, just sets it up correctly and exposes a callback
    mechanism. Underlying pyshark capture instance can be accessed via `instance.live_capture`
    """

    # Enum values
    SIMPLE_VIEW = '{:48} | {:18} | {:20} | {:17} | {:8} | {:24} | {:8}'
    RAW_PACKET = "RAW_PACKET"

    def __init__(self, interface: str, online: bool, callback: Callable[[dict], None], *args, **kwargs):
        self.online = online
        self.callback = callback

        self.schema = None
        self.__steam_discovery_data = {}

        self.live_capture = pyshark.LiveCapture(*args, interface=interface,
                                                display_filter='steam_ihs_discovery.header_msg_type == 1', **kwargs)

    def start_network_sniffing(self, timeout: int = 50, schema=RAW_PACKET) -> None:
        """
        Initiates the live capture of packets (execution blocking, consider using asynchronously)
        :param timeout: Pyshark live capture sniffing timeout
        :param schema: Either SteamLANCapture.RAW_PACKET (pyshark object) or SteamLANCapture.SIMPLE_VIEW (formatted)
        """
        self.live_capture.sniff(timeout=timeout)
        self.live_capture.apply_on_packets(self.process_ihsd_detection)
        self.schema = schema

        if schema == SteamLANCapture.SIMPLE_VIEW:
            pass
        elif self.schema == SteamLANCapture.RAW_PACKET:
            pass
        else:
            raise AttributeError("Invalid schema")

    def process_ihsd_detection(self, packet) -> None:
        """
        Individual captured packet processing function
        :param packet: pyshark packet
        """
        if self.schema == SteamLANCapture.SIMPLE_VIEW:
            # Dictionary prevents duplicate packet entries
            self.__steam_discovery_data[str(packet.eth.src)] = SteamLANCapture.SIMPLE_VIEW.format(
                packet.steam_ihs_discovery.body_status_timestamp,
                packet.eth.src,  # MAC
                packet.steam_ihs_discovery.body_status_hostname,
                packet.steam_ihs_discovery.body_status_user_steamid,
                packet.steam_ihs_discovery.body_status_euniverse,
                str(  # Get their Steam name
                    BeautifulSoup((requests.get(
                        'https://steamcommunity.com/profiles/'
                        + str(packet.steam_ihs_discovery.body_status_user_steamid)
                        + '/?xml=1')).content, "lxml-xml")
                    .find('steamID').string) if self.online else " - ",
                packet.steam_ihs_discovery.body_status_gamesrunning
            )
            self.callback(self.__steam_discovery_data)
        elif self.schema == SteamLANCapture.RAW_PACKET:
            self.callback(packet)
        else:
            raise AttributeError("Invalid schema")


if __name__ == "__main__":
    """
    Simple console app for quick usage of the tool, displays a live-updating table of previously discovered clients.
    To use, simply run `python3 steam_lan_capture.py` in your terminal, or click on it.
    """

    import configparser
    import os
    import subprocess
    from os.path import exists

    CONFIG_FILE = "SteamFinder.ini"


    def cls():
        return lambda: os.system('cls' if os.name == 'nt' else 'clear')

    def print_table(steam_discovery_data: dict):
        cls()
        print("You can force a refresh by restarting your Steam client, "
              "as it will send out another batch of discovery packets")
        print("")
        print(SteamLANCapture.SIMPLE_VIEW.format(
            "Timestamp", "Source MAC", "Hostname", "SteamID", "Universe", "Steam Name", "Playing?"))
        for p in steam_discovery_data:
            print(steam_discovery_data[p])

        print("")
        print("A tool by seraph :3")


    config = configparser.ConfigParser()
    if exists("./" + CONFIG_FILE):
        config.read(CONFIG_FILE)
    else:
        config['NETWORK'] = {
            "Online": "True",
            "Interface":
                subprocess.getoutput("route | grep '^default' | grep -o '[^ ]*$'") if os.name == "posix" else
                "Ethernet"
        }
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

        print("First-time run: Created new config file in current directory, exiting...")
        exit()

    client_sniffer = SteamLANCapture(config['NETWORK']["Interface"], config['NETWORK']["Online"] == "True", print_table)

    os.system('mode con: cols=172 lines=40')
    print("Waiting for Steam Discovery packets...")
    print("")
    print("You can force a refresh by restarting your Steam client, "
          "as it will send out another batch of discovery packets")

    client_sniffer.start_network_sniffing()

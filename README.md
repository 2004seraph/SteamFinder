# SteamFinder
 
A compact little python script which watches the Steam client's auto LAN discovery packets (for Steam's In-Home Streaming) and logs other Steam clients on the local network.

## Requirements

- Python 3
- Pip
- Wireshark + tshark
- A Steam client

## How To Use

Once all the required tools are added to your `PATH`, run either of the `INSTALL` scripts depending on which OS you use to set up the required python packages. This script has been verified to work on Microsoft Windows and Linux, but not MacOS.

This script requires you to have Steam installed and to be signed in to it. You must kill the Steam program, run this script, re-run Steam and then wait. You will gradually start discovering other clients on your network.

This script's reliance on the actual Steam client on your computer is a limitation, but the way I see it this means it should work even if Steam were to update their packet schema.

### Network Interface

The config file `SteamFinder.ini` is set up to use the default `Ethernet` interface from Microsoft Windows, if you don't use Ethernet or use another OS, you'll want to change this before running the script. You can see a list of your PC's interface names when you first start up Wireshark, it will display valid interfaces to start packet sniffing on. Do not put quotes in the config file.

## Hardening Your Own Client

You can hide your Steam client from being detected by this script by disabling Streaming and other LAN functions in your settings - consequently this also means the script cannot use your client to sniff others.

## Important Information

Use responsibly and legally in your country. A general rule of thumb is if it's not your network, it's not your right to sniff. 

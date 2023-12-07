# SteamFinder
 
A little python console script that watches the Steam client's auto LAN discovery packets (for Steam's In-Home Streaming feature) and logs information on the other Steam clients on the local network.

It can detect clients appearing offline and also steam running in offline mode, because you're still able to stream.

## Requirements

- Python 3
    - pip
- Wireshark + tshark
- A Steam client (and account)
- An internet connection for requests to Steam's API: allows for Steam name retrieval

## How To Use

Once all the required tools are added to your `PATH`, run either of the `INSTALL` scripts depending on which OS you use to set up the required python packages. This script has been verified to work on Microsoft Windows and Linux, but not MacOS.

This script requires your Steam client to be signed in. To start:
- You must kill the Steam program (*Exit Steam*)
- run this script from your terminal: `python3 main.py`, keep the console open - this is where the results appear
- re-run Steam after starting the script and then wait (booting Steam sends a massive burst of discovery packets, we want to watch them)

You will then gradually start discovering other clients on your network, the script can be left running along with the Steam client and it will continue to add newly discovered clients to the list.

This script's reliance on the actual Steam client on your computer is a limitation, but the way I see it this means it should work even if Steam were to update their packet schema.

### Network Interface

The config file `SteamFinder.ini` is set up to use the default `Ethernet` interface from Microsoft Windows, if you don't use Ethernet or use another OS, you'll want to change this before running the script. You can see a list of your PC's interface names when you first start up Wireshark, it will display valid interfaces to start packet sniffing on. Do not put quotes in the config file.

WiFi interfaces may not work with this script since *Wireshark* needs an interface to support **promiscuous mode** to sniff packets not for your machine - most Ethernet interfaces support this, only some WiFi interfaces do, YMMV.

## Hardening Your Own Client

You can hide your Steam client from being detected by this script by disabling Streaming and other LAN functions in your settings - consequently this also means the script cannot use your client to sniff others.

## Important Information

Use responsibly and legally in your country. A good rule of thumb is if it's not your network, it's not your right to poke/mess around with it. Rights and responsibilities can be found in the [License](LICENSE).

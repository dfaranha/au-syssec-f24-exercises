This file contains hints for environments other than the VirtualBox running Ubuntu in case your computer is not supported (like ARM-based Macs).

## Preliminaries: Installing software

### macOS

```
sudo brew install aircrack-ng libpcap libnet
```

You should install Wireshark natively by downloading from the [official website](https://www.wireshark.org/download.html).

## Exercise 1: Scanning the network

### GNU/Linux

You can scan the wireless networks by running:

```
iwlist <wifi_interface> scan
```

### macOS

Hold the `option` key and click the wireless icon in the menu bar, and it should give information about the various wireless networks.

### Windows

Apparently, you can scan the wireless networks by running:

```
netsh wlan show all
```

## Exercise 3: ARP Spoofing

Alternatives to the `dnisff` package can be found below.

### macOS

This experimental port of the `arpspoof` command to Mac OS X for [Intel](https://github.com/SuperMarcus/macos-arpspoof) or [ARM]( https://github.com/hjkeller16/macos-arpspoof) Macs should work.

Please notice that cloning software from a random GitHub repository and running it with root privileges goes against **everything** we teach in this course!

### Windows

At the time of writing, ARP spoofing does not play well with the WSL virtualized network interface.
Install native versions of Wireshark and an [ARP spoofer](https://github.com/alandau/arpspoof).

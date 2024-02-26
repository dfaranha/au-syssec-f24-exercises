# Exercises: Link Layer Security

There are some hints and troubleshooting information [in this page](hints.md). Make sure to check it if you have problems or if you are running a native enrivonment without support to virtualization (such as an ARM-based Mac). 

## Preliminaries

You should begin by installing required dependencies.

### Ubuntu 22.04 Virtual Machine

```
sudo apt install net-tools aircrack-ng dsniff wireshark
```

Wireshark will ask about users without priviledges being able to capture packets, for which you should answer affirmatively.


## Exercise 1: Dictionary Attack

The first exercise requires breaking into one of the wireless networks available in the classroom by running a dictionary attack.
There are two access points, with SSIDs `NETSEC` and `SYSSEC`, both configured to use WPA2-PSK with a **weak** password.
Note that these two networks have different addresses: `192.168.1.0/24` and `192.168.2.0/24`, respectively.

A typical attack starts by placing your network interface in _monitor_ mode, and then capturing traffic from other devices.
For attacking WPA-PSK2, a common approach is to capture the handshake packets when a new device enter the network, or alternatively to force the deauthentication of a device so it connects again and the handshake can be captured.

Because not all interfaces support monitor mode and this functionality is typically not available in Virtual Machines, we already provide packet captures of the handshake for the two access points in this repository, and refer interested readers to [a tutorial](https://www.aircrack-ng.org/doku.php?id=cracking_wpa) for more details.

Your first task is to find a dictionary of common words in English to run the attack, and to discover the link layer address (MAC) of the access point.
With these informations, you can then run:

```
aircrack-ng -w <dictionary_file> -b <link_layer_address> <packet_capture>
```

You should be able to obtain the correct password after a few minutes of computation.

**Hint**: You can find the link layer address by looking at the packet captures in the repository. If you want to find it yourself by scanning the network, hints for your _native_ operating system can be found [here](hints.md).

## Exercise 2: Sniffing the network

One immediate consequence of an attacker having access to traffic in plaintext at the link layer is the natural possibility of capturing sensitive data. This is especially dangerous in wireless networks, since essentially anyone within distance has access to the communication channel.

In this exercise, we will observe how sniffing works in practice. We will take the opportunity to assemble and verify a networking environment for the next exercises in the course, so please check your setup carefully.

### Material

You will need to have the Wireshark tool installed as per the dependencies above. You should also add your user to the group `wireshark` so that no root priviledges are required for sniffing (after adding your user to a new group, you need to logout and login again for the change to apply).
You will also need to configure your VM network interface to allow all network traffic to be captured inside the VM.

In VirtualBox, I had to change the Network Settings such that my Network Adapter was Attached to a Bridged Adapter. In Advanced, I marked Allow All in the Promiscuous Mode to be able to capture traffic from the host environment inside the VM. The screenshot below shows the settings:

![VirtualBox network configuration](vb-network.png)

### Procedure

We will abstract the Virtual Machine as a hostile node in a wireless network. Although the scenarios are obviously not the same, it should serve the illustration purposes we need here.

1. After the settings are changed, run Wireshark inside the Virtual Machine. You should be able to start a Capture session by clicking directly on the Shark symbol, and- all traffic from the host should become immediately visible. If you are completely new to Wireshark, a nice tutorial for beginners can be found at https://www.youtube.com/watch?v=TkCSr30UojM

2. We can perform more directed sniffing by restricting to a hostname. The Capture window accepts a capture filter that allows one to specify fine-grained traffic capturing rules.
To show how that works, we have an HTTP server running in the same network on every IP in the range `192.168.1.2--49` or `192.168.2.2--49`, depending on your network.
Pick one IP address in the range randomly and start a new capture with `host 192.168.X.Y` as the capture filter (replace `X` and `Y` with the actual address).

3. Now access the IP address on the host machine at port `8000` by typing `http://192.168.X.Y:8000/` in your browser. Since the VM uses a bridged interface, you should be able to see the plaintext HTTP traffic in Wireshark.

## Exercise 3: ARP Spoofing

We will use a classical ARP Spoofing attack to redirect traffic from a host in the local network to a malicious machine. Traffic redirection is a typical lower-level intermediate step in a higher-level attack such as man-in-the-middle at the network/transport layer. We will play with those in the next weeks, so today we will just focus on the link layer.

1. Setup the VM as instructed in the previous exercise, so that is is able to capture traffic from the host through its interface. Notice that this does not allow the VM to capture traffic to/from other machines connected in the same local wireless network.

2. Connect a mobile device to the same wireless network (`SYSSEC` or `NETSEC`) you have your host machine connected. Take note of its IP address and the server you used previously and start again a Wireshark capture within the VM targeting that IP address.

3. Open the address `http://192.168.X.Y:8000/` in your mobile device. You should see the same web page as you saw in the host. Click on the Login page in the top right corner.

4. Run ARP spoofing to poison the ARP cache of your mobile device (using the `-t` option) with the MAC address of the VM instead of the real server. Replace the interface (mine is `enp0s3`), the IP address (of your mobile) and of the server (that you picked randomly) in the command below. Note that the `arpspoof` command takes IP addresses as arguments.

```
$ sudo arpspoof -i <interface> -t <address> <server>
```

5. Now generate traffic from the mobile device by logging in with any username/password combination. You should suddenly see the traffic directed to your mobile in Wireshark.
This can include ARP traffic, TCP retransmission attempts and luckily an HTTP POST method sending the username/password.

6. Try a few times if it does not work at the first time, as there is a race condition between the ARP spoofing responses and the real ARP traffic. If successful, you should see the something similar to the screenshot below.

![image](https://user-images.githubusercontent.com/5369810/135161121-8879b20a-8ae0-4bb5-abaa-431015ce3351.png)

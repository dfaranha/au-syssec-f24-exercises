# Exercises: Transport Layer Security

## Preliminaries

We do not require any new dependencies for this exercise beyond what was installed in the last exercise. Make sure to have Wireshark and `mitmproxy` installed in your VM in bridged mode.

**Observation**: If your VM is not working you can also install Wireshark and `mitmproxy` in your own host machine. In that case, replace referrences to IP address `192.168.1/2.Z` with `192.168.1/2.Y` as per the diagram below.

### Network Layout and Preparation

This time the network will be simpler than the previous one, but will follow the same general layout, depicted below.

As previously, there are two wireless networks (`NETSEC` and `SYSSEC`), and the wired network is on subnetwork `192.168.3.0/24`.
Now the Access Point (AP) serves as the _router_ between the wireless and the wired network.
The Web server runs on a Raspberry Pi in the wired network, with IP addresses in the range `192.168.3.2-69`, and abstracts a machine running on the Internet, to/from which traffic is routed by intermediate nodes.

![image](https://github.com/dfaranha/au-syssec-f23/blob/master/exercises/06_transport_layer_security/network-layout.png)

Pick an IP address `192.168.3.W` in the range `192.168.3.2-69`.
Connect to one of the wireless networks using the host system (you know the password) and test that you can connect to `http://192.168.3.W/` using a Web browser (this time we are using the default port `80`).
The traffic between your browser and the server is now being routed by the AP with manually inserted static routes.

Start the VM and make sure that you can `ping 192.168.3.W` and access the HTTP address above in the VM.
Verify that you can capture traffic between the host and `192.168.3.W` using Wireshark running in the VM, to confirm that the interface is functional in bridged mode.
Now access `https://192.168.3.W/` (HTTPS) and you will receive a warning about the self-signed certificate, which you should accept as trusted.

## Exercise 1: Malicious-in-the-middle against HTTP

Connect a mobile device to the wireless network and take note of its address `192.168.1/2.X`, referred from here on as `mobile`.
You can typically find the IP address of your mobile device by looking into the network configurations.
In the VM, type `ifconfig` or `ip a` in a terminal and take note of its IP address `192.168.1/2.Z`

**Observation**: If you do not have a mobile device available, ask a colleague to be the client or use the host machine as the victim.

Change the network configuration of your mobile device manually. On Android, this means changing the `IP Settings` to `Static`.
Use the same `192.168.1/2.X` as the IP address, `192.168.1/2.Z` as the Gateway/DNS and `255.255.255.0` as the network mask.

In the VM, let's change the configuration for traffic to be forwarded.
The following configurations need to be performed to enable IP forwarding such that the VM can forward IPv4 traffic while avoiding ICMP redirects:

```
$ sudo sysctl -w net.ipv4.ip_forward=1
$ sudo sysctl -w net.ipv4.conf.all.send_redirects=0
```

We will run `mitmproxy` in the VM to be able to perform some processing of the captured traffic. First, configure the `iptables` firewall to send all HTTP traffic captured at ports `80` and `443` in the VM to port `8080` under control of `mitmproxy`:

```
$ sudo iptables -A FORWARD --in-interface <interface> -j ACCEPT
$ sudo iptables -t nat -A PREROUTING -i <interface> -p tcp --dport 80 -j REDIRECT --to-port 8080
$ sudo iptables -t nat -A PREROUTING -i <interface> -p tcp --dport 443 -j REDIRECT --to-port 8080
```

Now run `mitmproxy` in _transparent_ mode. Notice that we need it to accept the self-signed certificate from the Web server:

```
$ mitmproxy --ssl-insecure --mode transparent --showhost
```

**Observation**: If you are running `mitmproxy` in your host system directly (without a VM), make the same configurations above in your host machine firewall.

If everything is working correctly, you should try again to access the Web server `http://192.168.3.W/` in your mobile device and start seeing captured _flows_ in the `mitmproxy` window.
In this window, you can select a flow by using the arrows and pressing ENTER, while pressing the letter `q` goes back to the overview screen.

**Observation 1**: If you **cannot** see flows in `mitmproxy`, try running the command below to bypass [a problem with the VirtualBox driver](https://security.stackexchange.com/questions/197453/mitm-using-arp-spoofing-with-kali-linux-running-on-virtualbox-with-bridged-wifi):

```
sudo arpspoof -i <interface> -t <mobile> 192.168.3.W
```

**Observation 2**: If you still **cannot** see flows in `mitmproxy`, try restoring your `IP Settings` configuration to DHCP and configure ``192.168.1/2.Z`` as the `Proxy` running on port `8080`. Replace the command line above to run `mitmproxy` in _proxy_ mode:

```
$ mitmproxy --ssl-insecure --showhost
```
Access the Login page, enter some credentials and observe that they are visible in `mitmproxy` as part of an `HTTP POST` method.

## Exercise 2: Malicious-in-the-middle against HTTPS

Now try accessing `https://192.168.3.W/` in your mobile device.
You should get another warning about a non-trusted certificate! Inspect the certificate and check that it is suspicious indeed. :)
After accepting the new certificate, you should be able to access the website normally.
Make sure you access the Login page again and that captured credentials are still visible.

## FALLBACK: Running in proxy mode

If everything above fails, we can try a simple configuration that depends on the client forcing the traffic to pass through the adversary. This is not realistic for an attack in the local network, but it captures an attacker in a privileged network position.

Run `mitmproxy` in _proxy_ mode:

```
$ mitmproxy --ssl-insecure --showhost
```

Now manually configure the address of the machine running `mitmproxy` (port 8080) as the proxy in your mobile. All the HTTP traffic should now be captured by `mitmproxy` by definition.

## BONUS: Manipulate traffic in mitmproxy

If you reached here we have a bonus round for you. For this last exercise, we will simplify our setup to remove ARP spoofing.
Configure the gateway in your mobile device to point directly to the IP address of the VM and stop the execution of the `arpspoof` program.

Let's use the scripting capability of `mitmproxy` to mount an _active_ attack.
Our simple website has a login capability, for which the credentials are `admin`/`admin`.

Now access the website through your mobile device with the right credentials and login. You should now be able to access the `View Secrets` and `Upload Secrets` functionalities.
The `View Secrets` functionality will just show you some secret text, which should be visible in `mitmproxy` as well.
The `Upload Secrets` functionality is more interesting and allows the user to encrypt a message under a public key returned by the server.
Your final task is to _replace_ that public key with a key pair for which you know the private key (to be able to decrypt).
The code for the server portion is provided for reference in the repository inside the folder `simple-website`.

In order to achieve your goal, generate an RSA key pair in PEM format and plug the values marked as TODO in the file `simple-website/mitm_pk.py`. Now restart `mitmproxy` with the command below:

```
$ mitmproxy --mode transparent --showhost -s mitm_pk.py
```

Recover the message from the encryption provided by the client.

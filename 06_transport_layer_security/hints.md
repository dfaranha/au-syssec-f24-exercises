This file contains hints for macOS and Windows.

## Windows (native)

The mitmproxy [website](https://docs.mitmproxy.org/stable/howto-transparent/) has some hints to configure routing on Windows. You should also take the opportunity to disable the firewall.

## MacOS

To forward traffic on macOS:

```
sudo sysctl -w net.inet.ip.forwarding=1
sudo sysctl -w net.inet.ip.redirect=0
```

For configure the firewall, it may be necessary to [disable System Integrity Protection (SIP)](https://developer.apple.com/documentation/security/disabling_and_enabling_system_integrity_protection). To do so, restart your laptop in recover mode by holding the power button down while powering up. Launch the terminal from the Utilities menu and run the command `csrutil disable`.

To configure the firewall, create file `/etc/pf.anchors/redirection` and add the single line:
```
rdr pass inet proto tcp from any to any port 8000 -> localhost port 8080
```

Then reference this file in existing file `/etc/pf.conf`, adding a line `rdr-anchor "redirection"` after the other 'rdr-anchor' lines, and add `load anchor "redirection" from "/etc/pf.anchors/redirection` at the end of the file. To use this rule, enable pf, running

```
sudo pfctl -d
sudo pfctl -e
```

This approach successfully implements the rules; however, working with mitmproxy is still causing bugs and traffic was not forwarded by the firewall.
There are additional instructions at the [official docs](https://docs.mitmproxy.org/stable/howto-transparent/), but we could not get them working.

Feel free to give it a try and let us know if it works!

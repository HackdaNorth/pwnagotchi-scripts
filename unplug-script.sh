#!/bin/bash

# Check if wlan1mon exists
if iw dev | grep -q 'wlan1mon'; then
    # Disable the wlan1mon interface
    ip link set dev wlan1mon down
    RESULT=$?
    # if interface was successfully taken down, continue
    if [ "$RESULT" = "0" ]; then
        # Set the device in managed mode
        iw dev wlan1mon set type managed

        # Assign the original interface name
        ip link set dev wlan1mon name wlan1

        # Bring the interface up
        ip link set dev wlan1 up
    fi
fi
    # Check the config file
    if grep -q 'main.iface = "wlan1mon"' /etc/pwnagotchi/config.toml; then
        # Change the interface name in the config file
        sed -i 's/main.iface = "wlan1mon"/main.iface = "wlan0mon"/' /etc/pwnagotchi/config.toml

        # Restart pwnagotchi
        systemctl restart pwnagotchi
    fi
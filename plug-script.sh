#!/bin/bash

# Check if wlan1 exists
if iw dev | grep -q 'wlan1'; then
    # Disable the wlan1 interface
    ip link set dev wlan1 down
    RESULT=$?
    # if interface was successfully taken down, continue
    if [ "$RESULT" = "0" ]; then
      # disable interfering processes
        PROCESSES="wpa_action\|wpa_supplicant\|wpa_cli\|dhclient\|ifplugd\|dhcdbd\|dhcpcd\|udhcpc\|NetworkManager\|knetworkmanager\|avahi-autoipd\|avahi-daemon\|wlassistant\|wifibox\|net_applet\|wicd-daemon\|wicd-client\|iwd"
        badProcs=$(ps -A -o pid=PID -o comm=Name | grep "${PROCESSES}\|PID")

        for pid in $(ps -A -o pid= -o comm= | grep ${PROCESSES} | awk '{print $1}'); do
                command kill -19 "${pid}"
        done

# echo "${badProcs}"

    # Set the device in monitor mode
    iw dev wlan1 set monitor none

    # Assign a new monitor interface name
    ip link set dev wlan1 name wlan1mon

    # Bring the interface up
    ip link set dev wlan1mon up

    # Set the channel and txpower
    iw dev wlan1mon set channel 6
    sleep 3
    iw dev wlan1mon set txpower fixed 3000
    sleep 3

    # Check the config file
    if grep -q 'main.iface = "wlan0mon"' /etc/pwnagotchi/config.toml; then
        # Change the interface name in the config file
        sed -i 's/main.iface = "wlan0mon"/main.iface = "wlan1mon"/' /etc/pwnagotchi/config.toml

        # Restart pwnagotchi
        systemctl restart pwnagotchi
    fi

    echo "The device is now in monitor mode with interface wlan1mon."
    fi
else
    echo "The wlan1 interface does not exist."
fi
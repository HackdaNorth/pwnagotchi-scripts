Some random scripts I found and or made. 

------
make sure your idVendor, and idProduct match within the udev rules, and make sure your scripts are executeable! 
udev rule will run each time the device is either unplugged, or plugged in and modifiying the config.toml at the same time.

#plug-script.sh 

#unplug-script.sh 

#usb udev rules 

created by "https://www.reddit.com/user/attrib/"

Here is the explanation by attrib, "https://www.reddit.com/r/pwnagotchi/comments/1c3qw48/comment/l0bif17"

If that comment ever gets removed, I will have no idea what I am doing, so I copy pasted it into Realtek_tut.txt just in case....

---------


Realtek driver is 8812au-20210829, see here --> https://github.com/HackdaNorth/8812au-20210629 
You can clone it from here as well and find more detailed information regarding the original creator and installation instructions. 
I've forked it since the original creator removed it and no longer supports monitor mode in the newer verisons. I have not tested them.

Monitor mode script is also included, although it is not needed since the scripts attrib created do the exact same but for pwnagotchi. If you'd like to send the adapter into monitor mode etc without pwnagotchi, just use the monitor mode script and run it after plugging in your adapter and drivers are installed, select ./start_mon.sh [interface of adapter]



#Guarda watches for a internet connection, once found, starts transfering files!
import pwnagotchi.plugins as plugins
import pwnagotchi
import logging
import subprocess
import time

class HomeBase(plugins.Plugin):
    __author__ = '@HackdaNorth'
    __version__ = '0.1.0'
    __license__ = 'GPL3'
    __description__ = 'Connects to home network for internet when available'

    def __init__(self):
        self.ready = 0
        self.status = ''
        self.network = ''
        self.current_ssid = ''

    def on_loaded(self):
        for opt in ['ssid', 'password', 'minimum_signal_strength']:
            if opt not in self.options or (opt in self.options and self.options[opt] is None):
                logging.error(f"[Guarda] Option {opt} is not set.")
                return
        _log("plugin loaded")
        self.ready = 1

    def get_ssid(self):
        result = subprocess.run(["/usr/sbin/iwgetid", "wlan0", "-r"], capture_output=True, text=True)
        return result.stdout.strip()

    def match_ssid(self):
        current_ssid = self.get_ssid()
        target_ssid = self.options['ssid']
        if current_ssid:
            self.status = 'wifi_detected'
            _log(f"Current SSID: {current_ssid}")

            if current_ssid == target_ssid:
                _log(f"Connected to target SSID: {target_ssid}")
                self.status = 'uploading'
                self.execute_commands()
                self.status = 'finished'
            else:
                _log(f"Connected to a different SSID: {current_ssid}")
                self.status = 'Not_connected'
        else:
            _log("Interface wlan0 is down")
            self.status = 'Not_connected'

    def execute_commands(self):
        self.status = 'waiting'
        _log("Running commands...")
        _run("sudo cp -r /root/handshakes/ /home/pi/currentBackup/ && sudo cp /root/brain.nn /home/pi/currentBackup/brainBackup/ && sudo cp /root/brain.json /home/pi/currentBackup/brainBackup/")
        _run("cd /home/pi && scp -r -o IdentityFile=~/.ssh/id_ed22519 -P 768 /home/pi/currentBackup/* iridium@10.159.1.54:/mnt/nvme/pwnagotchi_backup/")
        _log("Commands executed...")

    def on_ui_update(self, ui):
        if self.status == 'Not_connected':
            ui.set('face', '(ﺏ__ﺏ)')
            ui.set('status', 'Not connected to wifi....')
        elif self.status == 'wifi_detected':
            ui.set('face', '(◕‿‿◕)')
            ui.set('status', f'Found home network at {self.network} ...')
        elif self.status == 'uploading':
            ui.set('face', '(*‿‿*)')
            ui.set('status', 'We\'re home! Uploading files mode ...')
        elif self.status == 'waiting':
            ui.set('face', '(◕‿◕ )')
            ui.set('status', 'Waiting for files to finish...')
        elif self.status == 'finished':
            ui.set('face', '(ᵔ◡◡ᵔ)')
            ui.set('status', 'All Transfers are finished!!')

    def on_epoch(self, agent, epoch, epoch_data):
        self.match_ssid()

def _run(cmd):
    result = subprocess.run(cmd, shell=True, stdin=None, stderr=None, stdout=subprocess.PIPE, executable="/bin/bash")
    return result.stdout.decode('utf-8').strip()

def _log(message):
    logging.info('[home_base] %s' % message)

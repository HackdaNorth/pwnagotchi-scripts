#Guarda watches for a internet connection, once found, starts transfering files!
import pwnagotchi.plugins as plugins
import pwnagotchi
import logging
import subprocess
import time

class HomeBase(plugins.Plugin):
    __author__ = '@HackdaNorth'
    __version__ = '0.3.0'
    __license__ = 'GPL3'
    __description__ = 'Transfers files to your home base, after finding the connection'

    def __init__(self):
        self.ready = 0
        self.status = ''
        self.network = ''
        self.current_ssid = ''

    def on_loaded(self):
        _log("plugin loaded")
        self.ready = 1

    def get_ssid(self):
        result = subprocess.run(["/usr/sbin/iwgetid", "wlan0", "-r"], capture_output=True, text=True)
        return result.stdout.strip()

    def on_internet_available(self,agent):
       if not self.ready:
           return
        _log("Checking connection ...")
        current_ssid = self.get_ssid()
        target_ssid = self.options['ssid']
        if current_ssid:
            self.status = 'wifi_detected'
            _log(f"Current SSID: {current_ssid} ...")

            if current_ssid == target_ssid:
                _log(f"Connected to target SSID: {target_ssid} ...")
                self.status = 'uploading'
                _execute_commands(self)
                self.status = 'finished'
            else:
                _log(f"Connected to a different SSID: {current_ssid} ...")
                self.status = 'Not_connected'
        else:
            _log("Not Connected ... awaiting internet connection")
            self.status = 'Not_connected'
        else:
            _log("Not at home.. awaiting internet connection...")
            self.status = 'Not_connected'

    def _execute_commands(self):
        self.status = 'waiting'
        time.sleep(5)
        _log("Running commands...")
        process = _run('sudo sh /home/pi/backup.sh')
        self.status = 'uploading'
        time.sleep(15)
        _log("Sleeping 15 seconds waiting for script execution to finish....")
        process.wait()
        self.status = 'finished'
        _log("Commands executed...")

    def on_ui_update(self, ui):
        if self.status == 'Not_connected':
            ui.set('face', '(ﺏ__ﺏ)')
            ui.set('status', 'Not connected to wifi ...')
        elif self.status == 'wifi_detected':
            ui.set('face', '(ᗒᗨᗕ)')
            ui.set('status', f'Found home network at {self.network} ...')
        elif self.status == 'uploading':
            ui.set('face', '(*‿‿*)')
            ui.set('status', 'We\'re home! Uploading files mode ...')
        elif self.status == 'waiting':
            ui.set('face', '(⊙︿⊙)')
            ui.set('status', 'Waiting for files to finish ...')
        elif self.status == 'checking':
            ui.set('face', '(⌐■_■)')
            ui.set('status', 'Checking for wifi ...')
        elif self.status == 'finished':
            ui.set('face', '( ﾟДﾟ)b')
            ui.set('status', 'All Transfers are finished !!!')
        elif self.status == 'failed':
            ui.set('face', '(¬_¬)')
            ui.set('status', 'Transfers failed ...')

def _run(cmd):
    result = subprocess.run(cmd, shell=True, stdin=None, stderr=None, stdout=None, executable="/bin/bash")
    return result.stdout.decode('utf-8').strip()

def _log(message):
    logging.info('[Guarda] %s' % message)

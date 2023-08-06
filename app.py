from flask import Flask, request, render_template
import os
import subprocess
import time
from threading import Timer
app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

def reboot():
    subprocess.run(['sudo', 'reboot', 'now'])

def run_command(command):
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if process.returncode != 0:
        print(f"Error: {' '.join(command)} failed with error code {process.returncode}")
        print(f"stderr: {process.stderr.decode().strip()}")
    else:
        print(f"Success: {' '.join(command)}")

@app.route('/', methods=['POST'])
def submit():
    ssid = request.form.get('ssid')
    password = request.form.get('password')

    print(f"SSID: {ssid}, Password: {password}")

    # Create a new wpa_supplicant.conf file
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f:
        f.write(
            'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n'
            'update_config=1\n'
            'country=SI\n'  # Change this to your country code
            '\n'
            'network={\n'
            f'    ssid="{ssid}"\n'
            f'    psk="{password}"\n'
            '}\n'
        )

    # Restart the wpa_supplicant service
    subprocess.run(['sudo', 'systemctl', 'restart', 'wpa_supplicant'])

    with open('/etc/dhcpcd.conf', 'r') as f:
        lines = f.readlines()

    ap_config = [
        'interface wlan0\n',
        '    static ip_address=192.168.4.1/24\n',
        '    nohook wpa_supplicant\n'
    ]

    # Remove the AP configuration lines
    lines = [line for line in lines if line not in ap_config]

    with open('/etc/dhcpcd.conf', 'w') as f:
        f.writelines(lines)

    # Run commands
    run_command(['sudo', 'service', 'dhcpcd', 'restart'])

    run_command(['sudo', 'systemctl', 'stop', 'hostapd'])
    run_command(['sudo', 'systemctl', 'disable', 'hostapd'])  # Disable hostapd service

    run_command(['sudo', 'systemctl', 'stop', 'dnsmasq'])
    run_command(['sudo', 'systemctl', 'disable', 'dnsmasq'])  # Disable dnsmasq service

    Timer(20, reboot).start()

    
    return 'WiFi configuration updated. The device will now restart.'
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

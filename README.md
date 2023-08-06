# Wifi-provisioning

The main goal of the project is Wifi provisioning on Raspberry pi model 4. The user has 2 options when accessing the Raspberry pi server: 
1. To first set Wifi credentials (SSID and password), and after submitting the changes, Raspberry pi reboots and connects to the specified Wifi.
2. If Raspberry pi is already connected to the wifi, the user can press the AP mode button and RPI returns into access point mode.

## Getting Started

If you choose to use RPI image file to load OS, all prerequisites are already installed and running. Python script is also running as a service, so there is no need to run the script. For it to work, you just need to download the image file to RPI and boot it. To access Wifi provisioning, connect to the RPI AP via available Wifi Options (name blaz), then search for http://raspberrypi.local/ in the selected browser. If you have already put in Wifi credentials, you have to be connected to the same Wifi as RPI to be able to access settings with the following address: http://raspberrypi.local/. 

### Prerequisites

If you didn't use the given OS image, then you need Raspberry pi with Wifi module and RPI OS 32 lite for the code to work. Files given in the source code are just for application and there are still some packages and files you need to modify if you want it to work. 

1. You need to install: 
 - sudo apt-get install dnsmasq hostapd
2. Then stop those two services to be able to configure them:
 - sudo systemctl stop dnsmasq
 - sudo systemctl stop hostapd
3. Configure a static ip adress of wlan0, by editing dhcpcd.conf file:
 - sudo nano /etc/dhcpcd.conf
4. Add the following lines to the end of the dhcpcd.conf file:
 - interface wlan0
 - static ip_address=192.168.4.1/24 (or select the ip address you want when it's in AP mode)
 - nohook wpa_supplicant
5. Restart dhcpcd service:
  - sudo service dhcpcd restart
6. Edit dnsmasq.conf file and add the following lines:
  - interface=wlan0
  - dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
7. Configure hostapd.conf file, and add the following lines:
  - interface=wlan0
  - driver=nl80211
  - ssid=YourNetworkSSID          (select SSID for AP mode)
  - wpa_passphrase=YourPassword   (select psk for AP mode)
8. Find the line #DAEMON_CONF and replace it with DAEMON_CONF="/etc/hostapd/hostapd.conf"
  - sudo nano /etc/default/hostapd
9. Configure the system to start the services at boot:
  - sudo systemctl unmask hostapd
  - sudo systemctl enable hostapd
  - sudo systemctl start hostapd
  - sudo systemctl start dnsmasq
10. Enable routing of the internet traffic:
  - sudo nano /etc/sysctl.conf
11. Reboot the system
12. After rebooting, navigate to the working directory where you have the script saved and run it with python3 command. 


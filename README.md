# wifi-provisioning

Main goal of the project is Wifi provisioning on Raspberry pi model 4. User has 2 options when accessing Raspberry pi server, To set Wifi credentials (SSID and password), after submiting the changes Raspberry pi reboots and connects to the specified Wifi. If Raspberry pi is already connected to the wifi, user can press AP mode button and RPI returns into access point mode.

## Getting Started

If you choose to use RPI image file to load OS all prerequisites are already installed and running. Python script is also running as a service, so there is no need to run the script, for it to work you just need to download image file to RPI and boot it. To access Wifi provisioning connect to the RPI AP via available Wifi Options (name blaz), to then connect to the settings in selected browser search for http://raspberrypi.local/. If you already put in Wifi credentials, you have to be connected to the same Wifi as RPI to be able to access settings with address: http://raspberrypi.local/. 

### Prerequisites

If you didnt use given OS image, then for the code to work you need raspberry pi with Wifi module and RPI OS 32 lite. Files given in the source code are just for application and there are still soma packages and files you need to modifiy if you want it to work. 

1. You need to install: 
 - sudo apt-get install dnsmasq hostapd
2. Then stop those two services to be able to configure them
 - sudo systemctl stop dnsmasq
 - sudo systemctl stop hostapd
3. Configure a static ip adress of wlan0, by editing dhcpcd.conf file:
 - sudo nano /etc/dhcpcd.conf
4. Add the followwing lines to the end of the dhcpcd.conf file:
 - interface wlan0
 - static ip_address=192.168.4.1/24 (or select ip address you want when its in AP mode)
 - nohook wpa_supplicant
5. restart dhcpcd service:
  - sudo service dhcpcd restart
6. Edit dnsmasq.conf file and add following lines:
  - interface=wlan0
  - dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
7. Configure hostapd.conf file, add the following lines:
  - interface=wlan0
  - driver=nl80211
  - ssid=YourNetworkSSID          (select SSID for AP mode)
  - wpa_passphrase=YourPassword   (select psk for AP mode)
8. find line #DAEMON_CONF and replace it with DAEMON_CONF="/etc/hostapd/hostapd.conf"
  - sudo nano /etc/default/hostapd
9. Configure the system to start the services at boot:
  - sudo systemctl unmask hostapd
  - sudo systemctl enable hostapd
  - sudo systemctl start hostapd
  - sudo systemctl start dnsmasq
10. Enable routing of the internet traffic:
  - sudo nano /etc/sysctl.conf
11. Reboot the system
12. After rebooting navigate to the working directory, where you have script saved and run it with python3 command. 


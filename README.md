# Raspberry-PI-Automated-Mushroom-Farm
 Outlines code &amp; components needed for an automated shotgun fruiting chamber for mushroom cultivation. See the Wiki for component requirements
 
 ## Setup Instructions

1. Flash the relevant zigbee2mqtt software onto the sniffer stick
   * https://www.zigbee2mqtt.io/guide/adapters/flashing/flashing_the_cc2531.html
3. Get zigbee2mqtt running as a service on the PI 
   * https://www.zigbee2mqtt.io/guide/getting-started/ for the official guide
   * A very useful guide can also be found at https://flemmingss.com/how-to-set-up-zigbee2mqtt-on-a-raspberry-pi-and-integrate-it-with-home-assistant/ 
   * If you get an error saying 'Cannot connect to MQTT server!' when trying to run zigbee2mqtt you can simply run 'sudo apt-get install mosquitto' which should fix it.
3. Plug the sniffer stick and the control component of the Energine remote-controlled sockets into the Raspberry PI
   * ![image](https://user-images.githubusercontent.com/38185772/170876467-03635355-fdff-4a28-9520-27e27a8f486b.png)
4. Plug the humidifier into the Energine socket
   * ![image](https://user-images.githubusercontent.com/38185772/170876691-da3c4ca3-801a-41d6-8c4d-21e215cf7821.png)
5. Stick the humidity sensors to the walls of the fruiting chamber and move the end of the humidifier hose inside the chamber
   * ![image](https://user-images.githubusercontent.com/38185772/170876885-0f9b8b4e-6cd1-4f87-aedc-775f2518df09.png)
   * Growing some barely alive lion's mane in the above picture
6. Run the code and keep it running via a crontab entry (sudo crontab -e)
   * I personally use **@reboot sudo python </path/to/the/program>**

### Troubleshooting
* Verify that the code is running: ps aux | grep python
* Verify that zigbee2mqtt is running: sudo service zigbee2mqtt status.
  * Turn it on: sudo service zigbee2mqtt start
  * Turn it off: sudo service zigbee2mqtt stop
  * Restart it: sudo service zigbee2mqtt restart

Get a peak on the stick-to-sensor communication: sudo journalctl -u zigbee2mqtt.service -f





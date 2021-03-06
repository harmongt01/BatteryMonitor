BatteryMonitor
==============

This project provides the information and software to make a low cost ($100-150) and flexible device to monitor and log individual battery cell voltages and other battery data using the Beaglebone Black Linux computer. The monitoring software can also set and reset I/O pins on the Beaglebone in response to cell voltages going out of programmed limits. Programming of the I/O is done via the config file. I have also written some webpages to display batery information on any web browser via the internet. For those that don't need or want all the IO and additional memory that the Beaglebone Black offers I see no reason why this project could not be run on the various models of the Raspberry Pi including maybe even the Raspberry Pi Zero which could cut the cost to below $50, or any Linux computer which has an  accessable built in I2C bus, might even be possible to run it on your router running OpenWRT or something similar.

The primary use for this would be to monitor large Lithium based battery banks of up to 48 volts but it would also be useful for other technologies like Lead Acid batteries. In my case I am using it to monitor and log data from our 24 volt 360ah LiFePO4 battery bank used in our off grid power system.


The main documentation for this project can be found in the wiki here https://github.com/simat/BatteryMonitor/wiki

My thanks to Adafruit for the ADS1X15 a/d drivers from here, https://github.com/adafruit/Adafruit_ADS1X15

I have made this an open source project with the hope that it maybe useful to others and if found useful that others will get involved and broaden the scope of the project. Please feel free to make suggestions, report bugs or provide positive or negative feedback. I am new to using the Beaglebone, Git and Python so suggestions on how to use features of the Beaglebone, Git and Python that I might not be aware of could also be useful.

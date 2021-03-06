# *****BatteryMonitor main file batteries.py*****
# Copyright (C) 2014 Simon Richard Matthews
# Project loaction https://github.com/simat/BatteryMonitor
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


#!/usr/bin/python
import sys

#import smbus
#from Adafruit_I2C import Adafruit_I2C
import time
from shutil import copy as filecopy
from config import config
from ConfigParser import SafeConfigParser
numcells = config['battery']['numcells']
from getdata import Readings
import Adafruit_BBIO.GPIO as GPIO
# Initialise and compile alarms
for i in config['alarms']:
  exec(config['alarms'][i][0])
  config['alarms'][i][1] = compile(config['alarms'][i][1], '<string>', 'exec') 
  config['alarms'][i][2] = compile(config['alarms'][i][2], '<string>', 'exec') 
  config['alarms'][i][3] = compile(config['alarms'][i][3], '<string>', 'exec') 
  config['alarms'][i][4] = compile(config['alarms'][i][4], '<string>', 'exec') 


def deamon(soc=-1):
  """ Main loop, gets battery data, gets summary.py to do logging"""
  import summary
  logsummary = summary.Summary()
  summary = logsummary.summary
  printtime = time.strftime("%Y%m%d%H%M%S ", time.localtime())
  while int(printtime) <= int(summary['current']['timestamp']):
    print(printtime,summary['current']['timestamp'])
    print "Error: Current time before last sample time"
    time.sleep(30)
    printtime = time.strftime("%Y%m%d%H%M%S ", time.localtime())
  batdata = Readings()  # initialise batdata after we have valid sys time

 
  filecopy(config['files']['summaryfile'],config['files']['summaryfile']+"R" + printtime)
  if soc > config['battery']['capacity']:
    print "Battery DOD must be less than Battery Capacity"
  else:
    if soc < 0:
       batdata.soc = summary['current']['ah'][0]
       batdata.socadj = summary['current']['dod'][0]
    else:
      batdata.soc = soc
      batdata.socadj = soc
      summary['current']['dod'][3] = 0
    summary['current']['dod'][3] = -100 # flag don't adjust leakage current
    prevtime = logsummary.currenttime
    prevbatvoltage = batdata.batvoltsav[numcells]
#    logsummary.startday(summary)
#    logsummary.starthour(summary)


    while True:
      try:
        for i in range(config['sampling']['samplesav']):
#          printvoltage = ''
#          for i in range(numcells+1):
#            printvoltage = printvoltage + str(round(batdata.batvolts[i],3)).ljust(5,'0') + ' '
#         print (printvoltage)
          batdata.getraw()
        
#          if batdata.batvoltsav[numcells] >= 55.2 and prevbatvoltage < 55.2:  # reset SOC counter?
          if batdata.batvoltsav[numcells] < config['battery']['vreset'] \
          and prevbatvoltage >= config['battery']['vreset'] \
          and batdata.batcurrentav < config['battery']['ireset']:  # reset SOC counter?

            if summary['current']['dod'][3] <= 0.0 :
              socerr=0
            else:
              socerr=batdata.socadj/(summary['current']['dod'][3]*24)
              socerr=max(socerr,-0.01)
              socerr=min(socerr,0.01)
            config['battery']['ahloss']=config['battery']['ahloss']-socerr/2
            batconfigdata=SafeConfigParser()
            batconfigdata.read('battery.cfg')
            batconfigdata.set('battery','ahloss',str(config['battery']['ahloss']))
            with open('battery.cfg', 'w') as batconfig:
              batconfigdata.write(batconfig)
            batconfig.closed

            batdata.soc = 0.0
            batdata.socadj = 0.0
            summary['current']['dod'][3] = 0
          else:
            batdata.soc = batdata.soc + batdata.batah
            batdata.socadj = batdata.socadj +batdata.batahadj
          batdata.ah = batdata.ah + batdata.batah
          batdata.inahtot = batdata.inahtot + batdata.inah
          batdata.pwrbattot = batdata.pwrbattot + batdata.pwrbat
          batdata.pwrintot = batdata.pwrintot + batdata.pwrin
        prevbatvoltage = batdata.batvoltsav[numcells]
# check alarms
        minvolts = 5.0
        maxvolts = 0.0
        for i in range(1,numcells):
          minvolts = min(batdata.deltav[i],minvolts)
          maxvolts = max(batdata.deltav[i],maxvolts)

        for i in config['alarms']:
          exec(config['alarms'][i][1])
          if test:
            exec(config['alarms'][i][2])
          exec(config['alarms'][i][3])
          if test:
            exec(config['alarms'][i][4])
# update summaries
        logsummary.update(summary, batdata)
        if logsummary.currenttime[4] <> logsummary.prevtime[4]:  # new minute
          logsummary.updatesection(summary, 'hour', 'current')
          logsummary.updatesection(summary, 'alltime','current')
          logsummary.updatesection(summary, 'currentday','current')
          logsummary.updatesection(summary, 'monthtodate', 'current')
          logsummary.updatesection(summary, 'yeartodate', 'current')
          logsummary.writesummary()
          batdata.ah = 0.0
          batdata.ahadj = 0.0
          batdata.inahtot = 0.0
          batdata.pwrbattot = 0.0
          batdata.pwrintot = 0.0

        if logsummary.currenttime[3] <> logsummary.prevtime[3]:  # new hour
          logsummary.starthour(summary)

        if logsummary.currenttime[3] < logsummary.prevtime[3]: # newday
          logsummary.startday(summary)

        if logsummary.currenttime[1] != logsummary.prevtime[1]: # new month
          logsummary.startmonth(summary)

        if logsummary.currenttime[0] != logsummary.prevtime[0]: # new year
          logsummary.startyear(summary)

      except KeyboardInterrupt:
        sys.stdout.write('\n')
        logsummary.close()
        sys.exit(9)
        break

if __name__ == "__main__":
  print (sys.argv)
  if len(sys.argv) > 1:
    deamon(float(sys.argv[1]))
  else:
    deamon()


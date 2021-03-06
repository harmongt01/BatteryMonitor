# *****BatteryMonitor parse Config data from battery config file*****
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

from ast import literal_eval
from ConfigParser import SafeConfigParser

class Config:
  def __init__(self):
    configfile = SafeConfigParser()
#    print configfile
    configfile.read('battery.cfg')
    self.config = {}
    for section in configfile.sections():
      self.config[section] = {}
      for key, val in configfile.items(section):
        self.config[section][key] = literal_eval(val)


config = Config()
config = config.config


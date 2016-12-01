#!/usr/bin/python2
#    combineAR: A milter for combining multiple Authentication-Results headers
#    Copyright © 2016  RunasSudo (Yingtong Li)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

MY_ID = 'example.com'
AUTHORISED_IDS = [MY_ID]

# END CONFIG

import Milter
import threading
import time
import sys
from Milter.utils import parse_addr

class CombineARMilter(Milter.Base):

  def __init__(self):
    print "%s new connection" % time.strftime('%Y%b%d %H:%M:%S')
    self.id = Milter.uniqueID()
    self.arheaders = []
  
  def header(self, name, hval):
    if name == 'Authentication-Results':
      self.arheaders.append(hval)
    return Milter.CONTINUE
  
  def eom(self):
    # Process all the AR headers
    arresults = []
    for arheader in self.arheaders:
      if ';' in arheader and arheader[:arheader.index(';')] in AUTHORISED_IDS:
        arresults.append(arheader[arheader.index(';')+1:].strip())
    
    # Remove the existing AR headers
    for i in xrange(0, len(self.arheaders)):
      # After removing preceding headers, this header is now the first!
      self.chgheader('Authentication-Results', 1, None)
    
    # Add our new AR header
    arheader = MY_ID
    if arresults:
      for arresult in arresults:
        arheader += ';\n\t' + arresult
    else:
      arheader += '; none'
    print arheader
    self.addheader('Authentication-Results', arheader, 0)
    
    return Milter.CONTINUE


def main():
  socketname = "/run/combinear/combinear.sock"
  timeout = 600
  # Register to have the Milter factory create instances of your class:
  Milter.factory = CombineARMilter
  print "%s milter startup" % time.strftime('%Y%b%d %H:%M:%S')
  sys.stdout.flush()
  Milter.runmilter("combinear", socketname, timeout)
  print "%s milter shutdown" % time.strftime('%Y%b%d %H:%M:%S')

if __name__ == "__main__":
  main()

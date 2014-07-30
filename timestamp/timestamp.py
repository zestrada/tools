#!/usr/bin/env python
import socket
import sys
import datetime
from optparse import OptionParser

START='0'
STOP='1'

def main():
  opt = parse_input()
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  if opt.port is None:
    fail("Must specify port") 
  if(opt.listen):
    listen(opt,s)
  else:
    if opt.host is None:
      fail("Must specify host address when a client") 
    client(opt,s)

####END MAIN

def listen(opt,s):
  sys.stderr.write("Listening on port %d\n" % opt.port)
  s.bind(('',opt.port))
  s.listen(1)
  then=datetime.datetime.now(None)
  now=datetime.datetime.now(None)
  while True:
    conn, addr = s.accept()
    data = conn.recv(8)
    #if not data:
    #  break
    if START in data:
      then = datetime.datetime.now(None)
      #print "Starting at %s" % then
    elif STOP in data:
      now = datetime.datetime.now(None)
      #print "Stopping at %s" % now
      print_time(now-then)
    #print data
  conn.close()

def client(opt,s):
  sys.stderr.write("Connecting to %s on port %d\n" % (opt.host,opt.port))
  s.connect((opt.host,opt.port))
  if opt.start:
    s.sendall(START)
  else:
    s.sendall(STOP)
  s.close()

def parse_input():
  usage = "usage: %prog [options] \n" +\
          "  Timestamp server for 3rd party measurements"
  parser = OptionParser(usage=usage)
  parser.add_option("-l", "--listen", action="store_true", dest="listen",
                    default=False, help="listen as the timestamp server")
  parser.add_option("-p", "--port", type="int", dest="port",
                    default=None, help="TCP port number")
  parser.add_option("-a", "--host", type="string", dest="host", default=None, 
                    help="Address of timestamp server (client mode)")
  parser.add_option("--start", action="store_true", dest="start", default=False,
                    help="start stopwatch")
  parser.add_option("--stop", action="store_false", dest="start", default=False,
                    help="stop stopwatch and record time since start")

  (opt, args) = parser.parse_args()
  return opt

#Might change to something else
def fail(msg):
  sys.exit(msg)

def print_time(td):
  print (td.microseconds + float(float(td.seconds + td.days * 24.0 * 3600.0) *\
        10.0**6.0)) / 10.0**6.0
  sys.stdout.flush()

main()

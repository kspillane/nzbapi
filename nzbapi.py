#!/usr/bin/python

# NZBapi.py
#
# A simple python script for accessing the xmlrpc API of
# an NZBGet server. Can handle basic status queries for now.
# New features add upon request/desire/need/PR.
#
# Copyroght 2018 - Kyle Spillane - spillman@gmail.com
#
# End user license granted under the MIT license, see lisence.
#

import xmlrpclib
from optparse import OptionParser

#Set up some options
def get_opts():
	parse = OptionParser()
	parse.add_option("--host", dest="host", help="IP or hostname of NZBGet server")
	parse.add_option("--port", "-p", dest="port", help="port NZBGet listening on, default 6789")
	parse.add_option("--user", dest="user", help="Control Username")
	parse.add_option("--pass", dest="password", help="Control Password")
	parse.add_option("-c", dest="cmd", help="command to execute")

	options, args = parse.parse_args()

	if not options.host:
		hostname = "127.0.0.1"
	else:
		hostname = options.host
	if not options.port:
		port = "6789"
	else:
		port = options.port
	if not options.user:
		username = "None"
	else:
		username = options.user
	if not options.password:
		password = "None"
	else:
		password = options.password
	if  not options.cmd:
		cmd = "qcount"
	else:
		cmd = options.cmd

	return hostname, port, cmd, username, password

#Main proram loop
if __name__ == "__main__":

	hostname, port, cmd, username, password = get_opts()

	if username == "None":
		remote = "http://" + hostname + ":" + port + "/xmlrpc"
	elif password == "None":
		remote = "http://" + username + "@" + hostname + ":" + port + "/xmlrpc"
	else:
		remote = "http://" + username + ":" + password + "@" + hostname + ":" + "port" + "/xmlrpc"


	if cmd == "qcount": #Returns count of items in download queue
		try:
			proxy = xmlrpclib.ServerProxy(remote)
			i = proxy.listgroups()
			print "There are " + str(len(i)) + " items in the download queue."
		except:
			print "There was a problem connecting to the remote server."
	elif cmd == "pause": #Pauses download queue
		try:
			proxy = xmlrpclib.ServerProxy(remote)
			if proxy.pausedownload() == True and proxy.pausepost() == True:
				print "Download queue and post processing queue are both paused."
				proxy.scheduleresume(7200)
			else:
				print "There was an error pausing the queues."
		except:
			print "There was an problem connecting to the remote server."
	elif cmd == "resume": #Resumes paused download queue
		try:
			proxy = xmlrpclib.ServerProxy(remote)
			if proxy.resumedownload() == True and proxy.resumepost() == True:
				print "The download queue has been resumed."
			else:
				print "There was a problem resuming the queues."
		except:
			print "There was a problem connecting to the remote server."
	elif cmd == "dsize": #Retrieves various download statistics
		try:
			proxy = xmlrpclib.ServerProxy(remote)
			ret = proxy.status()
			qsize = str(int(ret['RemainingSizeMB']) / 1024)
			avgdl = str(int(ret['AverageDownloadRate']) / 1024 / 1024)
			dskspace = str(int(ret['FreeDiskSpaceMB']) / 1024)
			qpaused = ret['DownloadPaused']
			qcount = str(len(proxy.listgroups()))

			if qpaused == True:
				str = "The download queue is currently paused."
			else:
				str = "The download queue is active."
			str = str + " There are currently: " + qcount + " items in the queue. "
			str = str + " Average download speed is" + avgdl + "Mbps."
			str = str + " There is  " + dskspace + "GB free disk space left."
			str = str + " There is " + qsize + "GB left to download in the queue."
		except:
			str = "There was a problem connecting to the remote server." 
		print str

#TODO - Add more commands to do more things!
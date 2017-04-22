import getopt, sys, os, socket, urllib2, datetime

keywords = ['pass', 'root']

def CheckAxisURL(address,passwd):
    cameraurl = 'http://' + address + '/axis-cgi/param.cgi?action=list&group=root.Brand.ProdNbr'
    errorcode = ''
    try:
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, cameraurl, 'root', passwd)
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPDigestAuthHandler(passman)))
        f = urllib2.urlopen(cameraurl, timeout=3)
        cameramodel = f.read().split('=')
        f.close()
    except socket.timeout as e:
        errorcode = "Connection Timeout"
    except urllib2.HTTPError, e:
        if e.code == 404:
            errorcode = "Page not found"
        elif e.code == 403:
            errorcode = "Access denied"
        elif e.code == 401:
            errorcode = "Bad password"
        else:
            errorcode = "Something else happened"
    except urllib2.URLError:
        errorcode = "URL Error"
    if errorcode:
		# print errorcode
		# print cameraurl
		return False
    else:
		# print "Camera Found - Address: "+address+" Pass:"+passwd
		# print address+" - "+passwd
		return True

def main():

	subnet = raw_input("Please enter subnet to scan: ")
	ping_delay=1 # in seconds

	cvs_export = open(subnet+ '.csv', 'w+')
	cvs_export.write("HardwareAddress,HardwarePort,HardwareUsername,HardwarePassword,HardwareDriverID\n")

	i=int(2)

	while i != 250:
		for passwd in keywords:
			if CheckAxisURL(subnet+"."+str(i),passwd):
				print "Found Camera at: "+subnet+"."+str(i)
				cvs_export.write(subnet+"."+str(i)+",80,root,"+passwd+",\n")
		i=i+1
	cvs_export.close

if __name__ == "__main__":
    main()

from urllib import urlopen as Open
import time,os,sys

def wait(T):
	while T>0.0:
		if T>1: time.sleep(1); sys.stdout.write('.')
		else: time.sleep(T)
		T -= 1
	print

#print sys.argv
	
print "running in mode: '%s'"%sys.argv[1]
print '\nChecking for updates...'#,;wait(3.01)
print 'Update checking disabled.\n'

if len(sys.argv)>2:
        print 'loading file: %s'%sys.argv[2]
        if len(sys.argv)>3:
                print 'unable to import files:'
                for f in sys.argv[3:]: print '- %s'%f
                print 'please wait until dev5, sorry :('
'''
try:
	Open('http://tcll5850.hostoi.com/Universal Model Converter/Connect.txt')
	CurVsn = U('>H',open('Version.dat','rb').read(2))[0]
	SvrVsn = 1
	while True:
		try: Open('http://tcll5850.hostoi.com/Universal Model Converter/UMC/'+str(SvrVsn)+'.py'); SvrVsn+=1
		except IOError: break
	if SvrVsn > CurVer:
		print 'Update Found!'
		I = raw_input('Would you like to install the update? (Y/N)').upper();print
		if I -- 'Y':
			keep_tryng = 1
			while keep_tryng:
				try:
					print 'Installing update'
					UD = Open('http://tcll5850.hostoi.com/Universal Model Converter/UMC/'+str(SvrVsn)+'.py')
					Fl = open('API.py','w')
					Fl.write(UD.read())
					open('Version.dat','wb').write(U('>H',SvrVsn)[0])
					print 'Update Complete!\n'
					
				except IOError:
					T = raw_input('Error: Connection lost... Try again? (Y/N)').upper()
					if T == 'Y': print 'Retrying.';wait(2)
					if T == 'N': print 'Update cancelled.'; keep_tryng=0
				
	else: print 'No update found\n'
	
except: print 'Could not establish a connection with the server.\n'
'''
try:
        import API
        API.run()
except:
        import sys,traceback
        typ,val,tb=sys.exc_info()#;tb=traceback.extract_tb(i[2])[0]
        print
        traceback.print_exception(
            typ,val,tb#,
            #limit=2,
            #file=sys.stdout
            )
        print
        raw_input('press enter to exit.')

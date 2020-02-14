#!/usr/bin/python36


import os
import subprocess
import cgi
import cgitb
cgitb.enable()


print("content-type: text/html")
print("\n")


print("-------------WELCOME TO HADOOP MENU---------------")

#system=input("where you want to run commands remote/local :\n")

form = cgi.FieldStorage()	
system = form.getvalue('l')


if system  == 'remote':
	#rip=input("enter the remote ip: ")
	#password=input("enter the remote password: ")
	form = cgi.FieldStorage()	
	rip = form.getvalue('i')
 
	form = cgi.FieldStorage()	
	password = form.getvalue('p')



#node= input("what you want to become master or slave: ")
form = cgi.FieldStorage()	
node = form.getvalue('n')


if node == 'master':
	a='name'
elif node == 'slave':
	a='data'
else:
	print("invalid node")
	subprocess.getoutput("exit")

#nip= input(" enter the namenode ip")
#b= input("enter folder name")
form = cgi.FieldStorage()	
nip = form.getvalue('ni')
form = cgi.FieldStorage()	
b = form.getvalue('b')


fil=open('/etc/hadoop/hdfs-site.xml','w')
fil.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>dfs.{}.dir</name>
<value>/{}</value>
</property>

</configuration>""".format(a,b))
fil.close()

core=open('/etc/hadoop/core-site.xml','w')
core.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>fs.default.name</name>
<value>hdfs://{}:9001</value>
</property>

</configuration>""".format(nip))
core.close()

if system == 'local':				
	if node == 'master':
		print(subprocess.getoutput("sudo mkdir /{}".format(b)))
		print(subprocess.getoutput("sudo echo 'Y' |hadoop namenode -format"))
		print(subprocess.getoutput("sudo iptables -F"))
		print(subprocess.getoutput("sudo hadoop-daemon.sh start namenode"))
		
	elif node == 'slave':
		subprocess.getoutput("sudo mkdir /{}".format(b))
		subprocess.getoutput("sudo iptables -F")
		subprocess.getoutput("sudo hadoop-daemon.sh start datanode")
		
elif system == 'remote':	
	if node == 'master':
		subprocess.getoutput("sudo sshpass -p {} scp -o StrictHostkeyChecking=no /etc/hadoop/core-site.xml {}:/etc/hadoop/core-site.xml".format(password,rip))

		subprocess.getoutput("sudo sshpass -p {} scp -o StrictHostkeyChecking=no /etc/hadoop/hdfs-site.xml {}:/etc/hadoop/hdfs-site.xml".format(password,rip))

		subprocess.getoutput("sudo sshpass -p {} ssh -o StrictHostkeyChecking=no -l root {} mkdir /{}".format(password,rip,b))
		print(subprocess.getoutput("""sudo sshpass -p {} ssh -o StrictHostkeyChecking=no -l root {}  echo  'Y' |hadoop namenode -format""".format(password,rip)))
		print(subprocess.getoutput("sudo sshpass -p {} ssh -o StrictHostkeyChecking=no -l root {} iptables -F".format(password,rip)))
		print(subprocess.getoutput("""sudo sshpass -p {} ssh -o StrictHostkeyChecking=no -l root  {} hadoop-daemon.sh start namenode""".format(password,rip)))
		
	elif node == 'slave':
		subprocess.getoutput("sudo sshpass -p {} scp -o StrictHostkeyChecking=no /etc/hadoop/core-site.xml {}:/etc/hadoop/core-site.xml".format(password,rip))

		subprocess.getoutput("sudo sshpass -p {} scp -o StrictHostkeyChecking=no /etc/hadoop/hdfs-site.xml {}:/etc/hadoop/hdfs-site.xml".format(password,rip))

		
		subprocess.getoutput("sudo sshpass -p {} ssh -o StrictHostkeyChecking=no -l root {} mkdir /{}".format(password,rip,b))
		subprocess.getoutput("sudo sshpass -p {} ssh -o StrictHostkeyChecking=no -l root  {} iptables -F".format(password,rip))
		subprocess.getoutput("""sudo sshpass -p {} ssh -o StrictHostkeyChecking=no -l root {} hadoop-daemon.sh  start datanode""".format(password,rip))


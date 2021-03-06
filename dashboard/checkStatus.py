#!/usr/bin/python
import paramiko, sys, getpass, requests
from paramiko import client
import docker, MySQLdb
from pymongo import MongoClient


class HostCheck():
    def checkSSHStatus(self,HOST,USER,PASS):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:    
            client.connect(HOST,username=USER,password=PASS, timeout=10)
            print "SSH connection to %s established" %HOST
            client.close()
            print "Logged out of device %s" %HOST
            return "SSH established successfully"
        except:
            return "SSH failed"

    def checkDockerStatus(self,Host):
        try:
            print "in docker status"
            dockerVer = docker.DockerClient(base_url='tcp://'+Host+':2735', timeout=10).version()
            dockerres = str(dockerVer['Components'][0]['Version'])
            return "Docker working:" + dockerres
           
        except:
            return "Docker not working"

        #     dockerres = str(dockerVer['Components'][0]['Version'])
        #     return "Docker working:" + dockerres
        # except:
        #     return "Docker not working"

    def checkUrlStatus(self,projectname,appname):
        try:    
            res = requests.get('http://' + projectname+'-'+appname+'.tothenew.tk')
            response =  str(res)
            return "Url is working: " + response
        except:
            return "Url is not working"
            

    # def checkMysql(self,mysqlHostname, mysqlPort, mysqlUsername, mysqlPassword):
    #     try:
    #         myDB = MySQLdb.connect(host="mysqlHostname", port="mysqlPort", user="mysqlUsername", passwd="mysqlPassword")
    #         handler = myDB.cursor()
    #         handler.execute("SELECT VERSION()")
    #         results = handler.fetchall()
    #         for items in results:
    #             return "MySql working fine:" + str(items[0]) 
    #     except:
    #         return "Can't connect to mysql"

    # def checkMongo(self,mongoHostname, mongoPort, mongoUsername, mongoPassword):
    #     client = MongoClient("mongodb://" + mongoUsername + ":" + mongoPassword + "@" + mongoHostname + ":" + mongoPort,serverSelectionTimeoutMS=10,connectTimeoutMS=1000 )
    #     try:
    #         info = client.server_info()
    #         mongoRes = str(info['version'])
    #         return "Mongo working fine:" +  mongoRes
    #     except:
    #         return "Can't connect to mongo"
    
    def checkStack(self,Projectname,Host):
    	projectname = Projectname
        host = Host
        nginxstatusval = False
        try:
            nginxphpres=requests.get('http://'+host+':2735/services?filters={"mode":["replicated"],"name":["'+projectname+"_nginx_php"'"]}', timeout=10).json()
            if nginxphpres[0]['Spec']['Mode']['Replicated']['Replicas']==1:
	    #  print "\n"+nginxphpres[0]['Spec']['Name'] + " is running."
                nginxstatusval = True
            elif nginxphpres[0]['Spec']['Mode']['Replicated']['Replicas']==0:
	    #  print "\n"+nginxphpres[0]['Spec']['Name'] + " is not running."
                nginxstatusval = False
        # else:
	    #  print "Service isn't in replicated mode."
        except:
            print "Connection timed out!!!"

    

        mysqlstatusval = False
        try:
    	    mysqlres=requests.get('http://'+host+':2735/services?filters={"mode":["replicated"],"name":["'+projectname+"_mysql"'"]}', timeout=10).json()
    	    if mysqlres[0]['Spec']['Mode']['Replicated']['Replicas']==1:
	    #  "\n"+mysqlres[0]['Spec']['Name'] + " is running."
                mysqlstatusval = True
            elif mysqlres[0]['Spec']['Mode']['Replicated']['Replicas']==0:
                mysqlstatusval = False
        except:
            print "Connection timed out"
	    #  print "\n"+mysqlres[0]['Spec']['Name'] + " is not running."
        # else:
	    #  print "Service isn't in replicated mode."

        mongostatusval = False
        try:
            mongores=requests.get('http://'+host+':2735/services?filters={"mode":["replicated"],"name":["'+projectname+"_mongodb"'"]}', timeout=10).json()
            if mongores[0]['Spec']['Mode']['Replicated']['Replicas']==1:
	    #  print "\n"+mongores[0]['Spec']['Name'] + " is running."
                mongostatusval = True
            elif mongores[0]['Spec']['Mode']['Replicated']['Replicas']==0:
	            mongostatusval = False
        except:
            print "Connection timed out"
            # print "\n"+monglseores[0]['Spec']['Name'] + " is not running."
        # else:
	    #  print "Service isn't in replicated mode."
	

        redisstatusval = False
        try:
            redisres=requests.get('http://'+host+':2735/services?filters={"mode":["replicated"],"name":["'+projectname+"_redis"'"]}', timeout=10).json()
            if redisres[0]['Spec']['Mode']['Replicated']['Replicas']==1:
	        #  print "\n"+redisres[0]['Spec']['Name'] + " is running."
                redisstatusval = True
            elif redisres[0]['Spec']['Mode']['Replicated']['Replicas']==0:
	    #  print "\n"+redisres[0]['Spec']['Name'] + " is not running."
                redisstatusval = False
        # else:
	    #  print "Service isn't in replicated mode."
        except:
            print "Connection timed out!!!"

        varnishstatusval = False
        try:
            varnishres=requests.get('http://'+host+':2735/services?filters={"mode":["replicated"],"name":["'+projectname+"_varnish"'"]}', timeout=10).json()
            if varnishres[0]['Spec']['Mode']['Replicated']['Replicas']==1:
                varnishstatusval = True
	    #  print "\n"+varnishres[0]['Spec']['Name'] + " is running."
            elif varnishres[0]['Spec']['Mode']['Replicated']['Replicas']==0:
                varnishstatusval = False
	    #  print "\n"+varnishres[0]['Spec']['Name'] + " is not running."
        # else:
	    #  print "Service isn't in replicated mode."
        except:
            print "Connection timed out!!!"
        
        try:
            nginxphpres=requests.get('http://'+host+':2735/containers/json?all=1&filters={ "name":["'+projectname+"_nginx_php"'"]}', timeout=10).json()
            #ngnixidval = str(nginxphpres[0]['Id']) + " | " + str(nginxphpres[0]['Names'][0]) + " | " + str(nginxphpres[0]['Status'])
            ngnixidval = str(nginxphpres[0]['Id'])
            nginxnameval = str(nginxphpres[0]['Names'][0])
            nginxstval = str(nginxphpres[0]['Status'])
        except:
            ngnixidval = "Unable to fetch nginx details"
            nginxnameval = "Unable to fetch nginx details"
            nginxstval = "Unable to fetch nginx details"

        try:
            mysqlres=requests.get('http://'+host+':2735/containers/json?all=1&filters={ "name":["'+projectname+"_mysql"'"]}', timeout=10).json()
            #mysqlidval = str(mysqlres[0]['Id']) + " | " + str(mysqlres[0]['Names'][0]) + " | " + str(mysqlres[0]['Status'])
            mysqlidval = str(mysqlres[0]['Id'])
            mysqlnameval = str(mysqlres[0]['Names'][0])
            mysqlstval = str(mysqlres[0]['Status'])
        except:
            mysqlidval = "Unable to fetch mysql details"
            mysqlnameval = "Unable to fetch mysql details"
            mysqlstval = "Unable to fetch mysql details"
        
        try:
            mongores=requests.get('http://'+host+':2735/containers/json?all=1&filters={ "name":["'+projectname+"_mongodb"'"]}', timeout=10).json()
            #mongoidval = str(mongores[0]['Id']) + " | " + str(mongores[0]['Names'][0]) + " | " + str(mongores[0]['Status'])
            mongoidval = str(mongores[0]['Id'])
            mongonameval = str(mongores[0]['Names'][0])
            mongostval = str(mongores[0]['Status'])
        except:
            mongoidval = "Unable to fetch mongo details"
            mongonameval = "Unable to fetch mongo details"
            mongostval = "Unable to fetch mongo details"
        
        try:
            varnishres=requests.get('http://'+host+':2735/containers/json?all=1&filters={ "name":["'+projectname+"_varnish"'"]}', timeout=10).json()
            #varnishidval = (varnishres[0]['Id']) + " | " + str(varnishres[0]['Names'][0]) + " | " + str(varnishres[0]['Status'])
            varnishidval = str(varnishres[0]['Id'])
            varnishnameval = str(varnishres[0]['Names'][0])
            varnishstval = str(varnishres[0]['Status'])
        except:
            varnishidval = "Unable to fetch varnish details"
            varnishnameval = "Unable to fetch varnish details"
            varnishstval = "Unable to fetch varnish details"

        try:
            redisres=requests.get('http://'+host+':2735/containers/json?all=1&filters={ "name":["'+projectname+"_redis"'"]}', timeout=10).json()
            # redisidval = (redisres[0]['Id']) + " | " + str(redisres[0]['Names'][0]) + " | " + str(redisres[0]['Status'])
            redisidval = str(redisres[0]['Id']) 
            redisnameval = str(redisres[0]['Names'][0])
            redisstval =  str(redisres[0]['Status'])
        except:
            redisidval = "Unable to fetch redis details"
            redisnameval = "Unable to fetch redis details"
            redisstval = "Unable to fetch redis details"

        checkstackoutput = dict()
        checkstackoutput['nginxstatus'] = nginxstatusval
        checkstackoutput['redisstatus'] = redisstatusval
        checkstackoutput['varnishstatus'] = varnishstatusval
        checkstackoutput['mongostatus'] = mongostatusval
        checkstackoutput['mysqlstatus'] = mysqlstatusval
        
        checkstackoutput['nginxid'] = ngnixidval
        checkstackoutput['nginxname'] = nginxnameval
        checkstackoutput['nginxst'] = nginxstval

        checkstackoutput['mysqlid'] = mysqlidval
        checkstackoutput['mysqlname'] = mysqlnameval
        checkstackoutput['mysqlst'] = mysqlstval

        checkstackoutput['mongoid'] = mongoidval
        checkstackoutput['mongoname'] = mongonameval
        checkstackoutput['mongost'] = mongostval

        checkstackoutput['varnishid'] = varnishidval
        checkstackoutput['varnishname'] = varnishnameval
        checkstackoutput['varnishst'] = varnishstval

        checkstackoutput['redisid'] = redisidval
        checkstackoutput['redisname'] = redisnameval
        checkstackoutput['redisst'] = redisstval
        return checkstackoutput

        

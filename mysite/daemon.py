#!/usr/bin/python

from django.core.management import setup_environ
import mysite.settings
setup_environ(mysite.settings)

from cpanel.models import JobList,Device
from cpanel.lib import choicer
import ConfigParser
import paramiko
from SocketServer import ThreadingTCPServer, StreamRequestHandler  
import traceback  
import time
import os
import signal

class MyStreamRequestHandlerr(StreamRequestHandler):  
    def handle(self):  
        while True:  
            try:
                jobid=self.request.recv(1024)
                print jobid
                job=JobList.objects.get(id=int(jobid))
                self.wfile.write("needstate")
                status=3
                status=self.request.recv(1024)
                print status
                if status=="2":
                    self.wfile.write("givemeresult")
                    result=self.request.recv(1024)
                    print result
                    fpname=jobid+".txt"
                    file=open(fpname,"wb")
                    print "file open"
                    file.write(result)
                    print "file write"
                    file.close()
                    self.wfile.write("88")
                    job.Result=jobid+".txt"
            except:  
                #traceback.print_exc()  
                break
            device=Device.objects.get(Ip=job.Ip)
            print device
            device.State=0
            device.save()
            job.State=status
            job.save()
            
def runServer():
    addr=(host,port)
    server = ThreadingTCPServer(addr, MyStreamRequestHandlerr)
    server.serve_forever()

def StartJob(jobid,deviceip,cmd):
    device=Device.objects.get(Ip=deviceip)
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print deviceip,device.Username,device.Password
        ssh.connect(deviceip,22,device.Username,device.Password) 
        cmd=cmd+" "+str(jobid)+" &"
        print "cmd:"+cmd
        ssh.exec_command(cmd)
        device.State=1
        device.save()
        job=JobList.objects.get(id=jobid)
        job.State=1
        job.save()
    except Exception,e:
        print e
        job=JobList.objects.get(id=jobid)
        job.State=3
        job.save()
    ssh.close()


if __name__=='__main__':
    cfg=ConfigParser.ConfigParser()
    redundant=1
    MAX_THREAD=5
    host=""
    port=3939
    WAIT_TIME=5
    try:
        cfg.read("daemon.conf")
        redundant=cfg.getint("config","redundant")
        MAX_THREAD=cfg.getint("config","MAX_THREAD")
        host=cfg.get("config","host")
        port=cfg.getint("config","port")
        WAIT_TIME=cfg.getint("config","WAIT_TIME")
        print "read"
    except Exception,e:
        cfg.add_section("config")
        cfg.set("config","redundant",redundant)
        cfg.set("config","MAX_THREAD",MAX_THREAD)
        cfg.set("config","host",host)
        cfg.set("config","port",port)
        cfg.set("config","WAIT_TIME",WAIT_TIME)
        cfg.write(open("daemon.conf","w"))
        print "init"
#init redundant
    print host,port,redundant,MAX_THREAD
    while True:
        try:
            job=JobList.objects.get(id=redundant)
            if job.State==0:
                break
            else:
                print redundant
                redundant=redundant+1
        except:
            break
    try:
        pid=os.fork()
    except OSError,e:
        pass

    if pid==0:  #child
        print "child running"
        runServer()
    else:
        print "parent sleeping"
        while True:
            for i in range(MAX_THREAD):
                try:
                    job=JobList.objects.get(id=redundant)
                except:
                    break
                deviceIp=job.Ip
                if deviceIp=="":
                    deviceIp=choicer.getDevice().Ip
                StartJob(redundant,deviceIp,job.Cmd)
                redundant=redundant+1
            cfg.set("config","redundant",redundant)
            cfg.write(open("daemon.conf","w"))
            time.sleep(WAIT_TIME)

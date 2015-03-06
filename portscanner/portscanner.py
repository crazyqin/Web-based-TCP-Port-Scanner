#!/usr/bin/python
# -*- coding: utf-8 -*-

import makeip

import threading
import Queue
import sys
import platform
from subprocess import Popen, PIPE
import re
import socket
import time
import ConfigParser
#Thread Number
NUM=50

#INIT SOME VAR
pinglist=[] #HOST TO BE SCANNED
pinged_list=[] #SURVIVAL HOST
ipQueue=Queue.Queue()
ipQueue_port=Queue.Queue()
result=[]  # list.append() ---> atomic operation 


def JobFinished(jobid,state):
    print "uploading"
    BUFFERSIZE=1024
    try:
        cfg=ConfigParser.ConfigParser()
        cfg.read("portscanner.conf")
        HOST=cfg.get("config","HOST")
        PORT=cfg.getint("config","PORT")
    except Exception,e:
        print e
        sys.exit()
    ADDR=(HOST,PORT)

    TCPClient=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    TCPClient.connect(ADDR)
    print jobid
    print "init finished"
    while True:
        TCPClient.send(jobid)
        recvdata=TCPClient.recv(BUFFERSIZE)
        if recvdata=="needstate":
            print "needstate received"
            if state=="2":
                senddata=open(jobid,"rb").read()
                TCPClient.send(state)
                recvdata=TCPClient.recv(BUFFERSIZE)
                if recvdata=="givemeresult":
                    print "givemeresult received"
                    TCPClient.send(senddata)
                    print TCPClient.recv(BUFFERSIZE)
                    TCPClient.close()
                    break
            else:
                TCPClient.send(state)
                TCPClient.close()
                break
                

def pinger():
    while True:
        ip=ipQueue.get()
        if platform.system()=='Linux':
            p=Popen(['ping','-c 2',ip],stdout=PIPE)
            q=p.stdout.read()
            m = re.search('(.*)\srecieved', q)
            if m!=0:
                pinged_list.append(ip)
                lock.acquire()
                print ip,'survive'
                lock.release()
                
        if platform.system()=='Windows':
            p=Popen('ping -n 2 ' + ip, stdout=PIPE)
            m = re.search('TTL', p.stdout.read())
            if m:
                pinged_list.append(ip)
                lock.acquire()
                print ip,'survive'
                lock.release()
        ipQueue.task_done()
    

    
def scanner():
    while True:
        host,port=ipQueue_port.get()
        scanSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        scanSocket.settimeout(3)
        try:
            scanSocket.connect((host,port))
            result.append((host,port))
            lock.acquire()
            print host,':',port,'......OPEN'
            lock.release()
        except:
            pass
        scanSocket.close()
        ipQueue_port.task_done()
    

if __name__=='__main__':
    lock=threading.Lock()
    try:
        pinglist=makeip.makeip(sys.argv[1],sys.argv[2])
        ports=sys.argv[3:-1]
        jobid=sys.argv[-1]
    except:
        jobid=sys.argv[-1]
        print 'Wrong input'
        JobFinished(jobid,"3")
        sys.exit()
        
    #LIST2QUEUE
    for ip in pinglist:
        ipQueue.put(ip)
    #FIND SURVIVAL HOST
    for i in range(NUM):
        t=threading.Thread(target=pinger)
        t.setDaemon(True)
        t.start()
    ipQueue.join()
    survivalhostnum=0        
    for ip in pinged_list:
        survivalhostnum=survivalhostnum+1
    print '%s survival hosts finded' % survivalhostnum
    if survivalhostnum==0:sys.exit()
    print 'port scan begin'
    #(ip,port)-->Queue
    for ip in pinged_list:
        for port in ports:
            ip_port=(ip,int(port))
            ipQueue_port.put(ip_port)
    
    #SCAN PORT
    for i in range(NUM):
        t=threading.Thread(target=scanner)
        t.setDaemon(True)
        t.start()
    ipQueue_port.join()
    print 'port scan finished'
    TIMEFORMAT='%Y-%m-%d %H-%M-%S'
    #filename=time.strftime(TIMEFORMAT, time.localtime())+' '+sys.argv[1]+'-'+sys.argv[2]+'.txt'
    #print filename
    filename=jobid
    f=open(filename,'w')
    f.write('Job ID:'+jobid+'\n')
    f.write('IP range from:'+sys.argv[1]+' to:'+sys.argv[2]+'\n')
    f.write('Port:'+str(sys.argv[3:-1])+'\n')
    f.write('-------Result-------'+'\n')    
    for item in result:
        host,port=item
        f.write(host+':'+str(port)+'\n')
    f.write('-------End----------'+'\n')
    f.write('Job finished at:'+time.strftime(TIMEFORMAT, time.localtime()))  
    f.close()
    JobFinished(jobid,"2")
    sys.exit()
    
    

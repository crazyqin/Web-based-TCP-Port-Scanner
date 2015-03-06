from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from cpanel.models import Device
from cpanel.models import JobList
from cpanel.lib import choicer
import paramiko
import os
import mysite.settings


@login_required(login_url='login')
def portScan(request):
    devices=Device.objects.all()
    if request.method=='POST':
        deviceip=request.POST['deviceip']
        Iprange=request.POST['Iprange']
        Ports=request.POST['Ports']
        print deviceip,Iprange,Ports
        if deviceip=='Auto':
            device=choicer.getDevice(devices)
        else:
            device=Device.objects.get(Ip=deviceip)
        cmd='cd portscanner ;'+' nohup python portscanner.py '+Iprange+' '+Ports
        newjob=JobList(Operator=request.user,
                       Ip=device.Ip,
                       Cmd=cmd,
                       State=0,
                       Date='datetest')
        newjob.save()
        
        #ssh=paramiko.SSHClient()
        #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.connect(deviceip,22,device.Username,device.Password) 
        ##cmd='cd portscanner ;'+' nohup python portscanner.py '+Iprange+' '+Ports+' &'
        print cmd
        #ssh.exec_command(cmd)
        #ssh.close()
        devices=Device.objects.all()
        return render_to_response('portscan.html',{'username':request.user,'newjobid':newjob.id,'devices':devices,'err_msg':'Job Added and Your Job Id is:'})
    return render_to_response('portscan.html',{'devices':devices,'username':request.user})

@login_required(login_url='login')
def portscanResult(request):
    jobs=JobList.objects.all()
    if request.user.is_superuser==0:
        jobs=JobList.objects.filter(Operator=request.user)
    return render_to_response('portscanresult.html',{'jobs':jobs,'username':request.user})
    #if request.method=='POST':
    #    device=Device.objects.get(Ip=request.POST['deviceip'])
    #    ssh=paramiko.SSHClient()
    #    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #    ssh.connect(device.Ip,22,device.Username,device.Password)
    #    cmd='cd portscanner ; '+'ls *.txt'
    #    stdin,stdout,stderr=ssh.exec_command(cmd)
    #    Results=stdout.readlines()
    #    ssh.close()
    #    print device.Ip
    #    return render_to_response('portscanresult.html',{'searched':True,'results':Results,'device':device})
    #device=Device.objects.all()
    #return render_to_response('portscanresult.html',{'searched':False,'devices':device}) 

@login_required(login_url='login')
def portscanresultClear(request,deviceip): 
    device=Device.objects.get(Ip=deviceip)
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(device.Ip,22,device.Username,device.Password)
    cmd='cd portscanner ; '+'rm *.txt -f'
    stdin,stdout,stderr=ssh.exec_command(cmd)
    Results=stdout.readlines()
    ssh.close()
    return HttpResponseRedirect('../dashboard')

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from cpanel.models import Device
import paramiko


@login_required(login_url='login')
@permission_required('cpanel.can_add_device',login_url='dashboard')
def addDevice(request):
    print request.user,'is adding device'
    if request.method=='POST':
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(request.POST['Ip'],22,request.POST['Username'],request.POST['Password'])
        except:
            return render_to_response('adddevice.html',{'err_msg':"Can't connect the Server."})
        stdin,stdout,stderr=ssh.exec_command('cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c ')
        Cpu=stdout.read()
        stdin,stdout,stderr=ssh.exec_command("cat /proc/meminfo | grep 'MemTotal' |awk '{print $2,$3}'")
        Mem=stdout.read()
        stdin,stdout,stderr=ssh.exec_command("smartctl -a /dev/sda |grep 'Capacity'|awk '{print $5,$6}'")
        Disk=stdout.read()
        stdin,stdout,stderr=ssh.exec_command("dmesg|grep -i eth")
        Nic=stdout.read()
        stdin,stdout,stderr=ssh.exec_command("lspci |grep 'VGA'")
        Vga=stdout.read()
        stdin,stdout,stderr=ssh.exec_command("uname -o")
        Os=stdout.read()
        stdin,stdout,stderr=ssh.exec_command("uname -m")
        Arch=stdout.read()
        stdin,stdout,stderr=ssh.exec_command("uname -r")
        Kernel=stdout.read()        
        ssh.close()
        
        device=Device(Ip=request.POST['Ip'],
                      Username=request.POST['Username'],
                      Password=request.POST['Password'],
                      Position=request.POST['Position'],
                      State=0,
                      Server=request.POST['Server'],
                      Owner=request.POST['Owner'],
                      Cpu=Cpu,Mem=Mem,Disk=Disk,Nic=Nic,Vga=Vga,Os=Os,Arch=Arch,Kernel=Kernel)
        device.save()
        return HttpResponseRedirect('deviceList')
    return render_to_response('adddevice.html',{'username':request.user})


@login_required(login_url='login')
def deviceList(request):
    device=Device.objects.all()
    return render_to_response('devicelist.html',{'Devices':device,'username':request.user})

@login_required(login_url='login')
@permission_required('cpanel.can_change_device',login_url='dashboard')
def deviceDetail(request,deviceid):
    try:
        device=Device.objects.get(id=int(deviceid))
        return render_to_response('devicedetail.html',{'err':False,'device':device,'username':request.user})
    except:
        return render_to_response('devicedetail.html',{'err':True,'username':request.user})
    return render_to_response('devicedetail.html')

@login_required(login_url='login')
@permission_required('cpanel.can_delete_device',login_url='dashboard')
def delDevice(request,deviceid):
    try:
        device=Device.objects.get(id=int(deviceid))
        device.delete()
    except:pass
    device=Device.objects.all()
    return render_to_response('devicelist.html',{'Devices':device,'username':request.user})

@login_required(login_url='login')
@permission_required('cpanel.can_change_device',login_url='dashboard')
def editDevice(request,deviceid):
    if request.method=='POST':
        device=Device.objects.get(id=int(deviceid))
        device=Device(id=deviceid,
                      Ip=request.POST['Ip'],
                      Username=request.POST['Username'],
                      Password=request.POST['Password'],
                      Position=request.POST['Position'],
                      State=request.POST['State'],
                      Server=request.POST['Server'],
                      Owner=request.POST['Owner'],
                      Cpu=request.POST['Cpu'],
                      Mem=request.POST['Mem'],
                      Disk=request.POST['Disk'],
                      Nic=request.POST['Nic'],
                      Vga=request.POST['Vga'],
                      Os=request.POST['Os'],
                      Arch=request.POST['Arch'],
                      Kernel=request.POST['Kernel']
                     )
        device.save()
        device=Device.objects.all()
        return render_to_response('devicelist.html',{'Devices':device,'username':request.user})
    try:
        device=Device.objects.get(id=int(deviceid))
    except:
        device=Device.objects.all()
        return render_to_response('devicelist.html',{'Devices':device,'username':request.user})
    return render_to_response('editdevice.html',{'device':device,'username':request.user})

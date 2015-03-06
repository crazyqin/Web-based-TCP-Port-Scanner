from django.db import models

# Create your models here.

class Device(models.Model):
    Ip=models.IPAddressField()
    Cpu=models.CharField(max_length=40)
    Mem=models.CharField(max_length=16)
    Disk=models.CharField(max_length=20)
    Nic=models.CharField(max_length=40)
    Vga=models.CharField(max_length=40)
    Os=models.CharField(max_length=40)
    Arch=models.CharField(max_length=40)
    Kernel=models.CharField(max_length=40)
    Position=models.CharField(max_length=40)
    State=models.IntegerField()
    Server=models.CharField(max_length=40)
    Owner=models.CharField(max_length=20)
    Username=models.CharField(max_length=40)
    Password=models.CharField(max_length=40)
    def __unicode__(self):
        return self.Ip

class JobList(models.Model):
    Operator=models.CharField(max_length=40)
    Ip=models.IPAddressField()
    Cmd=models.CharField(max_length=250)
    Date=models.CharField(max_length=250)
    State=models.IntegerField()
    Result=models.FilePathField()
    def __unicode__(self):
        return self.Operator + self.Cmd
#class SSH(models.Model):
#    Ip=models.IPAddressField()
#    Username=models.CharField(max_length=40)
#    Password=models.CharField(max_length=40)
#    
#    def __unicode__(self):
#        return self.Ip

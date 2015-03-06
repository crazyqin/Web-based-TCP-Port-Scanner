# Web-based-TCP-Port-Scanner
a TCP Port Scanner using Django as Web Framework.
# Require:
Linux<br>
Python 2.7.6<br>
Django 1.4.10<br>
Paramiko(include ecdsa and pycrypto)<br>
# How to start
## 1.Upload the mysite floder to the Control Server.<br>
## 2.Upload the portscanner to the Client Computers.<br>
Put the portscanner folder into / folder.
(Control Server==Client Computers √)
## 3.Edit the settings.py in mysite/mysite/
Change the Database path<br>
Initialize the Database.<br>
python manage.py syncdb<br>
## 4.Edit the .conf file in mysite floder and portscanner floder<br>
### daemon.conf
[config]<br>
redundant = 1<br>
max_thread = 5<br>
host =xxx.xxx.xxx(your Control Server's IP address ) <br>
port = 3939<br>
wait_time = 5<br>
### portscanner.conf
[config]<br>
HOST=xxx.xxx.xxx(your Control Server's IP address )<br>
PORT=3939<br>
## 5.Run
Control Server:<br>
cd mysite<br>
python daemon.py<br>
python manage.py runserver<br>

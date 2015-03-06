#--*-- coding:utf-8 --*--
from django.shortcuts import render_to_response
from django.http import HttpResponse

import datetime

def home(request):
    #t=get_template('index.html')
    #c=Context({'username':'Qinyi'})
    #html=t.render(c)
    html='''
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Welcome</title>
</head>

<body>
<div align=center><img src="img/home.jpeg" width="787" height="589" usemap="#Map">
<map name="Map">
  <area shape="rect" coords="71,108,711,278" href="admin">
  <area shape="rect" coords="64,347,717,519" href="cpanel/login">
</map>
</div>

</body>
</html>

'''
    return HttpResponse(html)

def login(request):
    return render_to_response('login.html')

def search_form(request):
    t=('''<html>
<head>
    <title>Search</title>
</head>
<body>
    <form action="/search/" method="post">
        <% csrf_token %>
        <input type="text" name="q">
        <input type="submit" value="Search">
    </form>
</body>
</html>''')
    return HttpResponse(t)

def search(request):
    if request.method=='POST':
        message=request.POST.get('q')
    return HttpResponse(message)

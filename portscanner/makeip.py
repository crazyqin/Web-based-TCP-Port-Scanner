#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random

def showerr():
    print 'wrong ip'

def usage():
    print 'usage: python '+sys.argv[0]+'startip endip'




def makeip(arg1,arg2):
    startip = arg1.split('.')
    endip = arg2.split('.')
    
    startip_1 = int(startip[0])
    startip_2 = int(startip[1])
    startip_3 = int(startip[2])
    startip_4 = int(startip[3])
    
    if ((startip_1 not in range(0,256)) or (startip_2 not in range(0,256)) or (startip_3 not in range(0,256)) or (startip_1 not in range(0,256))):
        showerr()
        sys.exit()

    endip_1 = int(endip[0])
    endip_2 = int(endip[1])
    endip_3 = int(endip[2])
    endip_4 = int(endip[3])
    
    if ((endip_1 not in range(0,256)) or (endip_2 not in range(0,256)) or (endip_3 not in range(0,256)) or (endip_1 not in range(0,256))):
        showerr()
        sys.exit()
    
    start_num = startip_4+256*startip_3+65536*startip_2+16777216*startip_1
    end_num = endip_4+256*endip_3+65536*endip_2+16777216*endip_1
    num = end_num-start_num+1
    
    if start_num>end_num:
        print 'wrong ip'
        sys.exit()
    else:
        pinglist=[]
        while start_num<=end_num:
            #pinglist.append(str(start_num//16777216)+'.'+str(start_num%16777216//65536)+'.'+str(start_num%65536/256)+'.'+str(start_num%256)+'\n')
            pinglist.append(str(start_num//16777216)+'.'+str(start_num%16777216//65536)+'.'+str(start_num%65536/256)+'.'+str(start_num%256))
            start_num+=1
        return pinglist

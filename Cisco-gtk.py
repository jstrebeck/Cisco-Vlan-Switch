#!/usr/bin/python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys
import getpass
import telnetlib
import gtk 
import gobject
import os
from subprocess import Popen, PIPE
import fcntl
global Var

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onEntry0Changed(self, entry):
        global HOST 
        HOST = entry.get_text()

    def onEntry1Changed(self, entry):
        global user
        user = entry.get_text()

    def onEntry2Changed(self, entry):
        global password
        password = entry.get_text()
        entry.set_visibility(False)

    def onButton1Clicked(self, button):
        Vlan1()

    def onButton2Clicked(self, button):
        Vlan2()

def SHVlan():
    tn = telnetlib.Telnet(HOST)
    tn.read_until("Username: ")
    tn.write(user + "\n")
    if password:
        tn.read_until("Password: ")
        tn.write(password + "\n")
    tn.write("enable\n")
    tn.write("cisco\n")
    tn.write("show vlan\n")
    tn.write("end\n")
    tn.write("exit\n")
    global var1
    var1 = tn.read_all()
    print (var1)
    terminal()

def Vlan1():
    tn = telnetlib.Telnet(HOST)
    tn.read_until("Username: ")
    tn.write(user + "\n")
    if password:
        tn.read_until("Password: ")
        tn.write(password + "\n")
    tn.write("enable\n")
    tn.write("cisco\n")
    tn.write("conf t\n")
    tn.write("int Gi1/0/37\n")
    tn.write("switchport access vlan 1\n")
    tn.write("shutdown\n")
    tn.write("no shutdown\n")
    tn.write("end\n")
    tn.write("exit\n")
    global var1
    var1 = tn.read_all()
    SHVlan()

def Vlan2():
    tn = telnetlib.Telnet(HOST)
    tn.read_until("Username: ")
    tn.write(user + "\n")
    if password:
        tn.read_until("Password: ")
        tn.write(password + "\n")
    tn.write("enable\n")
    tn.write("cisco\n")
    tn.write("conf t\n")
    tn.write("int Gi1/0/37\n")
    tn.write("switchport access vlan 2\n")
    tn.write("shutdown\n")
    tn.write("no shutdown\n")
    tn.write("end\n")
    tn.write("exit\n")
    global var1
    var1 = tn.read_all()
    SHVlan()

def terminal():
    myobject = builder.get_object("label1")
    myobject.set_text(var1)

builder = Gtk.Builder()
builder.add_from_file("cisco.glade")
builder.connect_signals(Handler())
window = builder.get_object("window")
window.show_all()

Gtk.main()
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
global state

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

    def onButtonPressed(self, button):
        print(state())

    def onButton1Toggled(self, button):
        if button.get_active():
            state = state + Vlan1()
        else:
            state = state - Vlan1()

    def onButton2Toggled(self, button):
        if button.get_active():
            state = state + Vlan2()
        else:
            state = state - Vlan2()

    def onButton3Toggled(self, button):
        if button.get_active():
            state = state + SHVlan()
        else:
            state = state - SHVlan()

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
    tn.write("int loop 0\n")
    tn.write("ip address 1.1.1.1 255.255.255.255\n")
    tn.write("int loop 1\n")
    tn.write("ip address 2.2.2.2 255.255.255.255\n")
    tn.write("router ospf 1\n")
    tn.write("network 0.0.0.0 255.255.255.255 area 0\n")
    tn.write("end\n")
    tn.write("exit\n")

def terminal():
    myobject = builder.get_object("label1")
    myobject.set_text(var1)

builder = Gtk.Builder()
builder.add_from_file("cisco.glade")
builder.connect_signals(Handler())
window = builder.get_object("window")
window.show_all()

Gtk.main()
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

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onEntry0Changed(self, entry):
        global HOST 
        HOST = entry.get_text()
        print(HOST)

    def onEntry1Changed(self, entry):
        global user
        user = entry.get_text()
        print(user)

    def onEntry2Changed(self, entry):
        global password
        password = entry.get_text()
        print(password)

    def onButtonPressed(self, button):
        connect()

    def onRadioButtonaActivate(self, radio):
        radio.connect("toggled", self.onRadioButtonaActivate)
 

def connect():
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

def terminal():
    myobject = builder.get_object("label1")
    myobject.set_text(var1)

builder = Gtk.Builder()
builder.add_from_file("cisco.glade")
builder.connect_signals(Handler())
window = builder.get_object("window")
window.show_all()

Gtk.main()
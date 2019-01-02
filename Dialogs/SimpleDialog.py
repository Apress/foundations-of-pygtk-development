#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import getpass
import socket
import pwd

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        button = Gtk.Button.new_with_mnemonic("_Click Me")
        button.connect("clicked", self.on_button_clicked, self)
        self.add(button)
        self.set_size_request(180, 50)
        self.show_all()

    def on_button_clicked(self, button, parent):
        dialog = Gtk.Dialog(title="Edit User Information", parent=parent,
                            flags=Gtk.DialogFlags.MODAL)
        dialog.add_button("Ok", Gtk.ResponseType.OK)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.set_default_response(Gtk.ResponseType.OK)
        lbl1 = Gtk.Label("User Name:")
        lbl2 = Gtk.Label("Real Name:")
        lbl3 = Gtk.Label("Home Dir:")
        lbl4 = Gtk.Label("Host Name:")
        user = Gtk.Entry()
        real_name = Gtk.Entry()
        home = Gtk.Entry()
        host = Gtk.Entry()
        user.set_text(getpass.getuser())
        real_name.set_text(pwd.getpwuid(os.getuid())[4]) 
        home.set_text(os.environ['HOME'])
        host.set_text(socket.gethostname())
        grid = Gtk.Grid()
        grid.attach(lbl1, 0, 0, 1, 1)
        grid.attach(lbl2, 0, 1, 1, 1)
        grid.attach(lbl3, 0, 2, 1, 1)
        grid.attach(lbl4, 0, 3, 1, 1)
        grid.attach(user, 1, 0, 1, 1)
        grid.attach(real_name, 1, 1, 1, 1)
        grid.attach(home, 1, 2, 1, 1)
        grid.attach(host, 1, 3, 1, 1)
        dialog.vbox.pack_start(grid, False, False, 5)
        dialog.show_all()
        result = dialog.run()
        if result == Gtk.ResponseType.OK:
            print("User Name: " + user.get_text())
            print("Real Name: " + real_name.get_text())
            print("Home: " + home.get_text())
            print("Host: " + host.get_text())
        dialog.destroy()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Simple Dialog")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

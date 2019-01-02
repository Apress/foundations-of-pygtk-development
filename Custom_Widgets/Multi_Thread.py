#!/usr/bin/python3

import sys, threading, queue, time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def dbsim(q1, q2):
    while True:
        data = q1.get()
        # the request is always the same for our purpose
        items = {'lname':"Bunny", 'fname':"Bugs", 
                 'street':"Termite Terrace", 'city':"Hollywood",
                 'state':"California", 'zip':"99999", 
                 'employer':"Warner Bros.", 'position':"Cartoon character",
                 'credits':"Rabbit Hood, Haredevil Hare, What's Up Doc?"}
        q2.put(items)
        q1.task_done()


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lname    = None
        self.fname    = None
        self.street   = None
        self.city     = None
        self.state    = None
        self.zip      = None
        self.employer = None
        self.position = None
        self.credits  = None
        self.q1 = queue.Queue()
        self.q2 = queue.Queue()
        self.thrd = threading.Thread(target=dbsim, daemon=True, args=(self.q1, self.q2))
        self.thrd.start()

        # window setup
        self.set_border_width(10)
        grid = Gtk.Grid.new()
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)
        # name
        label = Gtk.Label.new("Last name:")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 0, 0, 1, 1)
        self.lname = Gtk.Entry.new()
        grid.attach(self.lname, 1, 0, 1, 1)
        label = Gtk.Label.new("First name:")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 2, 0, 1, 1)
        self.fname = Gtk.Entry.new()
        grid.attach(self.fname, 3, 0, 1, 1)
        # address
        label = Gtk.Label.new("Street:")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 0, 1, 1, 1)
        self.street = Gtk.Entry.new()
        grid.attach(self.street, 1, 1, 1, 1)
        label = Gtk.Label.new("City:")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 2, 1, 1, 1)
        self.city = Gtk.Entry.new()
        grid.attach(self.city, 3, 1, 1, 1)
        label = Gtk.Label.new("State:")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 0, 2, 1, 1)
        self.state = Gtk.Entry.new()
        grid.attach(self.state, 1, 2, 1, 1)
        label = Gtk.Label.new("Zip:")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 2, 2, 1, 1)
        self.zip = Gtk.Entry.new()
        grid.attach(self.zip, 3, 2, 1, 1)
        # employment status
        label = Gtk.Label.new("Employer:")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 0, 3, 1, 1)
        self.employer = Gtk.Entry.new()
        grid.attach(self.employer, 1, 3, 1, 1)
        label = Gtk.Label.new("Position:")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 2, 3, 1, 1)
        self.position = Gtk.Entry.new()
        grid.attach(self.position, 3, 3, 1, 1)
        label = Gtk.Label.new("Credits:")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 0, 4, 1, 1)
        self.credits = Gtk.Entry.new()
        grid.attach(self.credits, 1, 4, 3, 1)
        # buttons
        bb = Gtk.ButtonBox(Gtk.Orientation.HORIZONTAL)
        load_button = Gtk.Button.new_with_label("Load")
        bb.pack_end(load_button, False, False, 0)
        load_button.connect("clicked", self.on_load_button_clicked)
        save_button = Gtk.Button.new_with_label("Save")
        bb.pack_end(save_button, False, False, 0)
        save_button.connect("clicked", self.on_save_button_clicked)
        cancel_button = Gtk.Button.new_with_label("Cancel")
        bb.pack_end(cancel_button, False, False, 0)
        cancel_button.connect("clicked", self.on_cancel_button_clicked)
        # box setup
        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.add(grid)
        vbox.add(bb)
        self.add(vbox)

    def on_cancel_button_clicked(self, button):
        self.destroy()

    def on_load_button_clicked(self, button):
        self.q1.put('request')
        # wait for the results to be queued
        data = None
        while Gtk.events_pending() or data == None:
            Gtk.main_iteration()
            try:
                data = self.q2.get(block=False)
            except queue.Empty:
                continue
        self.lname.set_text(data['lname'])
        self.fname.set_text(data['fname'])
        self.street.set_text(data['street'])
        self.city.set_text(data['city'])
        self.state.set_text(data['state'])
        self.zip.set_text(data['zip'])
        self.employer.set_text(data['employer'])
        self.position.set_text(data['position'])
        self.credits.set_text(data['credits'])
        self.q2.task_done()

    def on_save_button_clicked(self, button):
        self.lname.set_text("")
        self.fname.set_text("")
        self.street.set_text("")
        self.city.set_text("")
        self.state.set_text("")
        self.zip.set_text("")
        self.employer.set_text("")
        self.position.set_text("")
        self.credits.set_text("")


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, 
                                    title="Multi-Thread")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

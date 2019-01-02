#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.resize(300, 100)
        # create a grid
        grid1 = Gtk.Grid()
        grid1.height = 2
        grid1.width = 2
        grid1.set_column_homogeneous(True)
        grid1.set_row_homogeneous(True)
        self.add(grid1)
        # build the aligned labels
        label1 = Gtk.Label('Top left Aligned')
        label1.can_focus = False
        label1.set_halign(Gtk.Align.START)
        label1.set_valign(Gtk.Align.START)
        grid1.attach(label1, 0, 0, 1, 1)
        label2 = Gtk.Label('Top right Aligned')
        label2.can_focus = False
        label2.set_halign(Gtk.Align.END)
        label2.set_valign(Gtk.Align.START)
        grid1.attach(label2, 1, 0, 1, 1)
        label3 = Gtk.Label('Bottom left Aligned')
        label3.can_focus = False
        label3.set_halign(Gtk.Align.START)
        label3.set_valign(Gtk.Align.END)
        grid1.attach(label3, 0, 1, 1, 1)
        label4 = Gtk.Label('Bottom right Aligned')
        label4.can_focus = False
        label4.set_halign(Gtk.Align.END)
        label4.set_valign(Gtk.Align.END)
        grid1.attach(label4, 1, 1, 1, 1)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None
        gtk_version = float(str(Gtk.MAJOR_VERSION)+'.'+str(Gtk.MINOR_VERSION))
        if gtk_version < 3.16:
            print('There is a bug in versions of GTK older that 3.16.')
            print('Your version is not new enough to prevent this bug from')
            print('causing problems in the display of this solution.')
            exit(0)

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, 
                                    title="Alignment")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

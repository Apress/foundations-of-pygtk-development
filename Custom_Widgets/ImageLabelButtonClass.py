#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ImageLabelButton(Gtk.Button):

    def __init__(self, orientation=Gtk.Orientation.HORIZONTAL, 
                 image="image-missing", label="Missing", 
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        # now set up more properties
        hbox = Gtk.Box(orientation, spacing=0)
        if not isinstance(image, str):
            raise TypeError("Expected str, got %s instead." % str(image))
        icon_theme = Gtk.IconTheme.get_default()
        icon = icon_theme.load_icon(image, -1, 
                                    Gtk.IconLookupFlags.FORCE_SIZE)
        img = Gtk.Image.new_from_pixbuf(icon)
        hbox.pack_start(img, True, True, 0)
        img.set_halign(Gtk.Align.END)
        if not isinstance(label, str):
            raise TypeError("Expected str, got %s instead." % str(label))
        if len(label) > 15:
            raise ValueError("The length of str may not exceed 15 characters.")
        labelwidget = Gtk.Label(label)
        hbox.pack_start(labelwidget, True, True, 0)
        labelwidget.set_halign(Gtk.Align.START)
        self.add(hbox)

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(25)
        button = ImageLabelButton(image="window-close", label="Close")
        button.connect("clicked", self.on_button_clicked)
        button.set_relief(Gtk.ReliefStyle.NORMAL)
        self.add(button)
        self.set_size_request(170, 50)

    def on_button_clicked(self, button):
        self.destroy()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, 
                                    title="ImageLabelButton")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

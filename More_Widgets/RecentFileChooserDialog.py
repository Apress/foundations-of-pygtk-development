#!/usr/bin/python3

import sys
import urllib 
from urllib.request import pathname2url
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

class Widgets():

    def __init__(self):
        self.window = None
        self.textview = None
        self.recent = None

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w = Widgets()
        w.window = self
        self.set_border_width(5)
        self.set_size_request(600, 400)
        w.textview = Gtk.TextView.new()
        fd = Pango.font_description_from_string("Monospace 10")
        self.modify_font(fd)
        swin = Gtk.ScrolledWindow.new(None, None)
        openbutton = Gtk.Button.new_with_label("open")
        save = Gtk.Button.new_with_label("Save")
        icon_theme = Gtk.IconTheme.get_default()
        icon = icon_theme.load_icon("document-open", -1, 
                                    Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        w.recent = Gtk.MenuToolButton.new(image, "Recent Files")
        manager = Gtk.RecentManager.get_default()
        menu = Gtk.RecentChooserMenu.new_for_manager(manager)
        w.recent.set_menu(menu)
        menu.set_show_not_found(False)
        menu.set_local_only(True)
        menu.set_limit(10)
        menu.set_sort_type(Gtk.RecentSortType.MRU)
        menu.connect("selection-done", self.menu_activated, w)
        openbutton.connect("clicked", self.open_file, w)
        save.connect("clicked", self.save_file, w)
        w.recent.connect("clicked", self.open_recent_file, w)
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        hbox.pack_start(openbutton, False, False, 0)
        hbox.pack_start(save, False, False, 0)
        hbox.pack_start(w.recent, False, False, 0)
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        swin.add(w.textview)
        vbox.pack_start(hbox, False, False, 0)
        vbox.pack_start(swin, True, True, 0)
        w.window.add(vbox)

    def save_file(self, save, w):
        filename = w.window.get_title()
        buffer = w.textview.get_buffer()
        (start, end) = buffer.get_bounds()
        content = buffer.get_text(start, end, False)
        f = open(filename, 'w')
        f.write(content)
        f.close()

    def menu_activated(self, menu, w):
        filename = menu.get_current_uri()
        if filename != None:
            fn = os.path.basename(filename)
            f = open(fn, 'r')
            contents = f.read()
            f.close()
            w.window.set_title(fn)
            buffer = w.textview.get_buffer()
            buffer.set_text(content, -1)
        else:
            print("The file '%s' could not be read!" % filename)

    def open_file(self, openbutton, w):
        dialog = Gtk.FileChooserDialog(title="Open File", parent=w.window,
                                       action=Gtk.FileChooserAction.OPEN,
                                       buttons=("Cancel", 
                                       Gtk.ResponseType.CANCEL,
                                       "Open", 
                                       Gtk.ResponseType.OK))
        if dialog.run() == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            content = ""
            f = open(filename, 'r')
            content = f.read()
            f.close()
            if len(content) > 0:
                # Create a new recently used resource.
                data = Gtk.RecentData()
                data.display_name = None
                data.description = None
                data.mime_type = "text/plain"
                data.app_name = os.path.basename(__file__)
                data.app_exec = " " + data.app_name + "%u"
                #data.groups = ["testapp", None]
                data.is_private = False
                url = pathname2url(filename)
                # Add the recently used resource to the default recent manager.
                manager = Gtk.RecentManager.get_default()
                result = manager.add_full(url, data)
                # Load the file and set the filename as the title of the window. 
                w.window.set_title(filename)
                buffer = w.textview.get_buffer()
                buffer.set_text(content, -1)
        dialog.destroy()

    def open_recent_file(self, recent, w):
        manager = Gtk.RecentManager.get_default()
        dialog = Gtk.RecentChooserDialog(title="Open Recent File",
                                         parent=w.window, 
                                         recent_manager=manager,
                                         buttons=("Cancel", 
                                         Gtk.ResponseType.CANCEL,
                                         "Open", 
                                         Gtk.ResponseType.OK))
        # Add a filter that will display all of the files in the dialog.
        filter = Gtk.RecentFilter.new()
        filter.set_name("All Files")
        filter.add_pattern("*")
        dialog.add_filter(filter)
        # Add another filter that will only display plain text files.
        filter = Gtk.RecentFilter.new()
        filter.set_name("Plain Text")
        filter.add_mime_type("text/plain")
        dialog.add_filter(filter)
        dialog.set_show_not_found(False)
        dialog.set_local_only(True)
        dialog.set_limit(10)
        dialog.set_sort_type(Gtk.RecentSortType.MRU)
        if dialog.run() == Gtk.ResponseType.OK:
            filename = dialog.get_current_uri()
            if filename != None:
                # Remove the "file://" prefix from the beginning of the 
                # URI if it exists.
                content = ""
                fn = os.path.basename(filename)
                f = open(fn, 'r')
                contents = f.read()
                f.close()
                if len(content) > 0:
                    w.window.set_title(fn)
                    buffer = w.textview.get_buffer()
                    buffer.set_text(content, -1)
                else:
                    print("The file '%s' could not be read!" % filename)
        dialog.destroy()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, 
                                    title="Recent Files")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

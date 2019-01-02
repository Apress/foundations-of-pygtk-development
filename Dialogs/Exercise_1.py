#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)

        savebutton = Gtk.Button.new_with_label("Save a File")
        createbutton = Gtk.Button.new_with_label("Create a New Folder")
        openbutton = Gtk.Button.new_with_label("Open One or More Files")
        selectbutton = Gtk.Button.new_with_label("Select a Folder")

        savebutton.connect("clicked", self.on_save_clicked)
        createbutton.connect("clicked", self.on_create_clicked)
        openbutton.connect("clicked", self.on_open_clicked)
        selectbutton.connect("clicked", self.on_select_clicked)

        vbox = Gtk.Box.new (Gtk.Orientation.VERTICAL, 5)
        vbox.pack_start(savebutton, False, False, 5)
        vbox.pack_start(createbutton, False, False, 5)
        vbox.pack_start(openbutton, False, False, 5)
        vbox.pack_start(selectbutton, False, False, 5)

        self.add (vbox)

    def on_save_clicked(self, button):
        dialog = Gtk.Dialog(title="Save File As ...",
                            buttons=("Cancel", Gtk.ResponseType.CANCEL,
                                     "Save", Gtk.ResponseType.OK),
                            parent=self)
        dialog.set_border_width(10)
        dialog.set_size_request(600, -1)
        chooser = Gtk.FileChooserWidget.new(Gtk.FileChooserAction.SAVE)

        dialog.vbox.pack_start(chooser, False, False, 5)
        dialog.show_all()

        result = dialog.run()
        if result == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            print("Saving file as: %s", filename)

        dialog.destroy()

    def on_create_clicked(self, button):
        dialog = Gtk.Dialog(title="Create a Folder",
                            buttons=("Cancel", Gtk.ResponseType.CANCEL,
                                     "Create", Gtk.ResponseType.OK),
                            parent=self)
        dialog.set_border_width(10)
        dialog.set_size_request(600, -1)
        chooser = Gtk.FileChooserWidget.new(Gtk.FileChooserAction.CREATE_FOLDER)

        dialog.vbox.pack_start(chooser, False, False, 5)
        dialog.show_all()

        result = dialog.run()
        if result == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            print("Creating directory: %s", filename)

        dialog.destroy()


    def on_open_clicked(self, button):
        dialog = Gtk.Dialog(title="Open file(s) ...",
                            buttons=("Cancel", Gtk.ResponseType.CANCEL,
                                     "Open", Gtk.ResponseType.OK),
                            parent=self)
        dialog.set_border_width(10)
        dialog.set_size_request(600, -1)
        chooser = Gtk.FileChooserWidget.new(Gtk.FileChooserAction.OPEN)
        chooser.set_select_multiple(True)

        dialog.vbox.pack_start(chooser, False, False, 5)
        dialog.show_all()

        result = dialog.run()
        if result == Gtk.ResponseType.OK:
            filenames = chooser.get_filenames()
            for filename in filenames:
                print("Open file: %s", filename)

        dialog.destroy()


    def on_select_clicked(self, button):
        dialog = Gtk.Dialog(title="Select Folder ...",
                            buttons=("Cancel", Gtk.ResponseType.CANCEL,
                                     "Select", Gtk.ResponseType.OK),
                            parent=self)
        dialog.set_border_width(10)
        dialog.set_size_request(600, -1)
        chooser = Gtk.FileChooserWidget.new(Gtk.FileChooserAction.SELECT_FOLDER)

        dialog.vbox.pack_start(chooser, False, False, 5)
        dialog.show_all()

        result = dialog.run()
        if result == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            print("Selected directory: %s", filename)

        dialog.destroy()


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Exercise 1")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

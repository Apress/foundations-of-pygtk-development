#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        button = Gtk.Button.new_with_mnemonic("_Click Me")
        button.connect("clicked", self.on_button_clicked, self)
        self.add(button)
        self.set_size_request(150, 50)
        self.show_all()

    def on_button_clicked(self, button, parent):
        authors = ["Author #1", "Author #2"]
        documenters = ["Documenter #1", "Documenter #2"]
        dialog = Gtk.AboutDialog(parent=parent)
        logo = GdkPixbuf.Pixbuf.new_from_file("./logo.png")
        if logo != None:
            dialog.set_logo(logo)
        else:
            print("A GdkPixbuf Error has occurred.")
        dialog.set_name("Gtk.AboutDialog")
        dialog.set_version("3.0")
        dialog.set_copyright("(C) 2007 Andrew Krause")
        dialog.set_comments("All about Gtk.AboutDialog")
        dialog.set_license("Free to all!")
        dialog.set_website("http://book.andrewKrause.net")
        dialog.set_website_label("book.andrewkrause.net")
        dialog.set_authors(authors)
        dialog.set_documenters(documenters)
        dialog.set_translator_credits("Translator #1\nTranslator #2")
        dialog.connect("response", self.on_dialog_button_clicked)
        dialog.run()

    def on_dialog_button_clicked(self, dialog, response):
        dialog.destroy()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="About Dialog")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

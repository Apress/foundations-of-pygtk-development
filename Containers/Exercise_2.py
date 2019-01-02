#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(250, 200)

        notebook = Gtk.Notebook.new()
        notebook.set_show_tabs(False)

        for i in range(0, 4):
            label = Gtk.Label.new("Tab")
            button = Gtk.Button.new_with_mnemonic("_Next Tab")

            expander = Gtk.Expander.new("You Are Viewing Tab %s" % str(i+1))
            expander.set_expanded(True)
            expander.add (button)

            notebook.append_page(expander, label)
            expander.set_border_width(10)

            button.connect("clicked", self.on_notebook_button_clicked, notebook)

        buttonbox = Gtk.ButtonBox.new(Gtk.Orientation.HORIZONTAL)
        button_prev = Gtk.Button.new_with_label("Previous Page")
        button_prev.connect("clicked", self.on_button_prev_clicked, notebook)
        button_close = Gtk.Button.new_with_label("Close")
        button_close.connect("clicked", self.on_button_close_clicked)
        buttonbox.pack_end(button_prev, False, False, 5)
        buttonbox.pack_end(button_close, False, False, 5)

        paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
        paned.pack1(notebook, True, False)
        paned.pack2(buttonbox, True, False)

        self.add(paned)

    def on_notebook_button_clicked(self, button, notebook):
        nextpage = notebook.props.page + 1
        if nextpage == 4:
            nextpage = 0
        notebook.set_current_page(nextpage)

    def on_button_prev_clicked(self, button, notebook):
        nextpage = notebook.props.page - 1
        if nextpage == -1:
            nextpage = 3
        notebook.set_current_page(nextpage)

    def on_button_close_clicked(self, button):
        self.destroy()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Notebook")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

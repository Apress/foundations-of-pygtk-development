#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(250, 150)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        notebook = Gtk.Notebook.new()
        notebook.set_tab_pos(Gtk.PositionType.BOTTOM)
        vbox.pack_start(notebook, False, False, 5)

        label1 = Gtk.Label.new("Page 1")
        label2 = Gtk.Label.new("Page 2")
        label3 = Gtk.Label.new("Page 3")
        label4 = Gtk.Label.new("Page 4")

        button1 = Gtk.Button.new_with_label("Go to Page 2")
        button1.connect("clicked", self.on_notebook_button_clicked, notebook)
        button2 = Gtk.Button.new_with_label("Go to Page 3")
        button2.connect("clicked", self.on_notebook_button_clicked, notebook)
        button3 = Gtk.Button.new_with_label("Go to Page 4")
        button3.connect("clicked", self.on_notebook_button_clicked, notebook)
        button4 = Gtk.Button.new_with_label("Go to Page 1")
        button4.connect("clicked", self.on_notebook_button_clicked, notebook)

        page1 = notebook.append_page(button1, label1)
        page2 = notebook.append_page(button2, label2)
        page3 = notebook.append_page(button3, label3)
        page4 = notebook.append_page(button4, label4)

        buttonbox = Gtk.ButtonBox.new(Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(buttonbox, False, False, 5)
        button_prev = Gtk.Button.new_with_label("Previous Page")
        button_prev.connect("clicked", self.on_button_prev_clicked, notebook)
        button_close = Gtk.Button.new_with_label("Close")
        button_close.connect("clicked", self.on_button_close_clicked)
        buttonbox.pack_end(button_prev, False, False, 5)
        buttonbox.pack_end(button_close, False, False, 5)

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

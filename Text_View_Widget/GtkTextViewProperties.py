#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(250, 150)
        font = Pango.font_description_from_string("Monospace Bold 10")
        textview = Gtk.TextView.new()
        textview.modify_font(font)
        textview.set_wrap_mode(Gtk.WrapMode.WORD)
        textview.set_justification(Gtk.Justification.RIGHT)
        textview.set_editable(True)
        textview.set_cursor_visible(True)
        textview.set_pixels_above_lines(5)
        textview.set_pixels_below_lines(5)
        textview.set_pixels_inside_wrap(5)
        textview.set_left_margin(10)
        textview.set_right_margin(10)
        buffer = textview.get_buffer()
        text = "This is some text!\nChange me!\nPlease!"
        buffer.set_text(text, len(text))
        scrolled_win = Gtk.ScrolledWindow.new(None, None)
        scrolled_win.set_policy(Gtk.PolicyType.AUTOMATIC, 
                                Gtk.PolicyType.ALWAYS)
        scrolled_win.add(textview)
        self.add(scrolled_win)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, 
                                    title="Text Views Properties")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

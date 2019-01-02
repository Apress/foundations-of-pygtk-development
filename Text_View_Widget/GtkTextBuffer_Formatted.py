#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

text_to_scales = [("Quarter Sized", 0.25),
                  ("Double Extra Small", 0.5787037037037),
                  ("Extra Small", 0.6444444444444),
                  ("Small", 0.8333333333333),
                  ("Medium", 1.0), ("Large", 1.2),
                  ("Extra Large", 1.4399999999999),
                  ("Double Extra Large", 1.728),
                  ("Double Sized", 2.0)]

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(500, -1)
        textview = Gtk.TextView.new()
        buffer = textview.get_buffer()
        buffer.create_tag("bold", weight=Pango.Weight.BOLD)
        buffer.create_tag("italic", style=Pango.Style.ITALIC)
        buffer.create_tag("strike", strikethrough=True)
        buffer.create_tag("underline", underline=Pango.Underline.SINGLE)
        bold = Gtk.Button.new_with_label("Bold")
        italic = Gtk.Button.new_with_label("Italic")
        strike = Gtk.Button.new_with_label("Strike")
        underline = Gtk.Button.new_with_label("Underline")
        clear = Gtk.Button.new_with_label("Clear")
        scale_button = Gtk.ComboBoxText.new()
        i = 0
        while i < len(text_to_scales):
            (name, scale) = text_to_scales[i]
            scale_button.append_text(name)
            buffer.create_tag(tag_name=name, scale=scale)
            i += 1
        bold.__setattr__("tag", "bold")
        italic.__setattr__("tag", "italic")
        strike.__setattr__("tag", "strike")
        underline.__setattr__("tag", "underline")
        bold.connect("clicked", self.on_format, textview)
        italic.connect("clicked", self.on_format, textview)
        strike.connect("clicked", self.on_format, textview)
        underline.connect("clicked", self.on_format, textview)
        clear.connect("clicked", self.on_clear_clicked, textview)
        scale_button.connect("changed", self.on_scale_changed, textview)
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        vbox.pack_start(bold, False, False, 0)
        vbox.pack_start(italic, False, False, 0)
        vbox.pack_start(strike, False, False, 0)
        vbox.pack_start(underline, False, False, 0)
        vbox.pack_start(scale_button, False, False, 0)
        vbox.pack_start(clear, False, False, 0)
        scrolled_win = Gtk.ScrolledWindow.new(None, None)
        scrolled_win.add(textview)
        scrolled_win.set_policy(Gtk.PolicyType.AUTOMATIC, 
                                Gtk.PolicyType.ALWAYS)
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        hbox.pack_start(scrolled_win, True, True, 0)
        hbox.pack_start(vbox, False, True, 0)
        self.add(hbox)

    def on_format(self, button, textview):
        tagname = button.tag
        buffer = textview.get_buffer()
        (start, end) = buffer.get_selection_bounds()
        buffer.apply_tag_by_name(tagname, start, end)

    def on_scale_changed(self, button, textview):
        if button.get_active() == -1:
            return
        text = button.get_active_text()
        button.__setattr__("tag", text)
        self.on_format(button, textview)
        button.set_active(-1)

    def on_clear_clicked(self, button, textview):
        buffer = textview.get_buffer()
        (start, end) = buffer.get_selection_bounds()
        buffer.remove_all_tags(start, end)

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Text Tags")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

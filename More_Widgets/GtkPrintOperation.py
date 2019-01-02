#!/usr/bin/python3

import sys
import math
from os.path import expanduser
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Gtk, cairo, Pango, PangoCairo

class Widgets:
    
    def __init__(self):
        self.window = None
        self.chooser = None
        self.data = None
        self.settings = Gtk.PrintSettings.new()

class PrintData:

    def __init__(self):
        self.filename = None
        self.fontsize = None
        self.lines_per_page = None
        self.lines = None
        self.total_lines = None
        self.total_pages = None


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.HEADER_HEIGHT = 20.0
        self.HEADER_GAP = 8.5
        w = Widgets()
        w.window = self
        self.set_border_width(10)
        w.chooser = Gtk.FileChooserButton.new ("Select a File",
                                              Gtk.FileChooserAction.OPEN)
        w.chooser.set_current_folder(expanduser("~"))
        print = Gtk.Button.new_with_label("Print")
        print.connect("clicked", self.print_file, w)
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        hbox.pack_start(w.chooser, False, False, 0)
        hbox.pack_start(print, False, False, 0)
        self.add(hbox)

    def print_file(self, button, w):
        filename = w.chooser.get_filename()
        if filename == None:
            return
        operation = Gtk.PrintOperation.new()
        if w.settings != None:
            operation.set_print_settings(w.settings)
        w.data = PrintData()
        w.data.filename = filename
        w.data.font_size = 10.0
        operation.connect("begin_print", self.begin_print, w)
        operation.connect("draw_page", self.draw_page, w)
        operation.connect("end_print", self.end_print, w)
        res = operation.run(Gtk.PrintOperationAction.PRINT_DIALOG,
                            w.window)
        if res == Gtk.PrintOperationResult.APPLY:
            if w.settings != None:
                w.settings = None
            settings = operation.get_print_settings()
        elif res == Gtk.PrintOperationResult.ERROR:
            dialog = Gtk.MessageDialog.new(w.window, 
                                           Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                           Gtk.MessageType.ERROR, 
                                           Gtk.ButtonsType.S_CLOSE,
                                           "Print operation error.")
            dialog.run()
            dialog.destroy()

    def begin_print(self, operation, context, w):
        w.data.lines = []
        f = open(w.data.filename)
        for line in f:
            w.data.lines.append(line)
        f.close()
        w.data.total_lines = len(w.data.lines)
        height = context.get_height() - self.HEADER_HEIGHT - self.HEADER_GAP
        w.data.lines_per_page = math.floor(height / (w.data.font_size + 3))
        w.data.total_pages = (w.data.total_lines - 1) / w.data.lines_per_page + 1
        operation.set_n_pages(w.data.total_pages)

    def draw_page(self, operation, context, page_nr, w):
        cr = context.get_cairo_context()
        width = context.get_width()
        layout = context.create_pango_layout()
        desc = Pango.font_description_from_string("Monospace")
        desc.set_size(w.data.font_size * Pango.SCALE)
        layout.set_font_description(desc)
        layout.set_text(w.data.filename, -1)
        layout.set_width(-1)
        layout.set_alignment(Pango.Alignment.LEFT)
        (width, height) = layout.get_size()
        text_height = height / Pango.SCALE
        cr.move_to(0, (self.HEADER_HEIGHT - text_height) / 2)
        PangoCairo.show_layout(cr, layout)
        page_str = "%d of %d" % (page_nr + 1, w.data.total_pages)
        layout.set_text(page_str, -1)
        (width, height) = layout.get_size()
        layout.set_alignment(Pango.Alignment.RIGHT)
        cr.move_to(width - (width / Pango.SCALE),
                   (self.HEADER_HEIGHT - text_height) / 2)
        PangoCairo.show_layout(cr, layout)
        cr.move_to(0, self.HEADER_HEIGHT + self.HEADER_GAP)
        line = page_nr * w.data.lines_per_page
        #for (i = 0; i < w.data.lines_per_page && line < w.data.total_lines; i++)
        i = 0
        while i < w.data.lines_per_page and line < w.data.total_lines:
            layout.set_text(w.data.lines[line], -1)
            PangoCairo.show_layout(cr, layout)
            cr.rel_move_to(0, w.data.font_size + 3)
            line += 1
            i += 1

    def end_print(self, operation, context, w):
        w.data.lines = None
        w.data = None

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, 
                                    title="Calendar")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

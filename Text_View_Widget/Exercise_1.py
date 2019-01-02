#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(300, -1)

        textview = Gtk.TextView.new()
        search = Gtk.Entry.new()
        search.set_text("Search for ...")

        new = Gtk.Button.new_with_label("New")
        openb = Gtk.Button.new_with_label("Open")
        save = Gtk.Button.new_with_label("Save")
        cut = Gtk.Button.new_with_label("Cut")
        copy = Gtk.Button.new_with_label("Copy")
        paste = Gtk.Button.new_with_label("Paste")
        find = Gtk.Button.new_with_label("Find")

        new.connect("clicked", self.on_new_clicked, textview)
        openb.connect("clicked", self.on_open_clicked, textview)
        save.connect("clicked", self.on_save_clicked, textview)
        cut.connect("clicked", self.on_cut_clicked, textview)
        copy.connect("clicked", self.on_copy_clicked, textview)
        paste.connect("clicked", self.on_paste_clicked, textview)
        find.connect("clicked", self.on_find_clicked, textview, search)

        scrolled_win = Gtk.ScrolledWindow.new()
        scrolled_win.add(textview)

        vbox1 = Gtk.Box.new (Gtk.Orientation.VERTICAL, 5)
        vbox1.pack_start(new, False, False, 0)
        vbox1.pack_start(openb, False, False, 0)
        vbox1.pack_start(save, False, False, 0)
        vbox1.pack_start(cut, False, False, 0)
        vbox1.pack_start(copy, False, False, 0)
        vbox1.pack_start(paste, False, False, 0)

        searchbar = Gtk.Box.new (Gtk.Orientation.HORIZONTAL, 5)
        searchbar.pack_start(search, False, False, 0)
        searchbar.pack_start(find, False, False, 0)

        hbox1 = Gtk.Box.new (Gtk.Orientation.HORIZONTAL, 5)
        hbox1.pack_start(scrolled_win, True, True, 0)
        hbox1.pack_start(vbox1, False, False, 0)

        vbox2 = Gtk.Box.new (Gtk.Orientation.VERTICAL, 5)
        vbox2.pack_start(hbox1, True, True, 0)
        vbox2.pack_start(searchbar, False, False, 0)

        self.add(vbox2)
        self.show_all()

    def on_new_clicked(self, button, textview): 
       dialog = Gtk.MessageDialog(title="Question", parent=self, 
                                  flags=Gtk.DialogFlags.MODAL)
       dialog.set_border_width(10)
       dialog.add_button("Yes", Gtk.ResponseType.YES)
       dialog.add_button("No", Gtk.ResponseType.NO)
       dialog.props.text = "All changes will be lost.\nDo you want to continue?"
       dialog.show_all()
       response = dialog.run()
       if response == Gtk.ResponseType.YES:
           buffer = textview.get_buffer()
           buffer.set_text("")
       dialog.destroy()

    def on_open_clicked(self, button, textview): 
        dialog = Gtk.FileChooserDialog(title="Choose a file ..", 
                                       parent=self,
                                       flags=Gtk.FileChooserAction.OPEN,
                                       buttons=("Open", Gtk.ResponseType.APPLY,
                                       "Cancel", Gtk.ResponseType.CANCEL))
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.APPLY:
            buffer = textview.get_buffer()
            file = dialog.get_filename()
            f = open(file, 'r')
            content = f.read()
            f.close()
            buffer.set_text(content)
        dialog.destroy()

    def on_save_clicked(self, button, textview): 
        dialog = Gtk.FileChooserDialog(title="Save the file ..", 
                                       parent=self,
                                       flags=Gtk.FileChooserAction.SAVE,
                                       buttons=("Save", Gtk.ResponseType.APPLY,
                                       "Cancel", Gtk.ResponseType.CANCEL))
        response = dialog.run()
        if response == Gtk.ResponseType.APPLY:
            file = dialog.get_filename()
            buffer = textview.get_buffer()
            (start, end) = buffer.get_bounds()
            content = buffer.get_text(start, end, True)
            f = open(file, 'w')
            f.write(content)
            f.close()
        dialog.destroy()

    def on_cut_clicked(self, button, textview): 
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        buffer = textview.get_buffer()
        buffer.cut_clipboard(clipboard, True)

    def on_copy_clicked(self, button, textview): 
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        buffer = textview.get_buffer()
        buffer.copy_clipboard(clipboard)

    def on_paste_clicked(self, button, textview): 
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        buffer = textview.get_buffer()
        buffer.paste_clipboard(clipboard, None, True)

    def on_find_clicked(self, button, textview, search): 
        find = search.get_text()
        buffer = textview.get_buffer()
        cursorpos = buffer.props.cursor_position
        start = buffer.get_iter_at_offset(cursorpos)
        end = buffer.get_iter_at_offset(-1)
        if start.compare(end) != 0:
            start.forward_char()
        success = start.forward_search(find, 0, None)
        if success != None and len(success) != 0:
            (start, end) = success
            mark = buffer.create_mark(None, start, False)
            textview.scroll_mark_onscreen(mark)
            buffer.delete_mark(mark)
            buffer.select_range(start, end)
        else:
            dialog = Gtk.MessageDialog(title="Information", parent=self, 
                                       flags=Gtk.DialogFlags.MODAL)
            dialog.set_border_width(10)
            dialog.add_button("Ok", Gtk.ResponseType.OK)
            dialog.props.text = "The text was not found!"
            dialog.show_all()
            dialog.run()
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

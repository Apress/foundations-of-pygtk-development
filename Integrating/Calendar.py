#!/usr/bin/python3

import sys
import xml.sax
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Event():
    # A structure used to hold a single event.
    def __init__(self):
        self.name = None
        self.location = None
        self.day = None
        self.month = None
        self.year = None
        self.start = None
        self.end = None


class CalendarContentHandler(xml.sax.ContentHandler):

    def __init__(self):
        super().__init__()
        self.event = None      # the current event
        self.tag_name = None   # the current xml tag name
        self.events = []       # the list of events

    def startElement(self, name, attrs):
        if name == "event":
            self.event = Event()
        self.tag_name = name

    def endElement(self, name):
        if name == "event":
            self.events.append(self.event)

    def characters(self, content):
        cdata = content.strip()
        if cdata == None or cdata == "":
            return
        if self.tag_name == "name":
            self.event.name = cdata
        elif self.tag_name == "location":
            self.event.location = cdata
        elif self.tag_name == "day":
            self.event.day = cdata
        elif self.tag_name == "month":
            self.event.month = cdata
        elif self.tag_name == "year":
            self.event.year = cdata
        elif self.tag_name == "start":
            self.event.start = cdata
        elif self.tag_name == "end":
            self.event.end = cdata
        else:
            return


class SignalHandlers():

    def __init__(self, builder):
        self.builder = builder
        self.events = []        # the list of events
        self.NAME = 0           # treeview column 1
        self.LOCATION = 1       # treeview column 2
        self.TIME = 2           # treeview column 3
        self.filename = None    # the current events file


    def on_new_clicked(self, button):
        window = self.builder.get_object("window")
        dialog = Gtk.FileChooserDialog(title="Create a New Calendar", 
                                  action=Gtk.FileChooserAction.SAVE,
                                  modal=True, parent=window,
                                  buttons=("Cancel", 
                                           Gtk.ResponseType.CANCEL,
                                           "Save", 
                                           Gtk.ResponseType.ACCEPT))
        dialog.set_do_overwrite_confirmation(False)
        result = dialog.run()
        if result == Gtk.ResponseType.ACCEPT:
            self.save_calendar_list()
            self.filename = dialog.get_filename()
            self.events = []
            self. load_calendar_list(self.filename)
            calendar = self.builder.get_object("calendar")
            self.on_day_changed(calendar)
        dialog.destroy()


    def on_open_clicked(self, button):
        window = self.builder.get_object("window")
        dialog = Gtk.FileChooserDialog(title="Open a New Calendar", 
                                  action=Gtk.FileChooserAction.OPEN,
                                  modal=True, parent=window,
                                  buttons=("Cancel", 
                                           Gtk.ResponseType.CANCEL,
                                           "Open", 
                                           Gtk.ResponseType.ACCEPT))
        dialog.set_do_overwrite_confirmation(False)
        result = dialog.run()
        if result == Gtk.ResponseType.ACCEPT:
            self.save_calendar_list()
            self.filename = dialog.get_filename()
            self.events = []
            self. load_calendar_list(self.filename)
            calendar = self.builder.get_object("calendar")
            self.on_day_changed(calendar)
        dialog.destroy()


    def on_add_clicked(self, button):
        dialog = self.builder.get_object("dialog")
        name = self.builder.get_object("event_name")
        location = self.builder.get_object("location")
        start = self.builder.get_object("start_time")
        end = self.builder.get_object("end_time")
        # Reset the event name and location since the dialog is reused.
        name.set_text("")
        location.set_text("")
        response = dialog.run()
        if response == Gtk.ResponseType.APPLY:
            # Create a new event with the entered name, location and start time.
            calendar = self.builder.get_object("calendar")
            (year, month, day) = calendar.get_date()
            calendar = self.builder.get_object("calendar")
            (year, month, day) = calendar.get_date()
            event = Event()
            event.day = str(day)
            event.month = str(month+1)
            event.year = str(year)
            event.name = name.get_text()
            event.location = location.get_text()
            event.start = start.get_active_text()

            # If the start time is "All Day", make the end time an empty string.
            if event.start == "All Day":
                event.end = ""
            else:
                event.end = end.get_active_text()
            self.events.append(event)
            self.save_calendar_list()
            self.on_day_changed(calendar)
        dialog.hide()


    def on_remove_clicked(self, button):
        treeview = self.builder.get_object("treeview")
        store = self.builder.get_object("liststore")
        selection = treeview.get_selection()
        (model, iter) = selection.get_selected()
        if iter == None:
            return
        (name, location, time) = store.get(iter, self.NAME, self.LOCATION, self.TIME)
        words = time.split()
        if len(words) == 2:
            # start time was "All Day"
            start = time
            end = ""
        else:
            start = words[0]
            end = words[2]
        for event in self.events:
            if name == event.name and location == event.location and start == event.start and end == event.end:
                idx = self.events.index(event)
                del self.events[idx]
                self.save_calendar_list()
        calendar = self.builder.get_object("calendar")
        self.on_day_changed(calendar)


    def on_clear_clicked(self, button):
        self.events = []
        calendar = self.builder.get_object("calendar")
        self.on_day_changed(calendar)


    def on_month_changed(self, calendar):
        calendar = self.builder.get_object("calendar")
        self.on_day_changed(calendar)


    def on_day_changed(self, calendar):
        treeview = self.builder.get_object("treeview")
        store = self.builder.get_object("liststore")
        store.clear()
        (year, month, day) = calendar.get_date()
        for event in self.events:
            if event.end == None:
                event.end = ""
            if event.year == str(year) and event.month == str(month+1) and \
             event.day == str(day):
                if event.start != "All Day":
                    time = event.start + " to " + event.end
                else:
                    time = event.start
                iter = store.append()
                store.set(iter, (self.NAME, self.LOCATION, self.TIME),
                          (event.name, event.location, time))
        

    def load_calendar_list(self, filename):
        contenthandler = CalendarContentHandler()
        xml.sax.parse(filename, contenthandler)
        self.filename = filename
        self.events = contenthandler.events
        calendar = self.builder.get_object("calendar")
        self.on_day_changed(calendar)


    def save_calendar_list(self):
        f = open(self.filename, 'w')
        f.write("<calendar>\n")
        for event in self.events:
            f.write("  <event>\n")
            f.write("    <name>" + event.name + "</name>\n")
            f.write("    <location>" + event.location + "</location>\n")
            f.write("    <day>" + event.day + "</day>\n")
            f.write("    <month>" + event.month + "</month>\n")
            f.write("    <year>" + event.year + "</year>\n")
            f.write("    <start>" + event.start + "</start>\n")
            if event.end == None:
                event.end = ""
            f.write("    <end>" + event.end + "</end>\n")
            f.write("  </event>\n")
        f.write("</calendar>\n")
        f.close()


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(application_id="org.example.calendar",
                         *args, **kwargs)
        self.window = None


    def do_activate(self):
        if not self.window:
            builder = Gtk.Builder()
            builder.add_from_file("./Calendar.glade")
            self.window = builder.get_object("window")
            self.add_window(self.window)
            self.NAME = 0
            self.LOCATION = 1
            self.TIME = 2
            self.treeview = builder.get_object("treeview")
            self.config_treeview_columns(builder)
            sig = SignalHandlers(builder)
            builder.connect_signals(sig)
            sig.load_calendar_list("./Calendar_File.xml")
        self.window.show_all()


    def config_treeview_columns(self, builder):
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(cell_renderer=renderer, title="Event Name", text=self.NAME)
        self.treeview.append_column(column)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(cell_renderer=renderer, title="Location", text=self.LOCATION)
        self.treeview.append_column(column)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(cell_renderer=renderer, title="Event Time", text=self.TIME)
        self.treeview.append_column(column)

        store = builder.get_object("liststore")
        self.treeview.set_model(store)


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

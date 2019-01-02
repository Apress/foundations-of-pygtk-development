#!/usr/bin/python3

import sys
import os, signal
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GObject

class SignalHandlers():

    def __init__(self, builder):
        self.builder = builder
        self.SEQ = 0
        self.ADDRESS = 1
        self.TTL = 2
        self.TIME = 3
        self.UNITS = 4
        self.channel = None
        self.pid = None
        self.window = builder.get_object("window")
        self.treeview = builder.get_object("output")
        self.cpid = None
        self.setup_tree_view(self.treeview)

    def on_ping_clicked(self, button):
        requests = self.builder.get_object("requests")
        radio = self.builder.get_object("requests_num")
        address = self.builder.get_object("address")
        treeview = self.treeview
        
        # Create a new tree model with five columns for ping output.
        store = Gtk.ListStore.new((str, str, str, str, str))
        self.treeview.set_model(store)
        
        # Retrieve the current ping parameters entered by the user.
        num = requests.get_value_as_int()
        location = address.get_text()
        
        # Return if an address was not entered into the GtkEntry widget.
        if len(location) == 0:
            return
        # Otherwise, build the command based upon the user's preferences.
        elif radio.get_active():
            if num == 0:
                return
            command = "ping " + location + " -c " + str(num)
        else:
            command = "ping " + location
        
        # Parse the command and launch the process, monitoring standard output.
        (bool, argvp) = GLib.shell_parse_argv(command)
        if bool:
            (ret, self.cpid, fin, fout, ferr) = GLib.spawn_async_with_pipes(None, 
                                      argvp, None, GLib.SpawnFlags.SEARCH_PATH,
                                      None, None)
            if not ret:
                print("The 'ping' instruction has failed!")
            else:
                # Disable the Ping button and enable the Stop button.
                stop = self.builder.get_object("stop")
                stop.set_sensitive(True)
                ping = self.builder.get_object("ping")
                ping.set_sensitive(False)
            	  
                # Create a new IO channel and monitor it for data to read.
                channel = GLib.IOChannel.unix_new(fout)
                channel.add_watch(GLib.IOCondition.IN | GLib.IOCondition.ERR | 
                                  GLib.IOCondition.HUP, self.read_output, None)

    def on_stop_clicked(self, button):
        stop = self.builder.get_object("stop")
        stop.set_sensitive(False)
        ping = self.builder.get_object("ping")
        ping.set_sensitive(True)
  
        os.kill(self.cpid, signal.SIGINT)
        self.cpid = None

    def on_window_close(self, button):
        self.window.destroy()

    def setup_tree_view(self, treeview):
        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn(title="Seq", cell_renderer=renderer, 
                                    text=self.SEQ) 
        treeview.append_column(column)

        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn(title="Address", cell_renderer=renderer, 
                                    text=self.ADDRESS) 
        treeview.append_column(column)

        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn(title="TTL", cell_renderer=renderer, 
                                    text=self.TTL) 
        treeview.append_column(column)

        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn(title="Time", cell_renderer=renderer, 
                                    text=self.TIME) 
        treeview.append_column(column)

        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn(title="Units", cell_renderer=renderer, 
                                    text=self.UNITS) 
        treeview.append_column(column)


    def read_output(self, channel, condition, data):
        # Read the current line of data from the IO channel.
        errstatus = False
        try:
            (status, line, length, term) = channel.read_line()
        except IOError:
            print("Error reading IO channel.")
            errstatus = True

        # If some type of error has occurred, handle it.
        if errstatus or status != GLib.IOStatus.NORMAL or line == None: 
            print("Error reading IO channel.")

            # Disable the stop button and enable the ping button for future action.
            stop = self.builder.get_object("stop")
            stop.set_sensitive(False)
            ping = self.builder.get_object("ping")
            ping.set_sensitive(True)

            if channel != None:
                channel.shutdown(True)
            channel = None

            return False

        # Parse the line if an error has not occurred.
        self.parse_output(line)

        return True

    def parse_output(self, buffer):
        # Load the list store, split the string into lines and create a pointer.
        store = self.treeview.get_model()
        lines = buffer.splitlines()

        # Loop through each of the lines, parsing its content. 
        for line in lines:
            # If this is an empty string, move to the next string.
            if line == "":
                continue
            # Parse the line if it contains information about the current ping. 
            elif line.find("64 bytes") >= 0:
                # Extract the IP address of the computer you are pinging. 
                result = line.split("from ")
                result = result[1].split(':')
                address = result[0]

                # Extract the current ping count from the output. 
                result = line.split("seq=")
                result = result[1].split(" ")
                seq = result[0]

                # Extract the IP's "Time To Live" from the output.
                result = line.split("ttl=")
                result = result[1].split(" ")
                ttl = result[0]

                # Extract the time it took for this ping operation from the output.
                result = line.split("time=")
                result = result[1].split(" ")
                time = result[0]

                # Extrace the time units from the output.
                result = result[1].split(" ")
                units = result[0]

                # Append the information for the current ping operation. 
                iter = store.append ();
                store.set (iter, (self.SEQ, self.ADDRESS, self.TTL, self.TIME, 
                                  self.UNITS),
                           (seq, address, ttl, time, units))


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            builder = Gtk.Builder()
            builder.add_from_file("./Ping.glade")
            self.window = builder.get_object("window")
            builder.connect_signals(SignalHandlers(builder))
            self.add_window(self.window)
        self.window.show_all()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)


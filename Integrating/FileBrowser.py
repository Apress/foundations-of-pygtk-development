#!/usr/bin/python3

import sys
import os, time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GObject

ICON = 0
FILENAME = 1
SIZE = 2
MODIFIED = 3

size_type = ["B", "KiB", "MiB", "GiB"]

class History():

    def __init__(self):
        self.stack = []
        self.pos = -1

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(application_id="org.example.myapp", *args,
                         **kwargs)
        self.window = None
        self.dialog = None
        self.builder = None
        self.treeview = None
        self.history = History()
        self.statusbar = None

    def do_activate(self):
        if not self.window:
            self.builder = Gtk.Builder()
            self.builder.add_from_file("./FileBrowser.glade")
            self.window = self.builder.get_object("window")
            self.treeview = self.builder.get_object("treeview")

            # Glade does not allow us to add non-GTK items to the user data
            # for connection. Also, the Gtk.Builder widget is absent from
            # Glade as well. Therefore we have to make our connections to
            # the signal handlers manually.
            info = self.builder.get_object("info")
            info.connect_after("clicked", self.on_info_clicked, self.builder, 
                               self.history)

            self.treeview.connect_after("row_activated", self.on_row_activated, 
                                        self.builder, self.history)

            back = self.builder.get_object("back")
            back.connect_after("clicked", self.on_back_clicked, self.builder, 
                               self.history)

            forward = self.builder.get_object("forward")
            forward.connect_after("clicked", self.on_forward_clicked, self.builder, 
                               self.history)

            up = self.builder.get_object("up")
            up.connect_after("clicked", self.on_up_clicked, self.builder, 
                             self.history)

            home = self.builder.get_object("home")
            home.connect_after("clicked", self.on_home_clicked, self.builder, 
                               self.history)

            delete = self.builder.get_object("delete")
            delete.connect_after("clicked", self.on_delete_clicked, self.builder)

            go = self.builder.get_object("go")
            go.connect_after("clicked", self.on_go_clicked, self.builder, 
                             self.history)

            entry = self.builder.get_object("location")
            entry.connect_after("activate", self.on_location_activate, self.builder, 
                             self.history)

            refresh = self.builder.get_object("refresh")
            refresh.connect_after("clicked", self.on_refresh_clicked, self.builder) 

            self.setup_tree_view(self.treeview)
            self.setup_tree_model(self.treeview)
            self.add_window(self.window)
        self.window.show_all()

    def setup_tree_view(self, treeview):
        # Create a tree view column with an icon and file name.
        column = Gtk.TreeViewColumn.new()
        column.set_title("File Name")
        
        renderer = Gtk.CellRendererPixbuf.new()
        column.pack_start(renderer, False)
        column.set_attributes(renderer, pixbuf=ICON)
        
        renderer = Gtk.CellRendererText.new()
        column.pack_start(renderer, True)
        column.set_attributes(renderer, text=FILENAME)
        
        treeview.append_column(column)
        
        # Insert a second tree view column that displays the file size.
        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn.new()
        column.set_title("Size")
        column.pack_start(renderer, True)
        column.set_attributes(renderer, text=SIZE)
        treeview.append_column(column)
        
        # Insert a third tree view column that displays the last modified time/date.
        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn.new()
        column.set_title("Last Modified")
        column.pack_start(renderer, True)
        column.set_attributes(renderer, text=MODIFIED)
        treeview.append_column(column)

    def setup_tree_model(self, treeview):
        store = Gtk.ListStore.new((GdkPixbuf.Pixbuf, GObject.TYPE_STRING,
                              GObject.TYPE_STRING, GObject.TYPE_STRING))
        treeview.set_model(store)
        self.populate_tree_model(self.builder)

    def populate_tree_model(self, builder):
        treeview = builder.get_object("treeview")
        total_size = 0
        items = 0
        store = treeview.get_model()
        store.clear()
        location = os.getcwd()
        
        # If the current location is not the root directory, add the '..' entry.
        if len(location) > 1:
            icon_theme = Gtk.IconTheme.get_default()
            icon = icon_theme.load_icon("folder", -1, 
                                        Gtk.IconLookupFlags.FORCE_SIZE)
            iter = store.append()
            store.set(iter, (ICON, FILENAME), (icon, ".."))
        
        # Return if the path does not exist.
        if not os.path.isdir(location):
            self.file_manager_error("The path %s does not exist!" % (location,), builder)
        
        # Display the new location in the address bar.
        entry = builder.get_object("location")
        entry.set_text(location)
        
        # Add each file to the list along with the file size and modified date.
        pixbuf_dir = icon
        pixbuf_file = icon_theme.load_icon("text-x-generic", -1, 
                                        Gtk.IconLookupFlags.FORCE_SIZE)
        files = os.listdir(location)
        for file in files:
            fn = location + "/" + file
            st = os.stat(fn)
            if st:
                # Calculate the file size and order of magnitude.
                i = 0
                size = st.st_size
                total_size = size;
                while size >= 1024.0:
                    size = size / 1024.0
                    i += 1
                
                # Create strings for the file size and last modified date.
                filesize = "%.1f %s" % (size, size_type[i])
                modified = time.ctime(st.st_mtime)
            
            # Add the file and its properties as a new tree view row.
            iter = store.append()
            
            if os.path.isdir(fn):
                store.set(iter, (ICON, FILENAME, SIZE, MODIFIED),
                          (pixbuf_dir, file, filesize, modified))
            else:
                store.set(iter, (ICON, FILENAME, SIZE, MODIFIED),
                          (pixbuf_file, file, filesize, modified))
            items += 1
        
        # Calculate the total size of the directory content.
        i = 0
        while total_size >= 1024.0:
            total_size = total_size / 1024.0
            i += 1
        
        # Add the number of items and the total size of the directory content
        # to the status bar.
        statusbar = builder.get_object("statusbar")
        message = "%d items, Total Size: %.1f %s" % (items,
                                   total_size, size_type[i])
        context_id = statusbar.get_context_id("FileBrowser")
        statusbar.pop(context_id)
        statusbar.push(context_id, message)

    def file_manager_error(self, message, builder):
        window = builder.get_object("window")
        dialog = builder.get_object("dialog")
        dialog = Gtk.MessageDialog(parent=window, modal=True, 
                                   message_type=Gtk.MessageType.ERROR, 
                                   buttons=("OK", Gtk.ResponseType.OK),
                                   title="File Manager Error")
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def on_info_clicked(self, button, builder, history):
        treeview = builder.get_object("treeview")
        dialog = builder.get_object("dialog")
        selection = treeview.get_selection()

        (model, iter) = selection.get_selected()
        if iter:
            name = builder.get_object("name")
            loc = builder.get_object("location")
            type = builder.get_object("type")
            size = builder.get_object("size")
            mod = builder.get_object("modified")
            accessed = builder.get_object("accessed")
            (file,) = model.get(iter, FILENAME)

            # Set the file name, location and whether it is a file or directory.
            location = os.getcwd()
            name.set_text(file)
            loc.set_text(location)
            file = location + "/" + file
            if os.path.isdir(file):
                type.set_text("Directory")
            else:
                type.set_text("File")

            # Set the file size, last modified date and last accessed date.
            st = os.stat(file)
            if st:
                i = 0
                file_size = st.st_size
                while file_size >= 1024.0:
                    file_size = file_size / 1024.0
                    i += 1

            modified = time.ctime(st.st_mtime)
            access = time.ctime(st.st_atime)
            mod.set_text(modified)
            accessed.set_text(access)
            size.set_text("%.1f %s" % (file_size, size_type[i]))

            dialog.run()
            dialog.hide()

    def on_back_clicked(self, button, builder, history):
        if len(history.stack) > 0:
            if history.pos > -1:
                previous_loc = history.stack[history.pos]
                history.pos -= 1
                os.chdir(previous_loc)   
                self.populate_tree_model(builder)

    def on_forward_clicked(self, button, builder, history ):
        if history.pos < len(history.stack) - 1:
            history.pos += 1
        next_loc = history.stack[history.pos]
        os.chdir(next_loc)
        self.populate_tree_model(builder)

    def on_up_clicked(self, button, builder, history):
        os.chdir("..")
        location = os.getcwd()

        entry = builder.get_object("location")
        entry.set_text(location)
        go = builder.get_object("go")
        self.on_go_clicked(go, builder, history)

    def on_refresh_clicked(self, button, builder):
        self.populate_tree_model(builder)

    def on_home_clicked(self, button, builder, history):
        go = builder.get_object("go")
        entry = builder.get_object("location")
        entry.set_text(os.getenv("HOME"))
        self.on_go_clicked(go, builder, history)

    def on_delete_clicked(self, button, builder):
        entry = builder.get_object("location")
        treeview = builder.get_object("treeview")
        window = builder.get_object("window")
        location = os.getcwd()

        # If there is a selected file, delete it if the user approves.
        selection = treeview.get_selection()
        (model, iter) = selection.get_selected()
        if iter:
            (file,) = model.get(iter, FILENAME)
            if file == "..":
                self.file_manager_error("You cannot remove the '..' directory!", 
                                        builder)
                return

            entry.set_text(location)
            rmlocation = location + "/" + file
            
            # Ask the user if it is okay to remove the file or folder.
            msg = "Do you really want to delete %s?" % file
            dialog = Gtk.MessageDialog(parent=window, modal=True, 
                                       message_type=Gtk.MessageType.QUESTION, 
                                       buttons=("Yes", Gtk.ResponseType.YES,
                                                "No", Gtk.ResponseType.NO),
                                       text=msg)
            
            # If the user approves, remove the file or report ane error.
            response = dialog.run()
            if response == Gtk.ResponseType.YES:
                if os.path.isdir(rmlocation):
                    try:
                        shutil.rmtree(rmlocation)
                    except Exception as e:
                        self.file_manager_error(
                            "The file or folder could not be removed!", builder)
                    self.populate_tree_model(builder)
                else:
                    try:
                        os.remove(rmlocation)
                    except Exception as e:
                        self.file_manager_error(
                            "The file or folder could not be removed!", builder)
                    self.populate_tree_model(builder)
            dialog.destroy()

    def on_go_clicked(self, button, builder, history):
        treeview = builder.get_object("treeview")
        entry = builder.get_object("location")
        location = entry.get_text()
        
        # If the directory exists, visit the entered location.
        if os.path.isdir(location):
            self.store_history(history)
            os.chdir(location)
            self.populate_tree_model(builder)
        else:
            self.file_manager_error("The location does not exist!", builder)

    def on_location_activate(self, button, builder, history):
        go = builder.get_object("go")
        self.on_go_clicked(go, builder, history)

    def on_row_activated(self, treeview, path, column, builder, history):
        treeview = builder.get_object("treeview")
        model = treeview.get_model()
        iter = model.get_iter(path)
        if iter:
            (file,) = model.get(iter, FILENAME)
            
            # Move to the parent directory.
            if file == "..":
                self.store_history(history)
                os.chdir("..")
                self.populate_tree_model(builder)
            # Move to the chosen directory or show more information about the file.
            else:
                location = os.getcwd() + "/" + file
                if os.path.isdir(location):
                    self.store_history(history)
                    os.chdir(location)
                    self.populate_tree_model(builder)
                else:
                    info = builder.get_object("info")
                    self.on_info_clicked(info, builder, history)  

    def store_history(self, history):
        location = os.getcwd()
        history.stack.append(location)
        history.pos = len(history.stack) - 1

    def pop_history(self, history):
        if len(history.stack) > 0:
            history.stack.pop()
            if history.stack.pos > len(history.stack) - 1:
                history.pos = len(history.stack) - 1
            else:
                history.pos -= 1



if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

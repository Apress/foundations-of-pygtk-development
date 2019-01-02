    def set_up_treeview(self, treeview):
        column = Gtk.TreeViewColumn.new()
        column.set_resizable(True)
        column.set_title("Some Items")
        renderer = Gtk.CellRendererPixbuf.new()
        # it is important to pack the renderer BEFORE adding attributes!!
        column.pack_start(renderer, False)
        column.add_attribute(renderer, "pixbuf", ICON)
        renderer = Gtk.CellRendererText.new()
        # it is important to pack the renderer BEFORE adding attributes!!
        column.pack_start(renderer, True)
        column.add_attribute(renderer, "text", ICON_NAME)
        treeview.append_column(column)

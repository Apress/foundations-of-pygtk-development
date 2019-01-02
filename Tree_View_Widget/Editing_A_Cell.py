    def set_up_treeview(self, treeview):
        renderer = Gtk.CellRenderer.Text.new()
        column = Gtk.TreeViewColumn.new_with_attributes("Buy", renderer, 
                                                        "text", BUY_IT)
        treeview.append_column(column)
        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn.new_with_attributes("Count", renderer, 
                                                        "text", QUANTITY)
        treeview.append_column(column)

        # Set up the third column in the tree view to be editable.
        renderer = Gtk.CellRendererText.new()
        renderer.set_property("editable", True)
        renderer.connect("edited", self.cell_edited, treeview)
        column = Gtk.TreeViewColumn.new_with_attributes("Product", renderer, 
                                                        "text", PRODUCT)
        treeview.append_column(column)

    def cell_edited(self, renderer, path, new_text, treeview):
        if len(new_text) > 0:
            model = treeview.get_model()
            iter = model.get_iter_from_string(path)
            if iter:
                model.set(iter, PRODUCT, new_text)

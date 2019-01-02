    def setup_tree_view(self, treeview):
        # Create a GtkListStore that will be used for the combo box renderer.
        model = Gtk.ListStore.new((GObject.TYPE_STRING, 
                                  GObject.TYPE_STRING))
        iter = model.append()
        model.set(iter, 0, "None")
        iter = model.append()
        model.set(iter, 0, "One")
        iter = model.append()
        model.set(iter, 0, "Half a Dozen")
        iter = model.append()
        model.set(iter, 0, "Dozen")
        iter = model.append()
        model.set(iter, 0, "Two Dozen")
        # Create the GtkCellRendererCombo and add the tree model. Then, add the
        # renderer to a new column and add the column to the GtkTreeView.
        renderer = Gtk.CellRendererCombo(text_column=0, editable=True, 
                                         has_entry=True, model=model)
        column = Gtk.TreeViewColumn("Count", renderer, text=QUANTITY)
        treeview.append_column(column)
        renderer.connect("edited", self.cell_edited, treeview)
        renderer = Gtk.CellRendererText.new()
        column = Gtk.TreeViewColumn("Product", renderer, text=PRODUCT)
        treeview.append_column(column)

    def cell_edited(self, renderer, path, new_text, treeview):
        # Make sure the text is not empty. If not, apply it to the tree view cell.
        if new_text != "":
            model = treeview.get_model()
            iter = model.get_iter_from_string(path)
            if iter:
                model.set(iter, QUANTITY, new_text)

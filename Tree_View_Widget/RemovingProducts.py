    def remove_row(self, ref, model):
        # Convert the tree row reference to a path and retrieve the iterator.
        path = ref.get_path()
        iter = model.get_iter(path)
        # Only remove the row if it is not a root row.
        parent = model.iter_parent(iter)
        if parent:
            (buy, quantity) = model.get(iter, BUY_IT, QUANTITY)
            (pnum,) = model.get(parent, QUANTITY)
            if (buy):
                pnum -= quantity
                model.set(parent, QUANTITY, pnum)
            iter = model.get_iter(path)
            model.remove(iter)

    def remove_products(self, button, treeview):
        selection = treeview.get_selection()
        model = treeview.get_model()
        rows = selection.get_selected_rows(model)
        # Create tree row references to all of the selected rows.
        references = []
        for data in rows:
            ref = Gtk.TreeRowReference.new(model, data)
            references.append(ref)
        for ref in references:
            self.remove_row(ref, model)

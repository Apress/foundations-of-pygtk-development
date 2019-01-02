    def cell_edited(self, renderer, path, new_text, treeview):
        # Retrieve the current value stored by the spin button renderer's adjustment.
        adjustment = renderer.get_property("adjustment")
        value = "%.0f" % adjustment.get_value()
        model = treeview.get_model()
        iter = model.get_iter_from_string(path)
        if iter:
            model.set(iter, QUANTITY, value)

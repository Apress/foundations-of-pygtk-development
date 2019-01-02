    def setup_tree_view(self, renderer, column, adj):
        adj = Gtk.Adjustment.new(0.0, 0.0, 100.0, 1.0, 2.0, 2.0)
        renderer = Gtk.CellRendererSpin(editable=True, adjustment=adj, digits=0)
        column = Gtk.TreeViewColumn("Count", renderer, text=QUANTITY)
        treeview.append_column(column)        
        renderer.connect("edited", self.cell_edited, treeview)

        # Add a cell renderer for the PRODUCT column

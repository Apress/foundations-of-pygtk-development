
class ooQuestionDialog(Gtk.Dialog):

    hbox = None
    vbox = None

    def __init__(self, title="Error!", parent=None,
                 flags=Gtk.DialogFlags.MODAL, 
                 buttons=("NO", Gtk.ResponseType.NO, "_YES", 
                          Gtk.ResponseType.YES)):
        super().__init__(title=title, parent=parent, flags=flags, 
                         buttons=buttons)
        self.vbox = self.get_content_area()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, 
                            spacing=5)
        icon_theme = Gtk.IconTheme.get_default()
        icon = icon_theme.load_icon("dialog-question", 48,
                                    Gtk.IconLookupFlags.FORCE_SVG)
        image = Gtk.Image.new_from_pixbuf(icon)
        self.hbox.pack_start(image, False, False, 5)
        self.vbox.add(self.hbox)

    def set_message(self, message, add_msg=None):
        self.hbox.pack_start(Gtk.Label(message), False, False, 5)
        if add_msg != None:
            expander = Gtk.Expander.new_with_mnemonic( \
                "_Click me for more information.")
            expander.add(Gtk.Label(add_msg))
            self.vbox.pack_start(expander, False, False, 10)

    def run(self):
        self.show_all()
        response = super().run()
        self.destroy()
        return response

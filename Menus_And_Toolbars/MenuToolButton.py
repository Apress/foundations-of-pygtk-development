recent = Gtk.Menu.new()
# Add a number of menu items where each corresponds to one recent file.
icon_theme = Gtk.IconTheme.get_default()
icon = icon_theme.load_icon("document-open", -1, 
                            Gtk.IconLookupFlags.FORCE_SIZE)
image = Gtk.Image.new_from_pixbuf(icon)
open = Gtk.MenuToolButton.new(image, label)
open.set_menu(recent)

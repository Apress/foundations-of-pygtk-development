#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import time

class assistant(Gtk.Assistant):
    progress = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_request(450, 300)
        self.set_title("Gtk.Assistant Example")
        self.connect("destroy", Gtk.main_quit, None)
        # create page 0
        page0_widget = Gtk.Label("This in an example of a Gtk.Assistant. By\n" +
                                 "clicking the forward button, you can " +
                                 "continue\nto the next section!")
        self.append_page(page0_widget)
        self.set_page_title(page0_widget, "Introduction")
        self.set_page_type(page0_widget, Gtk.AssistantPageType.INTRO)
        self.set_page_complete(page0_widget, True)
        # create page 1
        page1_widget = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        label = Gtk.Label("Your Name: ")
        entry = Gtk.Entry()
        page1_widget.pack_start(label, False, False, 5)
        page1_widget.pack_start(entry, False, False, 5)
        self.append_page(page1_widget)
        self.set_page_title(page1_widget, "")
        self.set_page_type(page1_widget, Gtk.AssistantPageType.CONTENT)
        self.set_page_complete(page1_widget, False)
        # create page 2
        page2_widget = Gtk.CheckButton.new_with_label("Click me to Continue!")
        self.append_page(page2_widget)
        self.set_page_title(page2_widget, "Click the Check Button")
        self.set_page_type(page2_widget, Gtk.AssistantPageType.CONTENT)
        self.set_page_complete(page2_widget, False)
        # create page 3
        page3_widget = Gtk.Alignment.new(0.5, 0.5, 0.0, 0.0)
        button = Gtk.Button.new_with_label("Click Me!")
        self.progress = Gtk.ProgressBar()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox.pack_start(self.progress, True, False, 5)
        hbox.pack_start(button, False, False, 5)
        page3_widget.add(hbox)
        self.append_page(page3_widget)
        self.set_page_title(page3_widget, "Click the Check Button")
        self.set_page_type(page3_widget, Gtk.AssistantPageType.PROGRESS)
        self.set_page_complete(page3_widget, False)
        # create page 4
        page4_widget = Gtk.Label("Text has been entered in the label and the\n" +
                                 "combo box is clicked. If you are done, then\n" +
                                 "it is time to leave!")
        self.append_page(page4_widget)
        self.set_page_title(page4_widget, "Confirmation")
        self.set_page_type(page4_widget, Gtk.AssistantPageType.CONFIRM)
        self.set_page_complete(page4_widget, True)
        # set up the callbacks
        entry.connect("changed", self.entry_changed)
        page2_widget.connect("toggled", self.button_toggled)
        button.connect("clicked", self.button_clicked)
        self.connect("cancel", self.assistant_canceled)
        self.connect("close", self.assistant_close)

    def entry_changed(self, entry):
        text = entry.get_text()
        num = self.get_current_page()
        page = self.get_nth_page(num)
        self.set_page_complete(page, len(text) > 0)

    def button_toggled(self, toggle):
        active = toggle.get_active()
        self.set_page_complete(toggle, active)

    def button_clicked(self, button):
        percent = 0.0
        button.set_sensitive(False)
        page = self.get_nth_page(3)
        while (percent <= 100.0):
            message = str(percent) + " complete"
            print(message)
            self.progress.set_fraction(percent / 100.0)
            self.progress.set_text(message)
            while (Gtk.events_pending()):
                Gtk.main_iteration()
            time.sleep(1)
            percent += 5.0
        self.set_page_complete(page, True)

    def assistant_canceled(self, response):
        self.destroy()

    def assistant_close(self, response):
        print("You would apply your changes now!")
        self.destroy()

class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(25)
        button = Gtk.Button.new_with_mnemonic("_Open Assistant")
        button.connect("clicked", self.on_start_button_clicked)
        button.set_relief(Gtk.ReliefStyle.NORMAL)
        self.add(button)
        self.set_size_request(200, 100)

    def on_start_button_clicked(self, button):
        assistant()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Gtk.Assistant")
        self.window.show_all()
        self.window.present()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

#!/usr/bin/python3

import sys
import math
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango



class SignalHandlers():

    def __init__(self, builder):
        self.builder = builder
        self.entry = None
        self.OP_NULL = 0
        self.OP_ADD = 1
        self.OP_SUBTRACT = 2
        self.OP_MULTIPLY = 3
        self.OP_DIVIDE = 4
        self.OP_POWER = 5
        self.clear_value = False
        self.value_set = False
        self.prev_value = 0
        self.pending_op = self.OP_NULL

        entry = builder.get_object("output")
        self.entry = entry
        fd = Pango.font_description_from_string("Monospace Bold 16")
        entry.set_text("0")
        entry.modify_font(fd)

        # Set user data for the operators and decimal buttons.
        add = builder.get_object("add")
        add.operator = self.OP_ADD
        sub = builder.get_object("sub")
        sub.operator = self.OP_SUBTRACT
        mul = builder.get_object("mul")
        mul.operator = self.OP_MULTIPLY
        div = builder.get_object("div")
        div.operator = self.OP_DIVIDE
        power = builder.get_object("power")
        power.operator = self.OP_POWER
        decimal = builder.get_object("decimal")
        decimal.number = 10

        # Set the user data for the number buttons.
        for i in range(0, 10):
            name = "num_%i" % (i,)
            num = builder.get_object(name)
            num.number = i

    def do_operation(self, entry, value):
        # Perform the specified operation, either add, subtract, multiply, 
        # divide, or the power operation.

        # Perform the operation on prev_value with the new value and store 
        # the result back into prev_value.
        if self.pending_op == self.OP_ADD:
            self.prev_value += value
        elif self.pending_op == self.OP_SUBTRACT:
            self.prev_value -= value
        elif self.pending_op == self.OP_MULTIPLY:
            self.prev_value *= value
        elif self.pending_op == self.OP_DIVIDE:
            self.prev_value /= value;
        elif self.pending_op == self.OP_POWER:
            self.prev_value = pow(prev_value, value)
        else:
            return

        # Reset the pending operation and create a string with the new value.
        self.pending_op = self.OP_NULL
        entry.set_text(self.format_num(self.prev_value))

    def on_num_clicked(self, button):
        # Retrieve the number that is stored in user data.
        num = button.number

        # Clear the value if a new number should be entered.
        if self.clear_value:
            self.entry.set_text("0")
            self.clear_value = False

        # Append a decimal place to the GtkEntry. Make sure to keep track of
        #  whether the decimal place was already entered.
        text = self.entry.get_text()
        if (num == 10):
            if len(text) > 9:
                return
            elif text.find('.') >= 0:
                return
            else:
                text = text + '.'
        # Append a number place to the GtkEntry if the length is less than 10.
        else:
            text = text + str(num)
            if len(text) > 10:
                    return
        # Remove preceeding zeros. 
        text = text.lstrip('0')
        self.entry.set_text(text)

    def on_equal_clicked(self, button):
        # Perform any pending operations because the equal button was pressed.
        value = float(self.entry.get_text())
  
        self.do_operation(self.entry, value)
        self.clear_value = True
        self.value_set = False

    def on_op_clicked(self, button):
        op = button.operator
        value = float(self.entry.get_text())

        # Perform any pending operations and then store the new operation.
        self.do_operation(self.entry, value)
        self.pending_op = op;
        self.clear_value = True

        # Set the current value as the previous value if it should be 
        # overwritten.
        if not self.value_set:
            self.prev_value = value;
            self.value_set = True

    def on_sign_clicked(self, button):
        value = float(self.entry.get_text())
        
        # You cannot negate a value of zero.
        if value == 0.0:
            return
        value *= -1
        
        self.entry.set_text(self.format_num(value))

    def on_sqrt_clicked(self, button):
        # Take the square root of the current value.
        value = math.sqrt(float(self.entry.get_text()))
  
        self.entry.set_text(self.format_num(value))

    def on_clear_clicked(self, button):
        self.entry.set_text("0")
  
        self.clear_value = False
        self.value_set = False
        self.prev_value = 0
        self.pending_op = self.OP_NULL

    def format_num(self, num):
        text = str(num)
        text = text.rstrip('0')
        text = text.lstrip('0')
        text = text.rstrip('.')  # remove trailing decimal
        return text

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None
        self.builder = None

    def do_activate(self):
        if not self.window:
            self.builder = Gtk.Builder()
            self.builder.add_from_file("./Calculator.glade")
            self.window = self.builder.get_object("window")
            self.builder.connect_signals(SignalHandlers(self.builder))
            self.add_window(self.window)
        self.window.show_all()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)


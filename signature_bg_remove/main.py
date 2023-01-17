import gi
import gui
import img
import utils

gi.require_version("Gtk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gtk


def load() -> None:
    """Load images to windows from file."""
    original_pixbuf = utils.path_to_pixbuf(file)
    opencv_image = img.extract_signature(utils.path_to_opencv(file), method)
    opencv_pixbuf = utils.opencv_to_pixbuf(opencv_image)

    original_window.set_from_pixbuf(original_pixbuf)
    opencv_window.set_from_pixbuf(opencv_pixbuf)


def config_clicked() -> None:
    """Handle config button click."""
    global method
    method = gui.config_dialog(method)
    load()


def open_clicked() -> None:
    """Handle open button click."""
    global file
    file = gui.select_dialog()
    load()


def save_clicked() -> None:
    """Handle save button click."""
    gui.save_dialog(opencv_window.get_pixbuf())


method = "binary"
file = gui.select_dialog()

window = Gtk.Window()
window.set_title("Signature Extractor")
window.set_default_size(800, 600)
window.connect("destroy", Gtk.main_quit)

header = Gtk.HeaderBar()
header.set_show_close_button(True)

config = Gtk.Button()
config.set_label("Config")
config.connect(
    "clicked",
    lambda x: config_clicked(),
)

open = Gtk.Button()
open.set_label("Open")
open.set_image(Gtk.Image.new_from_icon_name("document-open", Gtk.IconSize.BUTTON))
open.connect("clicked", lambda _: open_clicked())

save = Gtk.Button()
save.set_label("Save")
save.set_image(Gtk.Image.new_from_icon_name("document-save", Gtk.IconSize.BUTTON))
save.connect(
    "clicked",
    lambda _: save_clicked(),
)

header.pack_end(save)
header.pack_end(open)
header.pack_end(config)
header.set_title("Signature Extractor")
window.set_titlebar(header)

stack = Gtk.Stack()
stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
stack.set_transition_duration(500)

original_window = Gtk.Image()
opencv_window = Gtk.Image()
load()

stack.add_titled(original_window, "original", "Original")
stack.add_titled(opencv_window, "extracted", "Extracted")

stack_switcher = Gtk.StackSwitcher()
stack_switcher.set_stack(stack)
stack_switcher.set_halign(Gtk.Align.CENTER)

header.pack_start(stack_switcher)
window.add(stack)
window.show_all()
Gtk.main()

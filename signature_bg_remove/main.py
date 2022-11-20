import cv2 as cv
import gi
import numpy as np

import img
import gui

gi.require_version("Gtk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf, Gtk


def open_image(
    og_window: Gtk.ScrolledWindow, ocv_window: Gtk.ScrolledWindow, method: str
) -> cv.Mat:
    """Open image from file."""
    # Get Original Image
    og_img = gui.select_dialog()

    # Convert to Transparent OpenCV Image
    ocv_img = img.extract_signature(cv.imread(og_img), method)

    # Convert Original and Transparent Images to GTK Images
    gtk_ocv_img = ocv_to_gtk(ocv_img)
    gtk_og_img = Gtk.Image.new_from_file(og_img)

    # Add GTK Images to Respective Windows
    og_window.add(gtk_og_img)
    ocv_window.add(gtk_ocv_img)
    return ocv_img


def main():
    """Run main function."""

    window = Gtk.Window()
    window.set_title("Signature Extractor")
    window.set_default_size(800, 600)
    window.set_border_width(10)
    window.connect("destroy", Gtk.main_quit)

    og_window = Gtk.ScrolledWindow()
    ocv_window = Gtk.ScrolledWindow()

    ocv_img = open_image(og_window, ocv_window, "binary")

    headerbar = Gtk.HeaderBar()
    headerbar.set_show_close_button(True)

    config_button = Gtk.Button()
    config_button.set_label("Config")
    config_button.connect(
        "clicked", lambda x: open_image(og_window, ocv_window, gui.config_dialog())
    )

    # open_button = Gtk.Button()
    # open_button.set_label("Open")
    # open_button.set_image(
    #     Gtk.Image.new_from_icon_name("document-open", Gtk.IconSize.BUTTON)
    # )
    # open_button.connect("clicked", lambda _: open_image(imagewindow))

    download_button = Gtk.Button()
    download_button.set_label("Save")
    download_button.set_image(
        Gtk.Image.new_from_icon_name("document-save", Gtk.IconSize.BUTTON)
    )
    download_button.connect("clicked", lambda _: gui.save_dialog(ocv_img))

    headerbar.pack_end(download_button)
    # headerbar.pack_end(open_button)
    headerbar.pack_end(config_button)
    headerbar.set_title("Signature Extractor")
    window.set_titlebar(headerbar)

    stack = Gtk.Stack()
    stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
    stack.set_transition_duration(500)

    stack.add_titled(og_window, "og", "Original")
    stack.add_titled(ocv_window, "ocv", "Extracted")

    stack_switcher = Gtk.StackSwitcher()
    stack_switcher.set_stack(stack)
    stack_switcher.set_halign(Gtk.Align.CENTER)

    # set stack switcher to headerbar
    headerbar.pack_start(stack_switcher)

    window.add(stack)
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()

"""GTK GUI for signature_bg_remove."""

import sys

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf, Gtk


def select_dialog() -> str:
    """Select image from file."""
    dialog = Gtk.FileChooserDialog(
        "Choose an image of your signature",
        None,
        Gtk.FileChooserAction.OPEN,
        (
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        ),
    )
    # Only show png files
    filter_image = Gtk.FileFilter()
    filter_image.set_name("Image files")
    filter_image.add_mime_type("image/png")
    filter_image.add_mime_type("image/jpeg")
    filter_image.add_mime_type("image/jpg")
    dialog.add_filter(filter_image)
    response = dialog.run()
    if response == Gtk.ResponseType.CANCEL:
        dialog.destroy()
        sys.exit(0)
    filename = dialog.get_filename()
    if filename is None:
        dialog.destroy()
        sys.exit(0)
    dialog.destroy()
    return filename


def config_dialog(current_method: str) -> str:
    """Allow user to pick extraction method."""
    dialog = Gtk.Dialog(
        "Choose an extraction method",
        None,
        Gtk.DialogFlags.MODAL,
        (
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK,
        ),
    )
    dialog.set_default_size(300, 100)

    methods = ["binary", "adaptive", "otsu", "canny", "sobel", "laplacian"]
    radio_group = None
    for method in methods:
        radio = Gtk.RadioButton.new_with_label_from_widget(radio_group, method.capitalize())
        radio_group = radio
        if method == current_method:
            radio.set_active(True)
        dialog.vbox.pack_start(radio, True, True, 0)

    dialog.show_all()
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        for radio in radio_group.get_group():
            if radio.get_active():
                current_method = radio.get_label().lower()
    dialog.destroy()
    return current_method


def save_dialog(pixbuf: GdkPixbuf.Pixbuf) -> None:
    """Save transparent signature to file of user's choosing."""
    dialog = Gtk.FileChooserDialog(
        "Choose a location to save your signature",
        None,
        Gtk.FileChooserAction.SAVE,
        (
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        ),
    )
    dialog.set_filename("transparent_signature.png")
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        pixbuf.savev(dialog.get_filename(), "png", [], [])
    dialog.destroy()

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
    img: str = dialog.get_filename()
    dialog.destroy()
    return img


def config_dialog() -> str:
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

    # radio group
    radio_buttons = ["binary", "adaptive", "otsu", "canny", "sobel", "laplacian"]
    for radio_button in radio_buttons:
        radio_button = Gtk.RadioButton.new_with_label_from_widget(
            None, radio_button.capitalize()
        )
        dialog.vbox.pack_start(radio_button, True, True, 0)

    dialog.show_all()
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        for radio_button in radio_buttons:
            if radio_button.get_active():
                method = radio_button.get_label().lower()
    else:
        method = "binary"
    return method


def save_dialog(img: Gtk.Image) -> None:
    """Save transparent signature to file of user's choosing."""
    if img is not None:
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
            img.get_pixbuf().savev(dialog.get_filename(), "png", [], [])
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

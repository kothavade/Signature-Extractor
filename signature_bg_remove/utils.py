import gi

gi.require_version("GdkPixbuf", "2.0")
gi.require_version("Gtk", "3.0")

from gi.repository import GdkPixbuf, Gtk


def opencv_to_gtk(opencv_img) -> Gtk.Image:
    """Convert OpenCV image to GTK image."""
    height, width, channels = opencv_img.shape
    return Gtk.Image.new_from_pixbuf(
        GdkPixbuf.Pixbuf.new_from_data(
            opencv_img.tobytes(),
            GdkPixbuf.Colorspace.RGB,
            True,
            8,
            width,
            height,
            channels * width,
        )
    )

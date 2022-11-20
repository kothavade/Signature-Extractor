import gi
import numpy as np

gi.require_version("GdkPixbuf", "2.0")
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")

import cv2 as cv
from gi.repository import Gdk, GdkPixbuf, Gtk


def opencv_to_pixbuf(opencv_image: cv.Mat) -> GdkPixbuf.Pixbuf:
    """Convert OpenCV image to GDK pixbuf."""
    height, width, channels = opencv_image.shape
    pixbuf = GdkPixbuf.Pixbuf.new_from_data(
        opencv_image.tobytes(),
        GdkPixbuf.Colorspace.RGB,
        True,
        8,
        width,
        height,
        channels * width,
    )
    return pixbuf


def path_to_opencv(path: str) -> cv.Mat:
    """Convert image path to OpenCV image."""
    return cv.imread(path)


def path_to_pixbuf(path: str) -> GdkPixbuf.Pixbuf:
    """Convert image path to GTK pixbuf."""
    return GdkPixbuf.Pixbuf.new_from_file(path)

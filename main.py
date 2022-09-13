import cv2 as cv
import numpy as np
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf


def select_dialog() -> cv.Mat:
    """Select image from file."""
    dialog = Gtk.FileChooserDialog(
        "Choose an image of your signature",
        None,
        Gtk.FileChooserAction.OPEN,
        (
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        ),
    )
    # only show png files
    filter_image = Gtk.FileFilter()
    filter_image.set_name("Image files")
    filter_image.add_mime_type("image/png")
    filter_image.add_mime_type("image/jpeg")
    filter_image.add_mime_type("image/jpg")
    dialog.add_filter(filter_image)
    response = dialog.run()
    if response == Gtk.ResponseType.CANCEL:
        dialog.destroy()
        return
        # TODO: better cancel handling
    img = dialog.get_filename()
    ocv_img = cv.imread(img)
    dialog.destroy()
    return img, ocv_img


def save_signature(ocv_img) -> None:
    """Save signature to file."""
    if ocv_img is not None:
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
        dialog.set_filename("signature.png")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            cv.imwrite(dialog.get_filename(), ocv_img)
        dialog.destroy()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            cv.imwrite(dialog.get_filename(), ocv_img)
        dialog.destroy()


def open_image(og_window, ocv_window) -> cv.Mat:
    """Open image from file."""
    og_img, ocv_og_img = select_dialog()
    ocv_img = extract_signature(ocv_og_img)
    gtk_ocv_img = ocv_to_gtk(ocv_img)
    gtk_og_img = img_to_gtk(og_img)
    og_window.add(gtk_og_img)
    ocv_window.add(gtk_ocv_img)
    return ocv_img


def ocv_to_gtk(ocv_img):
    """Convert OpenCV image to GTK image."""
    height, width, channels = ocv_img.shape
    return Gtk.Image.new_from_pixbuf(
        GdkPixbuf.Pixbuf.new_from_data(
            ocv_img.tobytes(),
            GdkPixbuf.Colorspace.RGB,
            True,
            8,
            width,
            height,
            channels * width,
        )
    )


def img_to_gtk(img):
    """Convert image to GTK image."""
    return Gtk.Image.new_from_file(img)


def main():
    """Run main function."""

    window = Gtk.Window()
    window.set_title("Signature Extractor")
    window.set_default_size(800, 600)
    window.set_border_width(10)
    window.connect("destroy", Gtk.main_quit)

    og_window = Gtk.ScrolledWindow()
    og_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

    ocv_window = Gtk.ScrolledWindow()
    ocv_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

    ocv_img = open_image(og_window, ocv_window)

    headerbar = Gtk.HeaderBar()
    headerbar.set_show_close_button(True)

    open_button = Gtk.Button()
    open_button.set_label(" Open")
    open_button.set_image(
        Gtk.Image.new_from_icon_name("document-open", Gtk.IconSize.BUTTON)
    )
    open_button.set_always_show_image(True)
    # open_button.connect("clicked", lambda _: open_image(imagewindow))

    download_button = Gtk.Button()
    download_button.set_label(" Save")
    download_button.set_image(
        Gtk.Image.new_from_icon_name("document-save", Gtk.IconSize.BUTTON)
    )
    download_button.set_always_show_image(True)
    download_button.connect("clicked", lambda _: save_signature(ocv_img))

    headerbar.pack_end(download_button)
    headerbar.pack_end(open_button)
    headerbar.props.title = "Signature Extractor"
    window.set_titlebar(headerbar)

    stack = Gtk.Stack()
    stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
    stack.set_transition_duration(500)

    stack.add_titled(og_window, "og", "Original")
    stack.add_titled(ocv_window, "ocv", "Extracted")

    stack_switcher = Gtk.StackSwitcher()
    stack_switcher.set_stack(stack)
    stack_switcher.set_halign(Gtk.Align.CENTER)

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    box.pack_start(stack_switcher, True, True, 0)
    box.pack_start(stack, True, True, 0)

    window.add(box)

    window.show_all()
    Gtk.main()


def extract_signature(image):
    """Extract signature from image."""
    grayscale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # convert to grayscale
    _, binary = cv.threshold(grayscale, 127, 255, cv.THRESH_BINARY)  # convert to binary
    rgba = cv.cvtColor(binary, cv.COLOR_GRAY2RGBA)  # convert to RGBA
    rgba[np.where((rgba == [255, 255, 255, 255]).all(axis=2))] = [
        0,
        0,
        0,
        0,
    ]  # make background transparent
    cv.imwrite("signature.png", rgba)  # save signature
    return rgba


if __name__ == "__main__":
    main()

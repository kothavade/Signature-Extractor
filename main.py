import cv2 as cv
import gi
import numpy as np

gi.require_version("Gtk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf, Gtk


def select_dialog() -> str:
    """Select image from file."""
    # TODO: add cancel handling
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
        select_dialog()
    img: str = dialog.get_filename()
    dialog.destroy()
    return img


def save_signature(ocv_img) -> None:
    """Save transparent signature to file of user's choosing."""
    # Check if Transparent Image is Empty
    if ocv_img is not None:
        # Create Save Dialog
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
        # Default file name
        dialog.set_filename("signature.png")

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            cv.imwrite(dialog.get_filename(), ocv_img)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()


def open_image(
    og_window: Gtk.ScrolledWindow, ocv_window: Gtk.ScrolledWindow, method: str
) -> cv.Mat:
    """Open image from file."""
    # Get Original Image
    og_img = select_dialog()

    # Convert to Transparent OpenCV Image
    ocv_img = extract_signature(cv.imread(og_img), method)

    # Convert Original and Transparent Images to GTK Images
    gtk_ocv_img = ocv_to_gtk(ocv_img)
    gtk_og_img = img_path_to_gtk(og_img)

    # Add GTK Images to Respective Windows
    og_window.add(gtk_og_img)
    ocv_window.add(gtk_ocv_img)
    return ocv_img


def set_image(
    og_window: Gtk.ScrolledWindow, ocv_window: Gtk.ScrolledWindow, method: str
) -> None:
    """Set images to windows."""


def ocv_to_gtk(ocv_img) -> Gtk.Image:
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


def img_path_to_gtk(img_path: str) -> Gtk.Image:
    """Convert image path to GTK image."""
    return Gtk.Image.new_from_file(img_path)


def method_config() -> str:
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

    # Create Radio Buttons
    radio_binary = Gtk.RadioButton.new_with_label_from_widget(None, "Binary")
    radio_adaptive = Gtk.RadioButton.new_with_label_from_widget(
        radio_binary, "Adaptive"
    )

    # Add Radio Buttons to Dialog
    dialog.vbox.pack_start(radio_binary, True, True, 0)
    dialog.vbox.pack_start(radio_adaptive, True, True, 0)

    dialog.show_all()
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        if radio_binary.get_active():
            return "binary"
        elif radio_adaptive.get_active():
            return "adaptive"


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

    # config_button = Gtk.Button()
    # config_button.set_label("Config")
    # config_button.connect(
    #     "clicked", lambda x: open_image(og_window, ocv_window, method_config())
    # )

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
    download_button.connect("clicked", lambda _: save_signature(ocv_img))

    headerbar.pack_end(download_button)
    # headerbar.pack_end(open_button)
    # headerbar.pack_end(config_button)
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

    # set stack switcher to headerbar
    headerbar.pack_start(stack_switcher)

    window.add(stack)
    window.show_all()
    Gtk.main()


def extract_signature(image, method="binary"):
    """Extract signature from image."""
    grayscale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # convert to grayscale
    if method == "binary":
        _, converted = cv.threshold(grayscale, 127, 255, cv.THRESH_BINARY)
    elif method == "adaptive":
        converted = cv.adaptiveThreshold(
            grayscale, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2
        )
    rgba = cv.cvtColor(converted, cv.COLOR_GRAY2RGBA)  # convert to RGBA
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

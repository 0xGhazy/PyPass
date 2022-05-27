import qrcode

class QRHandler:

    def __init__(self):
        self.qr_handle = qrcode.QRCode(
                                version = 1,
                                error_correction = qrcode.constants.ERROR_CORRECT_L,
                                box_size = 10,
                                border = 4)
        self.qr_image = None
        self._qr_image_color = "cyan"
        self._qr_image_bg = "black"


    def set_image_colors(self, fill_color, background_color):
        self._qr_image_color = fill_color
        self._qr_image_bg = background_color


    def generate_qr(self, text: str, img_name: str) -> None:
        self.qr_handle.add_data(text)
        self.qr_handle.make(fit = True)
        self.qr_image = self.qr_handle.make_image(fill_color = self._qr_image_color,
                                                  back_color = self._qr_image_bg)
        self.qr_image.save(img_name)


if __name__ == "__main__":
    # source:
    # https://www.javatpoint.com/generate-a-qr-code-using-python
    my_obj = QRHandler()
    my_obj.set_image_colors("red", "black")
    my_obj.generate_qr("Hello world!", "photo.png")

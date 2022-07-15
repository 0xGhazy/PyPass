import qrcode
import json
from pathlib import Path

class QRHandler:

    def __init__(self):
        self.qr_handle = qrcode.QRCode(
                                version = 1,
                                error_correction = qrcode.constants.ERROR_CORRECT_L,
                                box_size = 10,
                                border = 4)
        self.qr_image = None
        # img_color, bg_color = 
        result = self.load_current_css()["editQRColor"]
        img_color, bg_color = result.split(",")
        self.set_image_colors(img_color, bg_color)


    def set_image_colors(self, fill_color, background_color):
        self._qr_image_color = fill_color
        self._qr_image_bg = background_color


    def generate_qr(self, text: str, img_name: str) -> None:
        self.qr_handle.add_data(text)
        self.qr_handle.make(fit = True)
        self.qr_image = self.qr_handle.make_image(fill_color = self._qr_image_color,
                                                  back_color = self._qr_image_bg)
        self.qr_image.save(img_name)


    def load_current_css(self) -> dict:
        json_path = Path(__file__).parent.parent / 'ui' / "themes" / "mycss.json"
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data

if __name__ == "__main__":
    # source:
    # https://www.javatpoint.com/generate-a-qr-code-using-python
    my_obj = QRHandler()
    my_obj.generate_qr("Hello world!", "photo.png")

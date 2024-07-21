from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image
from rembg import remove
import io

app = Flask(__name__)
CORS(app)

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return "No image file found", 400

    image_file = request.files['image']
    img = Image.open(image_file.stream)
    img_without_bg = remove(img)
    white_bg = Image.new("RGBA", img_without_bg.size, (255, 255, 255, 255))
    white_bg.paste(img_without_bg, (0, 0), img_without_bg)
    white_bg_rgb = white_bg.convert('RGB')

    img_io = io.BytesIO()
    white_bg_rgb.save(img_io, 'JPG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpg')

if __name__ == '__main__':
    app.run(debug=True)

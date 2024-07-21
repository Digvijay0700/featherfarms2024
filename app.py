import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from rembg import remove
import io

app = Flask(__name__)
CORS(app)

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file found"}), 400

        image_file = request.files['image']
        img = Image.open(image_file.stream)
        img_without_bg = remove(img)
        white_bg = Image.new("RGBA", img_without_bg.size, (255, 255, 255, 255))
        white_bg.paste(img_without_bg, (0, 0), img_without_bg)
        white_bg_rgb = white_bg.convert('RGB')

        img_io = io.BytesIO()
        white_bg_rgb.save(img_io, 'JPEG')
        img_io.seek(0)

        base64_image = base64.b64encode(img_io.getvalue()).decode('utf-8')

        return jsonify({"base64_image": base64_image})

    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

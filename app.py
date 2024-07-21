import os
import flask
import io

try:
    from flask_cors import CORS
except ImportError as e:
    raise ImportError("flask_cors library is not installed. Please install it using 'pip install flask-cors'.") from e

try:
    from PIL import Image
except ImportError as e:
    raise ImportError("Pillow library is not installed. Please install it using 'pip install pillow'.") from e

try:
    from rembg import remove
except ImportError as e:
    raise ImportError("rembg library is not installed. Please install it using 'pip install rembg'.") from e

app = flask.Flask(__name__)
CORS(app)

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        if 'image' not in flask.request.files:
            return flask.jsonify({"error": "No image file found"}), 400

        image_file = flask.request.files['image']
        img = Image.open(image_file.stream)
        img_without_bg = remove(img)
        white_bg = Image.new("RGBA", img_without_bg.size, (255, 255, 255, 255))
        white_bg.paste(img_without_bg, (0, 0), img_without_bg)
        white_bg_rgb = white_bg.convert('RGB')

        img_io = io.BytesIO()
        white_bg_rgb.save(img_io, 'JPEG')
        img_io.seek(0)

        return flask.send_file(img_io, mimetype='image/jpeg')

    except Exception as e:
        print(f"Error processing image: {e}")
        return flask.jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

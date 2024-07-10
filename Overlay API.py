from flask import Flask, request, send_file
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/overlay', methods=['POST'])
def overlay_image():
    # Get the URL from the request
    url = request.form.get('url')
    
    if not url:
        return "URL is required", 400

    # Fetch the overlay image from the URL
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to fetch image", 400
    
    overlay_image = Image.open(BytesIO(response.content)).convert("RGBA")

    # Open the background image
    background_image = Image.open("background.png").convert("RGBA")

    # Calculate the position to paste the overlay (top-left corner)
    position = (0, 0)

    # Create a new image for the result with the same size as the background
    result_image = Image.new("RGBA", background_image.size)

    # Paste the background and the overlay
    result_image.paste(background_image, (0, 0))
    result_image.paste(overlay_image, position, overlay_image)

    # Convert result to RGB (if you want to save/send it as JPG)
    result_image = result_image.convert("RGB")

    # Save the result to a BytesIO object
    img_io = BytesIO()
    result_image.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

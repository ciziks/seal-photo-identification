from flask import Flask, render_template, request, redirect, url_for
import requests
import Wildbook

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('landing_page.html')

@app.route('/upload_image', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(request.url)
    image = request.files['image']
    if image.filename == '':
        return redirect(request.url)
    
    image_id_or_message = Wildbook.upload_image(image)
    # Handle the response appropriately
    return image_id_or_message

if __name__ == "__main__":
    app.run(debug=True)

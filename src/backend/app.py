from flask import Flask, render_template, request, redirect, url_for
from antidote import world, inject
from wrappers.Wildbook import Wildbook
import os

app = Flask(__name__,
            template_folder=os.path.join(os.pardir, 'frontend', 'templates'),
            static_folder=os.path.join(os.pardir, 'frontend', 'static'))


@app.route("/")
def home():
    return render_template("landing_page.html")

#Handle Get request to open new Html page
@app.route("/upload_form")
def upload_form():
    return render_template("AddSighting.html")

#Handle the Image Upload
@inject
@app.route("/upload_image", methods=["POST"])
def upload(wildbook: Wildbook = world[Wildbook]):
    if "image" not in request.files or "image_name" not in request.form:  # Check for image and image_name
        return redirect(request.url)
    
    image = request.files["image"]
    image_name = request.form["image_name"]  # Capture the name from the text input
    
    if image.filename == "":
        return redirect(request.url)

    # Save the file temporarily
    temp_image_path = "path_to_temp_storage" 
    image.save(temp_image_path)

    image_id = wildbook.upload_image(temp_image_path)
    
    aid_list = wildbook.detect_seal([int(image_id)])

    wildbook.rename_annotations(aid_list, [image_name])  # Rename the uploaded image with the provided name
    
    score = wildbook.seal_matching(aid_list[0])

    # Handle the response
    return str(score)

if __name__ == "__main__":
    app.run(debug=True)

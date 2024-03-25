from flask import Flask, render_template, request, redirect, url_for
from antidote import world, inject
from wrappers.Wildbook import Wildbook

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("landing_page.html")


@inject
@app.route("/upload_image", methods=["POST"])
def upload(wildbook: Wildbook = world[Wildbook]):
    if "image" not in request.files:
        return redirect(request.url)
    image = request.files["image"]
    if image.filename == "":
        return redirect(request.url)

    # Save the file temporarily
    temp_image_path = (
        "path_to_temp_storage"  # Specify the path to save the temporary file
    )
    image.save(temp_image_path)

    # Call the upload_image method on the instance of Wildbook
    image_id = wildbook.upload_image(temp_image_path)

    # Handle the response
    return str(image_id)


if __name__ == "__main__":
    app.run(debug=True)

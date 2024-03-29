from flask import Flask, render_template, request, redirect, send_file, url_for
from antidote import world, inject
from wrappers.Wildbook import Wildbook
from flask_swagger_ui import get_swaggerui_blueprint
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.pardir, "frontend", "templates"),
    static_folder=os.path.join(os.pardir, "frontend", "static"),
)

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Seal Center API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route("/")
def home():
    return render_template("menu.html")


# Handle Get request to open new Html page
@app.route("/seal_form")
def seal_form():
    return render_template("seal_form.html")


# Handle the request to store a image and compare with database
@inject
@app.route("/seal", methods=["POST"])
def new_seal(wildbook: Wildbook = world[Wildbook]):
    if (
        "image" not in request.files or "image_name" not in request.form
    ):  # Check for image and image_name
        return redirect(request.url)

    image = request.files["image"]
    image_name = request.form["image_name"]  # Capture the name from the text input

    if image.filename == "":
        return redirect(request.url)

    # Save the file temporarily
    temp_image_path = "path_to_temp_storage"
    image.save(temp_image_path)

    # Upload image
    image_id = wildbook.upload_image(temp_image_path)

    # Detect the seal in the image
    aid_list = wildbook.detect_seal([int(image_id)])

    # Set the name of the seal
    wildbook.rename_annotations(
        aid_list, [image_name]
    )  # Rename the uploaded image with the provided name

    # Match seal with seals in DB
    score = wildbook.seal_matching(aid_list[0])

    # Find aid and score for best match
    try:
        match_aid, match_score = next(iter(score.items()))
    except StopIteration:

        # Handle the case where there are no items
        match_aid, match_score = None, None

    # Get the uploaded image
    initial_image = wildbook.get_annotation_image(aid_list[0])

    # If there is a match, get the 'best match' image
    if match_aid:
        matched_image = wildbook.get_annotation_image(match_aid)
        matched_image_base64 = matched_image.split(",", 1)[1]  # Remove the prefix
    else:
        # If there is no match, set a placeholder
        matched_image_base64 = None

    # Encode the initial as base64 for embedding in HTML
    initial_image_base64 = initial_image.split(",", 1)[1]  # Remove the prefix

    return render_template(
        "confirmation.html",
        initial_image=initial_image_base64,
        matched_image=matched_image_base64,
        match_aid=match_aid,
        match_score=match_score,
        initial_aid=aid_list[0]
    )

# Handle the request to list seals stored inside the database
@inject
@app.route("/list_seals")
def list_seals(wildbook: Wildbook = world[Wildbook]):

    #Get the list of aids
    seal_aids = wildbook.list_annotations_id()
    seals_data = []

    # Get name and image for each Aid
    for aid in seal_aids:
        try:
            seal_name = wildbook.get_annotation_name(aid)
            image_url = wildbook.get_annotation_image(aid)

            seal = {'name': seal_name, 'image_url': image_url}
            seals_data.append(seal)
        except Exception as e:
            print(f"An error occurred: {e}") 

    # Return template with the data
    return render_template("list_seals.html", seals=seals_data)


if __name__ == "__main__":
    app.run(debug=True)

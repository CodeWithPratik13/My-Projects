from flask import Flask, render_template, request, redirect, url_for
import uuid
from werkzeug.utils import secure_filename
import os



UPLOAD_FOLDER = 'user_upload'
REELS_FOLDER = 'static/reels'  # Folder where reels are stored
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Create reel
@app.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid1()
    if request.method == "POST":
        rec_id = request.form.get("uuid")
        desc = request.form.get("text")
        input_files = []

        # Save uploaded images
        for key, file in request.files.items():
            if file:
                filename = secure_filename(file.filename)
                folder_path = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
                os.makedirs(folder_path, exist_ok=True)
                file.save(os.path.join(folder_path, filename))
                input_files.append(filename)

        # Save description (UTF-8 for Hindi & others)
        with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "desc.txt"), "w", encoding="utf-8") as f:
            f.write(desc)

        # Build FFmpeg input.txt
        with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "input.txt"), "w", encoding="utf-8") as f:
            for fl in input_files:
                f.write(f"file '{fl}'\n")
                f.write("duration 3\n")  # Show each image for 3 seconds

    return render_template("create.html", myid=myid)

# Gallery page
@app.route("/gallery")
def gallery():
    if not os.path.exists(REELS_FOLDER):
        os.makedirs(REELS_FOLDER)
    reels = os.listdir(REELS_FOLDER)
    return render_template("gallery.html", reels=reels)

# Delete a reel
@app.route("/delete/<reel_name>", methods=["POST"])
def delete_reel(reel_name):
    reel_path = os.path.join(REELS_FOLDER, reel_name)
    if os.path.exists(reel_path):
        try:
            os.remove(reel_path)
        except Exception as e:
            print(f"Error deleting {reel_name}: {e}")
    return redirect(url_for("gallery"))

if __name__ == "__main__":
    app.run(debug=True)


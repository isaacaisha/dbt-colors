from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'ico', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


@app.route('/', methods=['GET', 'POST'])
def home():
    uploaded_image = None
    top_10_colors = None
    error_message = None

    if request.method == 'POST':
        if 'file' not in request.files:
            error_message = 'No file part'
        else:
            file = request.files['file']

            if file.filename == '':
                error_message = 'Please First Select An Image ¡!¡'
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = image.resize((200, 200))
                img_array = np.array(image)
                pixels = img_array.reshape(-1, img_array.shape[-1])

                num_clusters = 10
                kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(pixels)
                centroids = kmeans.cluster_centers_.astype(int)
                top_10_colors = [rgb_to_hex(tuple(centroid)) for centroid in centroids]

                uploaded_image = filename
            else:
                error_message = 'Unsupported file format. Please upload a valid image (e.g., PNG, JPG).'

    return render_template('index.html', date=datetime.now().strftime("%a %d %B %Y"),
                           uploaded_image=uploaded_image, top_10_colors=top_10_colors, error_message=error_message)



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

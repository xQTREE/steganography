from flask import Flask, request , render_template
import os
import imghide

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        image = request.files['image']
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.png'))
        return 'Image uploaded successfully'
    else:
        return 'No image found in the request'

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, url_for
from pathlib import Path
from werkzeug.utils import secure_filename
from skimage.metrics import structural_similarity as ssim
import cv2

app = Flask(__name__)

# Use absolute path to avoid "static \ uploads" bug
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)

def compare_faces(img1_path, img2_path):
    img1 = cv2.imread(str(img1_path))
    img2 = cv2.imread(str(img2_path))

    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.resize(img2_gray, (img1_gray.shape[1], img1_gray.shape[0]))

    score, _ = ssim(img1_gray, img2_gray, full=True)
    result = "✅ Identity Verified: Faces are similar." if score > 0.7 else "❌ Identity Verification Failed: Faces are different."
    return result, score

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    score = None
    img1_url = None
    img2_url = None

    if request.method == 'POST':
        img1 = request.files['img1']
        img2 = request.files['img2']

        img1_filename = secure_filename(img1.filename)
        img2_filename = secure_filename(img2.filename)

        img1_path = UPLOAD_FOLDER / img1_filename
        img2_path = UPLOAD_FOLDER / img2_filename

        img1.save(str(img1_path))
        img2.save(str(img2_path))

        result, score = compare_faces(img1_path, img2_path)

        img1_url = url_for('static', filename=f'uploads/{img1_filename}')
        img2_url = url_for('static', filename=f'uploads/{img2_filename}')

    return render_template('index.html', result=result, score=score, img1_url=img1_url, img2_url=img2_url)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import cv2
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ORIGINAL_IMAGE'] = os.path.join(app.config['UPLOAD_FOLDER'], 'original.png')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Página principal
@app.route('/')
def index():
    return render_template('index.html', image_path=None)

# Upload da imagem
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if file:
        filepath = app.config['ORIGINAL_IMAGE']
        file.save(filepath)
        return render_template('index.html', image_path=filepath)
    return redirect(url_for('index'))

# Filtro Blur
@app.route('/blur', methods=['POST'])
def blur():
    image_path = request.form['image_path']
    img = cv2.imread(image_path)
    blurred = cv2.GaussianBlur(img, (15, 15), 0)
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'blurred.png')
    cv2.imwrite(output_path, blurred)
    return render_template('index.html', image_path=output_path)

# Filtro Sharpen
@app.route('/sharpen', methods=['POST'])
def sharpen():
    image_path = request.form['image_path']
    img = cv2.imread(image_path)
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    sharpened = cv2.filter2D(img, -1, kernel)
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'sharpened.png')
    cv2.imwrite(output_path, sharpened)
    return render_template('index.html', image_path=output_path)

# Rotação de 45 graus
@app.route('/rotate', methods=['POST'])
def rotate():
    image_path = request.form['image_path']
    img = cv2.imread(image_path)
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, 45, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'rotated.png')
    cv2.imwrite(output_path, rotated)
    return render_template('index.html', image_path=output_path)

# Limpar estilização - retorna imagem original
@app.route('/reset', methods=['POST'])
def reset():
    original_path = app.config['ORIGINAL_IMAGE']
    if os.path.exists(original_path):
        return render_template('index.html', image_path=original_path)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
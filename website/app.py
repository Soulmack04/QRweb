from flask import Flask, render_template, request, make_response
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form['url']
    fill_color = request.form['fill']
    back_color = request.form['back']

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    # Save the image temporarily
    img_bytes_io = BytesIO()
    img.save(img_bytes_io, format='PNG')
    img_bytes = img_bytes_io.getvalue()

    # Create a response and set the content type
    response = make_response(img_bytes)
    response.headers['Content-Type'] = 'image/png'

    return response

if __name__ == '__main__':
    app.run(debug=True)

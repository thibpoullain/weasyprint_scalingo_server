from flask import Flask, request, jsonify, make_response, render_template
import weasyprint
import base64
import os
import tempfile
import logging
from datetime import datetime
import hashlib

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', '*').split(',')

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    """Page d'accueil avec documentation"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Endpoint de santé"""
    try:
        # Test WeasyPrint
        weasyprint.HTML(string='<html><body>test</body></html>').write_pdf()
        return jsonify({
            'status': 'ok',
            'weasyprint_version': weasyprint.__version__,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/generate', methods=['POST'])
def generate_pdf():
    """Génère un PDF à partir de HTML"""
    try:
        data = request.get_json()

        if not data or 'html' not in data:
            return jsonify({'error': 'HTML content is required'}), 400

        html_content = data['html']
        options = data.get('options', {})

        # Options de génération
        base_url = options.get('base_url')

        # Générer le PDF
        logger.info(f"Generating PDF, HTML size: {len(html_content)} chars")

        pdf = weasyprint.HTML(
            string=html_content,
            base_url=base_url
        ).write_pdf()

        # Créer la réponse
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=document.pdf'

        # Headers CORS si nécessaire
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS or '*' in ALLOWED_ORIGINS:
            response.headers['Access-Control-Allow-Origin'] = origin or '*'

        logger.info(f"PDF generated successfully, size: {len(pdf)} bytes")
        return response

    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate-base64', methods=['POST'])
def generate_pdf_base64():
    """Génère un PDF et retourne en base64"""
    try:
        data = request.get_json()

        if not data or 'html' not in data:
            return jsonify({'error': 'HTML content is required'}), 400

        html_content = data['html']
        options = data.get('options', {})

        # Générer le PDF
        pdf = weasyprint.HTML(
            string=html_content,
            base_url=options.get('base_url')
        ).write_pdf()

        # Encoder en base64
        pdf_base64 = base64.b64encode(pdf).decode('utf-8')

        return jsonify({
            'pdf': pdf_base64,
            'size': len(pdf),
            'hash': hashlib.md5(pdf).hexdigest()
        })

    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/example')
def example_pdf():
    """Génère un PDF d'exemple"""
    html = render_template('example.html',
                         title="Document d'exemple",
                         date=datetime.now().strftime("%d/%m/%Y"))

    pdf = weasyprint.HTML(string=html).write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=example.pdf'

    return response

@app.route('/metrics')
def metrics():
    """Métriques simples"""
    return jsonify({
        'uptime': 'running',
        'version': '1.0.0',
        'weasyprint_version': weasyprint.__version__
    })

# CORS pour les requêtes OPTIONS
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin in ALLOWED_ORIGINS or '*' in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin or '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

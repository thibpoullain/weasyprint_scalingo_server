# WeasyPrint Server for Scalingo

[![Scalingo](https://img.shields.io/badge/Scalingo-Compatible-blue.svg)](https://scalingo.com)
[![WeasyPrint](https://img.shields.io/badge/WeasyPrint-65.1-green.svg)](https://weasyprint.org/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Production-ready **PDF generation server** powered by WeasyPrint on Scalingo. Convert HTML/CSS to high-quality PDF documents through a simple REST API.

## 🚀 Quick Start

### Deploy to Scalingo in minutes

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/weasyprint-server
   cd weasyprint-server
   ```

2. **Create a Scalingo app**:
   ```bash
   scalingo create my-pdf-server
   ```

3. **Deploy**:
   ```bash
   git push scalingo main
   ```

Your PDF server will be available at `https://my-pdf-server.osc-fr1.scalingo.io`

## 🔧 Configuration

### Environment Variables

Set these variables in your Scalingo dashboard or via CLI:

```bash
# CORS configuration (comma-separated origins)
scalingo -a my-pdf-server env-set ALLOWED_ORIGINS="https://myapp.com,https://app.myapp.com"

# Or allow all origins (not recommended for production)
scalingo -a my-pdf-server env-set ALLOWED_ORIGINS="*"
```

### Buildpack Configuration

This project uses the WeasyPrint buildpack. The `.buildpacks` file is already configured:

```
https://github.com/thibpoullain/weasyprint_buildpack
https://github.com/Scalingo/python-buildpack
```

## 📦 Features

- **REST API** for PDF generation
- **Base64 encoding** support
- **Custom page formats** and orientations
- **CSS3 support** including flexbox and grid
- **Async processing** with timeouts
- **Health monitoring** endpoint
- **CORS support** for web applications
- **Automatic font handling**

## 💻 API Documentation

### Generate PDF

**POST** `/generate`

Generate a PDF from HTML content.

```bash
curl -X POST https://your-app.scalingo.io/generate \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<html><body><h1>Hello World</h1></body></html>",
    "options": {
      "format": "A4",
      "landscape": false,
      "base_url": "https://example.com"
    }
  }' \
  --output document.pdf
```

**Request Body**:
```json
{
  "html": "<html>...</html>",
  "options": {
    "format": "A4",
    "landscape": false,
    "base_url": "https://example.com"
  }
}
```

**Response**: Binary PDF file

### Generate PDF as Base64

**POST** `/generate-base64`

Generate a PDF and return it as a base64-encoded string.

```javascript
// JavaScript example
const response = await fetch('https://your-app.scalingo.io/generate-base64', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    html: '<html><body><h1>Hello World</h1></body></html>'
  })
});

const data = await response.json();
// data.pdf contains the base64-encoded PDF
```

**Response**:
```json
{
  "pdf": "JVBERi0xLjQKJcfs...",
  "size": 12345,
  "hash": "d41d8cd98f00b204e9800998ecf8427e"
}
```

### Health Check

**GET** `/health`

Check server status and WeasyPrint availability.

```bash
curl https://your-app.scalingo.io/health
```

**Response**:
```json
{
  "status": "ok",
  "weasyprint_version": "65.1",
  "timestamp": "2025-01-19T12:00:00.000Z"
}
```

### Example PDF

**GET** `/example`

Generate a sample PDF to test the installation.

```bash
curl https://your-app.scalingo.io/example --output example.pdf
```

## 🎨 Advanced Usage

### Custom Fonts

Add custom fonts to your PDFs:

```html
<style>
  @font-face {
    font-family: 'CustomFont';
    src: url('https://example.com/fonts/custom.ttf');
  }

  body {
    font-family: 'CustomFont', Arial, sans-serif;
  }
</style>
```

### Page Setup

Configure page size, margins, and headers/footers:

```html
<style>
  @page {
    size: A4 landscape;
    margin: 2cm;

    @top-center {
      content: "Company Report";
    }

    @bottom-right {
      content: "Page " counter(page) " of " counter(pages);
    }
  }
</style>
```

### High-Quality Images

For best results with images:

```html
<img src="https://example.com/image.png"
     style="width: 300px; height: auto; image-rendering: -webkit-optimize-contrast;">
```

## 🧪 Local Development

### Using Docker

```bash
# Build the image
docker build -t weasyprint-server .

# Run **locally**
docker run -p 5000:5000 -e ALLOWED_ORIGINS="*" weasyprint-server

# Test
curl http://localhost:5000/health
```

### Without Docker

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py

# Server will be available at http://localhost:5000
```

## 🔍 Troubleshooting

### Large PDFs timeout

Increase the timeout in `Procfile`:
```
web: gunicorn app:app --timeout 300 --workers 2
```

### Memory issues with complex documents

Scale your dynos:
```bash
scalingo -a my-pdf-server scale web:M
```

### Custom fonts not loading

Ensure fonts are accessible via HTTPS and CORS is properly configured on the font server.

### Images not appearing

- Use absolute URLs for images
- Ensure the image server allows hotlinking
- Set the `base_url` option when generating PDFs

## 🚀 Performance Tips

1. **Cache static assets**: Use a CDN for images and fonts
2. **Optimize HTML**: Minimize the HTML before sending
3. **Use efficient CSS**: Avoid complex selectors and deep nesting
4. **Batch processing**: For multiple PDFs, consider implementing a queue system

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Changelog

### v1.0.0 (2025-01-19)
- Initial release
- REST API for PDF generation
- Base64 encoding support
- Health monitoring
- Example PDF generation
- CORS support

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/weasyprint-server/issues)
- **WeasyPrint Documentation**: [weasyprint.org](https://weasyprint.org/)
- **Scalingo Documentation**: [doc.scalingo.com](https://doc.scalingo.com/)

---

Made with ❤️

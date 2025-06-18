FROM python:3.11-slim

# Install system dependencies required for WeasyPrint and Pillow
RUN apt-get update && apt-get install -y \
  # Build essentials
  build-essential \
  pkg-config \
  # Cairo dependencies
  libcairo2 \
  libcairo2-dev \
  # Pango dependencies
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libpangoft2-1.0-0 \
  # GDK-Pixbuf dependencies
  libgdk-pixbuf2.0-0 \
  libgdk-pixbuf2.0-dev \
  # FFI dependencies
  libffi-dev \
  # Shared mime info
  shared-mime-info \
  # Pillow dependencies
  zlib1g-dev \
  libjpeg-dev \
  libpng-dev \
  libfreetype6-dev \
  libtiff5-dev \
  libopenjp2-7-dev \
  libwebp-dev \
  # Clean up
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--timeout", "120", "--workers", "2"]

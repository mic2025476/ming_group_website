# Complete PDF Optimization Guide for Ming Menu
**Source:** 77.5 MB menu PDF → **Target:** <5 MB, instant loading

---

## 1. Install Required Tools (macOS Homebrew)

```bash
# Core PDF optimization tools
brew install ghostscript qpdf mupdf-tools poppler

# Image processing
brew install imagemagick

# Optional: verify installations
gs --version        # Ghostscript
qpdf --version
mutool -v
pdfinfo --version
```

---

## 2. Create Build Directory

```bash
mkdir -p ./build/m1-pages
cd /Users/anirudhchawla/Downloads/ming_group_website
```

---

## 3. Two-Tier Optimization Pipeline

### TIER 1: Lossless/Structure-Only (5-15 MB expected)

**Preserves everything, just cleans + linearizes:**

```bash
# Step 1: Clean metadata & optimize structure (lossless)
qpdf --linearize \
     --compress-streams=y \
     --recompress-flate \
     --compression-level=9 \
     --object-streams=generate \
     "/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf" \
     ./build/m1-menu.lossless.pdf

# Step 2: Verify linearization
qpdf --check-linearization ./build/m1-menu.lossless.pdf
# Should output: "PDF file is linearized"

# Step 3: Check output size
ls -lh ./build/m1-menu.lossless.pdf
```

**What this does:**
- Linearizes for fast first-page render (streaming)
- Compresses object streams (metadata/structure only)
- Removes unused objects
- **Does NOT touch images or fonts**
- Text remains selectable, fonts embedded, vectors intact

---

### TIER 2: Visually Identical, Smaller (3-5 MB target)

**Downsamples images intelligently while keeping vectors/text perfect:**

```bash
# Step 1: Ghostscript optimization with careful image downsampling
gs -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.7 \
   -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH \
   -dDetectDuplicateImages=true \
   -dCompressFonts=true \
   -dSubsetFonts=true \
   -dEmbedAllFonts=true \
   -dAutoRotatePages=/None \
   -dColorImageDownsampleType=/Bicubic \
   -dColorImageResolution=150 \
   -dGrayImageDownsampleType=/Bicubic \
   -dGrayImageResolution=150 \
   -dMonoImageDownsampleType=/Bicubic \
   -dMonoImageResolution=300 \
   -dColorImageFilter=/DCTEncode \
   -dGrayImageFilter=/DCTEncode \
   -dJPEGQ=85 \
   -sOutputFile=./build/m1-menu.optimized.pdf \
   "/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf"

# Step 2: Linearize for web streaming
qpdf --linearize \
     --compress-streams=y \
     --object-streams=generate \
     ./build/m1-menu.optimized.pdf \
     ./build/m1-menu.linearized.pdf

# Step 3: Verify linearization
qpdf --check-linearization ./build/m1-menu.linearized.pdf

# Step 4: Check final size
ls -lh ./build/m1-menu.linearized.pdf
```

**Quality tiers (adjust flags in Step 1):**

| Tier | `-dPDFSETTINGS` | ColorImageRes | JPEGQ | Expected Size |
|------|-----------------|---------------|-------|---------------|
| **Max Quality** | `/printer` | 300 | 92 | 8-12 MB |
| **Balanced** (recommended) | `/ebook` | 150 | 85 | 3-5 MB |
| **Smallest** | `/screen` | 96 | 75 | 1-2 MB |

**For Max Quality, use:**
```bash
gs -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.7 \
   -dPDFSETTINGS=/printer \
   -dNOPAUSE -dQUIET -dBATCH \
   -dDetectDuplicateImages=true \
   -dCompressFonts=true \
   -dSubsetFonts=true \
   -dEmbedAllFonts=true \
   -dAutoRotatePages=/None \
   -dColorImageDownsampleType=/Bicubic \
   -dColorImageResolution=300 \
   -dGrayImageDownsampleType=/Bicubic \
   -dGrayImageResolution=300 \
   -dMonoImageDownsampleType=/Bicubic \
   -dMonoImageResolution=600 \
   -dColorImageFilter=/DCTEncode \
   -dJPEGQ=92 \
   -sOutputFile=./build/m1-menu.optimized.pdf \
   "/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf"
```

**For Smallest, use:**
```bash
gs -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.7 \
   -dPDFSETTINGS=/screen \
   -dNOPAUSE -dQUIET -dBATCH \
   -dDetectDuplicateImages=true \
   -dCompressFonts=true \
   -dSubsetFonts=true \
   -dEmbedAllFonts=true \
   -dAutoRotatePages=/None \
   -dColorImageDownsampleType=/Bicubic \
   -dColorImageResolution=96 \
   -dGrayImageDownsampleType=/Bicubic \
   -dGrayImageResolution=96 \
   -dMonoImageDownsampleType=/Bicubic \
   -dMonoImageResolution=300 \
   -dColorImageFilter=/DCTEncode \
   -dJPEGQ=75 \
   -sOutputFile=./build/m1-menu.optimized.pdf \
   "/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf"
```

---

## 4. Generate Per-Page WebP Images for Instant Preview

**Extract first page as high-quality preview (for LCP):**

```bash
# Extract first page as PDF
mutool poster -x 1 \
      "/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf" \
      ./build/m1-pages/page-001.pdf

# Convert to WebP at 2x resolution (1440px width for retina)
mutool draw -o ./build/m1-pages/page-001-2x.png -w 1440 -r 144 ./build/m1-pages/page-001.pdf 1
magick ./build/m1-pages/page-001-2x.png -quality 85 ./build/m1-pages/page-001-2x.webp

# Convert to WebP at 1x resolution (720px width for standard)
mutool draw -o ./build/m1-pages/page-001-1x.png -w 720 -r 72 ./build/m1-pages/page-001.pdf 1
magick ./build/m1-pages/page-001-1x.png -quality 85 ./build/m1-pages/page-001-1x.webp

# Cleanup temp PNGs
rm ./build/m1-pages/page-001*.png ./build/m1-pages/page-001.pdf
```

**Extract ALL pages (for full image viewer):**

```bash
# Get page count
PAGE_COUNT=$(pdfinfo "/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf" | grep "^Pages:" | awk '{print $2}')

# Loop through all pages
for i in $(seq 1 $PAGE_COUNT); do
  PAGE_NUM=$(printf "%03d" $i)

  # 2x (retina)
  mutool draw -o "./build/m1-pages/page-${PAGE_NUM}-2x.png" \
         -w 1440 -r 144 \
         "/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf" \
         $i
  magick "./build/m1-pages/page-${PAGE_NUM}-2x.png" \
         -quality 85 \
         "./build/m1-pages/page-${PAGE_NUM}-2x.webp"

  # 1x (standard)
  mutool draw -o "./build/m1-pages/page-${PAGE_NUM}-1x.png" \
         -w 720 -r 72 \
         "/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf" \
         $i
  magick "./build/m1-pages/page-${PAGE_NUM}-1x.png" \
         -quality 85 \
         "./build/m1-pages/page-${PAGE_NUM}-1x.webp"

  # Cleanup
  rm "./build/m1-pages/page-${PAGE_NUM}-2x.png" "./build/m1-pages/page-${PAGE_NUM}-1x.png"
done

# Check output
ls -lh ./build/m1-pages/
```

---

## 5. Django Integration

### Option A: Static Files (Recommended for CDN)

**Directory structure:**
```
myproject/
├── static/
│   └── m1/
│       ├── m1-menu.pdf          # Linearized PDF
│       └── pages/
│           ├── page-001-1x.webp
│           ├── page-001-2x.webp
│           └── ...
```

**Copy files:**
```bash
mkdir -p static/m1/pages
cp ./build/m1-menu.linearized.pdf static/m1/m1-menu.pdf
cp ./build/m1-pages/*.webp static/m1/pages/
```

**settings.py:**
```python
# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# For serving in development
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# WhiteNoise for efficient static file serving
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add after SecurityMiddleware
    # ... other middleware
]

# WhiteNoise settings for compression + long-lived caching
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Optional: Custom file types
WHITENOISE_MIMETYPES = {
    '.pdf': 'application/pdf',
    '.webp': 'image/webp',
}

# Don't compress PDFs (already compressed)
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['pdf', 'gz', 'br', 'webp']
```

**Collect static files:**
```bash
python manage.py collectstatic --noinput
```

**Access URL:**
- Development: `http://localhost:8000/static/m1/m1-menu.pdf`
- Production: `https://yourdomain.com/static/m1/m1-menu.pdf`

**For custom `/m1/` path (via URL routing):**

Add to `urls.py`:
```python
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # ... your other URLs
    path('m1/m1-menu.pdf', RedirectView.as_view(url=settings.STATIC_URL + 'm1/m1-menu.pdf', permanent=True)),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

### Option B: Media Files with S3/CloudFront

**Directory structure:**
```
myproject/
├── media/
│   └── m1/
│       ├── m1-menu.pdf
│       └── pages/
```

**settings.py:**
```python
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# django-storages with S3
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
AWS_S3_REGION_NAME = 'us-east-1'  # Your region
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Public read access for media files
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False

# Cache control for media files
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'public, max-age=31536000, immutable',
}

# Optional: CloudFront CDN
AWS_S3_CUSTOM_DOMAIN = 'your-cloudfront-id.cloudfront.net'
```

**Upload to S3:**
```bash
pip install django-storages boto3

# Copy to media directory
mkdir -p media/m1/pages
cp ./build/m1-menu.linearized.pdf media/m1/m1-menu.pdf
cp ./build/m1-pages/*.webp media/m1/pages/

# Upload via Django shell
python manage.py shell
```

```python
from django.core.files.storage import default_storage
from pathlib import Path

# Upload PDF
with open('media/m1/m1-menu.pdf', 'rb') as f:
    default_storage.save('m1/m1-menu.pdf', f)

# Upload images
pages_dir = Path('media/m1/pages')
for webp_file in pages_dir.glob('*.webp'):
    with open(webp_file, 'rb') as f:
        default_storage.save(f'm1/pages/{webp_file.name}', f)
```

**Or use AWS CLI:**
```bash
brew install awscli
aws configure

# Sync with cache headers
aws s3 sync ./build/m1-pages/ s3://your-bucket/m1/pages/ \
    --cache-control "public, max-age=31536000, immutable" \
    --content-type "image/webp"

aws s3 cp ./build/m1-menu.linearized.pdf s3://your-bucket/m1/m1-menu.pdf \
    --cache-control "public, max-age=31536000, immutable" \
    --content-type "application/pdf"
```

---

## 6. Versioned URLs for Immutable Caching

**Recommended pattern:**
```
/m1/m1-menu.v20250428.pdf  → Cache forever
/m1/m1-menu.pdf            → Short cache, redirects to versioned
```

**Implementation:**

1. **Rename file with version:**
```bash
VERSION=$(date +%Y%m%d)
cp ./build/m1-menu.linearized.pdf static/m1/m1-menu.v${VERSION}.pdf
```

2. **Symlink or redirect:**
```bash
# Symlink (for static files)
ln -sf m1-menu.v${VERSION}.pdf static/m1/m1-menu.pdf

# Or use Django view redirect
```

**Django view (urls.py):**
```python
from django.http import HttpResponsePermanentRedirect
from django.conf import settings

def menu_pdf_latest(request):
    # Update this version when you upload new PDF
    CURRENT_VERSION = "20250428"
    versioned_url = f"{settings.STATIC_URL}m1/m1-menu.v{CURRENT_VERSION}.pdf"
    return HttpResponsePermanentRedirect(versioned_url)

urlpatterns = [
    path('m1/m1-menu.pdf', menu_pdf_latest),
]
```

---

## 7. Nginx Configuration for Fast Delivery

**nginx.conf or site config:**

```nginx
# PDF and WebP MIME types
types {
    application/pdf pdf;
    image/webp webp;
}

# Serve static files
location /static/ {
    alias /path/to/your/staticfiles/;

    # Enable range requests for PDFs (critical for streaming)
    add_header Accept-Ranges bytes always;

    # Long-lived cache for versioned files
    location ~ \.(v\d{8})\.(pdf|webp)$ {
        add_header Cache-Control "public, max-age=31536000, immutable";
        add_header Accept-Ranges bytes always;
        expires 1y;
        access_log off;
    }

    # Short cache for unversioned files
    location ~ \.(pdf|webp)$ {
        add_header Cache-Control "public, max-age=3600, must-revalidate";
        add_header Accept-Ranges bytes always;
        expires 1h;
    }

    # Enable ETag
    etag on;

    # Gzip/Brotli (skip for PDFs/WebP - already compressed)
    gzip on;
    gzip_types text/html text/css application/javascript application/json;
    gzip_disable "msie6";

    # Brotli (if module available)
    # brotli on;
    # brotli_types text/html text/css application/javascript application/json;
}

# Enable HTTP/2 for multiplexing
listen 443 ssl http2;
```

**Test range requests:**
```bash
curl -I -H "Range: bytes=0-1023" https://yourdomain.com/static/m1/m1-menu.pdf
# Should return: HTTP/1.1 206 Partial Content
# Should have: Accept-Ranges: bytes
```

---

## 8. CloudFront / Cloudflare CDN Configuration

### Cloudflare Page Rules

1. **For versioned files** (`/static/m1/*.v*.pdf`, `/static/m1/pages/*.webp`):
   - Cache Level: Cache Everything
   - Edge Cache TTL: 1 year
   - Browser Cache TTL: 1 year

2. **For unversioned** (`/m1/m1-menu.pdf`):
   - Cache Level: Cache Everything
   - Edge Cache TTL: 1 hour
   - Browser Cache TTL: 1 hour

**Via Cloudflare Dashboard:**
```
Rules → Page Rules → Create Page Rule

Pattern: yourdomain.com/static/m1/*.v*.pdf
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 month
  - Browser Cache TTL: 1 year
```

---

### AWS CloudFront Behavior

**Distribution settings:**

1. **Create behavior for `/static/m1/*`:**
   - Path Pattern: `static/m1/*`
   - Viewer Protocol Policy: Redirect HTTP to HTTPS
   - Allowed HTTP Methods: GET, HEAD, OPTIONS
   - Cache Policy: Create custom:
     - Min TTL: 0
     - Max TTL: 31536000 (1 year)
     - Default TTL: 86400 (1 day)
   - Compress Objects: No (PDFs/WebP already compressed)

2. **Origin Custom Headers:**
   - Accept-Ranges: bytes

**Via AWS CLI:**
```bash
# Create cache policy for static assets
aws cloudfront create-cache-policy \
  --cache-policy-config file://cache-policy.json
```

**cache-policy.json:**
```json
{
  "Name": "Static-PDF-Cache-Policy",
  "MinTTL": 0,
  "MaxTTL": 31536000,
  "DefaultTTL": 86400,
  "ParametersInCacheKeyAndForwardedToOrigin": {
    "EnableAcceptEncodingGzip": false,
    "EnableAcceptEncodingBrotli": false,
    "QueryStringsConfig": {
      "QueryStringBehavior": "none"
    },
    "HeadersConfig": {
      "HeaderBehavior": "whitelist",
      "Headers": {
        "Items": ["Range", "If-Range"]
      }
    },
    "CookiesConfig": {
      "CookieBehavior": "none"
    }
  }
}
```

---

## 9. HTML Viewer Snippets

### Option A: Direct PDF Link with Preview Image (Best for LCP)

```html
<!-- First page preview for instant LCP -->
<link rel="preload" as="image" href="/static/m1/pages/page-001-1x.webp"
      imagesrcset="/static/m1/pages/page-001-1x.webp 1x, /static/m1/pages/page-001-2x.webp 2x">

<a href="/static/m1/m1-menu.pdf"
   target="_blank"
   class="menu-preview"
   aria-label="View Ming Menu (PDF)">
  <img
    src="/static/m1/pages/page-001-1x.webp"
    srcset="/static/m1/pages/page-001-1x.webp 1x, /static/m1/pages/page-001-2x.webp 2x"
    alt="Ming Menu - Page 1"
    loading="eager"
    decoding="async"
    width="720"
    height="1020"
    class="menu-preview-image">
  <span class="menu-cta">View Full Menu (PDF)</span>
</a>
```

**CSS:**
```css
.menu-preview {
  display: block;
  max-width: 720px;
  margin: 0 auto;
  text-decoration: none;
  position: relative;
  cursor: pointer;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.menu-preview-image {
  width: 100%;
  height: auto;
  display: block;
  transition: transform 0.2s ease;
}

.menu-preview:hover .menu-preview-image {
  transform: scale(1.02);
}

.menu-preview:focus {
  outline: 3px solid #0066cc;
  outline-offset: 4px;
}

.menu-cta {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.8);
  color: white;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.menu-preview:hover .menu-cta,
.menu-preview:focus .menu-cta {
  opacity: 1;
}

@media (max-width: 768px) {
  .menu-preview {
    border-radius: 0;
  }
}
```

---

### Option B: PDF.js Embed with Lazy Loading

```html
<div id="pdf-viewer" class="pdf-viewer-container">
  <!-- Loading preview -->
  <div id="pdf-loading" class="pdf-loading">
    <img
      src="/static/m1/pages/page-001-1x.webp"
      srcset="/static/m1/pages/page-001-1x.webp 1x, /static/m1/pages/page-001-2x.webp 2x"
      alt="Menu Preview"
      width="720"
      height="1020">
    <p>Loading menu...</p>
  </div>

  <!-- PDF.js iframe (lazy loaded) -->
  <iframe id="pdf-frame"
          data-src="/static/pdfjs/web/viewer.html?file=/static/m1/m1-menu.pdf"
          width="100%"
          height="800px"
          style="border: none; display: none;"
          title="Ming Menu"
          loading="lazy"></iframe>

  <a href="/static/m1/m1-menu.pdf"
     download="ming-menu.pdf"
     class="pdf-download-btn">
    Download PDF
  </a>
</div>

<script>
// Lazy load PDF.js on user interaction or scroll
const pdfFrame = document.getElementById('pdf-frame');
const pdfLoading = document.getElementById('pdf-loading');

function loadPDF() {
  pdfFrame.src = pdfFrame.dataset.src;
  pdfFrame.style.display = 'block';
  pdfLoading.style.display = 'none';
}

// Load on click or scroll into view
pdfLoading.addEventListener('click', loadPDF);

const observer = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) {
    loadPDF();
    observer.disconnect();
  }
}, { threshold: 0.1 });

observer.observe(pdfLoading);

// Keyboard accessibility
pdfFrame.addEventListener('load', () => {
  pdfFrame.focus();
});
</script>
```

**Install PDF.js:**
```bash
# Download latest PDF.js
wget https://github.com/mozilla/pdf.js/releases/download/v4.0.379/pdfjs-4.0.379-dist.zip
unzip pdfjs-4.0.379-dist.zip -d static/pdfjs/
rm pdfjs-4.0.379-dist.zip
```

---

### Option C: Pure WebP Page Viewer (Fastest)

```html
<div class="page-viewer">
  <div class="page-container" id="page-container">
    <!-- Pages loaded dynamically -->
  </div>

  <div class="viewer-controls">
    <button id="prev-page" aria-label="Previous page">← Prev</button>
    <span id="page-info">Page <span id="current-page">1</span> of <span id="total-pages">0</span></span>
    <button id="next-page" aria-label="Next page">Next →</button>
  </div>

  <a href="/static/m1/m1-menu.pdf"
     download="ming-menu.pdf"
     class="download-pdf-btn">
    Download Full PDF
  </a>
</div>

<script>
// Configuration
const TOTAL_PAGES = 32; // Update with actual page count
const BASE_PATH = '/static/m1/pages';
let currentPage = 1;

// Update page info
document.getElementById('total-pages').textContent = TOTAL_PAGES;

// Render page with srcset for retina
function renderPage(pageNum) {
  const pageId = String(pageNum).padStart(3, '0');
  const img = document.createElement('img');
  img.src = `${BASE_PATH}/page-${pageId}-1x.webp`;
  img.srcset = `${BASE_PATH}/page-${pageId}-1x.webp 1x, ${BASE_PATH}/page-${pageId}-2x.webp 2x`;
  img.alt = `Menu Page ${pageNum}`;
  img.loading = pageNum === 1 ? 'eager' : 'lazy';
  img.decoding = 'async';
  img.width = 720;
  img.className = 'page-image';

  const container = document.getElementById('page-container');
  container.innerHTML = '';
  container.appendChild(img);

  document.getElementById('current-page').textContent = pageNum;

  // Preload next page
  if (pageNum < TOTAL_PAGES) {
    const nextPageId = String(pageNum + 1).padStart(3, '0');
    const preload = document.createElement('link');
    preload.rel = 'prefetch';
    preload.href = `${BASE_PATH}/page-${nextPageId}-1x.webp`;
    document.head.appendChild(preload);
  }
}

// Navigation
document.getElementById('prev-page').addEventListener('click', () => {
  if (currentPage > 1) {
    currentPage--;
    renderPage(currentPage);
  }
});

document.getElementById('next-page').addEventListener('click', () => {
  if (currentPage < TOTAL_PAGES) {
    currentPage++;
    renderPage(currentPage);
  }
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowLeft' && currentPage > 1) {
    currentPage--;
    renderPage(currentPage);
  } else if (e.key === 'ArrowRight' && currentPage < TOTAL_PAGES) {
    currentPage++;
    renderPage(currentPage);
  }
});

// Initial render
renderPage(1);
</script>

<style>
.page-viewer {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-container {
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.page-image {
  width: 100%;
  height: auto;
  display: block;
}

.viewer-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.viewer-controls button {
  padding: 10px 20px;
  font-size: 16px;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.viewer-controls button:hover {
  background: #0052a3;
}

.viewer-controls button:focus {
  outline: 3px solid #0066cc;
  outline-offset: 2px;
}

.viewer-controls button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.download-pdf-btn {
  display: block;
  text-align: center;
  padding: 12px 24px;
  background: #28a745;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 600;
}

.download-pdf-btn:hover {
  background: #218838;
}
</style>
```

---

## 10. Quality Gates & Verification

### A. File Size Check
```bash
# Original
ls -lh "/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf"

# Optimized
ls -lh ./build/m1-menu.linearized.pdf

# Should be <5 MB for balanced tier
```

---

### B. Linearization Check
```bash
qpdf --check-linearization ./build/m1-menu.linearized.pdf
# Expected: "PDF file is linearized"
```

---

### C. Page Count Verification
```bash
# Original
pdfinfo "/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf" | grep "^Pages:"

# Optimized
pdfinfo ./build/m1-menu.linearized.pdf | grep "^Pages:"

# Should match exactly
```

---

### D. Font Embedding Check
```bash
# Check fonts are still embedded
pdffonts ./build/m1-menu.linearized.pdf
# All fonts should show "yes" in "emb" column
```

---

### E. Text Selectability
```bash
# Extract text from first page (should work)
mutool draw -F txt -o - ./build/m1-menu.linearized.pdf 1 | head -20

# Should output readable menu text, not empty
```

---

### F. HTTP Range Requests
```bash
# Test range request support
curl -I -H "Range: bytes=0-1023" https://yourdomain.com/static/m1/m1-menu.pdf

# Expected headers:
# HTTP/1.1 206 Partial Content
# Accept-Ranges: bytes
# Content-Range: bytes 0-1023/XXXXX
```

---

### G. Visual Comparison
```bash
# Open both PDFs side-by-side
open "/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf"
open ./build/m1-menu.linearized.pdf

# Check at 100%, 150%, 200% zoom
# Menu items and prices should be crisp and readable
```

---

### H. Lighthouse Performance Test

**Create test HTML:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Menu Test</title>
</head>
<body>
  <link rel="preload" as="image" href="/static/m1/pages/page-001-1x.webp">
  <img src="/static/m1/pages/page-001-1x.webp"
       srcset="/static/m1/pages/page-001-1x.webp 1x, /static/m1/pages/page-001-2x.webp 2x"
       alt="Menu" width="720" height="1020" loading="eager">
  <a href="/static/m1/m1-menu.pdf">View PDF</a>
</body>
</html>
```

**Run Lighthouse:**
```bash
# Install Lighthouse CLI
npm install -g lighthouse

# Test performance
lighthouse https://yourdomain.com/menu-test.html \
  --only-categories=performance \
  --output=html \
  --output-path=./lighthouse-report.html \
  --throttling.rttMs=150 \
  --throttling.throughputKbps=1638 \
  --throttling.cpuSlowdownMultiplier=4

# Target metrics:
# LCP (Largest Contentful Paint): < 2.5s
# FCP (First Contentful Paint): < 1.8s
# Speed Index: < 3.4s
```

---

### I. Automated Verification Script

**verify.sh:**
```bash
#!/bin/bash

echo "=== PDF Optimization Verification ==="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

PDF_PATH="./build/m1-menu.linearized.pdf"
ORIGINAL_PATH="/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf"

# 1. File exists
if [ -f "$PDF_PATH" ]; then
  echo -e "${GREEN}✓${NC} Optimized PDF exists"
else
  echo -e "${RED}✗${NC} Optimized PDF not found"
  exit 1
fi

# 2. File size
SIZE=$(stat -f%z "$PDF_PATH")
SIZE_MB=$((SIZE / 1024 / 1024))
if [ $SIZE_MB -le 5 ]; then
  echo -e "${GREEN}✓${NC} File size: ${SIZE_MB}MB (≤ 5MB target)"
else
  echo -e "${RED}✗${NC} File size: ${SIZE_MB}MB (exceeds 5MB target)"
fi

# 3. Linearization
if qpdf --check-linearization "$PDF_PATH" 2>&1 | grep -q "linearized"; then
  echo -e "${GREEN}✓${NC} PDF is linearized"
else
  echo -e "${RED}✗${NC} PDF is NOT linearized"
fi

# 4. Page count match
ORIG_PAGES=$(pdfinfo "$ORIGINAL_PATH" | grep "^Pages:" | awk '{print $2}')
OPT_PAGES=$(pdfinfo "$PDF_PATH" | grep "^Pages:" | awk '{print $2}')
if [ "$ORIG_PAGES" -eq "$OPT_PAGES" ]; then
  echo -e "${GREEN}✓${NC} Page count matches: ${OPT_PAGES} pages"
else
  echo -e "${RED}✗${NC} Page count mismatch: Original=${ORIG_PAGES}, Optimized=${OPT_PAGES}"
fi

# 5. Fonts embedded
FONT_COUNT=$(pdffonts "$PDF_PATH" | tail -n +3 | wc -l | xargs)
if [ "$FONT_COUNT" -gt 0 ]; then
  echo -e "${GREEN}✓${NC} Fonts embedded: ${FONT_COUNT} fonts"
else
  echo -e "${RED}✗${NC} No fonts found (potential issue)"
fi

# 6. Text extraction
TEXT_LENGTH=$(mutool draw -F txt -o - "$PDF_PATH" 1 | wc -c | xargs)
if [ "$TEXT_LENGTH" -gt 100 ]; then
  echo -e "${GREEN}✓${NC} Text is selectable (${TEXT_LENGTH} characters on page 1)"
else
  echo -e "${RED}✗${NC} Text extraction failed or empty"
fi

echo ""
echo "=== Verification Complete ==="
```

**Make executable and run:**
```bash
chmod +x verify.sh
./verify.sh
```

---

## 11. "Do This Now" Checklist

Copy-paste these commands in order:

```bash
# ============================================
# STEP 1: Install tools
# ============================================
brew install ghostscript qpdf mupdf-tools poppler imagemagick

# ============================================
# STEP 2: Create build directory
# ============================================
cd /Users/anirudhchawla/Downloads/ming_group_website
mkdir -p ./build/m1-pages

# ============================================
# STEP 3: Optimize PDF (Balanced Tier)
# ============================================
gs -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.7 \
   -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH \
   -dDetectDuplicateImages=true \
   -dCompressFonts=true \
   -dSubsetFonts=true \
   -dEmbedAllFonts=true \
   -dAutoRotatePages=/None \
   -dColorImageDownsampleType=/Bicubic \
   -dColorImageResolution=150 \
   -dGrayImageDownsampleType=/Bicubic \
   -dGrayImageResolution=150 \
   -dMonoImageDownsampleType=/Bicubic \
   -dMonoImageResolution=300 \
   -dColorImageFilter=/DCTEncode \
   -dGrayImageFilter=/DCTEncode \
   -dJPEGQ=85 \
   -sOutputFile=./build/m1-menu.optimized.pdf \
   "/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf"

# ============================================
# STEP 4: Linearize for web streaming
# ============================================
qpdf --linearize \
     --compress-streams=y \
     --object-streams=generate \
     ./build/m1-menu.optimized.pdf \
     ./build/m1-menu.linearized.pdf

# ============================================
# STEP 5: Verify linearization
# ============================================
qpdf --check-linearization ./build/m1-menu.linearized.pdf

# ============================================
# STEP 6: Check output size
# ============================================
ls -lh ./build/m1-menu.linearized.pdf

# ============================================
# STEP 7: Generate first page preview (WebP)
# ============================================
mutool draw -o ./build/m1-pages/page-001-2x.png -w 1440 -r 144 \
       "/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf" 1
mutool draw -o ./build/m1-pages/page-001-1x.png -w 720 -r 72 \
       "/Users/anirudhchawla/Downloads/陈玉华2025 大明 Ming I Janno 皮质菜单(21X29.7CM) 4-28+.pdf" 1
magick ./build/m1-pages/page-001-2x.png -quality 85 ./build/m1-pages/page-001-2x.webp
magick ./build/m1-pages/page-001-1x.png -quality 85 ./build/m1-pages/page-001-1x.webp
rm ./build/m1-pages/page-001*.png

# ============================================
# STEP 8: Copy to Django static directory
# ============================================
mkdir -p static/m1/pages
cp ./build/m1-menu.linearized.pdf static/m1/m1-menu.pdf
cp ./build/m1-pages/page-001*.webp static/m1/pages/

# ============================================
# STEP 9: Collect static files (Django)
# ============================================
python manage.py collectstatic --noinput

# ============================================
# STEP 10: Verify everything
# ============================================
pdfinfo ./build/m1-menu.linearized.pdf | grep "^Pages:"
pdffonts ./build/m1-menu.linearized.pdf
ls -lh static/m1/

# ============================================
# DONE! Deploy and test
# ============================================
# Access at: http://localhost:8000/static/m1/m1-menu.pdf
```

---

## Quick Reference Card

| Task | Command |
|------|---------|
| **Check PDF size** | `ls -lh ./build/m1-menu.linearized.pdf` |
| **Verify linearization** | `qpdf --check-linearization ./build/m1-menu.linearized.pdf` |
| **Check page count** | `pdfinfo ./build/m1-menu.linearized.pdf \| grep Pages` |
| **Check fonts** | `pdffonts ./build/m1-menu.linearized.pdf` |
| **Extract text** | `mutool draw -F txt -o - ./build/m1-menu.linearized.pdf 1` |
| **Test range requests** | `curl -I -H "Range: bytes=0-1023" URL` |
| **Re-optimize (smaller)** | Change `-dPDFSETTINGS=/ebook` to `/screen` in Step 3 |
| **Re-optimize (bigger/better)** | Change `-dPDFSETTINGS=/ebook` to `/printer` in Step 3 |

---

## Troubleshooting

### Issue: PDF still too large

**Solution:** Use `/screen` preset or lower JPEG quality:
```bash
gs ... -dPDFSETTINGS=/screen -dJPEGQ=75 ...
```

---

### Issue: Text not selectable

**Solution:** Original PDF may have rasterized text. Check:
```bash
mutool draw -F txt -o - "ORIGINAL.pdf" 1
```
If empty, text was images. Cannot be fixed without OCR.

---

### Issue: Fonts look blurry

**Solution:** Increase image resolution:
```bash
gs ... -dColorImageResolution=300 -dGrayImageResolution=300 ...
```

---

### Issue: Range requests not working

**Solution:** Check Nginx config has `add_header Accept-Ranges bytes;` and test:
```bash
curl -I -H "Range: bytes=0-1023" https://yourdomain.com/static/m1/m1-menu.pdf
# Should return HTTP 206, not 200
```

---

### Issue: WhiteNoise not serving files

**Solution:** Ensure middleware order:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be here
    ...
]
```

Run `python manage.py collectstatic` after changes.

---

## Performance Targets

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **File Size** | ≤ 5 MB | `ls -lh` |
| **LCP (Largest Contentful Paint)** | < 2.5s | Lighthouse |
| **First Byte (TTFB)** | < 600ms | Chrome DevTools Network tab |
| **First Page Render** | < 1s | Visual inspection |
| **Full Download (3G)** | < 10s | Lighthouse throttling |

---

## Security Notes

1. **No sensitive data in PDFs:** Ensure menu doesn't contain internal pricing notes, etc.
2. **Public access:** Files in `static/` are public. Don't put authentication-required content there.
3. **CORS headers:** If serving from different domain, add:
   ```nginx
   add_header Access-Control-Allow-Origin "https://yourdomain.com";
   ```

---

## Maintenance

**When uploading new menu:**

1. Re-run optimization pipeline with new source PDF
2. Bump version number: `m1-menu.v20250429.pdf`
3. Update Django view or symlink to point to new version
4. Old versioned files stay cached; new requests get new version
5. Optionally purge CDN cache: `cloudflare cache purge` or `aws cloudfront create-invalidation`

---

**End of Guide** — Questions? Check Ghostscript docs (`man gs`) or Django staticfiles docs.

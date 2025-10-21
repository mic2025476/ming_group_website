# Ming Menu - Local Deployment Complete! ✓

## What Was Done

### 1. PDF Optimization
- **Original Size:** 74 MB
- **Optimized Size:** 1.5 MB (98% reduction!)
- **Format:** Linearized PDF for fast streaming
- **Quality:** Balanced tier (150 DPI, JPEG Q85)
- **Pages:** 33 pages preserved exactly

### 2. WebP Image Generation
- Generated all 33 pages as WebP images
- Each page has 2 versions:
  - 1x (720px width) for standard screens
  - 2x (1440px width) for retina displays
- Total: 66 WebP images (tiny file sizes, ~8-21 KB each)

### 3. Mobile-Friendly Viewer Created
**Features:**
- ✓ Swipe left/right to navigate pages (mobile-friendly)
- ✓ Navigation arrows (left/right buttons)
- ✓ Keyboard support (arrow keys on desktop)
- ✓ Page counter (shows current page / total)
- ✓ Fullscreen mode
- ✓ Download PDF button
- ✓ Touch-optimized for mobile & tablet
- ✓ Smooth fade transitions between pages
- ✓ Image preloading for instant navigation
- ✓ Black background for menu focus
- ✓ Responsive design (works on all devices)

### 4. Django Configuration
- Installed & configured WhiteNoise for efficient static file serving
- Added custom MIME types for PDF and WebP
- Configured compression (skips already-compressed files)
- Set up long-lived caching headers

## File Locations

```
ming_group_website/
├── build/
│   ├── m1-menu.optimized.pdf       (Ghostscript output)
│   ├── m1-menu.linearized.pdf      (Final optimized PDF)
│   └── m1-pages/
│       ├── page-001-1x.webp
│       ├── page-001-2x.webp
│       ├── ... (all 66 images)
│       └── page-033-2x.webp
│
├── static/m1/
│   ├── m1-menu.pdf                 (Optimized PDF)
│   └── pages/
│       └── ... (all 66 WebP images)
│
├── staticfiles/                     (Collected & ready to serve)
│   └── m1/
│       ├── m1-menu.pdf
│       ├── m1-menu.8088bedeb602.pdf (hashed version)
│       └── pages/
│           └── ... (132 files: originals + hashed versions)
│
└── templates/
    └── menu_viewer.html             (Mobile-friendly viewer)
```

## How to Test Locally

### Option 1: Run Django Dev Server
```bash
cd /Users/anirudhchawla/Downloads/ming_group_website
python manage.py runserver 0.0.0.0:8000
```

Then visit:
- **Menu Viewer:** http://localhost:8000/m1/menu/
- **Direct PDF:** http://localhost:8000/static/m1/m1-menu.pdf

### Option 2: Test on Your Phone (Same WiFi)
1. Get your computer's local IP:
   ```bash
   ipconfig getifaddr en0  # For WiFi
   ```

2. Run server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

3. On your phone's browser, visit:
   ```
   http://YOUR_IP:8000/m1/menu/
   ```
   Example: `http://192.168.1.100:8000/m1/menu/`

## Viewer Features Explained

### Mobile Experience
1. **Swipe left** → Next page
2. **Swipe right** → Previous page
3. **Tap arrows** → Navigate
4. **Pinch/zoom** → Zoom into menu items
5. **Fullscreen button** → Immersive viewing

### Desktop Experience
1. **Click arrows** → Navigate
2. **Arrow keys** → Navigate
3. **Fullscreen button** → Expand to fullscreen
4. **Download button** → Get optimized PDF

### Performance Optimizations
- First 3 pages preloaded on initial load
- Adjacent pages preloaded as you navigate
- Lazy loading for other pages
- Smooth fade transitions
- No layout shifts
- Instant response to swipes/clicks

## URLs Configured

| URL | Purpose |
|-----|---------|
| `/m1/menu/` | Mobile-friendly swipeable viewer |
| `/static/m1/m1-menu.pdf` | Direct PDF download |
| `/static/m1/pages/page-XXX-1x.webp` | Individual page images (1x) |
| `/static/m1/pages/page-XXX-2x.webp` | Individual page images (2x) |

## Next Steps: AWS Deployment

When you're ready to deploy to AWS, you'll need to:

### 1. S3 Setup
```bash
# Install AWS CLI if not already
brew install awscli
aws configure

# Upload static files to S3
aws s3 sync ./staticfiles/m1/ s3://your-bucket/static/m1/ \
    --cache-control "public, max-age=31536000, immutable" \
    --acl public-read
```

### 2. Django Settings for S3
Add to `settings.py`:
```python
# S3 Storage (for production)
if not DEBUG:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        },
    }

    AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
```

### 3. CloudFront (Optional but Recommended)
- Create CloudFront distribution pointing to S3
- Enable gzip/brotli compression
- Set cache behaviors for long-lived caching
- Update `AWS_S3_CUSTOM_DOMAIN` to CloudFront URL

### 4. Update Template
The template will automatically use the correct paths from `{% static %}` tags, so no changes needed!

## File Sizes Summary

| Item | Size | Count |
|------|------|-------|
| Original PDF | 74 MB | 1 file |
| Optimized PDF | 1.5 MB | 1 file |
| WebP images (1x) | ~8 KB each | 33 files |
| WebP images (2x) | ~21 KB each | 33 files |
| **Total optimized** | **~2.5 MB** | **67 files** |

## Browser Support

The viewer works on:
- ✓ iOS Safari (iPhone/iPad)
- ✓ Android Chrome
- ✓ Desktop Chrome/Firefox/Safari/Edge
- ✓ All modern browsers with WebP support

## Maintenance

### Update Menu (When PDF Changes)
1. Replace the source PDF
2. Run optimization pipeline:
   ```bash
   # Re-optimize
   gs -sDEVICE=pdfwrite ... -sOutputFile=./build/m1-menu.optimized.pdf SOURCE.pdf
   qpdf --linearize ./build/m1-menu.optimized.pdf ./build/m1-menu.linearized.pdf

   # Re-generate pages
   for i in {1..33}; do
     mutool draw ... # (see PDF_OPTIMIZATION_GUIDE.md for full commands)
   done

   # Convert to WebP
   for i in {1..33}; do
     magick ... # (see guide for full commands)
   done

   # Copy & deploy
   cp ./build/m1-menu.linearized.pdf static/m1/m1-menu.pdf
   cp ./build/m1-pages/*.webp static/m1/pages/
   python manage.py collectstatic --noinput
   ```

3. Push to AWS (production) or restart dev server (local)

## Troubleshooting

### Menu not loading?
- Check browser console for errors
- Verify static files were collected: `ls staticfiles/m1/pages/`
- Ensure dev server is running: `python manage.py runserver`

### Images not showing?
- Run `python manage.py collectstatic` again
- Check file permissions: `chmod 644 static/m1/pages/*`
- Verify files exist: `ls static/m1/pages/page-001-1x.webp`

### Swipe not working on mobile?
- Ensure viewport meta tag is present (it is!)
- Try clearing browser cache
- Test in different browser

## Performance Metrics (Expected)

When deployed with proper caching:
- **First Load (3G):** ~2-3 seconds
- **Page Navigation:** Instant (preloaded)
- **LCP (Largest Contentful Paint):** < 2.5s
- **Total Download (all 33 pages):** ~2.5 MB
- **Mobile Score (Lighthouse):** 90+

---

**Everything is ready for local testing!**

Run `python manage.py runserver` and visit http://localhost:8000/m1/menu/ to see the swipeable menu viewer in action.

For AWS deployment, see `PDF_OPTIMIZATION_GUIDE.md` for detailed S3/CloudFront instructions.

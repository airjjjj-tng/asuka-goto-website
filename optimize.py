import os
import re
from PIL import Image

html_path = 'index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update H1 and Logo
h1_target = '''<h1 class="logo">
                <a href="#"><img src="image/Guest House ASUKA ロゴ.png" alt="Guest House ASUKA"></a>
            </h1>'''
h1_replacement = '''<h1 class="visually-hidden">五島市（福江島）の長期宿泊・工事関係者向けゲストハウス Guest House ASUKA</h1>
            <div class="logo">
                <a href="#"><img src="image/Guest House ASUKA ロゴ.png" alt="Guest House ASUKA"></a>
            </div>'''
html = html.replace(h1_target, h1_replacement)

# Inject visually-hidden CSS into head
css_hidden = '''<style>
      .visually-hidden {
          position: absolute;
          width: 1px;
          height: 1px;
          margin: -1px;
          padding: 0;
          overflow: hidden;
          clip: rect(0, 0, 0, 0);
          border: 0;
      }
    </style>
</head>'''
html = html.replace('</head>', css_hidden)

# 2. Update JSON-LD (Address and Price)
html = html.replace('"松山町80-2"', '"吉田町740番"')
html = html.replace('"¥3,500 - ¥8,500"', '"¥5,000 - ¥6,000"')

# 3. Add Twitter Card Tags
twitter_tags = '''    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Guest House ASUKA | 五島市の長期宿泊・長期出張におすすめ">
    <meta name="twitter:description" content="長崎県五島市（福江島）の工事関係者・公共事業・ビジネス長期滞在に特化。泊まるほど安くなる連泊割引、自炊キッチン、無料朝食トースト、24hシャワー完備で現場を支えます。">
    <meta name="twitter:image" content="https://asuka-goto.com/image/asuka-parking-entrance.webp">'''
html = html.replace('<meta name="twitter:card" content="summary_large_image">', twitter_tags)

# 4. Process Images
image_map = {
    'Guest House ASUKA ロゴ.png': 'guest-house-asuka-logo',
    'IMG_20231013_111421698_HDR.jpg': 'asuka-parking-entrance',
    'IMG_4356.JPG': 'asuka-private-room',
    'IMG_4384.JPG': 'asuka-kitchen',
    'IMG_4376.JPG': 'asuka-shower-laundry',
    'IMG_20231024_110340_325.jpg': 'asuka-plants-interior',
    'IMG_20231017_145530_505.jpg': 'asuka-invoice-bed',
    'IMG_4382.JPG': 'asuka-living-relax',
    'IMG_4388.JPG': 'asuka-kitchen-breakfast',
    'IMG_4357.JPG': 'asuka-sanitary-laundry',
    'IMG_4368.JPG': 'asuka-room-electronic-lock',
    'IMG_4353.JPG': 'asuka-living-sofa',
    'IMG_4374.JPG': 'asuka-kitchen-ih-stove',
    'IMG_4379.JPG': 'asuka-shower-room',
    'IMG_4377.JPG': 'asuka-washbasin',
    'IMG_4386.JPG': 'asuka-entrance-hall',
    'アメニティセット.jpg': 'asuka-amenities'
}

img_dir = 'image'
def process_img_tag(match):
    tag = match.group(0)
    src_match = re.search(r'src="([^"]+)"', tag)
    if not src_match: return tag
    
    src = src_match.group(1)
    if not src.startswith('image/'): return tag
    
    filename = src.split('/')[-1]
    name, ext = os.path.splitext(filename)
    
    new_name = image_map.get(filename, name)
    new_filename = f"{new_name}.webp"
    new_src = f"image/{new_filename}"
    
    # Process file if it exists
    old_path = os.path.join(img_dir, filename)
    new_path = os.path.join(img_dir, new_filename)
    width, height = 0, 0
    if os.path.exists(old_path) and not os.path.exists(new_path):
        try:
            with Image.open(old_path) as img:
                width, height = img.size
                img.save(new_path, 'WEBP', quality=85)
        except Exception as e:
            print(f"Error converting {old_path}: {e}")
            return tag
    elif os.path.exists(new_path):
        with Image.open(new_path) as img:
            width, height = img.size
            
    # Update tag
    new_tag = tag.replace(src, new_src)
    
    # Add width and height if not present
    if width and height and 'width=' not in new_tag:
        # insert before closing >
        new_tag = new_tag.replace('>', f' width="{width}" height="{height}">')
        
    return new_tag

html = re.sub(r'<img[^>]+>', process_img_tag, html)

# Also update the OGP image URL
html = html.replace('image/IMG_20231013_111421698_HDR.jpg', 'image/asuka-parking-entrance.webp')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("SEO and image optimization completed.")

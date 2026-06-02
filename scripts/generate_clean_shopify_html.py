#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"
LATEST_OUTPUT = sorted(OUTPUT_DIR.glob("*"), reverse=True)[0] if OUTPUT_DIR.exists() else None

def generate_clean_shopify_html():
    if not LATEST_OUTPUT or not LATEST_OUTPUT.is_dir():
        print("❌ No output directory found")
        return
    
    products_file = LATEST_OUTPUT / "shopify_products.json"
    
    if not products_file.exists():
        print(f"❌ Products file not found: {products_file}")
        return
    
    with open(products_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    products = data.get('products', [])
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Twessie Collection</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #ffffff;
            color: #222;
            line-height: 1.6;
        }
        
        header {
            text-align: center;
            padding: 60px 40px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        h1 {
            font-size: 2.5em;
            font-weight: 300;
            letter-spacing: 3px;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 0.95em;
            color: #888;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 35px;
        }
        
        .product {
            background: #fff;
            border: 1px solid #f0f0f0;
            border-radius: 8px;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .product:hover {
            border-color: #ddd;
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        }
        
        .product-image {
            width: 100%;
            height: 420px;
            background: linear-gradient(135deg, #f5f5f5 0%, #efefef 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
            font-size: 0.9em;
            position: relative;
            overflow: hidden;
        }
        
        .product-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .product-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            background: #222;
            color: white;
            padding: 6px 12px;
            border-radius: 3px;
            font-size: 0.75em;
            font-weight: 600;
            letter-spacing: 1px;
        }
        
        .product-info {
            padding: 25px;
        }
        
        .product-category {
            font-size: 0.8em;
            color: #999;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }
        
        .product-name {
            font-size: 1.1em;
            font-weight: 600;
            margin-bottom: 4px;
            line-height: 1.3;
        }
        
        .product-name-cn {
            font-size: 0.9em;
            color: #888;
            margin-bottom: 15px;
        }
        
        .product-price {
            font-size: 1.4em;
            font-weight: 700;
            margin-bottom: 4px;
        }
        
        .product-sku {
            font-size: 0.75em;
            color: #999;
            font-family: monospace;
            margin-bottom: 20px;
        }
        
        .product-description {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 20px;
            line-height: 1.5;
        }
        
        .options-section {
            margin-top: 20px;
            border-top: 1px solid #f0f0f0;
            padding-top: 20px;
        }
        
        .option-group {
            margin-bottom: 20px;
        }
        
        .option-label {
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #222;
            margin-bottom: 10px;
            display: block;
        }
        
        .option-values {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .option-btn {
            padding: 8px 14px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 4px;
            font-size: 0.85em;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 500;
        }
        
        .option-btn:hover {
            border-color: #222;
            background: #f8f8f8;
        }
        
        .option-btn.active {
            border-color: #222;
            background: #222;
            color: white;
        }
        
        footer {
            text-align: center;
            padding: 40px;
            border-top: 1px solid #f0f0f0;
            color: #999;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 1.8em;
            }
            
            .grid {
                grid-template-columns: 1fr;
            }
            
            .product-image {
                height: 300px;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>TWESSIE</h1>
        <p class="subtitle">Independent Magazine Minimalism</p>
    </header>
    
    <div class="container">
        <div class="grid">
"""
    
    for product in products:
        colors_html = "".join([
            '<button class="option-btn" onclick="this.classList.toggle(\'active\')">%s</button>' % color
            for color in product['colors']
        ])
        
        sizes_html = "".join([
            '<button class="option-btn" onclick="this.classList.toggle(\'active\')">%s</button>' % size
            for size in product['sizes']
        ])
        
        price = product['base_price']
        sku = product['sku']
        category = product['category']
        title_en = product['title_en']
        title_cn = product['title_cn']
        description = product['description_en']
        
        html_content += """
            <div class="product">
                <div class="product-image">
                    <span class="product-badge">""" + category + """</span>
                </div>
                
                <div class="product-info">
                    <div class="product-category">""" + category + """</div>
                    <div class="product-name">""" + title_en + """</div>
                    <div class="product-name-cn">""" + title_cn + """</div>
                    
                    <div class="product-price">$""" + str(price) + """</div>
                    <div class="product-sku">""" + sku + """</div>
                    
                    <div class="product-description">""" + description + """</div>
                    
                    <div class="options-section">
                        <div class="option-group">
                            <label class="option-label">Color</label>
                            <div class="option-values">
                                """ + colors_html + """
                            </div>
                        </div>
                        
                        <div class="option-group">
                            <label class="option-label">Size</label>
                            <div class="option-values">
                                """ + sizes_html + """
                            </div>
                        </div>
                    </div>
                </div>
            </div>
"""
    
    html_content += """
        </div>
    </div>
    
    <footer>
        <p>© 2026 Twessie. All rights reserved.</p>
    </footer>
    
    <script>
        document.querySelectorAll('.option-btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                this.classList.toggle('active');
            });
        });
    </script>
</body>
</html>
"""
    
    html_file = LATEST_OUTPUT / "shopify_preview.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Clean Shopify HTML preview generated: " + str(html_file))

if __name__ == "__main__":
    generate_clean_shopify_html()

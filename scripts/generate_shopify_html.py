#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"
LATEST_OUTPUT = sorted(OUTPUT_DIR.glob("*"), reverse=True)[0] if OUTPUT_DIR.exists() else None

def generate_shopify_html():
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
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Twessie Shopify Products - {data.get('batch_date')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f8f8f8;
            padding: 40px 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 60px;
            background: white;
            padding: 60px 40px;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }}
        
        h1 {{
            font-size: 3em;
            color: #222;
            margin-bottom: 15px;
            font-weight: 300;
            letter-spacing: 3px;
            text-transform: uppercase;
        }}
        
        .tagline {{
            font-size: 1.2em;
            color: #777;
            font-style: italic;
            margin-bottom: 30px;
            letter-spacing: 1px;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 60px;
            flex-wrap: wrap;
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            color: #999;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            color: #222;
            font-weight: 600;
        }}
        
        .filters {{
            margin-bottom: 40px;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        
        .filter-btn {{
            padding: 10px 20px;
            border: 2px solid #ddd;
            background: white;
            cursor: pointer;
            border-radius: 6px;
            font-size: 0.9em;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 500;
        }}
        
        .filter-btn:hover,
        .filter-btn.active {{
            border-color: #222;
            background: #222;
            color: white;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 40px;
            margin-bottom: 60px;
        }}
        
        .product-card {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
            display: flex;
            flex-direction: column;
        }}
        
        .product-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 12px 32px rgba(0,0,0,0.15);
        }}
        
        .product-image {{
            width: 100%;
            height: 320px;
            background: linear-gradient(135deg, #f0f0f0 0%, #e8e8e8 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
            font-size: 0.9em;
            text-align: center;
            padding: 20px;
            position: relative;
        }}
        
        .category-badge {{
            position: absolute;
            top: 12px;
            right: 12px;
            background: #222;
            color: white;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .product-content {{
            padding: 25px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }}
        
        .sku {{
            font-family: 'Courier New', monospace;
            font-size: 0.8em;
            color: #999;
            text-transform: uppercase;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }}
        
        .product-title {{
            font-size: 1.1em;
            font-weight: 600;
            color: #222;
            margin-bottom: 8px;
            line-height: 1.4;
        }}
        
        .product-title-cn {{
            font-size: 0.95em;
            color: #666;
            margin-bottom: 15px;
            line-height: 1.4;
        }}
        
        .product-price {{
            font-size: 1.6em;
            color: #222;
            font-weight: 700;
            margin-bottom: 15px;
        }}
        
        .product-description {{
            font-size: 0.9em;
            color: #666;
            line-height: 1.6;
            margin-bottom: 15px;
            flex-grow: 1;
        }}
        
        .colors {{
            display: flex;
            gap: 8px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }}
        
        .color-tag {{
            display: inline-block;
            background: #f0f0f0;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 0.85em;
            color: #666;
            text-transform: capitalize;
        }}
        
        .sizes {{
            display: flex;
            gap: 6px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }}
        
        .size-tag {{
            display: inline-block;
            background: #f9f9f9;
            border: 1px solid #ddd;
            padding: 6px 10px;
            border-radius: 4px;
            font-size: 0.8em;
            text-align: center;
            min-width: 35px;
        }}
        
        .midjourney-section {{
            background: #f9f9f9;
            padding: 12px;
            border-radius: 6px;
            margin-top: 12px;
            border-left: 3px solid #666;
        }}
        
        .midjourney-title {{
            font-size: 0.8em;
            font-weight: 600;
            text-transform: uppercase;
            color: #999;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }}
        
        .midjourney-prompt {{
            font-size: 0.85em;
            color: #555;
            line-height: 1.5;
            font-family: 'Courier New', monospace;
        }}
        
        .seo-keywords {{
            font-size: 0.8em;
            color: #999;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid #e0e0e0;
        }}
        
        .seo-keywords strong {{
            color: #666;
        }}
        
        footer {{
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 0.9em;
        }}
        
        .timestamp {{
            text-align: center;
            color: #999;
            font-size: 0.85em;
            margin-bottom: 40px;
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 2em;
            }}
            
            .grid {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            
            .stats {{
                gap: 30px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>✨ Twessie</h1>
            <p class="tagline">Independent Magazine Minimalism</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-label">Total Products</div>
                    <div class="stat-value">{len(products)}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Base Price</div>
                    <div class="stat-value">$168</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Batch Date</div>
                    <div class="stat-value">{data.get('batch_date')}</div>
                </div>
            </div>
        </header>
        
        <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</div>
        
        <div class="grid">
"""
    
    for product in products:
        colors_html = "".join([f'<span class="color-tag">{color}</span>' for color in product['colors']])
        sizes_html = "".join([f'<span class="size-tag">{size}</span>' for size in product['sizes']])
        
        html_content += f"""
            <div class="product-card">
                <div class="product-image">
                    <span class="category-badge">{product['category']}</span>
                    <span>📸 Midjourney Generated Image</span>
                </div>
                
                <div class="product-content">
                    <div class="sku">{product['sku']}</div>
                    <div class="product-title">{product['title_en']}</div>
                    <div class="product-title-cn">{product['title_cn']}</div>
                    <div class="product-price">${{product['base_price']:.2f}}</div>
                    
                    <div class="product-description">{product['description_en']}</div>
                    
                    <div>
                        <div style="font-size: 0.85em; font-weight: 600; color: #666; margin-bottom: 6px;">Colors:</div>
                        <div class="colors">{colors_html}</div>
                    </div>
                    
                    <div>
                        <div style="font-size: 0.85em; font-weight: 600; color: #666; margin-bottom: 6px;">Sizes:</div>
                        <div class="sizes">{sizes_html}</div>
                    </div>
                    
                    <div class="midjourney-section">
                        <div class="midjourney-title">🎨 Midjourney Prompt</div>
                        <div class="midjourney-prompt">{product['midjourney_prompt']}</div>
                    </div>
                    
                    <div class="seo-keywords">
                        <strong>SEO:</strong> {product['seo_keywords']}
                    </div>
                </div>
            </div>
"""
    
    html_content += """
        </div>
        
        <footer>
            <p>🚀 Twessie Content Generator | Minimal. Intelligent. Independent.</p>
        </footer>
    </div>
</body>
</html>
"""
    
    html_file = LATEST_OUTPUT / "shopify_preview.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Shopify HTML preview generated: {html_file}")
    print(f"📂 Timestamp: {datetime.now().isoformat()}")

if __name__ == "__main__":
    generate_shopify_html()

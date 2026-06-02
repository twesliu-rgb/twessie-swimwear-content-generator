#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"
LATEST_OUTPUT = sorted(OUTPUT_DIR.glob("*"), reverse=True)[0] if OUTPUT_DIR.exists() else None

def generate_html():
    if not LATEST_OUTPUT or not LATEST_OUTPUT.is_dir():
        print("❌ No output directory found")
        return
    
    manifest_file = LATEST_OUTPUT / "batch_manifest.json"
    
    with open(manifest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    assets = data.get('assets', [])
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Twessie Content Generator - {data.get('batch_date')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
            padding: 40px 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 50px;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            font-size: 2.5em;
            color: #222;
            margin-bottom: 10px;
            font-weight: 300;
            letter-spacing: 2px;
        }}
        
        .batch-info {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .info-item {{
            text-align: center;
        }}
        
        .info-label {{
            font-size: 0.9em;
            color: #999;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .info-value {{
            font-size: 1.8em;
            color: #222;
            font-weight: bold;
            margin-top: 5px;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }}
        
        .card {{
            background: white;
            border-radius: 8px;
            padding: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-left: 4px solid #666;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
            border-bottom: 1px solid #f0f0f0;
            padding-bottom: 15px;
        }}
        
        .sku {{
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            font-weight: bold;
            color: #666;
            background: #f5f5f5;
            padding: 5px 10px;
            border-radius: 4px;
        }}
        
        .group-badge {{
            display: inline-block;
            background: #333;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .fabric-section {{
            margin-bottom: 20px;
        }}
        
        .fabric-title {{
            font-size: 0.95em;
            font-weight: 600;
            color: #222;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .fabric-item {{
            margin-bottom: 12px;
            padding-left: 15px;
            border-left: 2px solid #ddd;
        }}
        
        .fabric-name {{
            font-size: 0.9em;
            color: #333;
            font-weight: 500;
        }}
        
        .fabric-desc {{
            font-size: 0.85em;
            color: #777;
            margin-top: 3px;
            line-height: 1.4;
        }}
        
        .slogan {{
            background: linear-gradient(135deg, #f9f9f9 0%, #f0f0f0 100%);
            padding: 15px;
            border-radius: 6px;
            font-size: 0.95em;
            font-style: italic;
            color: #555;
            border-left: 3px solid #666;
            margin-top: 15px;
            line-height: 1.6;
        }}
        
        .timestamp {{
            font-size: 0.8em;
            color: #999;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #f0f0f0;
        }}
        
        footer {{
            text-align: center;
            padding: 30px;
            color: #999;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 1.8em;
            }}
            
            .grid {{
                grid-template-columns: 1fr;
            }}
            
            .batch-info {{
                gap: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>✨ Twessie Content Generator</h1>
            <div class="batch-info">
                <div class="info-item">
                    <div class="info-label">Batch Date</div>
                    <div class="info-value">{data.get('batch_date')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Total Assets</div>
                    <div class="info-value">{data.get('total_assets')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Groups</div>
                    <div class="info-value">5</div>
                </div>
                <div class="info-item">
                    <div class="info-label">SKUs per Group</div>
                    <div class="info-value">10</div>
                </div>
            </div>
        </header>
        
        <div class="grid">
"""
    
    for idx, asset in enumerate(assets, 1):
        fabric_analysis = asset.get('fabric_analysis', {})
        
        fabric_html = ""
        for direction_key in ['direction_1', 'direction_2', 'direction_3']:
            if direction_key in fabric_analysis:
                fabric = fabric_analysis[direction_key]
                fabric_html += f"""
            <div class="fabric-item">
                <div class="fabric-name">{fabric.get('name')} ({fabric.get('name_en')})</div>
                <div class="fabric-desc">{fabric.get('spec')}</div>
                <div class="fabric-desc"><strong>Colors:</strong> {fabric.get('color_palette')}</div>
            </div>
"""
        
        html_content += f"""
            <div class="card">
                <div class="card-header">
                    <div>
                        <div class="sku">{asset.get('sku')}</div>
                        <span class="group-badge">{asset.get('group_id')}</span>
                    </div>
                </div>
                
                <div class="fabric-section">
                    <div class="fabric-title">📋 Fabric Directions</div>
                    {fabric_html}
                </div>
                
                <div class="slogan">{asset.get('shopify_slogan')}</div>
                
                <div class="timestamp">Generated: {asset.get('generated_at')}</div>
            </div>
"""
    
    html_content += """
        </div>
        
        <footer>
            <p>🚀 Powered by Twessie Content Generator | Independent Magazine Minimalism</p>
        </footer>
    </div>
</body>
</html>
"""
    
    html_file = LATEST_OUTPUT / "preview.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML preview generated: {html_file}")
    print(f"📂 Open this file in your browser to view the content")

if __name__ == "__main__":
    generate_html()

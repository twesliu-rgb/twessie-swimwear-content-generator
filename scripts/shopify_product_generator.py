#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import random
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
import hashlib

CONFIG_PATH = Path(__file__).parent.parent / "config" / "brand_guidelines.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    BRAND_CONFIG = json.load(f)

OUTPUT_DIR = Path(__file__).parent.parent / "output" / datetime.now().strftime("%Y-%m-%d")

@dataclass
class ShopifyProduct:
    id: str
    sku: str
    title_en: str
    title_cn: str
    description_en: str
    description_cn: str
    category: str
    base_price: float
    colors: list
    sizes: list
    fabric_main: dict
    fabric_secondary: dict
    midjourney_prompt: str
    seo_keywords: str
    group_id: str
    generated_at: str
    image_url: str

class ShopifyProductGenerator:
    def __init__(self):
        self.fabric_library = BRAND_CONFIG["fabric_library"]
        self.regions = BRAND_CONFIG["regions"]
        self.base_price = 168.00
        self.categories = ["Bikini Top", "Bikini Bottom", "One-Piece", "Halter Strap Accessory"]
        self.standard_sizes = ["XS", "S", "M", "L", "XL", "XXL"]
        
        self.tone_keywords = [
            "rebellious yet refined",
            "minimalist luxury",
            "architectural elegance",
            "intelligent aesthetic",
            "anti-fashion statement"
        ]
        
        self.settings = [
            "Nordic minimalist studio, concrete backdrop, natural overcast light",
            "South France riviera courtyard, golden hour, warm terracotta tones",
            "Tokyo minimalist gallery, cool fluorescent clinical light",
            "Berlin underground carpark, raw brutalist architecture",
            "Scandinavian forest clearing, dappled natural light through trees"
        ]
    
    def generate_image_url(self, sku, category, colors):
        """Generate a unique placeholder image URL for each product"""
        hash_input = sku + category + "".join(colors)
        hash_value = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        
        category_colors = {
            "Bikini Top": "3d4a5a",
            "Bikini Bottom": "4a5a6a",
            "One-Piece": "5a6a7a",
            "Halter Strap Accessory": "6a7a8a"
        }
        
        color_code = category_colors.get(category, "5a6a7a")
        
        image_url = f"https://via.placeholder.com/500x650/{color_code}/ffffff?text=TWESSIE+{hash_value.upper()}"
        
        return image_url
    
    def get_color_from_fabric(self, fabric):
        """Extract color palette from fabric"""
        colors = fabric.get("color_pairings", ["white", "gray"])
        return random.sample(colors, min(2, len(colors)))
    
    def generate_fabric_pair(self):
        """Generate main + secondary fabric combination"""
        fabrics = random.sample(self.fabric_library, 2)
        return {
            "main": fabrics[0],
            "secondary": fabrics[1]
        }
    
    def generate_product_title(self, category, colors, fabric_main):
        """Generate English product title"""
        titles = {
            "Bikini Top": [
                f"{colors[0].title()} Sculptural {fabric_main.get('name_en', 'Crinkle')} Bikini Top",
                f"Minimalist {colors[0].title()} Textured Bikini Top",
                f"{fabric_main.get('name_en', 'Crinkle')} High-Waist Bikini Top in {colors[0].title()}",
                f"Architecture-Cut {colors[0].title()} Bikini Top",
            ],
            "Bikini Bottom": [
                f"{colors[0].title()} Minimalist {fabric_main.get('name_en', 'Crinkle')} Bikini Bottom",
                f"High-Cut {colors[0].title()} Bikini Brief",
                f"Structural {fabric_main.get('name_en', 'Crinkle')} Bikini Bottom",
                f"Raw-Edge {colors[0].title()} Bikini Bottom",
            ],
            "One-Piece": [
                f"{colors[0].title()} Architectural One-Piece Swimsuit",
                f"Minimalist {fabric_main.get('name_en', 'Crinkle')} One-Piece",
                f"Sculptural {colors[0].title()} Monokini",
                f"High-Fashion {colors[0].title()} One-Piece Suit",
            ],
            "Halter Strap Accessory": [
                f"Convertible Halter Strap - {colors[0].title()}",
                f"Minimalist Halter Extension - {colors[0].title()}",
                f"Sculptural Halter Accessory - {colors[0].title()}",
                f"Architectural Halter Strap System - {colors[0].title()}",
            ]
        }
        return random.choice(titles.get(category, titles["Bikini Top"]))
    
    def generate_product_title_cn(self, category, colors, fabric_main):
        """Generate Chinese product title"""
        titles = {
            "Bikini Top": [
                f"{colors[0]} 极简主义雕塑感比基尼上装",
                f"{colors[0]} 纹理感高端泳装上衣",
                f"建筑风格 {colors[0]} 比基尼上装",
            ],
            "Bikini Bottom": [
                f"{colors[0]} 极简主义比基尼下装",
                f"{colors[0]} 高腰裁剪比基尼",
                f"雕塑感 {colors[0]} 比基尼下装",
            ],
            "One-Piece": [
                f"{colors[0]} 建筑风格连体泳衣",
                f"{colors[0]} 极简主义连体泳装",
                f"{colors[0]} 高端一片式泳衣",
            ],
            "Halter Strap Accessory": [
                f"{colors[0]} 多功能挂脖带配件",
                f"{colors[0]} 极简主义比基尼带",
                f"{colors[0]} 建筑风格泳装配件",
            ]
        }
        return random.choice(titles.get(category, titles["Bikini Top"]))
    
    def generate_description_en(self, category, fabric_main, fabric_secondary, colors):
        """Generate English product description"""
        tone = random.choice(self.tone_keywords)
        fabric_name = fabric_main.get('name_en', 'Premium Crinkle')
        
        descriptions = [
            f"Crafted in premium {fabric_name} with {fabric_secondary.get('name_en', 'ribbed knit')} accents. "
            f"This {category.lower()} epitomizes {tone} luxury. "
            f"Featuring color-blocking in {colors[0]} and {colors[1]}. "
            f"Perfect for the discerning swimmer who refuses the obvious.",
            
            f"A statement piece in {fabric_name}. "
            f"This {category.lower()} combines {tone} design with impeccable craftsmanship. "
            f"Available in {colors[0]} with {colors[1]} detailing. "
            f"Not loud. Not obvious. Unmistakably Twessie.",
            
            f"{fabric_name} construction meets architectural precision in this {category.lower()}. "
            f"Designed for the intelligent, independent woman. "
            f"The {colors[0]} colorway with {colors[1]} accents creates a sophisticated palette. "
            f"Pure {tone} elegance.",
        ]
        return random.choice(descriptions)
    
    def generate_description_cn(self, category, fabric_main, fabric_secondary, colors):
        """Generate Chinese product description"""
        fabric_name = fabric_main.get('name_cn', '高级皱纹面料')
        
        descriptions = [
            f"采用{fabric_name}和{fabric_secondary.get('name_cn', '罗纹针织')}精心打造。"
            f"这款{category}体现了极简主义奢侈品的精髓。"
            f"{colors[0]}和{colors[1]}的色彩搭配完美无缺。"
            f"为那些拒绝平庸的女性而设计。",
            
            f"{fabric_name}打造的标志性款式。"
            f"这款{category}结合了建筑风格的设计和无可挑剔的工艺。"
            f"{colors[0]}配以{colors[1]}细节。"
            f"不张扬。不明显。纯粹的Twessie风格。",
        ]
        return random.choice(descriptions)
    
    def generate_midjourney_prompt(self, category, colors, fabric_main, tone):
        """Generate detailed Midjourney prompt"""
        setting = random.choice(self.settings)
        
        model_descriptions = [
            "rebellious Nordic model with intelligent gaze, sun-kissed skin",
            "refined editorial model, minimalist aesthetic, cool confidence",
            "fashion-forward woman, independent spirit, sculptural features",
            "high-fashion model with architectural bone structure",
        ]
        
        model_desc = random.choice(model_descriptions)
        
        prompt = (
            f"Professional fashion editorial photography. "
            f"Premium {fabric_main.get('name_en', 'crinkled')} {category.lower()} "
            f"in {colors[0]} with {colors[1]} accents. "
            f"Model: {model_desc}. "
            f"Setting: {setting}. "
            f"Macro texture details showcasing premium fabric. "
            f"Style: {tone}, high-end independent magazine, film grain, 8k quality. "
            f"--ar 3:4 --q 2"
        )
        return prompt
    
    def generate_seo_keywords(self, category, colors, fabric_main):
        """Generate SEO keywords"""
        keywords = [
            f"minimalist {category.lower()}",
            f"luxury {colors[0]} swimwear",
            f"{fabric_main.get('name_en', 'crinkle')} bikini",
            "high-end swimwear",
            "independent fashion",
            "architectural swimsuit",
            "minimalist luxury"
        ]
        return ", ".join(random.sample(keywords, min(5, len(keywords))))
    
    def generate_sku(self, group_num, product_num, category):
        """Generate unique SKU"""
        region = random.choice(self.regions)
        category_code = {
            "Bikini Top": "BT",
            "Bikini Bottom": "BB",
            "One-Piece": "OP",
            "Halter Strap Accessory": "HA"
        }.get(category, "XX")
        
        return f"TWESSIE_{region}_{category_code}_{group_num:02d}{product_num:02d}"
    
    def generate_products(self):
        """Generate 50 unique products: 5 groups × 10 SKUs"""
        products = []
        now = datetime.now().isoformat() + "Z"
        
        category_distribution = (
            ["Bikini Top"] * 20 + 
            ["Bikini Bottom"] * 20 + 
            ["One-Piece"] * 8 + 
            ["Halter Strap Accessory"] * 2
        )
        random.shuffle(category_distribution)
        
        for group_num in range(1, 6):
            for product_num in range(1, 11):
                idx = (group_num - 1) * 10 + (product_num - 1)
                category = category_distribution[idx]
                
                fabric_pair = self.generate_fabric_pair()
                colors = self.get_color_from_fabric(fabric_pair["main"])
                if len(colors) < 2:
                    colors.append(random.choice(fabric_pair["secondary"].get("color_pairings", ["gray"])))
                
                tone = random.choice(self.tone_keywords)
                
                sku = self.generate_sku(group_num, product_num, category)
                title_en = self.generate_product_title(category, colors, fabric_pair["main"])
                title_cn = self.generate_product_title_cn(category, colors, fabric_pair["main"])
                image_url = self.generate_image_url(sku, category, colors)
                
                product = ShopifyProduct(
                    id=f"TWESSIE_{group_num}_{product_num}",
                    sku=sku,
                    title_en=title_en,
                    title_cn=title_cn,
                    description_en=self.generate_description_en(category, fabric_pair["main"], fabric_pair["secondary"], colors),
                    description_cn=self.generate_description_cn(category, fabric_pair["main"], fabric_pair["secondary"], colors),
                    category=category,
                    base_price=self.base_price,
                    colors=colors,
                    sizes=self.standard_sizes,
                    fabric_main=fabric_pair["main"],
                    fabric_secondary=fabric_pair["secondary"],
                    midjourney_prompt=self.generate_midjourney_prompt(category, colors, fabric_pair["main"], tone),
                    seo_keywords=self.generate_seo_keywords(category, colors, fabric_pair["main"]),
                    group_id=f"group_{group_num:03d}",
                    generated_at=now,
                    image_url=image_url
                )
                
                products.append(asdict(product))
        
        return products
    
    def save_products(self, products):
        """Save products as JSON and CSV"""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        json_file = OUTPUT_DIR / "shopify_products.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "batch_date": datetime.now().strftime("%Y-%m-%d"),
                "total_products": len(products),
                "products": products
            }, f, ensure_ascii=False, indent=2)
        
        print(f"OK JSON saved: {json_file}")
        
        import csv
        csv_file = OUTPUT_DIR / "shopify_import.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                "Handle", "Title", "Body (HTML)", "Vendor", "Product Type",
                "Tags", "Published", "Option1 Name", "Option1 Value",
                "Option2 Name", "Option2 Value", "Variant SKU", "Variant Price",
                "Variant Compare At Price", "Variant Inventory Qty"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for product in products:
                handle = product['sku'].lower().replace('_', '-')
                description = f"<p>{product['description_en']}</p>"
                
                for color in product['colors']:
                    for size in product['sizes']:
                        writer.writerow({
                            "Handle": handle,
                            "Title": product['title_en'],
                            "Body (HTML)": description,
                            "Vendor": "Twessie",
                            "Product Type": product['category'],
                            "Tags": product['seo_keywords'],
                            "Published": "TRUE",
                            "Option1 Name": "Color",
                            "Option1 Value": color,
                            "Option2 Name": "Size",
                            "Option2 Value": size,
                            "Variant SKU": f"{product['sku']}-{color}-{size}",
                            "Variant Price": product['base_price'],
                            "Variant Compare At Price": "",
                            "Variant Inventory Qty": 10
                        })
        
        print(f"OK CSV saved: {csv_file}")
    
    def run(self):
        print("OK Starting product generation...")
        products = self.generate_products()
        print(f"OK Generated {len(products)} products")
        self.save_products(products)
        print("OK Complete!")

if __name__ == "__main__":
    generator = ShopifyProductGenerator()
    generator.run()

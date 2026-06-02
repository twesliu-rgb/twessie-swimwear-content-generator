#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import random
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config" / "brand_guidelines.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    BRAND_CONFIG = json.load(f)

OUTPUT_DIR = Path(__file__).parent.parent / "output" / datetime.now().strftime("%Y-%m-%d")

class TwessieContentGenerator:
    def __init__(self):
        self.fabric_library = BRAND_CONFIG["fabric_library"]
        self.sku_regions = BRAND_CONFIG["regions"]
        
    def generate_fabric_analysis(self):
        selected_fabrics = random.sample(self.fabric_library, 3)
        analysis = {}
        for idx, fabric in enumerate(selected_fabrics, 1):
            analysis[f"direction_{idx}"] = {
                "name": fabric["name_cn"],
                "name_en": fabric["name_en"],
                "spec": fabric["description"],
                "texture_quality": fabric["texture_quality"],
                "color_palette": " & ".join(fabric["color_pairings"])
            }
        return analysis
    
    def generate_slogan(self):
        slogans = [
            "We don't design to be stared at. We design to stand apart.",
            "Refuse the expected. Embrace the refined.",
            "Not for the masses. Crafted for the discerning.",
            "We don't follow trends. We define silence.",
            "Minimalist by design. Intelligent by nature.",
            "Anti-aesthetic luxury. Pure architectural elegance.",
            "Not loud. Not obvious. Unmistakably us.",
            "Reject the obvious. Own the understated."
        ]
        return random.choice(slogans)
    
    def generate_sku(self, group_num, sku_num):
        region = random.choice(self.sku_regions)
        return f"TWESSIE_{region}_{group_num:02d}{sku_num:02d}"
    
    def generate_content_batch(self, num_groups=5, skus_per_group=10):
        batch = []
        now = datetime.now().isoformat() + "Z"
        today = datetime.now().strftime("%Y-%m-%d")
        
        for group_num in range(1, num_groups + 1):
            group_fabric_analysis = self.generate_fabric_analysis()
            
            for sku_num in range(1, skus_per_group + 1):
                sku_code = self.generate_sku(group_num, sku_num)
                
                content = {
                    "date": today,
                    "group_id": f"group_{group_num:03d}",
                    "sku": sku_code,
                    "fabric_analysis": group_fabric_analysis,
                    "shopify_slogan": self.generate_slogan(),
                    "generated_at": now
                }
                
                batch.append(content)
        
        return batch
    
    def save_output(self, batch):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        batch_file = OUTPUT_DIR / "batch_manifest.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump({
                "batch_date": datetime.now().strftime("%Y-%m-%d"),
                "total_assets": len(batch),
                "assets": batch
            }, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Batch manifest saved: {batch_file}")
    
    def run(self):
        print("🚀 Twessie Content Generator Starting...")
        batch = self.generate_content_batch(num_groups=5, skus_per_group=10)
        print(f"📊 Generated {len(batch)} content assets")
        self.save_output(batch)
        print("✨ Generation complete!")

if __name__ == "__main__":
    generator = TwessieContentGenerator()
    generator.run()

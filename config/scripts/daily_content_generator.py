#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Content Generator for Twessie Premium Swimwear
Generates 5 groups × 10 SKUs of high-end minimalist creative assets
"""

import json
import os
from datetime import datetime
from pathlib import Path
import random
from dataclasses import dataclass, asdict
from typing import List, Dict

# Load configuration
CONFIG_PATH = Path(__file__).parent.parent / "config" / "brand_guidelines.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    BRAND_CONFIG = json.load(f)

OUTPUT_DIR = Path(__file__).parent.parent / "output" / datetime.now().strftime("%Y-%m-%d")


@dataclass
class ContentAsset:
    date: str
    group_id: str
    sku: str
    fabric_analysis: Dict
    midjourney_prompts: Dict
    shopify_slogan: str
    generated_at: str


class TwessieContentGenerator:
    """Main content generation engine"""
    
    def __init__(self):
        self.fabric_library = BRAND_CONFIG["fabric_library"]
        self.midjourney_framework = BRAND_CONFIG["midjourney_base_framework"]
        self.slogan_keywords = BRAND_CONFIG["slogan_parameters"]["tone_keywords"]
        self.sku_regions = BRAND_CONFIG["regions"]
        
    def generate_fabric_analysis(self) -> Dict:
        """Generate 3 fabric direction analyses"""
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
    
    def generate_midjourney_prompts(self) -> Dict:
        """Generate 2 professional Midjourney prompts"""
        lighting_nordic = "overcast natural cinematic lighting, muted color grading"
        mood_nordic = random.choice(["high-fashion model with an intelligent and detached expression",
                                     "rebellious yet refined editorial model, cold Nordic gaze",
                                     "minimalist luxury, intelligent aesthetic"])
        setting_nordic = "raw concrete wall and cold Nordic sea backdrop"
        
        scene_1 = (
            f"An editorial fashion lookbook photography for an independent swimwear brand. "
            f"Premium matte crinkled seersucker bikini in chalk white or stone gray. "
            f"Model: {mood_nordic}. "
            f"Setting: {setting_nordic}. "
            f"Close-up macro shot focusing on exquisite textile micro-texture. "
            f"Lighting: {lighting_nordic}. "
            f"Style: Minimalist editorial, premium independent magazine, crisp detail, 8k. "
            f"--ar 3:4 --q 2"
        )
        
        lighting_france = "golden hour warm natural cinematic sunlight, long soft shadows"
        mood_france = random.choice(["rebellious yet elegant independent woman, sun-kissed confidence",
                                     "minimalist luxury, South France riviera leisure",
                                     "editorial elegance with matte sophistication"])
        setting_france = "sun-drenched wooden bench in South France courtyard, warm terracotta tones"
        
        scene_2 = (
            f"A premium fashion campaign lookbook. "
            f"Luxury matte ribbed knit bikini in warm terracotta or olive drab. "
            f"Model: {mood_france}. "
            f"Setting: {setting_france}. "
            f"Macro texture details of premium ribbed fabric. "
            f"Lighting: {lighting_france}. "
            f"Style: Film grain texture, high-end independent magazine, luxury holiday atmosphere, crisp, 8k. "
            f"--ar 3:4 --q 2"
        )
        
        return {
            "scene_1_nordic_minimalism": scene_1,
            "scene_2_south_france_sunlight": scene_2
        }
    
    def generate_slogan(self) -> str:
        """Generate ENTP-sharp, rebellious Shopify slogan"""
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
    
    def generate_sku(self, group_num: int, sku_num: int) -> str:
        """Generate SKU code"""
        region = random.choice(self.sku_regions)
        return f"TWESSIE_{region}_{group_num:02d}{sku_num:02d}"
    
    def generate_content_batch(self, num_groups: int = 5, skus_per_group: int = 10) -> List[Dict]:
        """Generate complete daily batch: 5 groups × 10 SKUs = 50 content assets"""
        batch = []
        now = datetime.now().isoformat() + "Z"
        today = datetime.now().strftime("%Y-%m-%d")
        
        for group_num in range(1, num_groups + 1):
            group_fabric_analysis = self.generate_fabric_analysis()
            group_prompts = self.generate_midjourney_prompts()
            
            for sku_num in range(1, skus_per_group + 1):
                sku_code = self.generate_sku(group_num, sku_num)
                
                content = ContentAsset(
                    date=today,
                    group_id=f"group_{group_num:03d}",
                    sku=sku_code,
                    fabric_analysis=group_fabric_analysis,
                    midjourney_prompts=group_prompts,
                    shopify_slogan=self.generate_slogan(),
                    generated_at=now
                )
                
                batch.append(asdict(content))
        
        return batch
    
    def save_output(self, batch: List[Dict]) -> None:
        """Save generated content to JSON files"""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Save complete batch as single file
        batch_file = OUTPUT_DIR / "batch_manifest.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump({
                "batch_date": datetime.now().strftime("%Y-%m-%d"),
                "total_assets": len(batch),
                "assets": batch
            }, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Batch manifest saved: {batch_file}")
        
        # Save individual group files
        groups = {}
        for asset in batch:
            group_id = asset["group_id"]
            if group_id not in groups:
                groups[group_id] = []
            groups[group_id].append(asset)
        
        for group_id, assets in groups.items():
            group_file = OUTPUT_DIR / f"{group_id}.json"
            with open(group_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "group_id": group_id,
                    "count": len(assets),
                    "skus": assets
                }, f, ensure_ascii=False, indent=2)
            
            print(f"✅ {group_id} saved: {group_file}")
    
    def run(self) -> None:
        """Execute full generation pipeline"""
        print("🚀 Twessie Content Generator Starting...")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        batch = self.generate_content_batch(num_groups=5, skus_per_group=10)
        print(f"📊 Generated {len(batch)} content assets")
        
        self.save_output(batch)
        
        print("✨ Generation complete!")
        print(f"📂 Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    generator = TwessieContentGenerator()
    generator.run()

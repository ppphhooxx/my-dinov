import os
import json
import base64
from tqdm import tqdm

# 修改这里：你的数据路径
IMAGE_DIR = '/opt/project/SA1B/images'      # e.g., contains 0001.jpg, 0001.json
TSV_FILE = '/opt/project/SA1B/output.tsv'
INDEX_FILE = '/opt/project/SA1B/output.index'

def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as img_f:
        return base64.b64encode(img_f.read()).decode('utf-8')

def main():
    images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith('.jpg') or f.lower().endswith('.png')]
    images.sort()  # 确保顺序一致

    ann_start = 0
    with open(TSV_FILE, 'w') as f1, open(INDEX_FILE, 'w') as f2:
        for img_name in tqdm(images, desc="Processing images"):
            base_name = os.path.splitext(img_name)[0]
            json_path = os.path.join(IMAGE_DIR, base_name + '.json')
            image_path = os.path.join(IMAGE_DIR, img_name)

            # 检查 JSON 是否存在
            if not os.path.exists(json_path):
                print(f"⚠️ Warning: JSON file not found for {img_name}, skipping...")
                continue

            try:
                with open(json_path, 'r') as jf:
                    ann = json.load(jf)
                anno = json.dumps(ann)
                img_base64 = encode_image_to_base64(image_path)

                lent = 0
                lent += f1.write(f"{img_name}\t")
                lent += f1.write(f"{anno}\t")
                lent += f1.write(f"{img_base64}\n")
                f2.write(f"{ann_start} {lent}\n")
                ann_start += lent
            except Exception as e:
                print(f"❌ Error processing {img_name}: {e}")

    print(f"\n✅ Done! TSV written to: {TSV_FILE}")
    print(f"📍 Index written to: {INDEX_FILE}")

if __name__ == '__main__':
    main()

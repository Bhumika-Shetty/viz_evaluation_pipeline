import sys
import os
import json
from metrics import calculate_metrics_for_visualization

def grade_manual(image_path, code_path, original_data_path):
    """
    Manually grades a file you downloaded from ChatGPT Plus.
    """
    print(f"--- Grading Manual Entry ---")
    print(f"Image: {image_path}")
    print(f"Code:  {code_path}")
    
    # 1. Read the code you copied from ChatGPT
    try:
        with open(code_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
    except Exception as e:
        print(f"Error reading code file: {e}")
        return

    # 2. Run the Metrics (Fidelity, Entropy, Color, etc.)
    # Note: We pass the code content, not the file path, to the calculator
    results = calculate_metrics_for_visualization(
        image_path=image_path,
        code=code_content,
        original_data_path=original_data_path
    )

    # 3. Print Results nicely
    print("\n===  RESULTS ===")
    print(json.dumps(results, indent=2))
    
    # 4. Save to a JSON file next to the image
    output_json = image_path.replace('.png', '_metrics.json')
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n Metrics saved to: {output_json}")

if __name__ == "__main__":
    # Usage: python grade_manual.py <image.png> <code.py> <data.csv>
    if len(sys.argv) < 4:
        print("Usage: python grade_manual.py <path_to_image> <path_to_code> <path_to_data>")
        sys.exit(1)
        
    grade_manual(sys.argv[1], sys.argv[2], sys.argv[3])
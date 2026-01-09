import sys
import os
import json

# --- PATH FIX START ---
# Get the absolute path of the folder where grade_manual.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the 'src' folder
src_path = os.path.join(current_dir, 'src')

# Force Python to look in that specific folder
if src_path not in sys.path:
    sys.path.insert(0, src_path)
# --- PATH FIX END ---



# Now import the metrics
try:
    from metrics import calculate_metrics_for_visualization
    print("✅ Successfully imported metrics from src")
except ImportError as e:
    print(f"❌ CRITICAL IMPORT ERROR: Could not find metrics.py iSn {src_path}")
    sys.exit(1)

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
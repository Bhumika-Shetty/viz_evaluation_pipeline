# Cloud API Setup - No Ollama Needed!

Since Ollama download isn't working on your server, use a cloud API instead. **All are FREE to use!**

---

## Option 1: Groq (RECOMMENDED - Free & Fast)

### Step 1: Get Free API Key

1. Go to: https://console.groq.com/
2. Sign up (free)
3. Go to "API Keys" → Create new key
4. Copy the key (starts with `gsk_...`)

### Step 2: Configure Pipeline

```bash
cd /scratch/bds9746/viz_evaluation_pipeline

# Set your API key
export GROQ_API_KEY="your-api-key-here"

# Update config
cat > config/config.yaml << 'EOF'
# Model Configuration
model:
  name: "llama-3.2-90b-text-preview"  # Free Groq model
  api_type: "openai"  # Groq is OpenAI-compatible
  api_base: "https://api.groq.com/openai/v1"
  temperature: 0.7
  max_retries: 3

# Dataset Configuration
dataset:
  name: "titanic"
  path: "data/titanic.csv"
  description: "Titanic survival classification visualization"
  task: "Survival classification visualization"
  dimensions: "10D -> 2D"

# Output Configuration
outputs:
  visualizations_dir: "outputs/visualizations"
  metrics_dir: "outputs/metrics"
  logs_dir: "outputs/logs"
  save_code: true
  save_images: true

# Metrics Configuration
metrics:
  calculate_fidelity: true
  calculate_color_delta_e: true
  calculate_visual_entropy: true
  calculate_code_accuracy: true
EOF
```

### Step 3: Update Pipeline to Use API Key

```bash
cat > run_groq.sh << 'EOF'
#!/bin/bash
cd /scratch/bds9746/viz_evaluation_pipeline
source venv/bin/activate

# Set your Groq API key
export OPENAI_API_KEY="$GROQ_API_KEY"

cd src
python pipeline.py
EOF

chmod +x run_groq.sh
```

### Step 4: Run!

```bash
# Set your API key (replace with your actual key)
export GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxx"

# Run pipeline
./run_groq.sh
```

---

## Option 2: Together AI (Also Free)

### Step 1: Get API Key

1. Go to: https://api.together.xyz/
2. Sign up (free $25 credit)
3. Get API key

### Step 2: Configure

```bash
cd /scratch/bds9746/viz_evaluation_pipeline

# Update config for Together AI
sed -i 's|api_base: .*|api_base: "https://api.together.xyz/v1"|' config/config.yaml
sed -i 's|name: .*|name: "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo"|' config/config.yaml

# Set API key and run
export OPENAI_API_KEY="your-together-api-key"
cd src
python pipeline.py
```

---

## Option 3: OpenAI (Paid but Reliable)

If you have an OpenAI API key:

```bash
cd /scratch/bds9746/viz_evaluation_pipeline

# Update config
sed -i 's|api_base: .*|api_base: "https://api.openai.com/v1"|' config/config.yaml
sed -i 's|name: .*|name: "gpt-4o-mini"|' config/config.yaml

# Set API key and run
export OPENAI_API_KEY="sk-xxxxxxxxxxxxx"
cd src
python pipeline.py
```

---

## Quick Comparison

| Provider | Free? | Speed | Quality | Best For |
|----------|-------|-------|---------|----------|
| **Groq** | ✅ Yes | ⚡ Very Fast | Good | Testing, Development |
| **Together AI** | ✅ $25 credit | Fast | Very Good | Production |
| **OpenAI** | ❌ Paid | Medium | Best | High Quality |

---

## Complete Setup (Using Groq)

**Copy-paste these commands:**

```bash
# 1. Go to https://console.groq.com/ and get your free API key

# 2. Set API key (replace with yours)
export GROQ_API_KEY="gsk_your_actual_key_here"

# 3. Update config
cd /scratch/bds9746/viz_evaluation_pipeline
cat > config/config.yaml << 'CONF'
model:
  name: "llama-3.2-90b-text-preview"
  api_type: "openai"
  api_base: "https://api.groq.com/openai/v1"
  temperature: 0.7
  max_retries: 3
dataset:
  name: "titanic"
  path: "data/titanic.csv"
outputs:
  visualizations_dir: "outputs/visualizations"
  metrics_dir: "outputs/metrics"
  logs_dir: "outputs/logs"
  save_code: true
  save_images: true
metrics:
  calculate_fidelity: true
  calculate_color_delta_e: true
  calculate_visual_entropy: true
  calculate_code_accuracy: true
CONF

# 4. Make sure dataset exists
source venv/bin/activate
python download_data.py

# 5. Create run script
cat > run_cloud.sh << 'RUNNER'
#!/bin/bash
cd /scratch/bds9746/viz_evaluation_pipeline
source venv/bin/activate
export OPENAI_API_KEY="$GROQ_API_KEY"
cd src
python pipeline.py
RUNNER

chmod +x run_cloud.sh

# 6. Run!
./run_cloud.sh
```

---

## Why This Is Better

✅ **No downloads** - Just API calls
✅ **Free** - Groq and Together AI have free tiers
✅ **Fast** - Groq is extremely fast
✅ **No local resources** - Runs on their servers
✅ **Same quality** - Uses same LLaMA models
✅ **Works anywhere** - No network restrictions

---

## Troubleshooting

**API key not working?**
```bash
# Test your Groq API key
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

**Pipeline crashes?**
```bash
# Check if API key is set
echo $GROQ_API_KEY

# Check config
cat config/config.yaml | grep api_base
```

---

## For Next Time

Save this in a file to easily set up:

```bash
cat > ~/.groq_key << 'EOF'
export GROQ_API_KEY="your_key_here"
EOF

# Then just run:
source ~/.groq_key
cd /scratch/bds9746/viz_evaluation_pipeline
./run_cloud.sh
```

---

**Get your free Groq API key now: https://console.groq.com/**

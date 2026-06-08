import os
import random
import time
from fast_langdetect import detect

# =========================================================
# CONFIG BY SCRIPT TIER
# =========================================================
# Kept intact for reference mapping and fallback loops
SCRIPT_MAPPING = {
    "Latin": {
        "en": "en_corpus.txt",
        "fr": "fr_corpus.txt",
    },
    "Devanagari": {
        "hi": "hi_corpus.txt",
        "mr": "mr_corpus.txt",
    },
    "Tamil": {
        "ta": "ta_corpus.txt",
    },
    "Arabic": {
        "ar": "ar_corpus.txt",
    }
}

INPUT_FILE = "telegram_scale_input.txt"
ANSWER_FILE = "telegram_scale_answers.txt"

CORPUS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gutenberg_corpus")

# 6 languages * 200,000 = 1,200,000 Total High-Volume Test Dataset
MESSAGES_PER_LANGUAGE = 200000 

# =========================================================
# UTILITIES & LOCAL READ SYSTEMS
# =========================================================

def get_local_cache(lang_code):
    """
    Strictly reads text content from the local disk path.
    Throws a clean error if the file has not been manually provisioned.
    """
    local_filename = f"{lang_code}_corpus.txt"
    local_filepath = os.path.join(CORPUS_DIR, local_filename)
    
    if os.path.exists(local_filepath):
        print(f" -> Local cache found for [{lang_code}]. Loading from file.")
        with open(local_filepath, "r", encoding="utf-8") as f:
            return f.read()
            
    # Raise a descriptive error rather than attempting network fallback routines
    raise FileNotFoundError(
        f"Missing local source! Please place your custom data at: {local_filepath}"
    )

def chunk_text_by_tier(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    full_clean_text = " ".join(lines)
    words = full_clean_text.split()
    
    tiers = {"small": [], "medium": [], "large": []}
    current_words = []
    
    for word in words:
        current_words.append(word)
        current_str = " ".join(current_words)
        curr_len = len(current_str)
        
        if curr_len > 1000:
            current_words = [word]
            continue
            
        # Telegram metric grouping criteria distribution
        if 15 <= curr_len <= 45 and random.random() < 0.15:
            tiers["small"].append(current_str)
        elif 46 <= curr_len <= 200 and random.random() < 0.05:
            tiers["medium"].append(current_str)
        elif 201 <= curr_len <= 1000 and random.random() < 0.01:
            tiers["large"].append(current_str)
            current_words = []
            
    return tiers

# =========================================================
# DATASET GENERATION PIPELINE
# =========================================================
all_inputs = []
all_answers = []

print("=== STARTING REALISTIC TELEGRAM-SCALE DATASET GENERATION (LOCAL ONLY) ===")
generation_start_time = time.time()

for script_name, langs in SCRIPT_MAPPING.items():
    print(f"\nProcessing Script Tier: {script_name}")
    for lang_code in langs.keys():
        try:
            # Swapped completely to local disk stream extraction
            raw_text = get_local_cache(lang_code)
            parsed_tiers = chunk_text_by_tier(raw_text)
            
            target_per_tier = MESSAGES_PER_LANGUAGE // 3
            lang_pool = []
            
            for tier_name in ["small", "medium", "large"]:
                pool = parsed_tiers[tier_name]
                if not pool:
                    pool = [f"Fallback placeholder string sizing text check evaluation mock data for {tier_name}."]
                
                scaled_pool = []
                while len(scaled_pool) < target_per_tier:
                    random.shuffle(pool)
                    scaled_pool.extend(pool)
                lang_pool.extend(scaled_pool[:target_per_tier])
            
            all_inputs.extend(lang_pool)
            all_answers.extend([lang_code] * len(lang_pool))
            print(f" ✅ Success: Scaled up {len(lang_pool):,} Telegram-profile samples for [{lang_code}]")

        except Exception as e:
            print(f" ❌ Failed reading data file for language {lang_code}: {e}")

generation_end_time = time.time()
generation_duration = generation_end_time - generation_start_time
print(f"\nDataset Assembly completed in: {generation_duration:.2f} seconds.")

# =========================================================
# DATASET SHUFFLING & DISK WRITE
# =========================================================
print(f"Shuffling and saving {len(all_inputs):,} records to disk...")
combined = list(zip(all_inputs, all_answers))
random.shuffle(combined)
all_inputs, all_answers = zip(*combined)

with open(INPUT_FILE, "w", encoding="utf-8") as f:
    f.writelines(f"{item.replace('\n', ' ')}\n" for item in all_inputs)

with open(ANSWER_FILE, "w", encoding="utf-8") as f:
    f.writelines(f"{item}\n" for item in all_answers)

# =========================================================
# HIGH-SPEED BENCHMARK PIPELINE (FIXED LOGIC)
# =========================================================
print(f"\n=== BENCHMARKING FAST_LANGDETECT OVER {len(all_inputs):,} SAMPLES ===")
total = len(all_inputs)

tier_metrics = {
    "small":  {"correct": 0, "total": 0},
    "medium": {"correct": 0, "total": 0},
    "large":  {"correct": 0, "total": 0}
}

test_start_time = time.time()

for idx, (text, expected) in enumerate(zip(all_inputs, all_answers), start=1):
    try:
        # Determine Telegram Tier Profile Grouping
        text_len = len(text)
        if text_len <= 45:
            tier_key = "small"
        elif text_len <= 200:
            tier_key = "medium"
        else:
            tier_key = "large"
            
        tier_metrics[tier_key]["total"] += 1
        
        # Run inference
        result = detect(text, model="auto")
        
        # Parsing the verified list[dict] data payload format
        if isinstance(result, list) and len(result) > 0:
            predicted = result[0].get("lang", "").lower()
        elif isinstance(result, dict):
            predicted = result.get("lang", "").lower()
        else:
            predicted = str(result).lower()

        if predicted == expected:
            tier_metrics[tier_key]["correct"] += 1

        # Responsive CLI display tracker
        if idx % 200000 == 0:
            elapsed = time.time() - test_start_time
            print(f"Processed {idx:,}/{total:,} items... Current runtime: {elapsed:.2f}s")

    except Exception as e:
        pass

test_end_time = time.time()
total_test_duration = test_end_time - test_start_time

# Calculations for metrics
global_correct = sum(tier["correct"] for tier in tier_metrics.values())
global_accuracy = (global_correct / total) * 100 if total > 0 else 0
avg_time_per_text_ms = (total_test_duration / total) * 1000

# =========================================================
# METRIC ANALYSIS REPORT
# =========================================================
print("\n===== FINAL METRIC RUNTIME REPORT =====")
print(f"TOTAL SAMPLES PROCESSED  : {total:,}")
print(f"CORRECT CLASSIFICATIONS  : {global_correct:,}")
print(f"DETECTOR GLOBAL ACCURACY : {global_accuracy:.2f}%")
print(f"AVG TIME TO PROCESS TEXT : {avg_time_per_text_ms:.4f} ms per message")
print(f"THROUGHPUT RUNTIME SPEED : {int(total / total_test_duration):,} inferences/second\n")

print("===== TIER ACCURACY BREAKDOWN =====")
for tier_name, data in tier_metrics.items():
    t_total = data["total"]
    t_correct = data["correct"]
    t_acc = (t_correct / t_total) * 100 if t_total > 0 else 0
    print(f"Tier [{tier_name.upper():<6}] Size Range: {t_total:,} items | Accuracy: {t_acc:.2f}%")


# Sample output : 
# D:\projects\new_era\z.Tests\groupSailBotLanguageDetectionModule\TEST_1>python dataSetGenerator.py
# === STARTING REALISTIC TELEGRAM-SCALE DATASET GENERATION ===

# Processing Script Tier: Latin
#  -> Local cache found for [en]. Loading from file.
#  ✅ Success: Scaled up 199,998 Telegram-profile samples for [en]
#  -> Local cache found for [fr]. Loading from file.
#  ✅ Success: Scaled up 199,998 Telegram-profile samples for [fr]

# Processing Script Tier: Devanagari
#  -> Local cache found for [hi]. Loading from file.
#  ✅ Success: Scaled up 199,998 Telegram-profile samples for [hi]
#  -> Local cache found for [mr]. Loading from file.
#  ✅ Success: Scaled up 199,998 Telegram-profile samples for [mr]

# Processing Script Tier: Tamil
#  -> Local cache found for [ta]. Loading from file.
#  ✅ Success: Scaled up 199,998 Telegram-profile samples for [ta]

# Processing Script Tier: Arabic
#  -> Local cache found for [ar]. Loading from file.
#  ✅ Success: Scaled up 199,998 Telegram-profile samples for [ar]

# Dataset Assembly completed in: 1.33 seconds.
# Shuffling and saving 1,199,988 records to disk...

# === BENCHMARKING FAST_LANGDETECT OVER 1,199,988 SAMPLES ===
# Processed 200,000/1,199,988 items... Current runtime: 8.07s
# Processed 400,000/1,199,988 items... Current runtime: 15.91s
# Processed 600,000/1,199,988 items... Current runtime: 23.59s
# Processed 800,000/1,199,988 items... Current runtime: 31.38s
# Processed 1,000,000/1,199,988 items... Current runtime: 39.41s

# ===== FINAL METRIC RUNTIME REPORT =====
# TOTAL SAMPLES PROCESSED  : 1,199,988
# CORRECT CLASSIFICATIONS  : 1,143,494
# DETECTOR GLOBAL ACCURACY : 95.29%
# AVG TIME TO PROCESS TEXT : 0.0395 ms per message
# THROUGHPUT RUNTIME SPEED : 25,293 inferences/second

# ===== TIER ACCURACY BREAKDOWN =====
# Tier [SMALL ] Size Range: 399,996 items | Accuracy: 91.96%
# Tier [MEDIUM] Size Range: 399,996 items | Accuracy: 96.50%
# Tier [LARGE ] Size Range: 399,996 items | Accuracy: 97.41%

# D:\projects\new_era\z.Tests\groupSailBotLanguageDetectionModule\TEST_1>  
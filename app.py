import streamlit as st
import pandas as pd
import os
import datetime

# ========================
# File Setup
# ========================
DATA_FILE = "data/contributions.csv"
CACHE_FILE = "data/cache.csv"

os.makedirs("data", exist_ok=True)

# Initialize data files if not present
for file in [DATA_FILE, CACHE_FILE]:
    if not os.path.exists(file):
        pd.DataFrame(columns=["timestamp", "language", "region", "proverb", "meaning"]).to_csv(file, index=False)


# ========================
# Helper Functions
# ========================
def save_contribution(language, region, proverb, meaning, cache=False):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "language": language,
        "region": region,
        "proverb": proverb,
        "meaning": meaning
    }

    file = CACHE_FILE if cache else DATA_FILE
    df = pd.read_csv(file)
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(file, index=False)


def sync_cache():
    """Sync cached offline entries into main contributions file"""
    if os.path.exists(CACHE_FILE):
        cache_df = pd.read_csv(CACHE_FILE)
        if len(cache_df) > 0:
            main_df = pd.read_csv(DATA_FILE)
            combined = pd.concat([main_df, cache_df], ignore_index=True)
            combined.to_csv(DATA_FILE, index=False)
            pd.DataFrame(columns=["timestamp", "language", "region", "proverb", "meaning"]).to_csv(CACHE_FILE, index=False)
            return len(cache_df)
    return 0


# ========================
# Streamlit UI
# ========================
st.set_page_config(page_title="Local Lore & Proverb Collector", layout="centered")

st.title("🌿 Local Lore & Proverb Collector")
st.write("Preserve your village’s wisdom by contributing proverbs and folk sayings in your own language.")

with st.form("proverb_form"):
    language = st.text_input("Language / Dialect", placeholder="e.g., Telugu, Hindi, Kannada")
    region = st.text_input("Region / Village", placeholder="e.g., Hyderabad, Andhra Pradesh")
    proverb = st.text_area("Your Proverb / Saying", placeholder="Write in your own language")
    meaning = st.text_area("Meaning / Context (optional)", placeholder="Explain its significance")

    submitted = st.form_submit_button("Submit")

if submitted:
    try:
        save_contribution(language, region, proverb, meaning, cache=False)
        st.success("✅ Thank you! Your proverb has been saved.")
    except Exception as e:
        save_contribution(language, region, proverb, meaning, cache=True)
        st.warning("⚠️ No internet? Saved locally, will sync later.")

# Show sync option
if st.button("🔄 Sync Offline Contributions"):
    synced = sync_cache()
    if synced > 0:
        st.success(f"✅ Synced {synced} cached contributions!")
    else:
        st.info("No cached contributions to sync.")

# Display recent contributions
st.subheader("📜 Recent Contributions")
try:
    data = pd.read_csv(DATA_FILE)
    st.dataframe(data.tail(5))
except Exception:
    st.info("No contributions yet.")

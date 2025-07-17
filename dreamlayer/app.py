import streamlit as st
import os
from dotenv import load_dotenv
from services import enhance_prompt, generate_hd_image
import requests
from datetime import datetime


st.set_page_config(
    page_title="DreamLayer",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)
load_dotenv()
api_key = os.getenv("BRIA_API_KEY")


def initialize_session_state():
    st.session_state.setdefault("api_key", api_key)
    st.session_state.setdefault("enhanced_prompt", None)
    st.session_state.setdefault("original_prompt", "")
    st.session_state.setdefault("all_image_sets", [])
    st.session_state.setdefault("aspect_ratio", "1:1")
    st.session_state.setdefault("style", "Realistic")

initialize_session_state()

def download_image_content(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response.content
    except Exception as e:
        st.error(f"❌ Failed to download image from {url}: {str(e)}")
        return None

def clear_history():
    st.session_state.all_image_sets = []
    st.success("Image history cleared!")
    st.rerun()


st.markdown("""
<style>





section[data-testid="stSidebar"] {
        width: 150px !important;
        min-width: 420px !important;
    }
    section[data-testid="stSidebar"] > div:first-child {
        width: 150x !important;
        min-width: 420px !important;
    }
    
    
    
    .reportview-container .main .block-container {
        padding: 2rem 3rem;
    }
    h1 {
        color: #FF4B4B;
        text-align: center;
        font-size: 3.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #262730;
        color: #f0f2f6;
        border: 1px solid #444;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        font-size: 1.05rem;
    }
    
    
    
    
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: bold;
        padding: 0.75rem 1rem;
        margin-top: 0.5rem;
        transition: all 0.2s ease-in-out;
        border: none;
        background-color: #20252b;
        color: #d3d3d3;
    }
    
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    .stButton>button[kind="primary"] {
        background-color: #FF4B4B;
        color: white;
    }
    
    
    .stButton>button[kind="secondary"] {
        background-color: #333;
        color: #ccc;
    }
    .stButton>button.selected-option {
        background-color: #FF4B4B !important;
        color: white !important;
        border: 2px solid #FF4B4B !important;
        box-shadow: 0 0 10px rgba(255, 75, 75, 0.5);
    }

    
   
</style>
""", unsafe_allow_html=True)

# Sidebar 
with st.sidebar:
    st.header("⚙️ Image Settings")
    num_images = st.slider("🖼️ Number of images to generate", 1, 4, 1)
    enhance_img = st.checkbox("✨ Apply AI quality enhancement", value=True)

    st.subheader("🖐️ Aspect Ratio")
    ar_options = ["1:1", "16:9", "9:16", "4:3", "3:4"]
    ar_cols = st.columns(len(ar_options))
    for i, option in enumerate(ar_options):
        if ar_cols[i].button(option, key=f"ar_btn_{option}"):
            st.session_state.aspect_ratio = option
            st.rerun()

    st.subheader("🎨 Artistic Style")
    style_options = ["Realistic", "Artistic", "Cartoon", "Sketch", "Watercolor", "Oil Painting", "Digital Art"]
    style_cols = st.columns(3)
    for i, option in enumerate(style_options):
        if style_cols[i % 3].button(option, key=f"style_btn_{option}"):
            st.session_state.style = option
            st.rerun()

# Main Area 
st.title("✨ DreamLayer – AI Image Generator")

prompt = st.text_area("Describe your image:", value=st.session_state.original_prompt, height=150)

if prompt != st.session_state.original_prompt:
    st.session_state.original_prompt = prompt
    st.session_state.enhanced_prompt = None

col_buttons = st.columns([1, 1])
with col_buttons[0]:
    if st.button("✨ Enhance My Prompt", key="enhance_button"):
        if not prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Enhancing prompt..."):
                try:
                    result = enhance_prompt(st.session_state.api_key, prompt)
                    if result:
                        st.session_state.enhanced_prompt = result
                        st.success("Prompt enhanced!")
                        st.rerun()
                    else:
                        st.error("Enhancement failed. Try again.")
                except Exception as e:
                    st.error(f"Enhancement error: {str(e)}")

with col_buttons[1]:
    generate_clicked = st.button("🚀 Generate Images", type="primary", key="generate_button")

if st.session_state.enhanced_prompt:
    st.subheader("💡 Enhanced Prompt:")
    st.info(st.session_state.enhanced_prompt)

if generate_clicked:
    if not prompt.strip():
        st.warning("Enter a prompt first.")
    elif not st.session_state.api_key:
        st.error("Missing API key in .env")
    else:
        with st.spinner("Generating images..."):
            try:
                used_prompt = st.session_state.enhanced_prompt or prompt
                final_prompt = f"{used_prompt}, in {st.session_state.style.lower()} style" if st.session_state.style != "Realistic" else used_prompt
                result = generate_hd_image(
                    prompt=final_prompt,
                    api_key=st.session_state.api_key,
                    num_results=num_images,
                    aspect_ratio=st.session_state.aspect_ratio,
                    sync=True,
                    enhance_image=enhance_img,
                    medium="art" if st.session_state.style != "Realistic" else "photography",
                    prompt_enhancement=False,
                    content_moderation=True
                )
                image_urls = []
                if isinstance(result, dict):
                    image_urls.extend(result.get("result_urls", []))
                    if "result_url" in result:
                        image_urls.append(result["result_url"])
                    if "result" in result:
                        for item in result["result"]:
                            if isinstance(item, dict) and "urls" in item:
                                image_urls.extend(item["urls"])
                            elif isinstance(item, list):
                                image_urls.extend(item)

                image_urls = list(set(image_urls))
                if image_urls:
                    st.success("Images ready!")
                    st.session_state.all_image_sets.insert(0, {
                        "prompt": final_prompt,
                        "urls": image_urls,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.rerun()
                else:
                    st.warning("No images returned. Try different settings.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

if st.session_state.all_image_sets:
    st.header("✨ Latest Creation")
    latest = st.session_state.all_image_sets[0]
    st.markdown(f"**Prompt:** *{latest['prompt']}*")
    st.caption(f"Generated on {latest['timestamp']}")
    cols = st.columns(min(len(latest["urls"]), 4))
    for i, url in enumerate(latest["urls"]):
        with cols[i % len(cols)]:
            st.image(url, use_column_width=True)
            st.download_button("Download", data=download_image_content(url), file_name=f"dreamlayer_{i+1}.jpg")

    if len(st.session_state.all_image_sets) > 1:
        st.header("🕰️ History")
        if st.button("🗑️ Clear All History", type="secondary"):
            clear_history()
        for idx, item in enumerate(st.session_state.all_image_sets[1:]):
            with st.expander(f"Prompt: {item['prompt']} ({item['timestamp']})"):
                cols = st.columns(min(len(item["urls"]), 3))
                for i, url in enumerate(item["urls"]):
                    with cols[i % len(cols)]:
                        st.image(url, use_column_width=True)
                        st.download_button("Download", data=download_image_content(url), file_name=f"history_{idx+1}_{i+1}.jpg")

import streamlit as st
from PIL import Image
import google.generativeai as genai

# ✅ Set up Streamlit page
st.set_page_config(page_title="📸 Image & Text to Blog Generator")

# ✅ Configure Gemini API
genai.configure(api_key="AIzaSyCmtBxTrQ_qJES4gR7ANDzuiNQ02c747Nk")

@st.cache_resource
def load_model():
    return genai.GenerativeModel("gemini-1.5-flash")

model = load_model()

# ✅ Title and instructions
st.title("🧠 AI Blog Generator")
st.write("Generate a blog post from a captured image or a custom text topic!")

# ----------- 📷 IMAGE TO BLOG SECTION -----------
st.header("📷 Generate Blog from Image")

# Initialize session state
if "show_camera" not in st.session_state:
    st.session_state.show_camera = False

# Show/hide camera buttons
col1, col2 = st.columns([1, 1])
with col1:
    if not st.session_state.show_camera:
        if st.button("📸 Take Photo"):
            st.session_state.show_camera = True
with col2:
    if st.session_state.show_camera:
        if st.button("❌ Close Camera"):
            st.session_state.show_camera = False

# Show camera input
if st.session_state.show_camera:
    img_file_buffer = st.camera_input("Capture your image")

    if img_file_buffer is not None:
        if st.button("✍️ Generate Blog from Image"):
            with st.spinner("Generating blog from image..."):
                try:
                    image = Image.open(img_file_buffer)
                    st.image(image, caption="📷 Captured Image", use_column_width=True)

                    prompt = "Generate a short caption for this image, then write a short blog post about it."
                    response = model.generate_content([image, prompt])
                    output = response.text.strip()

                    lines = output.split("\n")
                    caption = lines[0] if lines else "No caption generated."
                    blog = "\n".join(lines[1:]) if len(lines) > 1 else "No blog content generated."

                    st.success("✅ Caption and blog generated!")
                    st.markdown(f"**Caption:** *{caption}*")
                    st.markdown("### 📝 Auto-Generated Blog")
                    st.markdown(blog)

                except Exception as e:
                    st.error(f"⚠️ Generation error: {e}")

# ----------- 📝 TEXT TO BLOG SECTION -----------
st.header("📝 Generate Blog from Text")

custom_prompt = st.text_input("Enter a topic for your blog:", placeholder="e.g. Future of AI in Education")

if st.button("✍️ Generate Blog from Text"):
    if custom_prompt.strip():
        with st.spinner("Generating blog from text..."):
            try:
                prompt = f"Write a detailed blog post about: {custom_prompt}"
                response = model.generate_content(prompt)
                blog = response.text.strip()

                st.success("✅ Blog generated from text!")
                st.markdown(f"**Blog Topic:** *{custom_prompt}*")
                st.markdown("### 📝 Auto-Generated Blog")
                st.markdown(blog)

            except Exception as e:
                st.error(f"⚠️ Generation error: {e}")
    else:
        st.warning("⚠️ Please enter a topic before clicking generate.")

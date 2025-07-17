# DreamLayer 🎨

**DreamLayer** is an AI-powered image generator built with Streamlit. It enhances user prompts and produces high-quality images with adjustable settings like aspect ratio, image count, and style — all through a simple, dark-themed interface.

---

## 🚀 Run Locally

Follow these steps to download and run the project on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/dreamlayer.git
cd dreamlayer
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
# Activate the virtual environment:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

### 4. Add Environment Variables

Create a `.env` file in the root directory and add your API key or other necessary variables:

```
API_KEY=your_api_key_here
```

> 🔒 Do not commit this `.env` file to version control.

### 5. Start the Application

```bash
streamlit run app.py
```

The app will open automatically in your default web browser at:
```
http://localhost:8501
```

---

## 🗂 Project Structure

```
dreamlayer/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── .env                    # (User-created) Environment variables
├── components/             # UI components (buttons, sliders, layout)
├── services/               # Core AI functions (prompt enhancement, image generation)
├── workflows/              # Prompt preprocessing and enhancement logic
```

---

## 🧼 Clean Up (Optional)

Before packaging or redeploying locally:

```bash
# Remove Python cache files
find . -type d -name '__pycache__' -exec rm -r {} +
```

---

## ❓ Support

If you encounter any issues or have questions, feel free to open an issue or fork the repository to improve it.

---

🧠 Built with ❤️ using Streamlit and Python

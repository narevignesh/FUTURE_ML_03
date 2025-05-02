
---

### 📄 `README.md`

````markdown
# 🤖 Gemini AI ChatBot – Streamlit UI

An elegant and customizable AI chatbot built with **Streamlit** and **Google's Gemini 1.5 Flash model**. This chatbot supports multi-chat sessions, beautiful sidebar navigation, and a responsive interface – ready to use for any AI support or customer assistant needs.


---

## 🚀 Features

- ✅ Gemini 1.5 Flash integration
- ✅ Multi-chat sidebar with delete and switch functionality
- ✅ Stylish and responsive Streamlit UI
- ✅ Fixed chat input bar with clean UX
- ✅ No backend required – all frontend & API-based!

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/narevignesh/FUTURE_ML_03.git
cd FUTURE_ML_03
````

### 2. Install Requirements

Make sure you're using **Python 3.8+**, then install the dependencies:

```bash
pip install -r requirements.txt
```

> Contents of `requirements.txt`:
>
> ```
> streamlit==1.32.0
> google-generativeai==0.3.2
> python-dotenv==1.0.0  # Optional
> ```

---

## 🔑 Set Up Your Gemini API Key

You must generate your own Gemini API key:

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Log in with your Google account.
3. Create a new API key.
4. Copy it.

Then, **open `app.py` (or your script)** and **replace** the placeholder in this line:

```python
genai.configure(api_key="YOUR_API_KEY_HERE")
```

with your own key:

```python
genai.configure(api_key="AIzaSyXXXXXXX...")  # Your actual key
```

---

## 🏃 Run the Chatbot

```bash
streamlit run app.py
```

Once started, it will launch in your default browser at [http://localhost:8501](http://localhost:8501)

---

## 🧠 Powered By

* [Streamlit](https://streamlit.io/)
* [Google Generative AI](https://ai.google.dev/)
* [Gemini 1.5 Flash](https://ai.google.dev/gemini)

---


## 🧑‍💻 Author

Made with ❤️ by [Nare Vignesh](https://github.com/narevignesh)



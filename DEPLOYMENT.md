# How to Host on Streamlit Community Cloud

Hosting your Electrician Smart Assistant for free on Streamlit Cloud requires getting this code onto GitHub, as Streamlit uses GitHub to pull and update your app.

### Step 1: Push to GitHub
1. Create a new, blank repository on [GitHub](https://github.com/new). You can name it `electrician-assistant`.
2. Do **not** initialize it with a README or .gitignore (we already made them locally).
3. Open a terminal in `d:\AI_Agent_Build\dist\AI_Agent_Pro_App\electrician_assistant`.
4. Run these exact commands (replace `YOUR_USERNAME` and `REPO_NAME`):
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
   git push -u origin main
   ```

### Step 2: Link to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **New App** (or "Create App").
3. Select your new GitHub repository (`electrician-assistant`), branch (`main`), and Main file path (`app.py`).

### Step 3: Add Your GROQ API Key to Streamlit Secrets
Because we ignored the `.env` file (so hackers don't steal your key off GitHub), you need to give the key directly to Streamlit safely:
1. Before clicking "Deploy", click on **Advanced settings...** at the bottom of the Streamlit deployment screen.
2. Under **Secrets**, paste your `GROQ_API_KEY`:
   ```toml
   GROQ_API_KEY="your-groq-key-here"
   ```
3. Click **Save**, then click **Deploy!**

Your app will take a couple of minutes to build and install everything in `requirements.txt`. Once finished, you will have a live public website link you can share with any electrician!

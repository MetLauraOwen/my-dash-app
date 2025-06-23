# Hackathon May 2025

Welcome to the Hackathon May 2025 repository! This project was created as part of a collaborative hackathon event.

## Table of Contents

- [Project Overview](#project-overview)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)

## Project Overview

This project creates an interactive plot using dash to visualise and explore output from HOTdays model. 

## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

See requirements.txt 

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/hackathon_may_2025.git
cd hackathon_may_2025

# Install dependencies
# See requirements.txt 
```

## Usage

### Run Locally

To run the interactive plotting on your own computer:

```bash
python plot_UK_city_diff.ipynb
```

This will generate a link at the bottom of the script to view your interactive plot.

---

### Deploy on Render (for a shareable web link)

1. **Create a Web Service on Render**
   - Go to [https://render.com](https://render.com)
   - Sign up or log in
   - Click **"New Web Service"**
   - Choose **"Deploy from GitHub"**
   - Select your repo:  
     `https://github.com/MetLauraOwen/my-dash-app`

2. **Configure the Service**
   - **Environment:** Python
   - **Build Command:**  
     `pip install -r requirements.txt`
   - **Start Command:**  
     `gunicorn app:server`  
     *(Assuming your file is `app.py` and your Dash app is created with `app = dash.Dash(__name__)`.)*
   - **Instance Type:** Starter (Free)
   - Click **"Create Web Service"**

3. **Wait for Deployment**
   - The first build may take a couple of minutes.
   - You’ll get a public URL like:  
     `https://my-dash-app.onrender.com`

Your Dash app is now live!


# Dash App - interactive graphics for Hotdays from Hackathon May 2025

This project was created durng the CPP hackathon event May 2025.

## Table of Contents

- [Project Overview](#project-overview)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Extra Info](#info)

## Project Overview

This project creates an interactive plot using dash to visualise and explore output from HOTdays model. 

## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

See requirements.txt 

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/my-dash-app.git
cd my-dash-app

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

## Extra Info

- The dataframes needed to run the plotting are in /dataframes
- These were created using the scripts create_city_dfs.ipynb, create_city_dfs_NEWMEANS.ipynb (just an updated file that generated means within the script - this is default), create_UK_dfs.ipynb.
- The above scripts used data output from HOTdays that Laura generated from Simons' /data/users/laura.owen/extremes/heatwaves/HadUKGrid/dur-clim/CPM5km/v2/UK/EEE/SimHD/Observed/ files using the scripts /home/users/laura.owen/uk-heatwave-climatology-duration/sim-HOTdays/laura_probs.R and laura_probs_mean.R

- plot_compare_versions.ipynb is a W.I.P script where you can read in the new HOTdays output we recently generated (with the spatial make-stationary part) to compare with the results we submitted in the November report.


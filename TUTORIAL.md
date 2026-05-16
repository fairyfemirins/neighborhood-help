# Tutorial: Reproducible Setup for Neighborhood Help App

## Prerequisites
- Python 3.10+
- Git

## Step-by-Step Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/fairyfemirins/neighborhood-help.git
   cd neighborhood-help
   ```

2. **Install dependencies:**
   ```bash
   pip install --user --break-system-packages flask flask-login
   ```

3. **Run the app:**
   ```bash
   python3 app.py
   ```

4. **Access the app:**
   Open `http://localhost:5017` in your browser.

## Testing the App
1. **Register** as a user or helper.
2. **Post a job** (e.g., "Fix my leaky faucet").
3. **Apply for a job** (if you're a helper).
4. **Leave a review** after completing a job.

## Troubleshooting
- **Port already in use:** Change the port in `app.py` (e.g., `port=5018`).
- **No jobs showing:** Ensure you're logged in as a helper to see available jobs.
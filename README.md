# Neighborhood Help App

## Overview
A **mobile-friendly web app** that connects users with **trusted neighbors and local handymen** for small jobs and tasks.
- **Features:** User profiles, job posting, matching, and reviews.
- **Target Users:** Busy individuals, families, and local handymen.

## Technical Architecture
- **Backend:** Flask + SQLite.
- **Frontend:** HTML/CSS/JS + Bootstrap (mobile-friendly).
- **Database:** SQLite (for user profiles, jobs, and reviews).

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/fairyfemirins/neighborhood-help.git
   cd neighborhood-help
   ```
2. Install dependencies:
   ```bash
   pip install --user --break-system-packages flask flask-login
   ```
3. Run the app:
   ```bash
   python3 app.py
   ```
4. Open `http://localhost:5017` in your browser.

## Usage
- **Register** as a user or helper.
- **Post jobs** or **apply for jobs** based on your role.
- **Leave reviews** for completed jobs.

## License
MIT License.
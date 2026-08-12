# Robot Brain: Closed-Loop Autonomy Stack
A complete, from-scratch computer vision and control pipeline built in Python and OpenCV. 

## System Architecture
This project demonstrates a full sense-think-act loop, engineered to handle real-world sensor noise and physical constraints.

### 1. Perception Layer (OpenCV)
- **HSV Thresholding:** Color-space filtering tuned for real-world lighting (handling the physical limits of specular reflection and ambient light scatter).
- **Morphological Operations:** Using custom kernels to heal mask fragmentation and reject false positives.

### 2. Sensor Fusion & Tracking
- **Weighted Average Filter:** Combines historical state (70%) with current sensor data (30%) to eliminate jitter.
- **Occlusion Handling:** Maintains a "Ghost State" to predict target location during temporary visual blockages.

### 3. Control Layer (P-Controller)
- **Proportional Steering:** Calculates pixel-error from the screen center to generate smooth motor commands.
- **Dead Zone Implementation:** Enforces a tolerance threshold to prevent infinite oscillation at the target center.

### 4. State Machine (Behavior Hierarchy)
Context-aware state transitions that override low-level control when mission goals are met:
- `SEARCHING`: Target lost, relying on ghost memory.
- `TRACKING`: Target acquired, P-controller active.
- `ALIGNED`: Target centered within the dead zone.
- `ARRIVED`: Target area exceeds physical threshold; motors killed.

## How to Run
```bash
source .venv/bin/activate
python perception/brain_states.py

## Income Tools (Data & Scraping)
In addition to the robotics perception stack, this repository contains deployable tools for data engineering and automation tasks:

- `tools/broken_scraper.py`: Demonstrates fixing unescaped CSV commas using Python's built-in `csv` module.
- `tools/quotes_scraper.py`: A robust web scraper using `requests` and `BeautifulSoup` to extract structured data into clean CSVs.
- `tools/data_cleaner.py`: A `pandas` pipeline to deduplicate rows, fill missing numeric values, and standardize mixed-format dates.

### How to run the tools
```bash
pip install -r requirements.txt
python tools/data_cleaner.py

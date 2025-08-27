
# AI Virtual Personal Fitness Coach (Basic Rule-Based Demo)

**What this includes (sample)**:
- `app.py`: Streamlit app (rule-based recommendations using sample CSVs)
- `data/workouts.csv`: Sample workouts dataset
- `data/nutrition.csv`: Sample nutrition/diet dataset
- `utils.py`: small helper utilities
- `requirements.txt`

## How to run locally
1. Create and activate a virtual environment (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate   # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Next steps (recommended)
- Integrate MediaPipe for real-time pose detection and rep counting.
- Add persistence (user accounts + progress tracking).
- Improve diet assembly algorithm to match target calories automatically.
- Add audio cues and better UI/UX.

# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites

- Python 3.9+ installed
- Terminal/Command Prompt access

### Step-by-Step Setup

#### 1. Open Terminal

Navigate to the project directory:

```bash
cd Sequential-Pattern-Mining-with-Interactive-Visualization-Dashboard
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

⏱️ This takes ~2-3 minutes depending on your internet speed.

#### 3. Start Backend (Terminal 1)

```bash
python backend/main.py
```

You should see:

```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend is ready!

#### 4. Start Frontend (Terminal 2)

Open a NEW terminal window and run:

```bash
streamlit run frontend/app.py
```

Your browser will automatically open to `http://localhost:8501`

✅ You're ready to start mining!

### First Time Usage

#### Try with Sample Data

1. **Upload**: Click "Choose a CSV file" and select `datasets/sample.csv`
2. **Validate**: Click "🚀 Upload and Validate"
3. **Map Columns**:
   - Sequence ID: `UserID`
   - Item: `Product`
   - Timestamp: `Timestamp`
4. **Generate**: Click "🔄 Generate Sequences"
5. **Set Parameters**:
   - Minimum Support: `0.2` (20%)
   - Max Length: `5`
6. **Mine**: Click "⛏️ Start Mining Patterns"
7. **Explore**: Browse the visualizations!

Expected result: ~15-20 patterns in 1-2 seconds

### Using Your Own Data

Your CSV should have:

- **ID Column**: UserID, SessionID, CustomerID, etc.
- **Item Column**: Product, Action, Event, etc.
- **Timestamp** (optional): Any date/time format

Example:

```csv
UserID,Product,Date
1,Laptop,2023-01-01
1,Mouse,2023-01-02
2,Phone,2023-01-01
2,Case,2023-01-01
```

### Common Issues

**"Cannot connect to backend"**
→ Make sure backend is running in another terminal

**"Module not found"**
→ Run `pip install -r requirements.txt`

**Upload fails**
→ Ensure your file is a valid CSV with at least 2 columns

### Tips for Best Results

✨ **For small datasets** (<1000 sequences):

- Min Support: 0.05 - 0.2

🎯 **For medium datasets** (1K-10K sequences):

- Min Support: 0.01 - 0.05

🚀 **For large datasets** (>10K sequences):

- Min Support: 0.005 - 0.01
- Max Length: 5 or less

### Next Steps

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🔧 Check [TODO.md](TODO.md) for future features
- 💡 Try different datasets from Kaggle

### Need Help?

1. Check the Troubleshooting section in README.md
2. Review the error messages in the terminal
3. Ensure all dependencies are installed correctly

---

**Happy Pattern Mining! ⛏️**

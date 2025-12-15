# Sequential Pattern Mining with Interactive Visualization Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A comprehensive, production-ready web application for sequential pattern mining with interactive visualizations. Built for university final-year submission with clean architecture and professional UI/UX.

## 🎯 Overview

This project enables users to upload sequential transaction datasets and automatically discover frequent patterns using the **PrefixSpan algorithm**. Results are presented through beautiful, interactive visualizations including bar charts, line graphs, heatmaps, and network diagrams.

### Key Features

- ✨ **Beautiful Modern UI** - Clean, professional Streamlit interface
- 📤 **Easy Dataset Upload** - Drag-and-drop CSV file upload
- 🔄 **Automatic Preprocessing** - Smart column mapping and sequence generation
- ⛏️ **PrefixSpan Algorithm** - Efficient sequential pattern mining
- 📊 **Interactive Visualizations** - Multiple chart types with Plotly
- 🎨 **Network Graphs** - Visualize sequence flows and transitions
- 📥 **Export Results** - Download mined patterns as CSV
- 🚀 **Fast & Scalable** - FastAPI backend with async support

## 🧠 What is Sequential Pattern Mining?

Sequential pattern mining is a data mining technique that discovers frequently occurring patterns in sequential data. Unlike traditional association rule mining, it considers the **order** of events.

### Real-World Applications

- **E-commerce**: Analyze customer purchase sequences (e.g., "customers who buy A, then B, often buy C next")
- **Web Analytics**: Discover common navigation paths on websites
- **Healthcare**: Identify treatment sequences and patient care patterns
- **Mobile Apps**: Understand user interaction flows
- **Financial Services**: Detect transaction patterns for fraud detection

### Example

Given customer purchase sequences:

```
Customer 1: A → B → C
Customer 2: A → C
Customer 3: B → C → D
Customer 4: A → B → C
```

The algorithm discovers patterns like:

- `A → B → C` (support: 50%)
- `A → C` (support: 75%)
- `B → C` (support: 75%)

## 🏗️ Project Structure

```
sequential-pattern-mining/
│
├── backend/                      # FastAPI Backend
│   ├── main.py                   # API entry point & endpoints
│   ├── data_loader.py            # CSV upload & validation
│   ├── preprocessing.py          # Automatic column mapping & sequencing
│   ├── mining.py                 # PrefixSpan implementation
│   ├── visualization_data.py     # Convert results to chart format
│   ├── schemas.py                # Pydantic models for API
│   └── utils.py                  # Helper functions & logging
│
├── frontend/                     # Streamlit Frontend
│   ├── app.py                    # Main Streamlit application
│   └── components/
│       ├── upload.py             # Dataset upload component
│       ├── column_selector.py    # Column mapping interface
│       ├── parameters.py         # Mining parameter configuration
│       ├── dashboard.py          # Visualization dashboard
│       └── tables.py             # Results table display
│
├── datasets/                     # Sample datasets
│   └── sample.csv                # Example transaction data
│
├── outputs/                      # Generated outputs
│   ├── mined_patterns.csv        # Mining results
│   └── charts/                   # Saved visualizations
│
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── TODO.md                       # Future improvements
```

## 📋 Requirements

- Python 3.9 or higher
- pip (Python package manager)
- 4GB RAM minimum (8GB recommended for large datasets)

## 🚀 Installation & Setup

### 1. Clone or Download the Repository

```bash
cd Sequential-Pattern-Mining-with-Interactive-Visualization-Dashboard
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🎮 Running the Application

### Step 1: Start the Backend API

Open a terminal and run:

```bash
python backend/main.py
```

The API will start at `http://localhost:8000`

You can verify it's running by visiting: `http://localhost:8000` in your browser.

### Step 2: Start the Frontend

Open a **new terminal** (keep the backend running) and run:

```bash
streamlit run frontend/app.py
```

The application will automatically open in your browser at `http://localhost:8501`

## 📖 How to Use

### 1. Upload Dataset

- Click "Choose a CSV file" or drag-and-drop your dataset
- Supported format: CSV with columns for ID, Item, and optionally Timestamp
- Click "Upload and Validate"

**Dataset Format Example:**

```csv
UserID,Product,Timestamp
1,A,2023-01-01 10:00:00
1,B,2023-01-01 10:15:00
1,C,2023-01-01 10:30:00
2,A,2023-01-01 11:00:00
2,C,2023-01-01 11:20:00
```

### 2. Configure Data Mapping

- Select your **Sequence ID** column (e.g., UserID, SessionID)
- Select your **Item/Event** column (e.g., Product, Action)
- Optionally select a **Timestamp** column for ordering
- Click "Generate Sequences"

### 3. Set Mining Parameters

- Adjust **Minimum Support** (0.1% to 50%)
  - Lower values find more patterns but take longer
  - Higher values find only very common patterns
- Set **Maximum Pattern Length** (2 to 10 items)
- Click "Start Mining Patterns"

### 4. Explore Results

View results through multiple visualizations:

- **📊 Top Patterns**: Bar chart of most frequent patterns
- **📈 Support Trends**: Line chart showing support by pattern length
- **🔥 Co-occurrence Heatmap**: Item association matrix
- **🕸️ Sequence Flow Network**: Interactive network graph
- **📋 Results Table**: Filterable table of all patterns

### 5. Export Results

- Download patterns as CSV
- Use filters to focus on specific pattern lengths
- Sort by support or length

## 🎨 Visualizations Explained

### Bar Chart - Top Patterns

Shows the most frequent sequential patterns with their support counts. Colors indicate support percentage.

### Line Chart - Support Trends

Displays how average, maximum, and minimum support values change with pattern length. Also shows the distribution of pattern counts by length.

### Heatmap - Item Co-occurrence

A symmetric matrix showing how often pairs of items appear together in sequences. Darker colors indicate stronger associations.

### Network Graph - Sequence Flow

A directed graph where:

- **Nodes** represent items
- **Edges** represent transitions (A → B)
- **Edge thickness** indicates transition frequency

## 🔧 Configuration

### Backend Configuration

Edit `backend/main.py` to change:

- API host and port (default: `0.0.0.0:8000`)
- CORS settings
- Logging level

### Frontend Configuration

Edit `frontend/app.py` to change:

- API URL (default: `http://localhost:8000`)
- Page title and icon
- Theme colors

## 📊 Dataset Requirements

Your CSV file should contain:

1. **Sequence Identifier** (Required)

   - Column identifying different sequences
   - Examples: UserID, SessionID, TransactionID, CustomerID

2. **Item/Event** (Required)

   - Column containing the items or events
   - Examples: Product, Action, Page, Event

3. **Timestamp** (Optional)
   - Column for temporal ordering
   - Can be date, datetime, or numeric
   - If not provided, sequences are ordered as they appear

### Supported Dataset Formats

The application works with **any Kaggle dataset** or custom CSV that follows this structure:

```csv
# E-commerce Example
UserID,Product,Date
1,Laptop,2023-01-01
1,Mouse,2023-01-02
1,Keyboard,2023-01-03

# Web Analytics Example
SessionID,Page,Timestamp
S1,Home,2023-01-01 10:00:00
S1,Products,2023-01-01 10:05:00
S1,Checkout,2023-01-01 10:10:00

# Healthcare Example
PatientID,Treatment,Date
P1,Diagnosis,2023-01-01
P1,Medication,2023-01-02
P1,Follow-up,2023-01-15
```

## 🧪 Testing with Sample Data

A sample dataset is included at `datasets/sample.csv`:

1. Start both backend and frontend
2. Upload `datasets/sample.csv`
3. Select:
   - Sequence ID: `UserID`
   - Item: `Product`
   - Timestamp: `Timestamp`
4. Set minimum support to `0.2` (20%)
5. Click "Start Mining Patterns"

Expected results: ~15-20 patterns including `A → B → C`, `A → C`, `B → C`, etc.

## 🎓 Algorithm: PrefixSpan

This project implements the **PrefixSpan** (Prefix-Projected Sequential Pattern Mining) algorithm.

### Why PrefixSpan?

- ✅ No candidate generation (unlike Apriori-based methods)
- ✅ Efficient memory usage
- ✅ Scales well with large databases
- ✅ Produces complete results

### How It Works

1. **Find frequent items** (1-patterns)
2. **Build projected databases** for each frequent item
3. **Recursively mine patterns** in projected databases
4. **Prune** patterns below minimum support threshold

### Time Complexity

- Best case: O(n × m) where n = sequences, m = avg sequence length
- Worst case: O(n × m × 2^m) for very low support thresholds

## 🐛 Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Install dependencies

```bash
pip install -r requirements.txt
```

### Frontend can't connect to backend

**Error**: "Cannot connect to backend server"

**Solution**:

1. Ensure backend is running (`python backend/main.py`)
2. Check API URL in `frontend/app.py` is `http://localhost:8000`
3. Verify firewall isn't blocking port 8000

### CSV upload fails

**Error**: "Invalid CSV format"

**Solution**:

- Ensure file has `.csv` extension
- Check file has at least 2 columns
- Verify file is not empty
- Try opening in Excel/text editor to check format

### Mining takes too long

**Solution**:

- Increase minimum support threshold
- Reduce maximum pattern length
- Use a smaller dataset for testing

### Visualizations not showing

**Solution**:

- Check browser console for errors (F12)
- Verify mining completed successfully
- Refresh the page
- Clear browser cache

## 📈 Performance Tips

### For Large Datasets (>100,000 sequences)

1. **Increase minimum support**: Start with 0.05 (5%) or higher
2. **Limit pattern length**: Set max length to 5 or less
3. **Pre-filter data**: Remove infrequent items before upload
4. **Use sampling**: Test with a random sample first

### For Faster Results

1. **Use timestamps**: Improves sequence quality
2. **Clean data**: Remove duplicates and nulls beforehand
3. **Optimize support**: Find the sweet spot (usually 0.01-0.1)

## 🔒 Production Deployment

For production use, consider:

### Backend

- Use a production ASGI server (Gunicorn + Uvicorn workers)
- Add authentication and authorization
- Implement rate limiting
- Use a proper database instead of in-memory state
- Add input validation and sanitization
- Enable HTTPS

### Frontend

- Configure specific CORS origins
- Add user authentication
- Implement session management
- Use environment variables for configuration
- Add error tracking (e.g., Sentry)

### Infrastructure

- Deploy backend and frontend separately
- Use Docker containers
- Set up load balancing
- Implement caching (Redis)
- Add monitoring and logging

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Author

**University Final Year Project**

- Subject: Data Mining & Machine Learning
- Topic: Sequential Pattern Mining with Interactive Visualization

## 🙏 Acknowledgments

- **PrefixSpan Algorithm**: Pei et al. (2004)
- **FastAPI**: Modern, fast web framework for Python
- **Streamlit**: Beautiful data app framework
- **Plotly**: Interactive visualization library

## 📞 Support

For issues or questions:

1. Check the troubleshooting section above
2. Review the TODO.md file for known limitations

## 🔮 Future Enhancements

See `TODO.md` for planned features and improvements.

---

**⭐ If you find this project helpful, please star it!**

Built with ❤️ for sequential pattern mining research and education.

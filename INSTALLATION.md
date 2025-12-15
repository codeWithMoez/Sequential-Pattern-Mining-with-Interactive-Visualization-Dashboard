# 🔧 Installation Guide

Complete installation instructions for all platforms and scenarios.

---

## 📋 Prerequisites

### Required

- **Python**: Version 3.9 or higher
- **pip**: Python package manager (usually comes with Python)
- **Internet connection**: For downloading packages

### Verify Python Installation

```bash
# Check Python version
python --version
# or
python3 --version

# Should show: Python 3.9.x or higher
```

```bash
# Check pip installation
pip --version
# or
pip3 --version
```

If Python is not installed, download from: https://www.python.org/downloads/

---

## 💻 Installation by Platform

### Windows

#### Method 1: Simple Setup

1. **Open Command Prompt**

   - Press `Win + R`
   - Type `cmd` and press Enter

2. **Navigate to Project**

   ```cmd
   cd Desktop\Sequential-Pattern-Mining-with-Interactive-Visualization-Dashboard
   ```

3. **Install Dependencies**

   ```cmd
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```cmd
   run.bat
   ```

#### Method 2: PowerShell

1. **Open PowerShell**

   - Press `Win + X`
   - Select "Windows PowerShell"

2. **Navigate and Install**

   ```powershell
   cd Desktop\Sequential-Pattern-Mining-with-Interactive-Visualization-Dashboard
   pip install -r requirements.txt
   ```

3. **Run Backend**

   ```powershell
   python backend\main.py
   ```

4. **Run Frontend** (New PowerShell window)
   ```powershell
   cd Desktop\Sequential-Pattern-Mining-with-Interactive-Visualization-Dashboard
   streamlit run frontend\app.py
   ```

---

### macOS

#### Method 1: Using Terminal

1. **Open Terminal**

   - Press `Cmd + Space`
   - Type "Terminal" and press Enter

2. **Navigate to Project**

   ```bash
   cd ~/Desktop/Sequential-Pattern-Mining-with-Interactive-Visualization-Dashboard
   ```

3. **Install Dependencies**

   ```bash
   pip3 install -r requirements.txt
   ```

4. **Make Script Executable**

   ```bash
   chmod +x run.sh
   ```

5. **Run Application**
   ```bash
   ./run.sh
   ```

#### Method 2: Manual Start

1. **Terminal 1 - Backend**

   ```bash
   cd ~/Desktop/Sequential-Pattern-Mining-with-Interactive-Visualization-Dashboard
   python3 backend/main.py
   ```

2. **Terminal 2 - Frontend**
   ```bash
   cd ~/Desktop/Sequential-Pattern-Mining-with-Interactive-Visualization-Dashboard
   streamlit run frontend/app.py
   ```

---

### Linux (Ubuntu/Debian)

#### Method 1: Using Shell Script

1. **Open Terminal**

   - Press `Ctrl + Alt + T`

2. **Navigate to Project**

   ```bash
   cd ~/Desktop/Sequential-Pattern-Mining-with-Interactive-Visualization-Dashboard
   ```

3. **Install Dependencies**

   ```bash
   pip3 install -r requirements.txt
   ```

4. **Make Script Executable**

   ```bash
   chmod +x run.sh
   ```

5. **Run Application**
   ```bash
   ./run.sh
   ```

#### Method 2: With Virtual Environment

1. **Create Virtual Environment**

   ```bash
   python3 -m venv venv
   ```

2. **Activate Virtual Environment**

   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**

   ```bash
   # Terminal 1
   python backend/main.py

   # Terminal 2 (new terminal, activate venv first)
   streamlit run frontend/app.py
   ```

---

## 🐍 Virtual Environment Setup (Recommended)

Using a virtual environment isolates project dependencies.

### Why Use Virtual Environment?

- ✅ Prevents conflicts with other Python projects
- ✅ Makes dependency management cleaner
- ✅ Easy to recreate exact environment
- ✅ Professional best practice

### Windows

```cmd
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python backend\main.py
```

### macOS/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python backend/main.py
```

### Deactivate Virtual Environment

```bash
deactivate
```

---

## 📦 Manual Dependency Installation

If `requirements.txt` fails, install packages individually:

```bash
# Core backend
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install pydantic==2.5.0
pip install python-multipart==0.0.6

# Data processing
pip install pandas==2.1.3
pip install numpy==1.26.2

# Visualization
pip install plotly==5.18.0
pip install networkx==3.2.1

# Frontend
pip install streamlit==1.29.0
pip install requests==2.31.0

# Utilities
pip install python-dateutil==2.8.2
```

---

## 🔍 Verification Steps

After installation, verify everything works:

### 1. Check Dependencies

```bash
# List installed packages
pip list

# Should see: fastapi, streamlit, pandas, plotly, etc.
```

### 2. Test Backend

```bash
# Start backend
python backend/main.py

# In another terminal, test API
curl http://localhost:8000
# or open http://localhost:8000 in browser

# Should see: {"message":"Sequential Pattern Mining API",...}
```

### 3. Test Frontend

```bash
# Start frontend
streamlit run frontend/app.py

# Browser should open automatically
# If not, manually open: http://localhost:8501
```

### 4. Test Complete Flow

1. Upload `datasets/sample.csv`
2. Select columns: UserID, Product, Timestamp
3. Generate sequences
4. Set support: 0.2
5. Mine patterns
6. View visualizations

Expected: ~15-20 patterns found

---

## 🚨 Troubleshooting Installation

### Problem: Python not found

**Error:** `'python' is not recognized as an internal or external command`

**Solution:**

```bash
# Try python3 instead
python3 --version

# Or add Python to PATH:
# Windows: System Properties > Environment Variables > Path > Add Python installation directory
# Mac/Linux: Add to ~/.bashrc or ~/.zshrc:
export PATH="/usr/local/bin/python3:$PATH"
```

---

### Problem: pip not found

**Error:** `'pip' is not recognized`

**Solution:**

```bash
# Windows
python -m pip install --upgrade pip

# Mac/Linux
python3 -m pip install --upgrade pip
```

---

### Problem: Permission denied

**Error:** `PermissionError` or `Access denied`

**Solution:**

```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use sudo (Linux/Mac only)
sudo pip3 install -r requirements.txt
```

---

### Problem: SSL Certificate error

**Error:** `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution:**

```bash
# Temporary workaround (not recommended for production)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

---

### Problem: Package conflicts

**Error:** `ERROR: pip's dependency resolver does not currently take into account all the packages that are installed`

**Solution:**

```bash
# Use a fresh virtual environment
python -m venv fresh_venv
source fresh_venv/bin/activate  # or fresh_venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

### Problem: Slow installation

**Solution:**

```bash
# Use a faster mirror (example: Tsinghua mirror for China)
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# Or increase timeout
pip install --timeout=1000 -r requirements.txt
```

---

### Problem: Port already in use

**Error:** `Address already in use: 8000` or `8501`

**Solution:**

```bash
# Find and kill process using the port
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
lsof -ti:8501 | xargs kill -9

# Or change ports in code:
# backend/main.py: uvicorn.run(app, host="0.0.0.0", port=8001)
# frontend/app.py: API_URL = "http://localhost:8001"
```

---

### Problem: Module import errors

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**

```bash
# Ensure you're in the correct directory
cd Sequential-Pattern-Mining-with-Interactive-Visualization-Dashboard

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip show fastapi
```

---

## 🎓 University/Lab Computer Setup

If you're using a shared computer without admin rights:

```bash
# Install to user directory
pip install --user -r requirements.txt

# Run with full path
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
python -m streamlit run frontend/app.py
```

---

## 🐳 Docker Installation (Advanced)

For containerized deployment:

### Create Dockerfile (Backend)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ ./backend/
CMD ["python", "backend/main.py"]
```

### Create Dockerfile (Frontend)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY frontend/ ./frontend/
CMD ["streamlit", "run", "frontend/app.py"]
```

### Docker Compose

```yaml
version: "3.8"
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend
```

### Run with Docker

```bash
docker-compose up
```

---

## ✅ Post-Installation Checklist

- [ ] Python 3.9+ installed and verified
- [ ] pip working correctly
- [ ] All dependencies installed (check with `pip list`)
- [ ] Backend starts without errors
- [ ] Frontend opens in browser
- [ ] Can access both http://localhost:8000 and http://localhost:8501
- [ ] Sample data upload works
- [ ] Mining completes successfully
- [ ] Visualizations display correctly

---

## 📞 Still Having Issues?

1. **Check Python version**: Must be 3.9 or higher
2. **Update pip**: `pip install --upgrade pip`
3. **Try virtual environment**: Isolates dependencies
4. **Check firewall**: Ensure ports 8000 and 8501 aren't blocked
5. **Restart computer**: Sometimes helps with PATH issues
6. **Read error messages**: They usually indicate the problem
7. **Check documentation**: README.md has more troubleshooting

---

## 🎯 Quick Commands Reference

```bash
# Install
pip install -r requirements.txt

# Run (Manual)
python backend/main.py
streamlit run frontend/app.py

# Run (Automatic)
./run.sh         # Mac/Linux
run.bat          # Windows

# Virtual Environment
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows

# Check Installation
python --version
pip list
pip show fastapi streamlit
```

---

**Installation support completed! You're ready to run the application.** 🚀

If you've completed all steps successfully, proceed to QUICKSTART.md for usage instructions.

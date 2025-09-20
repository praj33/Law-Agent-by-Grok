# Legal Agent - Quick Start Guide

## 🚀 Super Simple Setup

### 1. Install Dependencies (First Time Only)
```bash
python run.py --install
```

### 2. Run the Agent
```bash
python run.py
```

That's it! The interactive CLI will start and you can ask legal questions.

## 📋 Available Options

| Command | Description |
|---------|-------------|
| `python run.py` | Interactive CLI |
| `python run.py --web` | **🌐 Web Interface** at http://localhost:5000 (RECOMMENDED) |
| `python run.py --api` | API server at http://localhost:8000 |
| `python run.py --test` | Run tests |
| `python run.py --install` | Install dependencies |

## 🌐 Web Interface (Recommended)

The web interface provides a modern, user-friendly experience:

```bash
python run.py --web
```

**Features:**
- 🎨 Beautiful, responsive design
- 📱 Mobile-friendly interface  
- 📊 Real-time confidence meters
- 📜 Constitutional articles display
- 🔍 Example queries to get started
- �� Query history and statistics
- 👍 Feedback system for continuous improvement

**Access:** Open http://localhost:5000 in your browser

## 💡 Example Queries

Try these in the CLI:
- "Employee discloses all company secrets to another company"
- "My landlord is not returning my security deposit"
- "My phone is being hacked by someone"
- "I want to divorce my spouse"
- "I was in a car accident"

## 🎯 Features

✅ **10+ Legal Domains** - Corporate law, tenant rights, family law, etc.  
✅ **Constitutional Analysis** - Relevant constitutional articles with confidence  
✅ **ML Classification** - Smart query understanding  
✅ **Legal Framework Integration** - Contract Act, IT Act, IPC  
✅ **Step-by-step Guidance** - Clear process explanations  
✅ **Real-time Processing** - Fast responses  

## 🔧 What Changed

**REMOVED:** All those confusing `.bat` files  
**ADDED:** One simple `run.py` script that does everything  

**Before:** 6+ batch files, complex menus, confusing options  
**After:** One command: `python run.py`

## 🆘 Troubleshooting

**Problem:** `python run.py` doesn't work  
**Solution:** Make sure you're in the project directory and Python is installed

**Problem:** Missing dependencies  
**Solution:** Run `python run.py --install`

**Problem:** Want web interface  
**Solution:** Run `python run.py --web`

---

**That's it! No more batch file confusion. Just run `python run.py` and start asking legal questions.**
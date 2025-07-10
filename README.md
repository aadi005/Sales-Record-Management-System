# Sales Record Management System

A Python-based system for managing, extracting, and querying retail sales records from PDFs and structured CSV files.  
This was a **custom software designed specifically according to the company's requirements**.

---

## Features

- Parse sales data directly from **PDF invoices**
- Extracts and updates structured CSVs by item and party
- Tracks processed invoices with a log system
- GUI to search by **item name** and **party name**
- Display results in a Tkinter-based fullscreen table
- Easy plug-in for business workflows

---

## Tech Stack

- Python 3.9+
- PyPDF2
- tkinter / ttkthemes
- CSV / File I/O

---

## Directory Structure

```
sales-record-management-system/
├── bills/                   # Input PDFs
├── ITEMS/                   # Auto-generated CSVs (per item)
├── logs/
│   └── done.txt             # Tracks parsed PDFs
├── parsers/
│   ├── __init__.py
│   └── parse.py             # PDF parsing & CSV update logic
├── scripts/
│   ├── install_dependencies.py
│   ├── main.py              # GUI search interface
│   └── requirements.txt
├── README.md
└── .gitignore
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone git@github.com:aadi005/sales-record-management-system.git
cd sales-record-management-system
```

### 2. Install dependencies

```bash
python scripts/install_dependencies.py
```

### 3. Add your input PDF invoices to `/bills`

> Files already processed are tracked in `logs/done.txt`. You can delete or edit this file to reprocess PDFs.

### 4. Run the PDF parser

```bash
python parsers/parse.py
```

### 5. Launch the GUI to search records

```bash
python scripts/main.py
```

---

## Security & Sample Data Notice

This tool was originally developed as part of a **freelance project** for a private company.  
As such, I am **not permitted to share actual sample data or invoice files**, due to **security and confidentiality agreements**.

This was a **custom software designed specifically according to the company's requirements**.

However, the code is modular and adaptable for any business that requires sales record processing and querying.

---

## .gitignore

```
__pycache__/
*.pyc
*.db
.env
.idea/
.vscode/
```

---

## Author

## **Aaditya Goel**

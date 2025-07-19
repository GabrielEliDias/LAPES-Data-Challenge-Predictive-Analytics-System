# LAPES Data Challenge – Predictive Analytics System

This repository contains the complete end-to-end solution developed for the **LAPES Predictive Data Challenge**. The objective of this project is to extract real business value from raw data through advanced data processing, machine learning, and deep learning models.

---

## Key Features

- Automated ELT pipeline using Docker and CI/CD (GitHub Actions)
- Medallion Data Lake Architecture (Bronze → Silver → Gold → Diamond)
- Exploratory Data Analysis (EDA) and statistical insights
- Interactive dashboards built with Plotly and Streamlit
- Supervised and unsupervised machine learning models
- Deep learning models implemented with PyTorch and/or Keras
- Automated PDF/HTML reports with visual storytelling
- Fully documented and reproducible environment

---

## Dataset Used

**[Credit Card Fraud Detection – Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)**

### Why this dataset?

- High complexity and real-world relevance
- Applicable to fraud detection in financial and e-commerce sectors
- Enables exploration of imbalanced classification problems
- Supports advanced ML/DL modeling and visualization
- Ideal for developing anomaly detection techniques and dashboards

---

## Tech Stack

| Category           | Tools & Libraries                               |
|--------------------|-------------------------------------------------|
| Language           | Python 3.11+                                    |
| Data Processing    | Pandas, Polars                                  |
| Visualization      | Matplotlib, Seaborn, Plotly                     |
| Machine Learning   | Scikit-learn                                    |
| Deep Learning      | PyTorch, Keras                                  |
| Dashboards         | Streamlit                                       |
| Data Storage       | PostgreSQL                                      |
| Automation         | Docker, GitHub Actions                          |
| Deployment         | FastAPI (optional), Docker Compose              |
| Big Data (optional)| Spark, Dask, Kafka, Hadoop Ecosystem            |

---

 ## 📁 Project Structure
```
├── data/ # Raw and processed data (Bronze → Silver → Gold)
├── notebooks/ # Jupyter notebooks for EDA, ML, and DL
├── src/ # Source code for ELT, preprocessing, and modeling
├── sql/
│ ├── DDL/ # Database schema definitions
│ └── DML/ # Data manipulation scripts
├── app/ # Streamlit dashboard application
├── requirements.txt # List of project dependencies
└── README.md # Project documentation (you are here)
```

## Pipeline Overview

### 1. Data Ingestion and ELT
- Automated pipeline using Docker and GitHub Actions
- Raw data stored in Bronze, transformations handled via SQL triggers
- Access policies applied at each layer

### 2. Exploratory Data Analysis (EDA)
- Descriptive statistics, correlation matrices, missing value analysis
- Anomaly detection and data profiling

### 3. Machine Learning
- Supervised learning: logistic regression, random forests, XGBoost
- Cross-validation and metric tracking (accuracy, recall, F1-score, ROC-AUC)

### 4. Deep Learning
- Neural networks for fraud detection (imbalanced classification)
- Training with class balancing techniques (e.g., SMOTE)
- Model evaluation with robust metrics

### 5. Visualization and Reporting
- Static plots with matplotlib/seaborn
- Interactive dashboards with Streamlit and Plotly

---

## Reproducibility & Setup

### Installation

Clone the repository and install dependencies in a virtual environment:

```bash
git clone https://github.com/your-username/lapes-predictive-analytics.git
cd lapes-predictive-analytics

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt


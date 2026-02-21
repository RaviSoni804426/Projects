# Professional Data Science & Generative AI Portfolio

Welcome to my Data Science and Generative AI portfolio. This workspace is organized to showcase end-to-end projects, from SQL data extraction and Exploratory Data Analysis (EDA) to Deep Learning and Generative AI implementations.

## 📁 Project Structure

```text
Projects/
├── data/               # Raw and processed datasets
├── notebooks/          # Jupyter notebooks sorted by project type
├── sql/               # SQL scripts, schemas, and queries
├── src/               # Production-grade source code
├── projects/          # Dedicated folders for individual projects
├── models/             # Saved model weights and binaries
├── reports/            # Analysis and project reports
├── dashboards/         # Visualization dashboard files (PowerBI/Tableau)
├── configs/            # Configuration files
└── tests/              # Unit and integration tests
```

## 🚀 Getting Started

### 1. Environment Setup (Windows)

I have provided a `setup_env.bat` script to automate the environment creation.

1. **Run the setup script:**
   ```bash
   setup_env.bat
   ```
   *This will create a `venv`, upgrade pip, and install all dependencies.*

2. **Manual Activation:**
   ```bash
   venv\Scripts\activate
   ```

### 2. Installing Dependencies
If you prefer manual installation:
```bash
pip install -r requirements.txt
```

## 📖 How to Run

### Jupyter Notebooks
To explore the analysis and models:
```bash
jupyter notebook
```
Navigate to the `notebooks/` folder.

### ML Models
Pre-trained models are stored in `models/`. To run inference scripts:
```bash
python projects/03-ml-project/predict.py
```

### Streamlit Application
Interactive dashboards:
```bash
streamlit run src/visualization/app.py
```

### FastAPI Backend
To serve models via API:
```bash
uvicorn src.main:app --reload
```

### SQL Projects
SQL scripts and schema definitions are located in the `sql/` directory. You can execute them using your preferred SQL client or via the `sqlalchemy` scripts in `src/data/`.

## 🛠️ Tech Stack
- **Core DS:** Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn
- **Deep Learning:** PyTorch, TensorFlow
- **Generative AI:** Transformers (HuggingFace), OpenAI, LangChain
- **SQL:** SQLite, MySQL, SQLAlchemy
- **Web App:** Streamlit, FastAPI

## 📝 Author
**Ravi Soni**
- [GitHub](https://github.com/RaviSoni804426)
- [Project Repository](https://github.com/RaviSoni804426/Projects)

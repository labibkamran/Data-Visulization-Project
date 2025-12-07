# How to Use This Project - Quick Guide

## 🎯 I want to... (Choose Your Path)

### 📖 Understand what this project is about
**→ Read:** [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md) (5 min read)
- Quick overview of the project
- What data is available
- What questions it can answer

**→ Then read:** [`README.md`](README.md) (15 min read)
- Detailed project description
- Full context on ASER surveys
- Comprehensive information

### 🔍 Look up what a specific variable means
**→ Use:** [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md)
- Search for your variable name (Ctrl+F / Cmd+F)
- Find all 184 variables explained
- Understand codes and categories

**Examples:**
- What does `reading_level` mean? → See Child Dataset section
- What is `infra_drinking_water`? → See School Infrastructure section
- How are disabilities tracked? → See Disability Details section

### 💻 Start analyzing the data
**→ Follow:** [`ANALYSIS_GUIDE.md`](ANALYSIS_GUIDE.md)
- Copy-paste ready Python code
- 10+ example analyses
- Visualization templates

**Quick start code:**
```python
import pandas as pd

# Load the cleaned data
school_df = pd.read_csv('cleaned_excel/aser_school_cleaned.csv')
child_df = pd.read_csv('cleaned_excel/aser_child_cleaned.csv')

# Start exploring!
print(school_df.head())
print(child_df.head())
```

### 🔧 Understand how data was processed
**→ Check:** [`DOCUMENTATION.md`](DOCUMENTATION.md)
- Data cleaning workflow
- Technical processing steps
- Variable renaming methodology

**→ And:** [`renaming.ipynb`](renaming.ipynb)
- Actual code used for processing
- Mapping dictionaries
- Transformation logic

### 🎨 Create visualizations
**→ Use examples from:** [`ANALYSIS_GUIDE.md`](ANALYSIS_GUIDE.md)
- Section 1-10 have ready-to-use visualization code
- Modify colors, labels, and styling to your needs
- Export as PNG/PDF for presentations

**Popular visualizations:**
- Bar charts: Facility coverage, teacher qualifications
- Pie charts: Schooling status, urban vs rural
- Histograms: Learning level distributions
- Maps: Geographic comparisons (need additional packages)

### 📊 Answer specific questions

#### "How many children are out of school?"
```python
status_counts = child_df['schooling_status'].value_counts()
dropped_out = (child_df['schooling_status'] == 2).sum()
never_enrolled = (child_df['schooling_status'] == 3).sum()
out_of_school_pct = (dropped_out + never_enrolled) / len(child_df) * 100
print(f"Out of school: {out_of_school_pct:.1f}%")
```

#### "Do schools have basic toilets?"
```python
with_toilets = (school_df['infra_functional_toilets'] == 1).sum()
total_schools = len(school_df)
pct = with_toilets / total_schools * 100
print(f"Schools with functional toilets: {pct:.1f}%")
```

#### "What's the average reading level?"
```python
avg_reading = child_df['reading_level'].mean()
print(f"Average reading level: {avg_reading:.2f}")
# Levels: 0=Nothing, 1=Letters, 2=Words, 3=Sentences, 4=Story
```

#### "Compare government vs private schools"
```python
comparison = school_df.groupby('school_type').agg({
    'enrollment_total': 'mean',
    'teachers_total': 'mean',
    'infra_library_available': 'mean'
})
print(comparison)
```

### 📈 Do advanced analysis

**Correlation analysis:**
```python
# Does library availability affect reading levels?
merged = child_df.merge(school_df[['village_code', 'infra_library_available']], 
                        on='village_code', how='left')
correlation = merged[['reading_level', 'infra_library_available']].corr()
```

**Geographic analysis:**
```python
# Learning outcomes by province
by_province = child_df.groupby('province').agg({
    'reading_level': 'mean',
    'arithmetic_level': 'mean',
    'child_age': 'mean'
})
```

**Regression modeling:**
```python
from sklearn.linear_model import LinearRegression
# Predict learning outcomes based on school features
X = school_df[['teachers_total', 'infra_library_available', 'enrollment_total']]
y = child_df['reading_level']
# ... continue with model training
```

### 📝 Write a report or paper

**Structure suggestion:**
1. **Introduction** - Use context from README.md
2. **Data & Methods** - Reference DOCUMENTATION.md
3. **Results** - Generate using ANALYSIS_GUIDE.md code
4. **Discussion** - Interpret findings in context
5. **References** - Cite ASER Pakistan

**Key citations to include:**
- ASER Pakistan 2023 Survey
- This dataset and documentation
- Any additional sources used

### 🎓 Use for learning/teaching

**For students:**
- Practice data manipulation with real-world data
- Learn visualization techniques
- Understand education policy issues
- Complete a full data science project

**For instructors:**
- Rich dataset with multiple analysis possibilities
- Well-documented with clear structure
- Socially relevant topic
- Can support various assignment types

**Assignment ideas:**
1. Calculate and visualize basic statistics
2. Compare different groups (gender, urban/rural)
3. Create an interactive dashboard
4. Write a policy brief based on findings
5. Identify and explain patterns in the data

## 📂 File Navigation Map

```
Project Root/
│
├── Quick Start Documents
│   ├── HOW_TO_USE.md          ← You are here
│   ├── PROJECT_SUMMARY.md     ← Overview (read first!)
│   └── README.md              ← Complete guide
│
├── Reference Documents
│   ├── DATA_DICTIONARY.md     ← Variable definitions
│   ├── ANALYSIS_GUIDE.md      ← Code examples
│   └── DOCUMENTATION.md       ← Technical details
│
├── Code & Notebooks
│   ├── renaming.ipynb         ← Data processing code
│   └── exploratory-data-analysis-1.ipynb  ← (empty, for your analysis)
│
├── Data Files
│   ├── ASER_RAW_excel/        ← Original data
│   │   ├── ITAASER2023School (1).xlsx
│   │   ├── ITAASER2023Child.xlsx
│   │   └── coding-manual-2023 copy.pdf
│   │
│   ├── cleaned_excel/         ← Use these for analysis! ⭐
│   │   ├── aser_school_cleaned.csv
│   │   └── aser_child_cleaned.csv
│   │
│   └── NON_ASER_EXCEL_SHEETS/ ← Additional datasets
│       ├── household.csv
│       ├── Annual-School-Census-2023-24.csv
│       └── [other files]
```

## 🚦 Recommended Learning Path

### Beginner Level
1. ✅ Read PROJECT_SUMMARY.md
2. ✅ Browse DATA_DICTIONARY.md to see what's available
3. ✅ Copy basic code from ANALYSIS_GUIDE.md
4. ✅ Load data and create simple charts
5. ✅ Calculate basic statistics (means, counts)

### Intermediate Level
1. ✅ Read full README.md
2. ✅ Run multiple analyses from ANALYSIS_GUIDE.md
3. ✅ Combine school and child datasets
4. ✅ Create custom visualizations
5. ✅ Compare different groups/regions

### Advanced Level
1. ✅ Study DOCUMENTATION.md for processing details
2. ✅ Build statistical models
3. ✅ Create interactive dashboards
4. ✅ Perform geographic analysis
5. ✅ Write research paper or policy brief

## 🛠️ Setup Requirements

### Minimum Requirements
```bash
# Install Python 3.7+
# Install required packages:
pip install pandas numpy jupyter

# For visualization:
pip install matplotlib seaborn

# For Excel files (if needed):
pip install openpyxl
```

### Recommended Setup
```bash
# Create virtual environment
python -m venv aser_env
source aser_env/bin/activate  # On Windows: aser_env\Scripts\activate

# Install all packages
pip install pandas numpy matplotlib seaborn jupyter openpyxl plotly

# Start Jupyter
jupyter notebook
```

### No Installation Option
- Use Google Colab (upload CSV files)
- Use Kaggle Notebooks
- Use any online Python environment

## 💡 Tips for Success

### Data Analysis Tips
1. **Start small** - Analyze one province or district first
2. **Visualize early** - Charts help understand patterns
3. **Check data quality** - Look for missing values and outliers
4. **Compare groups** - Government vs private, urban vs rural, etc.
5. **Tell a story** - Connect findings to real-world impact

### Common Pitfalls to Avoid
❌ Not handling missing values  
✅ Use `.dropna()` or `.fillna()` appropriately

❌ Treating categorical codes as numbers  
✅ Map codes to meaningful labels first

❌ Ignoring data documentation  
✅ Always check DATA_DICTIONARY.md for variable meanings

❌ Overwhelming yourself with all data at once  
✅ Start with subset of variables/rows

❌ Forgetting to cite sources  
✅ Always credit ASER Pakistan

## 🔗 Quick Links

| I want to... | Go to |
|--------------|-------|
| Get quick overview | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| Understand project fully | [README.md](README.md) |
| Look up a variable | [DATA_DICTIONARY.md](DATA_DICTIONARY.md) |
| Get analysis code | [ANALYSIS_GUIDE.md](ANALYSIS_GUIDE.md) |
| See technical details | [DOCUMENTATION.md](DOCUMENTATION.md) |
| Access clean data | `cleaned_excel/` folder |
| See raw data | `ASER_RAW_excel/` folder |

## ❓ Frequently Asked Questions

**Q: Which file should I read first?**  
A: Start with PROJECT_SUMMARY.md (5 min read), then README.md for details.

**Q: Which data files should I use for analysis?**  
A: Use the CSV files in `cleaned_excel/` folder - they're ready to use!

**Q: How do I know what a variable means?**  
A: Search for it in DATA_DICTIONARY.md using Ctrl+F / Cmd+F.

**Q: Can I see example code?**  
A: Yes! ANALYSIS_GUIDE.md has 10+ complete examples you can copy.

**Q: What if I find an error?**  
A: Double-check against the coding manual in ASER_RAW_excel/ folder.

**Q: Can I use this for my thesis/project?**  
A: Yes! Just cite ASER Pakistan 2023 as your data source.

**Q: How do I link school and child data?**  
A: Use the `village_code` column present in both datasets.

**Q: What software do I need?**  
A: Python 3.7+ with pandas. See Setup Requirements above.

**Q: Is the data already cleaned?**  
A: Yes! Files in `cleaned_excel/` are ready to use.

**Q: Where can I learn more about ASER?**  
A: Visit www.aserpakistan.org or read the coding manual in the project.

## 🎉 Ready to Start!

**Three ways to begin right now:**

### Option 1: Quick Explorer (5 minutes)
```python
import pandas as pd
df = pd.read_csv('cleaned_excel/aser_child_cleaned.csv')
print(df.describe())
print(df['reading_level'].value_counts())
```

### Option 2: Visual Analysis (15 minutes)
Open ANALYSIS_GUIDE.md → Pick an example → Copy code → Run → Modify

### Option 3: Deep Dive (1+ hour)
Read README.md → Study DATA_DICTIONARY.md → Create custom analysis

---

**Need help?** Refer to the relevant documentation file above!  
**Found this useful?** Share it with others interested in education data!  

**Happy Analyzing! 📊✨**

# ASER Pakistan 2023 - Data Visualization Project

## Project Overview

This project analyzes educational data from Pakistan, focusing on the **Annual Status of Education Report (ASER) 2023**. ASER is a citizen-led household-based assessment that provides crucial insights into children's schooling status and basic learning levels across Pakistan.

The project performs data cleaning, transformation, and preparation for visualization and analysis of educational outcomes in Pakistan.

## What is ASER?

ASER (Annual Status of Education Report) is Pakistan's largest citizen-led survey that:
- Assesses children's enrollment status and basic learning levels
- Covers rural and urban areas across all provinces
- Tests children aged 5-16 in reading (Urdu/Pashto/Sindhi) and arithmetic
- Evaluates school infrastructure and facilities
- Provides district-level data for evidence-based policy making

## Data Sources

### Primary Datasets (ASER 2023)

1. **ASER School Dataset** (`ITAASER2023School.xlsx`)
   - **Records**: ~6,000 schools
   - **Variables**: 137 columns after cleaning
   - **Coverage**: Schools surveyed across Pakistan including AJK
   - **Information includes**:
     - School infrastructure (classrooms, toilets, drinking water, electricity)
     - Teacher information (qualifications, training, attendance)
     - Enrollment data (total and by gender)
     - Disability inclusion facilities
     - School Management Committee (SMC) activities
     - Learning resources availability

2. **ASER Child Dataset** (`ITAASER2023Child.xlsx`)
   - **Records**: ~214,000 children
   - **Variables**: 47 columns after cleaning
   - **Age Range**: 5-16 years
   - **Information includes**:
     - Demographic data (age, gender, location)
     - Schooling status (enrolled, dropped out, never enrolled)
     - Learning assessments (reading levels, arithmetic, English)
     - Health and vaccination records
     - Tuition and scholarship information

### Supporting Datasets

Located in `NON_ASER_EXCEL_SHEETS/`:

1. **Annual-School-Census-2023-24.csv** - Official government school census data
2. **household.csv** - Household-level demographic data (~10MB)
3. **key-indicators-of-education-in-pakistan.csv** - National education indicators
4. **number-of-govt-middle-schools-non-functional-2021-numbers-kpk-pakistan.csv** - Non-functional middle schools in KPK
5. **number-of-govt-primary-schools-non-functional-2021-numbers-kpk-pakistan.csv** - Non-functional primary schools in KPK

## Project Structure

```
Data-Visulization-Project/
│
├── ASER_RAW_excel/              # Original raw data files
│   ├── ITAASER2023Child.xlsx    # Raw child assessment data
│   ├── ITAASER2023School (1).xlsx  # Raw school survey data
│   └── coding-manual-2023 copy.pdf  # ASER coding manual
│
├── NON_ASER_EXCEL_SHEETS/       # Additional educational data
│   ├── Annual-School-Census-2023-24.csv
│   ├── household.csv
│   └── [other supporting files]
│
├── cleaned_excel/               # Processed and cleaned data
│   ├── aser_school_cleaned.csv  # Cleaned school data with readable column names
│   └── aser_child_cleaned.csv   # Cleaned child data with readable column names
│
├── renaming.ipynb              # Main data processing notebook
├── exploratory-data-analysis-1.ipynb  # EDA notebook (empty/in progress)
├── DOCUMENTATION.md            # Brief project documentation
└── README.md                   # This file
```

## Data Processing Workflow

### Step 1: Column Renaming (`renaming.ipynb`)

The original ASER datasets use cryptic column codes (e.g., "S003a1", "C15", "S004VB1") that are difficult to understand. The notebook creates comprehensive mapping dictionaries to transform these into human-readable names:

**Example transformations:**

**School Data:**
- `SYEAR` → `survey_year`
- `RNAME` → `province`
- `S007E` → `enrollment_total`
- `S004VB1` → `disability_visual_boys_some`
- `S011Ob6` → `infra_drinking_water`

**Child Data:**
- `C03` → `child_age`
- `C04` → `child_gender`
- `C15` → `reading_level`
- `C19` → `arithmetic_level`
- `BasicVaccines` → `vaccination_basic`

### Step 2: Data Cleaning Process

The `renaming.ipynb` notebook performs:

1. **Loading** raw Excel files
2. **Renaming** columns using predefined dictionaries
3. **Exporting** cleaned CSV files for analysis

**Note**: The notebook shows an error during execution because file paths are specific to the original developer's machine. The cleaned output files are already available in the `cleaned_excel/` directory.

## Key Variables and Categories

### School Infrastructure Variables

- **Basic Facilities**: boundary wall, school gate, playground, classrooms
- **Utilities**: electricity, lighting, fans, drinking water sources
- **Sanitation**: clean toilets, functional toilets, handwashing facilities, disability-accessible toilets
- **Learning Resources**: library, science lab, computer lab, internet, multimedia equipment
- **Safety**: security personnel, CCTV cameras

### Classroom Conditions

For both Class 2 and Class 8:
- Multigrade teaching status
- Learning materials availability
- Blackboard condition
- Textbook availability
- Seating arrangements

### Disability Inclusion

The dataset tracks six types of disabilities (Visual, Hearing, Physical, Intellectual, Speech/Communication, Cognitive) with granular data:
- Number of boys/girls affected
- Severity levels (some difficulty, a lot of difficulty, cannot do at all)
- Support facilities (ramps, accessible toilets, assistive devices, trained teachers)

### Teacher Information

- **Qualifications**: Matriculation, Intermediate, Bachelors, Masters, MPhil, PhD
- **Professional Training**: PTC, CT, B.Ed, M.Ed
- **Attendance**: Total teachers vs. present on survey day

### School Management

- **SMC Activity**: Active status, meeting frequency, membership composition
- **Financial Management**: Bank balance
- **Oversight**: Teacher attendance monitoring

### Child Assessment Levels

**Reading Levels** (Progressive):
1. Nothing
2. Letters
3. Words
4. Sentences
5. Story

**Arithmetic Levels** (Progressive):
1. Nothing
2. Number recognition (1-9)
3. Number recognition (10-99)
4. Subtraction
5. Division

**English Assessment**:
- Word reading
- Sentence reading
- Comprehension

## Geographic Coverage

### Provinces Included:
- Punjab
- Sindh
- Khyber Pakhtunkhwa (KPK)
- Balochistan
- Azad Jammu and Kashmir (AJK)

Data is hierarchical:
- **Province** → **District** → **Village** → **School** / **Household**

## Potential Research Questions

This dataset can answer questions like:

1. **Access & Equity**:
   - What percentage of children are out of school?
   - Are there gender disparities in enrollment?
   - How does rural vs. urban enrollment differ?

2. **Learning Outcomes**:
   - What proportion of children can read at grade level?
   - How do learning levels vary by region?
   - What's the correlation between school infrastructure and learning?

3. **Infrastructure**:
   - Which facilities are most lacking in schools?
   - How does infrastructure differ between public and private schools?
   - What percentage of schools have disability-accessible facilities?

4. **Teacher Quality**:
   - What are the qualification levels of teachers?
   - What's the teacher absenteeism rate?
   - How does teacher training correlate with student outcomes?

5. **Inclusion**:
   - How many children with disabilities are enrolled?
   - What support systems exist for children with disabilities?
   - Which types of disabilities are most prevalent?

## Data Quality Notes

### Strengths:
- Large sample size (~6,000 schools, ~214,000 children)
- Comprehensive coverage across Pakistan
- Standardized assessment tools
- Rich infrastructure and facility data
- Detailed disability inclusion metrics

### Limitations:
- Survey-based data (potential reporting bias)
- Point-in-time snapshot (2023 survey year)
- Some missing values (shown as blank or NaN)
- Geographic identifiers may need additional mapping for visualization

## Next Steps for Analysis

1. **Exploratory Data Analysis** (EDA):
   - Generate summary statistics
   - Create frequency distributions
   - Identify patterns and outliers
   - Analyze missing data

2. **Data Visualization**:
   - Geographic maps showing district-level indicators
   - Comparison charts (public vs. private, rural vs. urban)
   - Trend analysis if multi-year data available
   - Correlation heatmaps

3. **Statistical Analysis**:
   - Regression models for learning outcomes
   - Factor analysis for infrastructure quality
   - Cluster analysis for school typologies
   - Gap analysis by demographic groups

4. **Dashboard Creation**:
   - Interactive visualizations
   - Filters by geography, school type, demographics
   - Key performance indicators (KPIs)

## Technical Requirements

To run the analysis notebooks:

```bash
# Required Python packages
pip install pandas numpy openpyxl jupyter

# For visualization (when implemented)
pip install matplotlib seaborn plotly
```

## Data Usage and Citation

If using this data for research or publication, please cite:
- ASER Pakistan 2023 Survey
- Original data source: ASER Pakistan (www.aserpakistan.org)

## References

- **ASER Pakistan**: Official website for Annual Status of Education Report
- **Coding Manual 2023**: Detailed variable definitions and survey methodology
- **Government of Pakistan Education Data**: Ministry of Federal Education and Professional Training

## Contributing

This is an educational project analyzing public education data. Contributions for improved analysis, visualizations, or insights are welcome.

## License

This project uses publicly available educational data from ASER Pakistan. Please refer to ASER Pakistan's terms of use for data usage policies.

---

*Last Updated: 2023*
*Survey Year: 2023*
*Data Processing: Column renaming and cleaning completed*

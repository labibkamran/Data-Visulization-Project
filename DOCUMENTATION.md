# Project Documentation

## Overview
This project processes and prepares ASER (Annual Status of Education Report) Pakistan 2023 data for analysis and visualization.

## Data Processing Steps

### 1. Column Renaming
**Objective**: Transform cryptic column codes into human-readable variable names

**Process**:
- Used ASER 2023 Coding Manual as reference
- Created comprehensive mapping dictionaries for both datasets
- Renamed 137 school variables and 47 child variables
- Output: Clean CSV files with meaningful column names

### 2. Datasets Processed

#### ASER School Dataset
- **Source**: `ASER_RAW_excel/ITAASER2023School (1).xlsx`
- **Output**: `cleaned_excel/aser_school_cleaned.csv`
- **Records**: ~6,000 schools
- **Variables**: 137 columns covering infrastructure, teachers, enrollment, disabilities, facilities

#### ASER Child Dataset
- **Source**: `ASER_RAW_excel/ITAASER2023Child.xlsx`
- **Output**: `cleaned_excel/aser_child_cleaned.csv`
- **Records**: ~214,000 children
- **Variables**: 47 columns covering demographics, schooling, learning assessments, health

## Variable Categories

### School Data Categories:
1. **Basic Information**: Survey year, province, district, village, school type
2. **Infrastructure**: Buildings, classrooms, toilets, water, electricity
3. **Facilities**: Library, computer lab, science lab, internet, sports materials
4. **Teachers**: Qualifications, professional training, attendance
5. **Enrollment**: Total and present students
6. **Disability Support**: Ramps, accessible toilets, trained staff, assistive devices
7. **Disabilities**: Detailed tracking of 6 disability types by gender and severity
8. **School Management**: SMC activities, meetings, financial management

### Child Data Categories:
1. **Demographics**: Age, gender, location (province, district, village)
2. **Schooling Status**: Enrolled, dropped out, never enrolled, reasons
3. **Current Education**: Class, institution type, scholarship, tuition
4. **Reading Assessment**: Levels from nothing to story reading
5. **Arithmetic Assessment**: Levels from number recognition to division
6. **English Assessment**: Word, sentence, and comprehension
7. **General Knowledge**: Question attempts and performance
8. **Health**: Vaccination status, illnesses, allergies

## File Structure
```
ASER_RAW_excel/         - Original survey data files
NON_ASER_EXCEL_SHEETS/  - Supporting datasets (census, household, indicators)
cleaned_excel/          - Processed CSV files with renamed columns
renaming.ipynb          - Main data processing notebook
```

## Technical Notes
- Encoding issues may occur with Excel files; use appropriate encoding parameters
- Missing values represented as blank or NaN
- Some columns have spaces in names after rename (minor formatting issue)
- Geographic codes allow linking datasets at village level 
# ASER Pakistan 2023 - Analysis Guide

This guide provides code examples and analytical approaches for working with the ASER datasets.

## Quick Start

### Loading the Data

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned datasets
school_df = pd.read_csv('cleaned_excel/aser_school_cleaned.csv')
child_df = pd.read_csv('cleaned_excel/aser_child_cleaned.csv')

# Basic inspection
print(f"Schools: {len(school_df)} records")
print(f"Children: {len(child_df)} records")
print(f"\nSchool columns: {school_df.columns.tolist()}")
print(f"\nChild columns: {child_df.columns.tolist()}")
```

## Exploratory Data Analysis Examples

### 1. School Infrastructure Analysis

#### Basic Facilities Coverage

```python
# Calculate percentage of schools with basic facilities
facilities = [
    'infra_boundary_wall', 'infra_drinking_water', 
    'infra_clean_toilets', 'infra_functional_toilets',
    'infra_electricity_functional', 'infra_playground'
]

facility_coverage = {}
for facility in facilities:
    if facility in school_df.columns:
        coverage = (school_df[facility] == 1).sum() / len(school_df) * 100
        facility_coverage[facility] = coverage

# Visualize
plt.figure(figsize=(10, 6))
plt.barh(list(facility_coverage.keys()), list(facility_coverage.values()))
plt.xlabel('Percentage of Schools')
plt.title('Basic Facility Coverage Across Schools')
plt.tight_layout()
plt.show()
```

#### Infrastructure by School Type

```python
# Compare government vs private schools
infrastructure_comparison = school_df.groupby('school_type')[facilities].mean() * 100

infrastructure_comparison.T.plot(kind='bar', figsize=(12, 6))
plt.title('Infrastructure Comparison: Government vs Private Schools')
plt.ylabel('Percentage of Schools')
plt.xlabel('Facility Type')
plt.legend(['Government', 'Private'])
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

### 2. Geographic Analysis

#### Schools by Province

```python
# Count schools by province
schools_by_province = school_df['province'].value_counts()

plt.figure(figsize=(10, 6))
schools_by_province.plot(kind='bar')
plt.title('Number of Schools Surveyed by Province')
plt.xlabel('Province')
plt.ylabel('Number of Schools')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

#### Urban vs Rural Distribution

```python
# Compare urban vs rural
area_comparison = school_df.groupby('area_type').size()
area_labels = {1: 'Rural', 2: 'Urban'}
area_comparison.index = area_comparison.index.map(area_labels)

plt.figure(figsize=(8, 6))
area_comparison.plot(kind='pie', autopct='%1.1f%%')
plt.title('School Distribution: Urban vs Rural')
plt.ylabel('')
plt.show()
```

### 3. Teacher Analysis

#### Teacher Qualifications

```python
# Analyze teacher qualification distribution
qual_columns = [
    'teacher_qualification_matric', 'teacher_qualification_intermediate',
    'teacher_qualification_bachelors', 'teacher_qualification_masters',
    'teacher_qualification_mphil', 'teacher_qualification_phd'
]

total_teachers = school_df['teachers_total'].sum()
qual_distribution = {}

for col in qual_columns:
    if col in school_df.columns:
        qual_distribution[col.replace('teacher_qualification_', '').title()] = \
            school_df[col].sum()

plt.figure(figsize=(10, 6))
plt.bar(qual_distribution.keys(), qual_distribution.values())
plt.title('Teacher Qualification Distribution')
plt.xlabel('Qualification Level')
plt.ylabel('Number of Teachers')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

#### Teacher Attendance Rate

```python
# Calculate average teacher attendance
school_df['teacher_attendance_rate'] = \
    (school_df['teachers_present_today'] / school_df['teachers_total']) * 100

# Remove infinite and NaN values
attendance_clean = school_df['teacher_attendance_rate'].replace([np.inf, -np.inf], np.nan).dropna()

print(f"Average Teacher Attendance: {attendance_clean.mean():.2f}%")
print(f"Median Teacher Attendance: {attendance_clean.median():.2f}%")

plt.figure(figsize=(10, 6))
plt.hist(attendance_clean, bins=20, edgecolor='black')
plt.title('Distribution of Teacher Attendance Rates')
plt.xlabel('Attendance Rate (%)')
plt.ylabel('Number of Schools')
plt.axvline(attendance_clean.mean(), color='red', linestyle='--', label=f'Mean: {attendance_clean.mean():.1f}%')
plt.legend()
plt.tight_layout()
plt.show()
```

### 4. Enrollment Analysis

#### Enrollment by School Type and Gender

```python
# Analyze enrollment patterns
enrollment_summary = school_df.groupby(['school_type', 'gender_type']).agg({
    'enrollment_total': 'sum',
    'enrollment_present_today': 'sum'
}).reset_index()

# Map codes to labels
school_type_map = {1: 'Government', 2: 'Private'}
gender_type_map = {1: 'Boys', 2: 'Girls', 3: 'Mixed'}

enrollment_summary['school_type'] = enrollment_summary['school_type'].map(school_type_map)
enrollment_summary['gender_type'] = enrollment_summary['gender_type'].map(gender_type_map)

print(enrollment_summary)
```

#### Student-Teacher Ratio

```python
# Calculate student-teacher ratio
school_df['student_teacher_ratio'] = \
    school_df['enrollment_total'] / school_df['teachers_total']

# Clean data
str_clean = school_df['student_teacher_ratio'].replace([np.inf, -np.inf], np.nan).dropna()

print(f"Average Student-Teacher Ratio: {str_clean.mean():.2f}")
print(f"Median Student-Teacher Ratio: {str_clean.median():.2f}")

# By school type
str_by_type = school_df.groupby('school_type')['student_teacher_ratio'].mean()
print("\nStudent-Teacher Ratio by School Type:")
print(str_by_type)
```

### 5. Child Learning Outcomes

#### Reading Level Distribution

```python
# Analyze reading levels
reading_levels = {
    0: 'Nothing',
    1: 'Letters',
    2: 'Words',
    3: 'Sentences',
    4: 'Story'
}

reading_distribution = child_df['reading_level'].value_counts().sort_index()
reading_distribution.index = reading_distribution.index.map(reading_levels)

plt.figure(figsize=(10, 6))
reading_distribution.plot(kind='bar')
plt.title('Distribution of Reading Levels Among Children')
plt.xlabel('Reading Level')
plt.ylabel('Number of Children')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

#### Reading Levels by Age

```python
# Reading proficiency by age
reading_by_age = pd.crosstab(
    child_df['child_age'], 
    child_df['reading_level'], 
    normalize='index'
) * 100

reading_by_age.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Reading Level Distribution by Age')
plt.xlabel('Age')
plt.ylabel('Percentage of Children')
plt.legend(title='Reading Level', labels=list(reading_levels.values()))
plt.tight_layout()
plt.show()
```

#### Arithmetic Performance

```python
# Analyze arithmetic levels
arithmetic_levels = {
    0: 'Nothing',
    1: '1-9',
    2: '10-99',
    3: 'Subtraction',
    4: 'Division'
}

arithmetic_distribution = child_df['arithmetic_level'].value_counts().sort_index()
arithmetic_distribution.index = arithmetic_distribution.index.map(arithmetic_levels)

plt.figure(figsize=(10, 6))
arithmetic_distribution.plot(kind='bar')
plt.title('Distribution of Arithmetic Levels Among Children')
plt.xlabel('Arithmetic Level')
plt.ylabel('Number of Children')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### 6. Schooling Status Analysis

#### Out-of-School Children

```python
# Analyze schooling status
schooling_status = {
    1: 'Currently Enrolled',
    2: 'Dropped Out',
    3: 'Never Enrolled'
}

status_distribution = child_df['schooling_status'].value_counts()
status_distribution.index = status_distribution.index.map(schooling_status)

plt.figure(figsize=(10, 6))
status_distribution.plot(kind='pie', autopct='%1.1f%%')
plt.title('Distribution of Schooling Status')
plt.ylabel('')
plt.tight_layout()
plt.show()

# Calculate out-of-school percentage
out_of_school = ((status_distribution.get('Dropped Out', 0) + 
                  status_distribution.get('Never Enrolled', 0)) / 
                 len(child_df)) * 100
print(f"\nPercentage of Out-of-School Children: {out_of_school:.2f}%")
```

#### Gender Gap in Enrollment

```python
# Analyze gender disparities
enrollment_by_gender = child_df.groupby(['child_gender', 'schooling_status']).size().unstack(fill_value=0)

gender_labels = {1: 'Male', 2: 'Female'}
enrollment_by_gender.index = enrollment_by_gender.index.map(gender_labels)
enrollment_by_gender.columns = enrollment_by_gender.columns.map(schooling_status)

enrollment_by_gender_pct = enrollment_by_gender.div(enrollment_by_gender.sum(axis=1), axis=0) * 100

enrollment_by_gender_pct.plot(kind='bar', figsize=(10, 6))
plt.title('Schooling Status by Gender')
plt.xlabel('Gender')
plt.ylabel('Percentage')
plt.xticks(rotation=0)
plt.legend(title='Status')
plt.tight_layout()
plt.show()
```

### 7. Disability Inclusion Analysis

#### Children with Disabilities

```python
# Analyze disability prevalence in schools
disability_any = (school_df['disability_any'] == 1).sum()
total_schools = len(school_df)

print(f"Schools with children with disabilities: {disability_any} ({disability_any/total_schools*100:.1f}%)")

# Analyze support facilities
support_facilities = [
    'facility_ramp_available',
    'facility_accessible_toilet', 
    'facility_special_training_teacher',
    'facility_hearing_assistive_device'
]

support_coverage = {}
for facility in support_facilities:
    if facility in school_df.columns:
        coverage = (school_df[facility] == 1).sum() / len(school_df) * 100
        support_coverage[facility.replace('facility_', '').replace('_', ' ').title()] = coverage

plt.figure(figsize=(10, 6))
plt.barh(list(support_coverage.keys()), list(support_coverage.values()))
plt.xlabel('Percentage of Schools')
plt.title('Availability of Disability Support Facilities')
plt.tight_layout()
plt.show()
```

### 8. Vaccination Coverage

```python
# Analyze vaccination status
vaccination_vars = [
    'vaccination_basic', 'vaccine_polio', 'vaccine_dpt_hepb_hib',
    'vaccine_pneumococcal', 'vaccine_measles', 'vaccine_bcg'
]

vaccination_coverage = {}
for vaccine in vaccination_vars:
    if vaccine in child_df.columns:
        coverage = (child_df[vaccine] == 1).sum() / len(child_df) * 100
        vaccination_coverage[vaccine.replace('vaccine_', '').replace('vaccination_', '').upper()] = coverage

plt.figure(figsize=(10, 6))
plt.bar(vaccination_coverage.keys(), vaccination_coverage.values())
plt.title('Vaccination Coverage Among Children')
plt.xlabel('Vaccine Type')
plt.ylabel('Coverage (%)')
plt.xticks(rotation=45)
plt.axhline(y=90, color='r', linestyle='--', label='90% Target')
plt.legend()
plt.tight_layout()
plt.show()
```

### 9. Linking School and Child Data

#### Analyzing School Impact on Learning

```python
# Merge datasets on village_code
merged_df = child_df.merge(
    school_df[['village_code', 'school_type', 'infra_library_available', 
               'infra_computer_lab_available', 'teachers_total', 'enrollment_total']],
    on='village_code',
    how='left'
)

# Analyze reading levels by school infrastructure
reading_by_library = merged_df.groupby('infra_library_available')['reading_level'].mean()
print("Average Reading Level by Library Availability:")
print(reading_by_library)

# Analyze by school type
reading_by_school_type = merged_df.groupby('school_type')['reading_level'].mean()
print("\nAverage Reading Level by School Type:")
print(reading_by_school_type)
```

### 10. Provincial Comparisons

#### Learning Outcomes by Province

```python
# Compare provinces
province_learning = child_df.groupby('province').agg({
    'reading_level': 'mean',
    'arithmetic_level': 'mean',
    'child_age': 'mean'
}).round(2)

province_learning[['reading_level', 'arithmetic_level']].plot(kind='bar', figsize=(12, 6))
plt.title('Average Learning Levels by Province')
plt.xlabel('Province')
plt.ylabel('Average Level')
plt.legend(['Reading', 'Arithmetic'])
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

## Advanced Analysis Ideas

### 1. Regression Analysis
- Predict reading/arithmetic levels based on school infrastructure
- Analyze factors affecting student-teacher ratio
- Model dropout risk factors

### 2. Clustering Analysis
- Group schools by infrastructure quality
- Identify similar districts by education indicators
- Segment children by learning profiles

### 3. Geographic Visualization
- Create choropleth maps of learning outcomes by district
- Visualize infrastructure gaps geographically
- Map out-of-school children hotspots

### 4. Time Series (if multiple years available)
- Track learning level improvements
- Monitor infrastructure development
- Analyze enrollment trends

### 5. Equity Analysis
- Gender parity indices
- Urban-rural disparities
- Wealth-based inequalities (if wealth data available)

## Data Quality Checks

```python
# Check for missing values
print("Missing Values in School Data:")
print(school_df.isnull().sum()[school_df.isnull().sum() > 0])

print("\nMissing Values in Child Data:")
print(child_df.isnull().sum()[child_df.isnull().sum() > 0])

# Check for duplicates
print(f"\nDuplicate schools: {school_df.duplicated(subset=['school_id']).sum()}")
print(f"Duplicate children: {child_df.duplicated(subset=['child_id']).sum()}")

# Check value ranges
print(f"\nChild age range: {child_df['child_age'].min()} - {child_df['child_age'].max()}")
print(f"Reading level range: {child_df['reading_level'].min()} - {child_df['reading_level'].max()}")
```

## Export Results

```python
# Save analysis results
summary_stats = {
    'total_schools': len(school_df),
    'total_children': len(child_df),
    'avg_enrollment': school_df['enrollment_total'].mean(),
    'avg_reading_level': child_df['reading_level'].mean(),
    'avg_arithmetic_level': child_df['arithmetic_level'].mean(),
    'out_of_school_pct': out_of_school
}

import json
with open('analysis_summary.json', 'w') as f:
    json.dump(summary_stats, f, indent=2)

print("Analysis summary saved to analysis_summary.json")
```

## Tips for Effective Analysis

1. **Always check data types** - Some numeric columns might be stored as strings
2. **Handle missing values appropriately** - Decide whether to drop, fill, or analyze separately
3. **Use appropriate aggregations** - Mean for continuous, count/proportion for categorical
4. **Visualize before modeling** - Understand distributions and relationships first
5. **Consider weights** - If sampling weights are provided, use them for population estimates
6. **Document assumptions** - Keep track of data transformations and decisions
7. **Cross-validate findings** - Compare results with official ASER reports
8. **Consider context** - Educational policies and events in 2023 may affect results

## Resources

- ASER Pakistan Website: www.aserpakistan.org
- ASER Coding Manual: `ASER_RAW_excel/coding-manual-2023 copy.pdf`
- Data Dictionary: `DATA_DICTIONARY.md`
- Project README: `README.md`

## Getting Help

If you encounter issues:
1. Check the DATA_DICTIONARY.md for variable definitions
2. Review the coding manual for question wording
3. Examine the original ASER reports for comparison
4. Verify data types and missing value handling

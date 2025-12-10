#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')

plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['axes.grid'] = True
sns.set_style('whitegrid')


# In[2]:


primary = pd.read_csv(r'non-asher-cleaned\number-of-govt-primary-schools-non-functional-2021-numbers-kpk-pakistan.csv', encoding='latin1')
middle = pd.read_csv(r'non-asher-cleaned\number-of-govt-middle-schools-non-functional-2021-numbers-kpk-pakistan.csv', encoding='latin1')
ind = pd.read_csv(r"non-asher-cleaned\key-indicators-of-education-in-pakistan.csv", encoding='latin1')


# Objective 1: Measure the burden of non-functional schools by level (Primary vs Middle) and gender (Male vs Female) across KPK districts in 2021.

# Primary dataset

# In[3]:


primary.columns


# In[4]:


primary.rename(columns={"ï»¿District": "District"}, inplace=True)


# In[5]:


primary.columns


# In[6]:


# STEP 2.1: Clean primary

# Drop empty District rows and force a proper copy
primary = primary.dropna(subset=['District']).copy()

# Ensure numeric types (SAFE assignment)
for col in ['Male', 'Female', 'Total']:
    primary.loc[:, col] = pd.to_numeric(primary[col], errors='coerce')

# Check if Total == Male + Female (SAFE assignment)
primary.loc[:, 'Total_check'] = primary['Male'] + primary['Female']

mismatch_primary = primary[primary['Total'] != primary['Total_check']]


# In[7]:


# Dervied columns
primary['Level'] = 'Primary'
primary['female_share'] = primary['Female'] / primary['Total']
primary['male_share'] = primary['Male'] / primary['Total']


# middle dataset

# In[8]:


middle.rename(columns={"ï»¿District": "District"}, inplace=True)


# In[9]:


# STEP 2.2: Clean middle

for col in ['Male', 'Female', 'Total']:
    middle[col] = pd.to_numeric(middle[col], errors='coerce')

middle['Total_check'] = middle['Male'] + middle['Female']
mismatch_middle = middle[middle['Total'] != middle['Total_check']]

mismatch_middle


# In[10]:


# Derived columns
middle['Level'] = 'Middle'
middle['female_share'] = middle['Female'] / middle['Total']
middle['male_share'] = middle['Male'] / middle['Total']


# big-picture KPK summary

# In[11]:


# STEP 3.1: Overall KPK summary for primary
print("Primary Schools in KPK - non functional")
primary_totals = primary[['Male', 'Female', 'Total']].sum()
primary_totals


# In[12]:


primary_male_share_kpk = primary_totals['Male'] / primary_totals['Total']
primary_female_share_kpk = primary_totals['Female'] / primary_totals['Total']

primary_male_share_kpk, primary_female_share_kpk


# In[13]:


print("Middle Schools in KPK - non functional")
middle_totals = middle[['Male', 'Female', 'Total']].sum()
middle_totals


# In[14]:


# STEP 3.2: Overall KPK summary for middle

middle_totals = middle[['Male', 'Female', 'Total']].sum()
middle_totals

middle_male_share_kpk = middle_totals['Male'] / middle_totals['Total']
middle_female_share_kpk = middle_totals['Female'] / middle_totals['Total']

middle_male_share_kpk, middle_female_share_kpk


# In[15]:


# STEP 3.3: Combined level-wise summary

summary_levels = pd.DataFrame({
    'Level': ['Primary', 'Middle'],
    'Total_nonfunctional': [primary_totals['Total'], middle_totals['Total']],
    'Male_nonfunctional': [primary_totals['Male'], middle_totals['Male']],
    'Female_nonfunctional': [primary_totals['Female'], middle_totals['Female']],
})

summary_levels['Female_share'] = summary_levels['Female_nonfunctional'] / summary_levels['Total_nonfunctional']
summary_levels['Male_share']   = summary_levels['Male_nonfunctional'] / summary_levels['Total_nonfunctional']

summary_levels


# In[16]:


# Optional: bar chart of total non-functional schools by level

plt.figure()
plt.bar(summary_levels['Level'], summary_levels['Total_nonfunctional'])
plt.title("Total Non-Functional Govt Schools in KPK by Level (2021)")
plt.ylabel("Number of schools")
plt.show()


# District wise burden for primary level

# In[17]:


# STEP 4.1: Descriptive stats (primary)

primary.describe()


# In[18]:


primary_sorted = primary.sort_values('Total', ascending=False)
primary_sorted[['District', 'Male', 'Female', 'Total', 'female_share']].head(10)


# In[19]:


# STEP 4.2: Bar chart of total non-functional primary schools by district

plt.figure(figsize=(12, 6))
plt.bar(primary_sorted['District'], primary_sorted['Total'])
plt.xticks(rotation=75, ha='right')
plt.ylabel("Number of non-functional schools")
plt.title("Non-Functional Govt Primary Schools by District (KPK, 2021)")
plt.tight_layout()
plt.show()


# In[20]:


# STEP 4.3: Stacked bar for gender composition (primary)

primary_sorted = primary.sort_values('Total', ascending=False)

x = np.arange(len(primary_sorted))
width = 0.6

plt.figure(figsize=(12, 6))
plt.bar(x, primary_sorted['Male'], width, label='Male')
plt.bar(x, primary_sorted['Female'], width, bottom=primary_sorted['Male'], label='Female')

plt.xticks(x, primary_sorted['District'], rotation=75, ha='right')
plt.ylabel("Number of non-functional schools")
plt.title("Non-Functional Govt Primary Schools by Gender & District (KPK, 2021)")
plt.legend()
plt.tight_layout()
plt.show()


# In[21]:


# STEP 4.4: Female share by district (primary)

primary_fs = primary.sort_values('female_share', ascending=False)

plt.figure(figsize=(8, 10))

y = np.arange(len(primary_fs))
plt.hlines(y, 0, primary_fs['female_share'])   # horizontal lines
plt.plot(primary_fs['female_share'], y, 'o')   # dots

plt.yticks(y, primary_fs['District'])
plt.axvline(0.5, color='red', linestyle='--', linewidth=1)  # 0.5 reference line

plt.xlabel("Female share of non-functional schools")
plt.title("Female Share of Non-Functional Primary Schools by District (KPK, 2021)")
plt.xlim(0, 1)
plt.tight_layout()
plt.show()


# District wise burden for middle level

# In[22]:


# STEP 5.1: Descriptive stats (middle)

middle.describe()


# In[23]:


# STEP 5.2: Total non-functional middle schools by district

middle_sorted = middle.sort_values('Total', ascending=False)

plt.figure(figsize=(10, 6))
plt.bar(middle_sorted['District'], middle_sorted['Total'], color='steelblue')
plt.xticks(rotation=75, ha='right')
plt.ylabel("Number of non-functional schools")
plt.title("Non-Functional Govt Middle Schools by District (KPK, 2021)")
plt.tight_layout()
plt.show()


# In[24]:


# STEP 5.3: Stacked bar for gender composition (middle)

x = np.arange(len(middle_sorted))
width = 0.6

plt.figure(figsize=(10, 6))
plt.bar(x, middle_sorted['Male'], width, label='Male')
plt.bar(x, middle_sorted['Female'], width, bottom=middle_sorted['Male'], label='Female')

plt.xticks(x, middle_sorted['District'], rotation=75, ha='right')
plt.ylabel("Number of non-functional schools")
plt.title("Non-Functional Govt Middle Schools by Gender & District (KPK, 2021)")
plt.legend()
plt.tight_layout()
plt.show()


# In[25]:


# STEP 5.4: Female share by district (middle)

middle_fs = middle.sort_values('female_share', ascending=False)

plt.figure(figsize=(8, 6))

y = np.arange(len(middle_fs))
plt.hlines(y, 0, middle_fs['female_share'])
plt.plot(middle_fs['female_share'], y, 'o')

plt.yticks(y, middle_fs['District'])
plt.axvline(0.5, color='red', linestyle='--', linewidth=1)

plt.xlabel("Female share of non-functional schools")
plt.title("Female Share of Non-Functional Middle Schools by District (KPK, 2021)")
plt.xlim(0, 1)
plt.tight_layout()
plt.show()


# #### Final Summarised Versions

# In[60]:


import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


# ##### Primary vs Middle Schools 

# In[61]:


import plotly.graph_objects as go

# Step 1: Prepare data
# Assuming primary and middle are already cleaned and have the necessary columns

# Combine primary and middle data into one DataFrame
primary_totals = primary[['District', 'Total', 'Male', 'Female', 'Level']].copy()
middle_totals = middle[['District', 'Total', 'Male', 'Female', 'Level']].copy()

combined = pd.concat([primary_totals, middle_totals])

# Step 2: Create Stacked Bar Chart
fig = go.Figure()

# Add Primary and Middle bars to the figure
fig.add_trace(go.Bar(
    x=combined[combined['Level'] == 'Primary']['District'],
    y=combined[combined['Level'] == 'Primary']['Male'],
    name='Primary - Male',
    marker_color='blue'
))

fig.add_trace(go.Bar(
    x=combined[combined['Level'] == 'Primary']['District'],
    y=combined[combined['Level'] == 'Primary']['Female'],
    name='Primary - Female',
    marker_color='lightblue'
))

fig.add_trace(go.Bar(
    x=combined[combined['Level'] == 'Middle']['District'],
    y=combined[combined['Level'] == 'Middle']['Male'],
    name='Middle - Male',
    marker_color='green'
))

fig.add_trace(go.Bar(
    x=combined[combined['Level'] == 'Middle']['District'],
    y=combined[combined['Level'] == 'Middle']['Female'],
    name='Middle - Female',
    marker_color='lightgreen'
))

# Step 3: Layout and configuration
fig.update_layout(
    title='Non-Functional Schools by Level and Gender',
    xaxis_title='District',
    yaxis_title='Number of Non-Functional Schools',
    barmode='stack',
    xaxis_tickangle=90,
    legend_title='School Level & Gender'
)

fig.show()


# ##### Gender Share across Districts

# In[62]:


# Step 1: Prepare data for gender share
primary['gender_share'] = primary['Female'] / primary['Total']
middle['gender_share'] = middle['Female'] / middle['Total']

# Combine primary and middle data into one DataFrame
combined_gender_share = pd.concat([
    primary[['District', 'gender_share', 'Level']],
    middle[['District', 'gender_share', 'Level']]
])

# Step 2: Create Line Chart
fig = px.line(
    combined_gender_share,
    x="District",
    y="gender_share",
    color="Level",
    title="Gender Share (Female) in Non-Functional Schools by District",
    labels={"gender_share": "Female Share of Non-Functional Schools", "District": "District"},
)

fig.update_traces(mode='lines+markers')
fig.update_layout(
    xaxis_tickangle=45,
    legend_title="School Level"
)

fig.show()


# ##### Combined Summary 

# In[66]:


import plotly.express as px
import pandas as pd

# Step 1: Prepare data for gender breakdown summary
summary = pd.DataFrame({
    'Level': ['Primary - Male', 'Primary - Female', 'Middle - Male', 'Middle - Female'],
    'Nonfunctional': [
        primary_totals['Male'].sum(), primary_totals['Female'].sum(),
        middle_totals['Male'].sum(), middle_totals['Female'].sum()
    ]
})

# Step 2: Create Pie Chart (Donut chart)
fig = px.pie(
    summary,
    values='Nonfunctional',
    names='Level',
    title="Gender Breakdown of Non-Functional Schools by Level",
    hole=0.3  # Create a donut chart
)

# Step 3: Customize the chart
fig.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1, 0.1])  # Optionally pull the slices out for emphasis

# Show the pie chart
fig.show()


# In[64]:


level_gender = summary_levels.melt(
    id_vars='Level',
    value_vars=['Male_nonfunctional','Female_nonfunctional'],
    var_name='Gender',
    value_name='Count'
)

plt.figure()
sns.barplot(data=level_gender, x='Level', y='Count', hue='Gender')
plt.title("Non-Functional Govt Schools in KPK by Level & Gender (2021)")
plt.ylabel("Number of schools")
plt.tight_layout()
plt.show()


# Objective 2: Compare non-functional primary vs middle schools across districts to understand where the education pipeline breaks.

# In[26]:


# STEP 1: Merge primary and middle into a single combined dataframe

combined = pd.concat([primary, middle], ignore_index=True)

combined.head()


# In[27]:


combined.tail()


# In[28]:


# STEP 2: Pivot to make district-level comparison easier

district_summary = combined.pivot_table(
    index='District',
    columns='Level',
    values=['Total', 'Male', 'Female', 'female_share'],
    aggfunc='sum'
)

district_summary


# In[29]:


# Replace NaN with 0 because absence in a category = 0 non-functional schools
district_summary = district_summary.fillna(0)


# In[30]:


district_summary.head()


# In[31]:


# REBUILD district_summary SAFELY

district_summary = combined.pivot_table(
    index='District',
    columns='Level',
    values=['Total', 'Male', 'Female'],
    aggfunc='sum'
)

# Flatten multi-index columns
district_summary.columns = ['_'.join(col) for col in district_summary.columns]

# Fill missing school counts with 0 (meaning "no non-functional schools at this level")
district_summary[['Total_Primary','Total_Middle',
                  'Male_Primary','Male_Middle',
                  'Female_Primary','Female_Middle']] = (
    district_summary[['Total_Primary','Total_Middle',
                      'Male_Primary','Male_Middle',
                      'Female_Primary','Female_Middle']].fillna(0)
)

# RE-CALCULATE GENDER SHARES SAFELY
district_summary['female_share_Primary'] = district_summary['Female_Primary'] / district_summary['Total_Primary']
district_summary['female_share_Middle']  = district_summary['Female_Middle']  / district_summary['Total_Middle']

# Replace division-by-zero with NaN
district_summary = district_summary.replace([np.inf, -np.inf], np.nan)

district_summary = district_summary.reset_index()

district_summary.head()


# In[32]:


# GROUPED BAR: TOTAL NON-FUNCTIONAL PRIMARY VS MIDDLE

df = district_summary.sort_values('Total_Primary', ascending=False)

x = np.arange(len(df))
width = 0.35

plt.figure(figsize=(14,6))
plt.bar(x - width/2, df['Total_Primary'], width, label='Primary')
plt.bar(x + width/2, df['Total_Middle'], width, label='Middle')

plt.xticks(x, df['District'], rotation=75, ha='right')
plt.ylabel("Number of Non-Functional Schools")
plt.title("Primary vs Middle Non-Functional Schools across KPK Districts (2021)")

plt.legend()
plt.tight_layout()
plt.show()


# Interpretation (Paste in Report)
# 
# The grouped bar chart compares primary and middle non-functional schools across all districts.
# Most districts show higher counts of non-functional primary schools, suggesting that infrastructure challenges begin at the foundational level.
# 
# However, several districts such as ___ and ___ demonstrate equally severe or even higher non-functionality at the middle level, indicating a pipeline breakdown as students progress to post-primary grades.

# In[33]:


# SLOPE CHART: PIPELINE COMPARISON

slope_df = pd.melt(
    district_summary,
    id_vars='District',
    value_vars=['Total_Primary','Total_Middle'],
    var_name='Level',
    value_name='Total'
)

# Clean level names
slope_df['Level'] = slope_df['Level'].str.replace('Total_', '')

# Order levels
slope_df['Level'] = pd.Categorical(slope_df['Level'], categories=['Primary','Middle'], ordered=True)

# Sort districts by Primary level
district_order = district_summary.sort_values('Total_Primary', ascending=False)['District']


# In[34]:


top_n = 8   # or 10
top_districts = district_order.head(top_n)

plt.figure(figsize=(8, 6))
colors = plt.cm.tab10(np.linspace(0, 1, len(top_districts)))

for color, district in zip(colors, top_districts):
    d = slope_df[slope_df['District'] == district]
    plt.plot(d['Level'], d['Total'], marker='o',
             color=color, label=district)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
plt.title("Pipeline Analysis (Top districts only)")
plt.ylabel("Number of Non-Functional Schools")
plt.grid(axis='y')
plt.tight_layout()
plt.show()


# Interpretation (Paste in Report)
# 
# The slope chart visualizes the direction and magnitude of non-functional schools as students move from primary to middle levels.
# 
# Districts where the line slopes upward show higher non-functional middle schools, indicating a worsening pipeline.
# 
# Districts where the line slopes downward show issues concentrated at primary level.
# 
# Horizontal lines represent districts with similar burden across both levels.
# 
# This allows easy visual identification of districts where infrastructure problems intensify at the middle level — a critical insight for planning resource allocation.

# In[35]:


# MIDDLE-TO-PRIMARY RATIO

district_summary['ratio_middle_to_primary'] = (
    district_summary['Total_Middle'] / district_summary['Total_Primary']
)

ratio_df = district_summary.sort_values('ratio_middle_to_primary', ascending=False)

plt.figure(figsize=(10, 12))
plt.barh(ratio_df['District'], ratio_df['ratio_middle_to_primary'], color='purple')

plt.xlabel("Middle / Primary Ratio")
plt.title("Ratio of Middle to Primary Non-Functional Schools (KPK, 2021)")

plt.tight_layout()
plt.show()


# Interpretation (Paste in Report)
# 
# The ratio of non-functional middle to primary schools provides a compact measure of pipeline weakness.
# 
# Ratios > 1 indicate districts where middle school infrastructure is worse than primary.
# 
# Ratios near 0 indicate very few middle schools are non-functional compared to primary.
# 
# Districts with the highest ratios represent critical pipeline failure points where access to middle education is structurally compromised.

# In[36]:


# Compute overall female total across both levels
district_summary['Female_Total_All'] = (
    district_summary['Female_Primary'] +
    district_summary['Female_Middle']
)

# Top 6 districts by overall female non-functional schools
top6_female = (district_summary
               .sort_values('Female_Total_All', ascending=False)
               ['District']
               .head(6))

# FEMALE PIPELINE: PRIMARY → MIDDLE
female_df = pd.melt(
    district_summary,
    id_vars='District',
    value_vars=['Female_Primary','Female_Middle'],
    var_name='Level',
    value_name='Female_Total'
)

female_df['Level'] = female_df['Level'].str.replace('Female_', '')
female_df['Level'] = pd.Categorical(female_df['Level'],
                                    categories=['Primary','Middle'],
                                    ordered=True)

plt.figure(figsize=(10, 10))

colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(top6_female)))

for color, district in zip(colors, top6_female):
    d = female_df[female_df['District'] == district]
    plt.plot(
        d['Level'], d['Female_Total'],
        marker='o',
        color=color,
        label=district
    )

# Build a deduplicated legend
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))

plt.legend(
    by_label.values(), by_label.keys(),
    bbox_to_anchor=(1.05, 1),
    loc='upper left',
    fontsize=8
)

plt.title("Female-Specific Pipeline Analysis (Top 6 Districts, Primary → Middle), KPK 2021")
plt.ylabel("Number of Non-Functional Female Schools")
plt.grid(axis='y')
plt.tight_layout()
plt.show()


# Interpretation (Paste in Report)
# 
# The female-only slope chart reveals districts where girls’ education is disproportionately impacted.
# In several districts, female middle schools show sharp increases in non-functionality compared to primary schools, implying a compounding disadvantage as girls progress to higher grades.
# 
# This confirms a gendered breakdown in the educational pipeline, reinforcing the need for targeted infrastructure investments in girls' middle schools.

# In[68]:


# Prepare the slope chart data
slope_df = pd.melt(
    district_summary,
    id_vars='District',
    value_vars=['Total_Primary', 'Total_Middle'],
    var_name='Level',
    value_name='Total'
)

# Clean level names
slope_df['Level'] = slope_df['Level'].str.replace('Total_', '')

# Interactive Slope Chart
fig = go.Figure()

# Loop through top districts
top_districts = slope_df['District'].unique()

for district in top_districts:
    d = slope_df[slope_df['District'] == district]
    fig.add_trace(go.Scatter(
        x=d['Level'],
        y=d['Total'],
        mode='lines+markers',
        name=district
    ))

# Update Layout
fig.update_layout(
    title="Pipeline Comparison (Primary → Middle)",
    xaxis_title="School Level",
    yaxis_title="Number of Non-Functional Schools",
    hovermode="x unified",  # Unified hover across districts
    legend_title="Districts"
)

fig.show()


# In[69]:


fig = go.Figure()

# Bar chart for middle-to-primary ratio
fig.add_trace(go.Bar(
    y=ratio_df['District'],
    x=ratio_df['ratio_middle_to_primary'],
    orientation='h',
    name="Middle / Primary Ratio",
    marker_color='purple'
))

# Update Layout for interactivity
fig.update_layout(
    title="Ratio of Middle to Primary Non-Functional Schools",
    xaxis_title="Middle / Primary Ratio",
    yaxis_title="District",
    hovermode="y unified",  # Hover over each bar to see details for the district
    showlegend=False
)

fig.show()


# In[70]:


# Prepare female pipeline data
female_df = pd.melt(
    district_summary,
    id_vars='District',
    value_vars=['Female_Primary', 'Female_Middle'],
    var_name='Level',
    value_name='Female_Total'
)

female_df['Level'] = female_df['Level'].str.replace('Female_', '')
female_df['Level'] = pd.Categorical(female_df['Level'], categories=['Primary', 'Middle'], ordered=True)

fig = go.Figure()

# Add traces for each district
for district in top6_female:
    d = female_df[female_df['District'] == district]
    fig.add_trace(go.Scatter(
        x=d['Level'],
        y=d['Female_Total'],
        mode='lines+markers',
        name=district
    ))

# Update layout
fig.update_layout(
    title="Female-Specific Pipeline Analysis (Primary → Middle)",
    xaxis_title="School Level",
    yaxis_title="Number of Non-Functional Female Schools",
    hovermode="x unified",  # Unified hover for all districts
    legend_title="Districts"
)

fig.show()


# Objective 3: Classify KPK districts into severity tiers (Low, Medium, High) based on non-functional school burden and explore associated gender and pipeline patterns.

# In[37]:


district_summary['Total_All'] = (
    district_summary['Total_Primary'] + district_summary['Total_Middle']
)

district_summary[['District','Total_Primary','Total_Middle','Total_All']].head()


# In[38]:


district_summary['Severity'] = pd.qcut(
    district_summary['Total_All'],
    q=3,
    labels=['Low', 'Medium', 'High']
)


# In[39]:


district_summary[['District','Total_All','Severity']].sort_values('Total_All', ascending=False)


# INTERPRETATION (paste in report)
# 
# To reduce the continuous variable “total non-functional schools” into a more interpretable form, districts were grouped into three severity tiers using quantile-based classification.
# This data reduction approach allows clearer pattern identification and removes noise caused by small variations in absolute counts.
# 
# High-severity districts exhibit the greatest infrastructure burden.
# 
# Medium-severity districts have moderate but non-trivial infrastructure failure.
# 
# Low-severity districts show minimal non-functional schools.

# In[40]:


import matplotlib.patches as mpatches

df = district_summary.sort_values('Total_All', ascending=False)

color_map = {'High': 'red', 'Medium': 'orange', 'Low': 'green'}

plt.figure(figsize=(14,6))
bars = plt.bar(df['District'],
               df['Total_All'],
               color=df['Severity'].map(color_map))

plt.xticks(rotation=75, ha='right')
plt.ylabel("Total Non-Functional Schools (Primary + Middle)")
plt.title("District-Level Severity Classification of School Non-Functionality (KPK, 2021)")

# --- custom legend ---
legend_handles = [
    mpatches.Patch(color=color_map['High'],   label='High severity'),
    mpatches.Patch(color=color_map['Medium'], label='Medium severity'),
    mpatches.Patch(color=color_map['Low'],    label='Low severity')
]
plt.legend(handles=legend_handles, title='Severity', loc='upper right')

plt.tight_layout()
plt.show()



# Interpretation (paste in report)
# 
# The severity bar chart reveals strong spatial variation in infrastructure failure across districts.
# High-severity districts (red) contribute disproportionately to KPK’s total non-functional schools, indicating critical structural challenges.
# Medium-severity districts (orange) represent areas where intervention may prevent further deterioration.
# Low-severity districts (green) show minimal burden, suggesting relatively stable school infrastructure.

# In[41]:


import matplotlib.patches as mpatches

plt.figure(figsize=(10,6))

color_map = {'High':'red', 'Medium':'orange', 'Low':'green'}

plt.scatter(
    district_summary['Total_All'],
    district_summary['female_share_Primary'],
    c=district_summary['Severity'].map(color_map),
    s=120,
    edgecolors='black'
)

for i, row in district_summary.iterrows():
    plt.text(row['Total_All']+0.3,
             row['female_share_Primary'],
             row['District'],
             fontsize=8)

plt.xlabel("Total Non-Functional Schools (Primary + Middle)")
plt.ylabel("Female Share (Primary Level)")
plt.title("Severity vs Female Share of Non-Functional Schools (Primary)")
plt.grid(True)

# legend for severity
legend_handles = [
    mpatches.Patch(color=color_map['High'],   label='High severity'),
    mpatches.Patch(color=color_map['Medium'], label='Medium severity'),
    mpatches.Patch(color=color_map['Low'],    label='Low severity')
]
plt.legend(handles=legend_handles, title='Severity', loc='lower right')

plt.tight_layout()
plt.show()



# Interpretation for Report
# 
# A clear relationship emerges between severity and gender burden:
# High-severity districts often exhibit elevated female-share values, meaning girls’ schools are disproportionately non-functional in the most infrastructure-stressed regions.
# 
# This suggests that structural constraints in high-severity districts may particularly limit girls' educational access.

# Objective 4: Reshape and explore the “key-indicators-of-education-in-pakistan” dataset to analyze provincial trends (2013–14 vs 2018–19) and gender gaps.

# In[42]:


ind.head()
ind.info()


# In[43]:


ind.columns


# In[44]:


ind.rename(columns={"ï»¿Province /Gender": "Province/Gender"}, inplace=True)


# In[45]:


ind.columns


# In[46]:


ind.head(10)


# changing and reshaping the columns.

# In[47]:


# STEP 1: Define numeric columns exactly as in your DataFrame
numeric_cols = [
    'Male (2018-19',
    'Female (2018-19)',
    'Total (2018-19)',
    'Male (2013-14)',
    'Female(2013-14)',
    'Total (2013-14)'
]

# Check they exist (optional sanity check)
print(ind.columns.tolist())

# Identify rows that are indicator titles (all NaN in numeric columns)
is_header = ind[numeric_cols].isna().all(axis=1)

ind[is_header]


# In[48]:


# STEP 2: Make a working copy and add 'Indicator' column

ind2 = ind.copy()

# Initialize Indicator column as None
ind2['Indicator'] = None

# Set Indicator where rows are headers
ind2.loc[is_header, 'Indicator'] = ind2.loc[is_header, 'Province/Gender']

# Forward-fill Indicator downward
ind2['Indicator'] = ind2['Indicator'].ffill()

ind2.head(10)


# In[49]:


# STEP 3: Keep only rows with at least one numeric value (i.e., data rows)

data_rows = ~is_header         # invert mask: True = data row

ind_clean = ind2[data_rows].copy()

ind_clean.head(10)


# In[50]:


# STEP 4: Rename Province column

ind_clean = ind_clean.rename(columns={'Province/Gender': 'Province'})
ind_clean.head(10)


# In[51]:


# wide to long format 
# Define numeric columns again for safety
numeric_cols = [
    'Male (2018-19',
    'Female (2018-19)',
    'Total (2018-19)',
    'Male (2013-14)',
    'Female(2013-14)',
    'Total (2013-14)'
]

# Melt wide -> long
long_ind = ind_clean.melt(
    id_vars=['Province', 'Indicator'],
    value_vars=numeric_cols,
    var_name='Gender_Year',
    value_name='Value'
)

long_ind.head(12)


# In[52]:


# splitting gender and year into separate columns
import re

# Extract Gender and Year from 'Gender_Year'
long_ind[['Gender', 'Year']] = long_ind['Gender_Year'].str.extract(
    r'^(Male|Female|Total)\s*\(?([\d\-]+)'
)

# Drop the original Gender_Year column
long_ind = long_ind.drop(columns=['Gender_Year'])

# Make Year a string or category
long_ind['Year'] = long_ind['Year'].astype(str)

long_ind.head(12)


# In[53]:


long_ind.tail()


# In[54]:


import matplotlib.pyplot as plt

# Filter for literacy indicator and Total gender
lit_total = long_ind[
    (long_ind['Indicator'].str.contains('LITERACY', case=False)) &
    (long_ind['Gender'] == 'Total')
].copy()

# Plot setup
plt.figure(figsize=(10, 6))

# Loop through each province and plot
for province, grp in lit_total.groupby('Province'):
    if province == 'Pakistan':
        # Highlight Pakistan: use a different color or line style
        plt.plot(grp['Year'], grp['Value'], marker='o', label=province, color='blue', linewidth=3, markersize=8)
    else:
        # Normal plotting for other provinces
        plt.plot(grp['Year'], grp['Value'], marker='o', label=province)

# Title and labels
plt.title("Literacy Rate (Total, 10+ years) by Province, 2013-14 vs 2018-19")
plt.xlabel("Year")
plt.ylabel("Literacy Rate (%)")

# Adjust legend placement to the side
plt.legend(title="Province", loc='center left', bbox_to_anchor=(1, 0.5))   # Legend to the side

# Add grid and layout adjustments
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()


# In[55]:


import seaborn as sns
import matplotlib.pyplot as plt

# STEP 1: Filter the data for the indicator of interest
indicators_of_interest = ['OUT OF SCHOOL CHILDREN AGED (5-16) YEARS']
filtered_data = long_ind[long_ind['Indicator'].isin(indicators_of_interest)]

# STEP 2: Exclude "Total" gender and "Pakistan"
filtered_data = filtered_data[(filtered_data['Gender'] != 'Total') & (filtered_data['Province'] != 'Pakistan')]

# STEP 3: Average over gender (Male and Female) for each province and indicator
# Group by Province, Indicator, and Year, and calculate the average Value for Male and Female
filtered_data_avg = filtered_data.groupby(['Province', 'Indicator', 'Year'])['Value'].mean().reset_index()

# STEP 4: Pivot the data so that we have one row per province and one column per year
pivoted_data = filtered_data_avg.pivot_table(
    index=['Province'], columns=['Year'], values='Value', aggfunc='mean'
)

# STEP 5: Plot the data for the indicator
plt.figure(figsize=(12, 8))

# Loop through each indicator (we're only interested in one here)
for idx, indicator in enumerate(indicators_of_interest, start=1):
    indicator_data = filtered_data_avg[filtered_data_avg['Indicator'] == indicator]

    # Plot each province
    for province, grp in indicator_data.groupby('Province'):
        plt.plot(grp['Year'], grp['Value'], marker='o', label=province, linewidth=2)

    # Title, labels, and grid
    plt.title(f"{indicator} by Province, Averaged Over Gender (2013-14 and 2018-19)")
    plt.xlabel("Year")
    plt.ylabel(f"{indicator} (%)")
    plt.legend(title="Province", loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)

plt.tight_layout()
plt.show()


# In[56]:


import seaborn as sns
import matplotlib.pyplot as plt

# STEP 1: Filter the data for the indicators of interest
indicators_of_interest = ['LITERACY RATES (10 YEARS AND OLDER)', 'OUT OF SCHOOL CHILDREN AGED (5-16) YEARS']
filtered_data = long_ind[long_ind['Indicator'].isin(indicators_of_interest)]

# STEP 2: Exclude "Total" gender and "Pakistan"
filtered_data = filtered_data[(filtered_data['Gender'] != 'Total') & (filtered_data['Province'] != 'Pakistan')]

# STEP 3: Aggregate (average) the data over gender (Male and Female) for each province and indicator
# Group by Province, Indicator, and Gender, and calculate the average for Male and Female
filtered_data_avg_gender = filtered_data.groupby(['Province', 'Indicator', 'Gender'])['Value'].mean().reset_index()

# STEP 4: Pivot the data for the heatmap (Province x Gender)
heatmap_data = filtered_data_avg_gender.pivot_table(
    index=['Province', 'Indicator'], columns='Gender', values='Value', aggfunc='mean'
)

# STEP 5: Plot the heatmap for Literacy Rates
plt.figure(figsize=(10, 8))

literacy_data = heatmap_data.loc[heatmap_data.index.get_level_values('Indicator')
                                 == 'LITERACY RATES (10 YEARS AND OLDER)']

sns.heatmap(
    literacy_data,
    annot=True,
    cmap='Blues',      # steelblue-like palette
    linewidths=0.5
)

plt.title("Average Literacy Rate by Gender and Province")
plt.xlabel("Gender")
plt.ylabel("Province")
plt.tight_layout()
plt.show()

# STEP 6: Plot the heatmap for Out-of-School Children (use the same method as above)
plt.figure(figsize=(10, 8))

oos_data = heatmap_data.loc[heatmap_data.index.get_level_values('Indicator')
                            == 'OUT OF SCHOOL CHILDREN AGED (5-16) YEARS']

sns.heatmap(
    oos_data,
    annot=True,
    cmap='coolwarm',      # steelblue-like palette
    linewidths=0.5
)

plt.title("Average Out-of-School Children by Gender and Province")
plt.xlabel("Gender")
plt.ylabel("Province")
plt.tight_layout()
plt.show()


# In[57]:


# Create a grouped bar chart for literacy and OOSC for 2018-19
indicators_for_comparison = ['LITERACY', 'OUT OF SCHOOL CHILDREN AGED (5-16) YEARS']

# Filter data for the indicators of interest in 2018-19
data_to_plot = long_ind[long_ind['Indicator'].isin(indicators_for_comparison) & (long_ind['Year'] == '2018-19') & (long_ind['Province'] != 'Pakistan')]

# Pivot the data for easy plotting (Province x Indicator)
data_pivot = data_to_plot.pivot_table(
    index='Province', columns='Indicator', values='Value', aggfunc='mean'
)

# Plot the grouped bar chart
data_pivot.plot(kind='bar', figsize=(14, 7), color=['steelblue', 'lightgreen'])

# Title and labels
plt.title("Comparison of Literacy & Out-of-School Children by Province (2018-19)")
plt.xlabel("Province")
plt.ylabel("Percentage (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[58]:


# Filter for literacy indicator and exclude "Total"
lit_gender = long_ind[(long_ind['Indicator'] == 'LITERACY RATES (10 YEARS AND OLDER)') & 
                      (long_ind['Gender'].isin(['Male', 'Female'])) & (long_ind['Province'] != 'Pakistan')]

# Pivot the data for a stacked bar chart (Male vs Female)
lit_gender_pivot = lit_gender.pivot_table(
    index='Province', columns='Gender', values='Value', aggfunc='mean'
)

# Plot the stacked bar chart
lit_gender_pivot.plot(kind='bar', stacked=True, figsize=(12, 7), color=['steelblue', 'lightgreen'])

plt.title("Gender Breakdown of Literacy Rates by Province, 2018-19")
plt.xlabel("Province")
plt.ylabel("Literacy Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[59]:


# Calculate the change between 2013-14 and 2018-19
change_data = long_ind[long_ind['Year'] == '2018-19'].copy()

# Merge with 2013-14 data
change_data = change_data.rename(columns={'Value': 'Value_2018_19'})
change_data_2013_14 = long_ind[long_ind['Year'] == '2013-14'].copy()
change_data_2013_14 = change_data_2013_14.rename(columns={'Value': 'Value_2013_14'})

# Merge the two dataframes
change_data = pd.merge(change_data, change_data_2013_14[['Province', 'Indicator', 'Value_2013_14']], on=['Province', 'Indicator'])

# Calculate the change
change_data['Change'] = change_data['Value_2018_19'] - change_data['Value_2013_14']

# Plot with limited provinces (for clarity)
provinces_to_plot = ['Punjab', 'Sindh', 'Khyber Pakhtunkhwa Excluding Merged Areas', 'Balochistan']  # Focus on a few

plt.figure(figsize=(15, 10))
for province, grp in change_data[change_data['Province'].isin(provinces_to_plot)].groupby('Province'):
    plt.plot(grp['Indicator'], grp['Change'], marker='o', label=province, linewidth=2)

plt.title("Change in Key Indicators (2013-14 to 2018-19) by Province")
plt.xlabel("Indicator")
plt.ylabel("Change in Value (%)")
plt.legend(title="Province", loc='center left', bbox_to_anchor=(1, 0.5))  # Legend outside
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[71]:


# 1) Middle-to-Primary ratio (pipeline strength)
district_summary['ratio_middle_to_primary'] = (
    district_summary['Total_Middle'] / district_summary['Total_Primary']
)

# 2) Female pipeline drop: how many female schools "lost" from primary to middle
district_summary['Female_Drop'] = (
    district_summary['Female_Primary'] - district_summary['Female_Middle']
)

# Clean up impossible values (division by zero, etc.)
district_summary = district_summary.replace([np.inf, -np.inf], np.nan)


# In[72]:


pipeline_df = district_summary.dropna(subset=['ratio_middle_to_primary']).copy()


# In[73]:


import seaborn as sns
import matplotlib.pyplot as plt

# Use the cleaned subset with a valid ratio
pipeline_df = district_summary.dropna(subset=['ratio_middle_to_primary']).copy()

plt.figure(figsize=(8, 6))

sns.violinplot(
    data=pipeline_df,
    x='Severity',
    y='ratio_middle_to_primary',
    order=['Low', 'Medium', 'High'],
    inner='box',        # shows median & IQR inside the violin
    cut=0
)

plt.axhline(1.0, color='red', linestyle='--', linewidth=1, label='Ratio = 1 (Middle = Primary)')

plt.title("Distribution of Middle-to-Primary Non-Functional School Ratios\nby Severity Tier (KPK, 2021)")
plt.xlabel("Severity Tier")
plt.ylabel("Middle / Primary Ratio of Non-Functional Schools")
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()


# In[74]:


import plotly.graph_objects as go

# Make a copy to avoid SettingWithCopy issues
metric_df = district_summary.copy()

# Ensure the metrics exist
metric_df['ratio_middle_to_primary'] = (
    metric_df['Total_Middle'] / metric_df['Total_Primary']
)
metric_df['Female_Drop'] = (
    metric_df['Female_Primary'] - metric_df['Female_Middle']
)

metric_df = metric_df.replace([np.inf, -np.inf], np.nan)

# Keep only rows where ratio makes sense
metric_df = metric_df.dropna(subset=['ratio_middle_to_primary'])

# Define the metrics we want in the dropdown
metric_map = {
    'Middle / Primary Ratio': 'ratio_middle_to_primary',
    'Female Pipeline Drop (Primary - Middle)': 'Female_Drop',
    'Female Share (Primary)': 'female_share_Primary',
    'Female Share (Middle)': 'female_share_Middle'
}

severity_order = ['Low', 'Medium', 'High']
fig = go.Figure()

traces = []
visibility_sets = []   # each element is a visibility list for one metric button

# We'll add traces metric-by-metric, storing visibility states
all_metric_names = list(metric_map.keys())
n_metrics = len(all_metric_names)

for metric_label, metric_col in metric_map.items():
    vis = []
    for sev in severity_order:
        sev_data = metric_df[metric_df['Severity'] == sev][metric_col].dropna()
        
        trace = go.Box(
            y=sev_data,
            name=f"{sev}",
            boxmean='sd',
            visible=False   # we'll turn on later
        )
        fig.add_trace(trace)
        vis.append(True)   # this metric will control visibility per its own traces
    
    # For this metric, we want only its 3 traces visible; others False
    visibility_for_this_metric = [False] * (n_metrics * len(severity_order))
    start_idx = all_metric_names.index(metric_label) * len(severity_order)
    for i in range(len(severity_order)):
        visibility_for_this_metric[start_idx + i] = True
    
    visibility_sets.append(visibility_for_this_metric)

# Initially show the first metric (e.g., Middle / Primary Ratio)
for i, v in enumerate(visibility_sets[0]):
    fig.data[i].visible = v

# Build dropdown buttons
buttons = []
for metric_idx, metric_label in enumerate(all_metric_names):
    buttons.append(
        dict(
            label=metric_label,
            method="update",
            args=[
                {"visible": visibility_sets[metric_idx]},
                {"yaxis": {"title": metric_label}}
            ]
        )
    )

fig.update_layout(
    title="Pipeline Metrics by Severity Tier (Interactive)",
    xaxis_title="Severity Tier",
    yaxis_title="Middle / Primary Ratio",
    boxmode='group',
    showlegend=False,
    updatemenus=[
        dict(
            type="dropdown",
            x=1.15,
            y=1.0,
            showactive=True,
            buttons=buttons,
            xanchor="left"
        )
    ]
)

fig.show()



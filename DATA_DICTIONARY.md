# ASER Pakistan 2023 - Data Dictionary

This document provides detailed explanations of all variables in the cleaned datasets.

## School Dataset Variables (137 columns)

### Geographic & Administrative Information

| Original Code | Cleaned Name | Description | Type |
|--------------|--------------|-------------|------|
| SYEAR | survey_year | Year of ASER survey (2023) | Integer |
| AREA | area_type | Rural (1) or Urban (2) classification | Integer |
| VMAPID | village_map_id | Unique village mapping identifier | String |
| RNAME | province | Province name (Punjab, Sindh, KPK, Balochistan, AJK) | String |
| DNAME | district | District name | String |
| VlgId | village_id | Village unique identifier | Integer |
| VlgCode | village_code | Village code for linking datasets | Integer |
| SID | school_id | School unique identifier | Integer |
| STYPE | school_type | 1=Government, 2=Private | Integer |
| SURID | surveyor_id | Surveyor unique identifier | String |

### School Basic Information

| Original Code | Cleaned Name | Description | Values/Notes |
|--------------|--------------|-------------|--------------|
| S006 | private_school_ownership | Type of private ownership | For private schools only |
| S00 | class_range_from_to | Grade levels offered | e.g., "N TO 5" (Nursery to Grade 5) |
| S00a | class_range_other | Other grade specifications | Text field |
| S001 | gender_type | School gender type | 1=Boys, 2=Girls, 3=Mixed |
| S002 | medium_of_instruction | Primary language of teaching | 1=Urdu, 2=English, 3=Sindhi, etc. |
| S002a | medium_of_instruction_other | Other medium details | Text field |
| S002Y | year_established | Year school was established | Year (YYYY) |

### Enrollment Data

| Original Code | Cleaned Name | Description |
|--------------|--------------|-------------|
| S007E | enrollment_total | Total enrolled students |
| S007P | enrollment_present_today | Students present on survey day |

### Classroom Conditions - Class 2

| Original Code | Cleaned Name | Description | Values |
|--------------|--------------|-------------|--------|
| S03a1 | class2_multigrade | Is Class 2 multigrade? | 0=No, 1=Yes |
| S03b1 | class2_multigrade_with_class | Which classes combined | Class numbers |
| S03f1 | class2_learning_material | Learning materials available | 0=No, 1=Yes |
| S03d1 | class2_blackboard_available | Blackboard in Class 2 | 0=No, 1=Yes |
| S03e1 | class2_textbooks_available | Textbooks available | 0=No, 1=Yes |
| S03c1 | class2_seating_place | Seating arrangements | 1=Floor, 2=Benches, 3=Desks |

### Classroom Conditions - Class 8

| Original Code | Cleaned Name | Description | Values |
|--------------|--------------|-------------|--------|
| S03a2 | class8_multigrade | Is Class 8 multigrade? | 0=No, 1=Yes |
| S03b2 | class8_multigrade_with_class | Which classes combined | Class numbers |
| S03f2 | class8_learning_material | Learning materials available | 0=No, 1=Yes |
| S03d2 | class8_blackboard_available | Blackboard in Class 8 | 0=No, 1=Yes |
| S03e2 | class8_textbooks_available | Textbooks available | 0=No, 1=Yes |
| S03c2 | class8_seating_place | Seating arrangements | 1=Floor, 2=Benches, 3=Desks |

### Disability Inclusion - General

| Original Code | Cleaned Name | Description |
|--------------|--------------|-------------|
| S004 | disability_any | Any children with disabilities enrolled |
| S004FR | facility_ramp_available | Ramp for wheelchair access |
| S004FT | facility_accessible_toilet | Disability-accessible toilet |
| S004FHN | facility_health_worker | Health worker available |
| S004TSS | facility_special_training_teacher | Teachers with special needs training |
| S004ADHI | facility_hearing_assistive_device | Hearing assistive devices |
| S004TF | facility_transport | Transport facility for disabled students |

### Disability Details by Type and Gender

Each disability type has 3 severity levels tracked separately for boys and girls:
- Some difficulty (1)
- A lot of difficulty (2)  
- Cannot do at all / None (3)

**Visual Disabilities:**
- S004VB1 → disability_visual_boys_some
- S004VB2 → disability_visual_boys_lot
- S004VB3 → disability_visual_boys_none
- S004VG1 → disability_visual_girls_some
- S004VG2 → disability_visual_girls_lot
- S004VG3 → disability_visual_girls_none

**Similar patterns for:**
- Hearing (S004HB/HG)
- Physical (S004PB/PG)
- Intellectual (S004IB/IG)
- Speech/Communication (S004SCRB/SCRG)
- Cognitive (S004COTB/COTG)

### Infrastructure - Basic Facilities (S011 series)

All binary (0=No, 1=Yes):

| Original Code | Cleaned Name | Description |
|--------------|--------------|-------------|
| S011Ob1 | infra_boundary_wall | School has boundary wall |
| S011Ob2 | infra_school_gate | School has gate |
| S011Ob3 | infra_playground | Playground available |
| S011Ob4 | infra_lighting | Lighting available |
| S011Ob5 | infra_fans | Fans installed |
| S011Ob6 | infra_drinking_water | Drinking water available |
| S011Ob7 | infra_clean_toilets | Clean toilets available |
| S011Ob8 | infra_functional_toilets | Functional toilets |
| S011Ob9 | infra_handwashing | Handwashing facility |
| S011Ob10 | infra_disability_toilet | Disability-accessible toilet |
| S011Ob11 | infra_library | Library available |
| S011Ob12 | infra_science_lab | Science lab available |
| S011Ob13 | infra_computer_lab | Computer lab available |
| S011Ob14 | infra_generator | Generator available |
| S011Ob15 | infra_office_room | Office room available |
| S011Ob16 | infra_classrooms | Classrooms available |
| S011Ob17 | infra_furniture | Furniture available |
| S011Ob18 | infra_security | Security personnel |
| S011Ob19 | infra_cctv | CCTV cameras |
| S011Ob20 | infra_other | Other facilities |

### Infrastructure - Learning Resources (S012 series)

| Original Code | Cleaned Name | Description | Values |
|--------------|--------------|-------------|--------|
| S012Ob1 | infra_library_available | Library in working condition | 0=No, 1=Yes |
| S012Ob2 | infra_computer_lab_available | Computer lab functional | 0=No, 1=Yes |
| S012Ob3 | infra_internet_available | Internet connectivity | 0=No, 1=Yes |
| S012Ob4 | infra_firstaid_available | First aid kit | 0=No, 1=Yes |
| S012Ob5 | infra_science_kit_available | Science kit/equipment | 0=No, 1=Yes |
| S012Ob6 | infra_sports_material_available | Sports materials | 0=No, 1=Yes |
| S012Ob7 | infra_multimedia_available | Multimedia equipment | 0=No, 1=Yes |
| S012Ob8 | infra_art_material_available | Art materials | 0=No, 1=Yes |

### Infrastructure - Condition Assessment

| Original Code | Cleaned Name | Description | Values |
|--------------|--------------|-------------|--------|
| S012Ob11 | infra_roof_condition | Roof condition | 1=Good, 2=Fair, 3=Poor |
| S012Ob12 | infra_classroom_condition | Classroom condition | 1=Good, 2=Fair, 3=Poor |
| S012Ob13 | infra_school_cleanliness | Overall cleanliness | 1=Good, 2=Fair, 3=Poor |
| S012Ob14 | infra_boundary_condition | Boundary wall condition | 1=Good, 2=Fair, 3=Poor |
| S012Ob15 | infra_furniture_condition | Furniture condition | 1=Good, 2=Fair, 3=Poor |
| S012Ob16 | infra_electricity_functional | Electricity working | 0=No, 1=Yes |

### Teacher Information

| Original Code | Cleaned Name | Description |
|--------------|--------------|-------------|
| S008TA | teachers_total | Total number of teachers |
| S008TP | teachers_present_today | Teachers present on survey day |

### Teacher Qualifications (S009 series)

Number of teachers with each qualification:

| Original Code | Cleaned Name | Education Level |
|--------------|--------------|-----------------|
| S009b | teacher_qualification_matric | Matriculation (Grade 10) |
| S009c | teacher_qualification_intermediate | Intermediate (Grade 12) |
| S009d | teacher_qualification_bachelors | Bachelor's degree |
| S009e | teacher_qualification_masters | Master's degree |
| S009f | teacher_qualification_mphil | MPhil degree |
| S009g | teacher_qualification_phd | PhD degree |
| S009z | teacher_qualification_other | Other qualifications |

### Teacher Professional Training (S010 series)

Number of teachers with professional certifications:

| Original Code | Cleaned Name | Training Type |
|--------------|--------------|---------------|
| S010b | teacher_professional_ptc | Primary Teaching Certificate |
| S010c | teacher_professional_ct | Certificate of Teaching |
| S010d | teacher_professional_bed | Bachelor of Education |
| S010e | teacher_professional_med | Master of Education |
| S010z | teacher_professional_other | Other professional training |

### School Management Committee (SMC)

| Original Code | Cleaned Name | Description |
|--------------|--------------|-------------|
| S014a | smc_active | Is SMC active? |
| S014c | smc_members_total | Total SMC members |
| S014d | smc_female_members | Female members in SMC |
| S014e | smc_bank_balance | Bank balance (PKR) |
| S014f | smc_teacher_attendance_monitoring | Monitors teacher attendance |
| S014g | smc_last_meeting_date | Date of last meeting |

### SMC Training Topics (S014h series)

Binary indicators for training received:

| Original Code | Cleaned Name |
|--------------|--------------|
| S014h1 | smc_training_1 |
| S014h2 | smc_training_2 |
| S014h3 | smc_training_3 |
| S014h4 | smc_training_4 |

### Water Sources (S013 series)

Multiple water source options:

| Original Code | Cleaned Name | Description |
|--------------|--------------|-------------|
| S013a | water_source_1 | Primary water source |
| S013b | water_source_2 | Secondary water source |
| S013c | water_source_3 | Tertiary water source |
| S013d | water_source_4 | Additional water source |
| S013e | water_source_5 | Additional water source |

---

## Child Dataset Variables (47 columns)

### Demographics & Location

| Original Code | Cleaned Name | Description | Type/Values |
|--------------|--------------|-------------|-------------|
| Id | child_id | Unique child identifier | Integer |
| RNAME | province | Province name | String |
| PrvCode | province_code | Province code | Integer |
| DNAME | district | District name | String |
| DstCode | district_code | District code | Integer |
| VCODES | village_code | Village code (links to school data) | Integer |
| AREA | area_type | Rural (1) or Urban (2) | Integer |
| HHID | household_id | Household identifier | Integer |
| PRID | parent_id | Parent/guardian identifier | Integer |

### Child Basic Information

| Original Code | Cleaned Name | Description | Values |
|--------------|--------------|-------------|--------|
| C03 | child_age | Age of child | 5-16 years |
| C04 | child_gender | Gender | 1=Male, 2=Female |
| C28 | child_available_for_testing | Available for learning assessment | 0=No, 1=Yes |

### Schooling Status

| Original Code | Cleaned Name | Description | Values |
|--------------|--------------|-------------|--------|
| C05 | schooling_status | Current schooling situation | 1=Currently enrolled, 2=Dropped out, 3=Never enrolled |
| C06 | dropout_class | Class when dropped out | Class number |
| C08 | dropout_reason | Reason for dropout | Code (see manual) |
| C09 | never_enrolled_reason | Why never enrolled | Code (see manual) |
| C10 | current_class | Current grade/class | N=Nursery, KG=Kindergarten, 1-12 |
| C11 | institution_type | Type of institution attending | 1=Government, 2=Private, etc. |
| C12 | attends_surveyed_school | Attends school that was surveyed | 0=No, 1=Yes |

### Financial Aspects

| Original Code | Cleaned Name | Description |
|--------------|--------------|-------------|
| C07 | scholarship_received | Receives any scholarship |
| C13 | takes_tuition | Takes private tuition |
| C14 | tuition_fee | Monthly tuition fee (PKR) |

### Reading Assessment

| Original Code | Cleaned Name | Description | Levels |
|--------------|--------------|-------------|--------|
| C15 | reading_level | Urdu/Sindhi/Pashto reading ability | 0=Nothing, 1=Letters, 2=Words, 3=Sentences, 4=Story |
| C16 | bonus_reading_q1 | Bonus reading question 1 | Assessment score |
| B17 | bonus_reading_q2 | Bonus reading question 2 | Assessment score |

### Arithmetic Assessment

| Original Code | Cleaned Name | Description | Levels |
|--------------|--------------|-------------|--------|
| C18 | arithmetic_language | Language arithmetic test given in | Language code |
| C19 | arithmetic_level | Arithmetic ability | 0=Nothing, 1=1-9, 2=10-99, 3=Subtraction, 4=Division |

### English Assessment

| Original Code | Cleaned Name | Description | Levels |
|--------------|--------------|-------------|--------|
| C20 | english_word_reading | Can read English words | 0=No, 1=Yes |
| C21 | english_sentence_reading | Can read English sentences | 0=No, 1=Yes |
| C22 | english_comprehension | English comprehension | 0=No, 1=Yes |

### General Knowledge

| Original Code | Cleaned Name | Description |
|--------------|--------------|-------------|
| C23 | gk_q1_attempt | General knowledge question 1 attempted |
| C24 | gk_q2_attempt | General knowledge question 2 attempted |
| C25 | gk_q3_attempt | General knowledge question 3 attempted |

### Cognitive Development

| Original Code | Cleaned Name | Description |
|--------------|--------------|-------------|
| C26a | figure_identification_1 | Can identify figure 1 |
| C26b | figure_identification_2 | Can identify figure 2 |
| C27 | object_naming | Can name objects correctly |

### Health & Vaccination

| Original Code | Cleaned Name | Description | Values |
|--------------|--------------|-------------|--------|
| BasicVaccines | vaccination_basic | Has basic vaccinations | 0=No, 1=Yes |
| Polio | vaccine_polio | Polio vaccine | 0=No, 1=Yes |
| DPT_HepB_Hib | vaccine_dpt_hepb_hib | DPT, Hepatitis B, Hib vaccine | 0=No, 1=Yes |
| Pneumococcal | vaccine_pneumococcal | Pneumococcal vaccine | 0=No, 1=Yes |
| Measles | vaccine_measles | Measles vaccine | 0=No, 1=Yes |
| BCG | vaccine_bcg | BCG vaccine | 0=No, 1=Yes |
| Allergies | has_allergies | Has known allergies | 0=No, 1=Yes |

### Child Health Issues

| Original Code | Cleaned Name | Description |
|--------------|--------------|-------------|
| ICH01 | child_illness_1 | Specific illness type 1 |
| ICH02 | child_illness_2 | Specific illness type 2 |
| ICH03 | child_illness_3 | Specific illness type 3 |
| ICH05 | child_illness_5 | Specific illness type 5 |

---

## Common Codes and Categories

### Area Type
- 1 = Rural
- 2 = Urban

### School Type
- 1 = Government
- 2 = Private

### Gender
- 1 = Male/Boys
- 2 = Female/Girls
- 3 = Mixed (for schools)

### Condition Ratings (Infrastructure)
- 1 = Good
- 2 = Fair
- 3 = Poor

### Yes/No Variables
- 0 = No
- 1 = Yes

### Missing Data
- Blank cells = Data not collected or not applicable
- NaN = Missing value

## Data Linkage

### Linking School and Child Data:
- Use `village_code` present in both datasets
- Additional geographic linkages via `province` and `district` names

### Hierarchical Structure:
```
Province
  └── District
      └── Village
          ├── Schools (school_id)
          └── Households (household_id)
              └── Children (child_id)
```

## Notes on Data Usage

1. **Categorical Variables**: Most numeric codes represent categories, not quantities
2. **Multiple Response**: Some variables allow multiple responses (e.g., water sources)
3. **Conditional Questions**: Some variables only apply if certain conditions met (e.g., dropout reasons only for dropouts)
4. **Standardized Assessments**: Reading and arithmetic use standardized ASER tools
5. **Geographic Variations**: Some questions may vary by province/region

## For More Information

Refer to the ASER 2023 Coding Manual (available in `ASER_RAW_excel/coding-manual-2023 copy.pdf`) for:
- Detailed question wording
- Survey methodology
- Sampling procedures
- Enumerator training
- Quality control measures

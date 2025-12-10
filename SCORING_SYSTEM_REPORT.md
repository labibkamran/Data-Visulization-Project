# School Performance Scoring System - Technical Report
## Data Visualization Project | Public Census Dataset Analysis



---

## 4. Lab Readiness Score

**Purpose:** Measures overall laboratory infrastructure

### Formula:
```
lab_score = physics_lab + physics_appratus + 
            biology_lab + biology_appratus + 
            chemistry_lab + chemistry_appratus + 
            home_economic_lab + home_economic_appratus + 
            combine_lab + combine_appratus + 
            computer_lab
```

Each binary column contributes 0 or 1. Maximum possible = 11.

### Readiness Labels:
| Score Range | Label |
|-------------|-------|
| 0 - 3 | Very Low |
| 4 - 7 | Low |
| 8 - 11 | Medium |
| 12 - 15 | High |
| 16+ | Excellent |

---

## 5. Main Performance Scores

We created 4 composite scores, each ranging from 0 to 100:

---

### 5.1 Infrastructure Score (0-100)

**Purpose:** Measures physical infrastructure quality

**Formula:**
```
Infrastructure_Score = [
    0.20 × normalize(total_rooms) +
    0.20 × normalize(functional_classrooms / total_rooms) +
    0.20 × electricity +
    0.20 × drink_water +
    0.10 × usable_toilets +
    0.10 × main_gate
] × 100
```

**Weight Breakdown:**
| Component | Weight | Reasoning |
|-----------|--------|-----------|
| Total Rooms (normalized) | 20% | Building capacity |
| Classroom Utilization | 20% | % of rooms that are functional classrooms |
| Electricity | 20% | Basic utility |
| Drinking Water | 20% | Basic utility |
| Usable Toilets | 10% | Sanitation |
| Main Gate | 10% | Security/infrastructure |

---

### 5.2 Safety Score (0-100)

**Purpose:** Measures school safety conditions

**Formula:**
```
Safety_Score = [
    0.30 × (1 - normalize(dangerous_classrooms)) +
    0.20 × (1 - normalize(dangerous_non_classrooms)) +
    0.20 × boundary_wall_state +
    0.20 × main_gate +
    0.10 × security
] × 100
```

**Key Point:** For dangerous classrooms/non-classrooms, we use `(1 - normalized value)` because **fewer dangerous rooms = higher safety**.

**Weight Breakdown:**
| Component | Weight | Reasoning |
|-----------|--------|-----------|
| Dangerous Classrooms (inverse) | 30% | Most critical safety factor |
| Dangerous Non-Classrooms (inverse) | 20% | Secondary safety factor |
| Boundary Wall State | 20% | Physical security |
| Main Gate | 20% | Access control |
| Security Personnel | 10% | Active security |

---

### 5.3 Facilities Score (0-100)

**Purpose:** Measures availability of educational facilities

**Formula:**
```
Facilities_Score = [
    0.20 × play_ground +
    0.20 × library +
    0.20 × science_lab +
    0.15 × computer_lab +
    0.15 × internet
] × 100
```

**Weight Breakdown:**
| Component | Weight | Reasoning |
|-----------|--------|-----------|
| Playground | 20% | Physical education |
| Library | 20% | Academic resource |
| Science Lab | 20% | Practical learning |
| Computer Lab | 15% | Digital literacy |
| Internet | 15% | Connectivity |

---

### 5.4 Total Performance Score (0-100)

**Purpose:** Overall school performance combining all dimensions

**Formula:**
```
Total_Performance = [
    0.40 × Infrastructure_Score +
    0.30 × Safety_Score +
    0.30 × Facilities_Score
] / 100
```

**Weight Breakdown:**
| Component | Weight | Reasoning |
|-----------|--------|-----------|
| Infrastructure Score | 40% | Foundation of school operations |
| Safety Score | 30% | Critical for student wellbeing |
| Facilities Score | 30% | Learning enhancement |

---


---

## 7. Summary

| Score Name | Range | Formula Type |
|------------|-------|--------------|
| Infrastructure Score | 0-100 | Weighted sum with normalization |
| Safety Score | 0-100 | Weighted sum with inverse normalization |
| Facilities Score | 0-100 | Weighted sum of binary values |
| Total Performance | 0-100 | Weighted average of 3 scores |
| Lab Score | 0-11 | Simple sum of binary values |

---

## 8. Usage in Dashboard

These scores are used to:
1. **Rank schools** (Top 10 / Bottom 10)
2. **Compare districts** (grouped bar charts)
3. **Analyze correlations** (heatmaps)
4. **Filter and explore** (interactive sliders)

---

*Report prepared for Data Visualization Project | December 2024*

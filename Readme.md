# Internship Performance, Attendance & Stipend Analytics Dashboard

An interactive analytics dashboard for exploring internship attendance, academic indicators, mentor engagement, completion outcomes, stipend patterns, and intern-level information.

---

## Project Overview

The **Internship Performance, Attendance & Stipend Analytics Dashboard** is a Python-based interactive analytics application built to transform internship records into meaningful, easy-to-understand visual insights.

The application allows users to:

- Monitor overall internship statistics
- Analyze attendance patterns
- Explore CGPA as an academic indicator
- Analyze stipend distributions
- Examine completion outcomes
- Study mentor engagement
- Search and inspect individual interns
- Apply interactive filters
- Review dataset quality and limitations
- Download filtered internship records

The dashboard is designed as a practical analytics solution rather than a collection of static charts.

---

## Problem Statement

Internship programs generate useful information about interns, including attendance, academic indicators, mentor interactions, completion status, internship mode, department, university, and stipend.

However, raw tabular data makes it difficult to identify patterns quickly.

This project addresses that problem by providing an interactive dashboard that converts internship records into visual and descriptive analytics.

---

## Objectives

The major objectives of this project are:

1. Analyze internship completion outcomes.
2. Understand attendance patterns across different groups.
3. Analyze CGPA as an academic indicator.
4. Analyze stipend distributions and group-level differences.
5. Examine mentor engagement through mentor meeting data.
6. Provide intern-level search and profile analysis.
7. Provide interactive filtering across major dimensions.
8. Identify and display data-quality information.
9. Present analytics through a clean and interactive interface.

---

## Dataset

### Dataset Name

`Professional_Internship_Dataset_150.xlsx`

### Dataset Size

- **Records:** 150
- **Source Columns:** 13
- **Source Sheet:** `Internship`

### Source Columns

| Column | Description |
|---|---|
| Intern ID | Unique identifier for each intern |
| Name | Intern name |
| Gender | Gender category |
| University | University associated with the intern |
| Department | Internship department |
| Mode | Internship mode |
| Completed | Internship completion status |
| Dropped | Internship drop/non-completion status |
| Duration (Weeks) | Internship duration |
| Mentor Meetings | Number of mentor meetings |
| Attendance % | Attendance percentage |
| CGPA | Academic indicator |
| Stipend | Recorded stipend value |

---

## Dataset Characteristics

The dataset contains:

- 150 unique intern IDs
- 5 departments
- 5 universities
- 3 internship modes
- 2 gender categories
- Completed / Non-Completed outcomes
- Attendance percentages
- CGPA values
- Mentor meeting counts
- Stipend values
- Internship duration

The dataset contains no missing values or duplicate rows in the supplied source data.

---

## Important Analytical Notes

### CGPA

The dataset does not contain a formal internship performance score.

Therefore:

> **CGPA is treated as an academic indicator and not as an internship performance score.**

No artificial weighted performance score is created.

### Stipend

The source dataset does not specify:

- Currency
- Payment frequency
- Payment period

Therefore the dashboard uses wording such as:

> **Stipend — Source Unit Unspecified**

A stipend value of `0` is retained as an observed value and is **not automatically treated as missing data**.

### Completion and Dropped

`Completed` is used as the canonical completion measure.

`Dropped` is treated as a related/redundant field and is validated for consistency.

### Causation

The dashboard presents descriptive patterns and associations.

It does not claim that one variable causes another.

For example, a difference in completion rates between internship modes is presented as an observed dataset pattern, not as proof that internship mode causes a particular completion outcome.

---

# Technology Stack

## Dashboard / Visualization

- Streamlit
- Plotly

## Data Processing

- Python
- Pandas
- NumPy
- OpenPyXL

## Testing

- Pytest

## Version Control

- Git
- GitHub

---

# System Architecture

```text
                   Excel Dataset
                         |
                         v
                    OpenPyXL
                         |
                         v
                      Pandas
                         |
              Data Validation & Cleaning
                         |
                         v
                  Analytics Layer
                         |
          +--------------+--------------+
          |              |              |
        KPIs       Group Analysis   Intern Analysis
          |              |              |
          +--------------+--------------+
                         |
                         v
                      Streamlit
                         |
                         v
                  Plotly Visualizations
                         |
                         v
                 Interactive Dashboard
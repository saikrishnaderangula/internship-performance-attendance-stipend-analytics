from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Internship Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DATA
# =========================================================

DATA_PATH = Path(
    "data/Professional_Internship_Dataset_150.xlsx"
)


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}"
        )

    return pd.read_excel(
        DATA_PATH,
        sheet_name="Internship",
    )


try:
    df = load_data()
except Exception as error:
    st.error(str(error))
    st.stop()


# =========================================================
# THEME
# =========================================================

st.sidebar.markdown(
    "### Appearance"
)

dark_mode = st.sidebar.toggle(
    "Dark mode",
    value=False,
)

if dark_mode:
    BG = "#0b1120"
    SURFACE = "#111827"
    SURFACE_2 = "#172033"
    BORDER = "#263247"
    TEXT = "#f8fafc"
    MUTED = "#94a3b8"
    ACCENT = "#60a5fa"
    CHART_TEMPLATE = "plotly_dark"
else:
    BG = "#f5f7fb"
    SURFACE = "#ffffff"
    SURFACE_2 = "#f8fafc"
    BORDER = "#e2e8f0"
    TEXT = "#111827"
    MUTED = "#64748b"
    ACCENT = "#2563eb"
    CHART_TEMPLATE = "plotly_white"


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    f"""
    <style>

    /* Remove Streamlit's default page/background containers */
    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    [data-testid="stMain"],
    section.main,
    .stApp,
    .main {{
        background: {BG} !important;
        color: {TEXT} !important;
    }}

    /* Remove the white rounded outer container */
    [data-testid="stAppViewContainer"] > .main {{
        background: {BG} !important;
    }}

    [data-testid="stMainBlockContainer"] {{
        background: transparent !important;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
        box-shadow: none !important;
    }}

    [data-testid="stToolbar"] {{
        background: transparent !important;
    }}

    [data-testid="stDecoration"] {{
        display: none !important;
    }}

    /* Main content */
    .block-container {{
        max-width: 1500px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        background: transparent !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: {SURFACE} !important;
        border-right: 1px solid {BORDER} !important;
    }}

    [data-testid="stSidebar"] * {{
        color: {TEXT};
    }}

    /* Text */
    h1,
    h2,
    h3,
    h4,
    p,
    label,
    span {{
        color: {TEXT};
    }}

    .main-title {{
        font-size: 2.15rem;
        font-weight: 800;
        color: {TEXT};
        line-height: 1.15;
        margin-bottom: 0.25rem;
    }}

    .main-subtitle {{
        color: {MUTED};
        font-size: 0.98rem;
        margin-bottom: 1.5rem;
    }}

    .section-heading {{
        font-size: 1.3rem;
        font-weight: 750;
        color: {TEXT};
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }}

    /* KPI cards */
    [data-testid="stMetric"] {{
        background: {SURFACE} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 14px !important;
        padding: 16px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06) !important;
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {TEXT} !important;
        font-weight: 750 !important;
    }}

    /* Chart containers */
    div[data-testid="stPlotlyChart"] {{
        background: {SURFACE} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 14px !important;
        padding: 6px !important;
        margin-bottom: 1rem !important;
    }}

    /* Dataframes */
    div[data-testid="stDataFrame"] {{
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }}

    /* Inputs */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {{
        background: {SURFACE} !important;
        border-color: {BORDER} !important;
    }}

    /* Buttons */
    .stButton > button {{
        background: {SURFACE} !important;
        color: {TEXT} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 10px !important;
    }}

    .stButton > button:hover {{
        border-color: {ACCENT} !important;
        color: {ACCENT} !important;
    }}

    /* Info / warning boxes */
    [data-testid="stAlert"] {{
        border-radius: 12px !important;
    }}

    /* Dividers */
    hr {{
        border-color: {BORDER} !important;
    }}

    /* Sidebar branding */
    .brand-title {{
        font-size: 1.35rem;
        font-weight: 800;
        color: {TEXT};
    }}

    .brand-subtitle {{
        color: {MUTED};
        font-size: 0.82rem;
        margin-top: -5px;
    }}

    /* Footer */
    .footer {{
        color: {MUTED};
        text-align: center;
        font-size: 0.8rem;
        padding-top: 1rem;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPER
# =========================================================

def style_figure(fig):
    fig.update_layout(
        template=CHART_TEMPLATE,
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font={
            "color": TEXT,
            "family": "Arial, sans-serif",
        },
        title={
            "font": {
                "size": 17,
                "color": TEXT,
            }
        },
        margin={
            "l": 20,
            "r": 20,
            "t": 55,
            "b": 20,
        },
        legend={
            "font": {
                "color": TEXT,
            }
        },
    )

    return fig


def completion_by(column: str) -> pd.DataFrame:
    result = (
        filtered.groupby(column)
        .agg(
            Interns=("Intern ID", "count"),
            Completed=(
                "Completed",
                lambda x: (x == "Yes").sum(),
            ),
        )
        .reset_index()
    )

    result["Completion Rate"] = (
        result["Completed"]
        / result["Interns"]
        * 100
    )

    return result


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    '<div class="brand-title">📊 Internship Analytics</div>',
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    '<div class="brand-subtitle">'
    "Performance • Attendance • Stipend"
    "</div>",
    unsafe_allow_html=True,
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Overview",
        "Attendance & Engagement",
        "CGPA Analytics",
        "Stipend Analytics",
        "Completion Analysis",
        "Intern Directory",
        "Data Quality",
    ],
)

st.sidebar.divider()

st.sidebar.markdown(
    "### Filters"
)

department_options = sorted(
    df["Department"].dropna().unique()
)

mode_options = sorted(
    df["Mode"].dropna().unique()
)

university_options = sorted(
    df["University"].dropna().unique()
)

gender_options = sorted(
    df["Gender"].dropna().unique()
)

completion_options = sorted(
    df["Completed"].dropna().unique()
)

selected_departments = st.sidebar.multiselect(
    "Department",
    department_options,
    default=department_options,
)

selected_modes = st.sidebar.multiselect(
    "Internship Mode",
    mode_options,
    default=mode_options,
)

selected_universities = st.sidebar.multiselect(
    "University",
    university_options,
    default=university_options,
)

selected_genders = st.sidebar.multiselect(
    "Gender",
    gender_options,
    default=gender_options,
)

selected_completion = st.sidebar.multiselect(
    "Completion Status",
    completion_options,
    default=completion_options,
)

attendance_threshold = st.sidebar.slider(
    "Low Attendance Threshold",
    min_value=50,
    max_value=100,
    value=70,
)


# =========================================================
# FILTER
# =========================================================

filtered = df[
    df["Department"].isin(selected_departments)
    & df["Mode"].isin(selected_modes)
    & df["University"].isin(selected_universities)
    & df["Gender"].isin(selected_genders)
    & df["Completed"].isin(selected_completion)
].copy()


if filtered.empty:
    st.warning(
        "No records match the selected filters."
    )
    st.stop()


# =========================================================
# CALCULATIONS
# =========================================================

total_interns = len(filtered)

completed_count = int(
    (filtered["Completed"] == "Yes").sum()
)

non_completed_count = int(
    (filtered["Completed"] == "No").sum()
)

completion_rate = (
    completed_count
    / total_interns
    * 100
)

average_attendance = (
    filtered["Attendance %"].mean()
)

median_attendance = (
    filtered["Attendance %"].median()
)

average_cgpa = (
    filtered["CGPA"].mean()
)

median_cgpa = (
    filtered["CGPA"].median()
)

average_stipend = (
    filtered["Stipend"].mean()
)

median_stipend = (
    filtered["Stipend"].median()
)

minimum_stipend = (
    filtered["Stipend"].min()
)

maximum_stipend = (
    filtered["Stipend"].max()
)

average_mentor = (
    filtered["Mentor Meetings"].mean()
)

zero_stipend_count = int(
    (filtered["Stipend"] == 0).sum()
)

zero_stipend_rate = (
    zero_stipend_count
    / total_interns
    * 100
)

low_attendance = filtered[
    filtered["Attendance %"]
    < attendance_threshold
]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    "Internship Performance, Attendance & Stipend Analytics"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-subtitle">'
    "Interactive analysis of internship attendance, academic indicators, "
    "mentor engagement, completion outcomes and stipend."
    "</div>",
    unsafe_allow_html=True,
)


# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

if page == "Executive Overview":

    cards = st.columns(6)

    cards[0].metric(
        "Total Interns",
        f"{total_interns:,}",
    )

    cards[1].metric(
        "Completion Rate",
        f"{completion_rate:.1f}%",
    )

    cards[2].metric(
        "Avg Attendance",
        f"{average_attendance:.1f}%",
    )

    cards[3].metric(
        "Avg CGPA",
        f"{average_cgpa:.2f}",
    )

    cards[4].metric(
        "Avg Stipend",
        f"{average_stipend:,.0f}",
    )

    cards[5].metric(
        "Mentor Meetings",
        f"{average_mentor:.2f}",
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        data = (
            filtered["Department"]
            .value_counts()
            .reset_index()
        )

        data.columns = [
            "Department",
            "Interns",
        ]

        fig = px.bar(
            data,
            x="Department",
            y="Interns",
            text_auto=True,
            title="Interns by Department",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    with right:

        data = (
            filtered["Mode"]
            .value_counts()
            .reset_index()
        )

        data.columns = [
            "Mode",
            "Interns",
        ]

        fig = px.bar(
            data,
            x="Mode",
            y="Interns",
            text_auto=True,
            title="Interns by Internship Mode",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    left, right = st.columns(2)

    with left:

        data = completion_by(
            "Department"
        )

        fig = px.bar(
            data,
            x="Department",
            y="Completion Rate",
            text_auto=".1f",
            title="Observed Completion Rate by Department",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    with right:

        data = (
            filtered["University"]
            .value_counts()
            .reset_index()
        )

        data.columns = [
            "University",
            "Interns",
        ]

        fig = px.bar(
            data,
            x="University",
            y="Interns",
            text_auto=True,
            title="Interns by University",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    left, right = st.columns(2)

    with left:

        fig = px.histogram(
            filtered,
            x="Attendance %",
            nbins=12,
            title="Attendance Distribution",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    with right:

        fig = px.histogram(
            filtered,
            x="Stipend",
            nbins=12,
            title="Stipend Distribution",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    st.markdown(
        "### Key Observations"
    )

    st.write(
        f"• {completed_count} of {total_interns} "
        "filtered interns are marked completed."
    )

    st.write(
        f"• {len(low_attendance)} interns are below "
        f"the selected {attendance_threshold}% attendance threshold."
    )

    st.write(
        f"• {zero_stipend_count} interns have "
        "a stipend value of zero."
    )

    st.info(
        "The dashboard reports descriptive patterns in the dataset "
        "and does not establish causal relationships."
    )


# =========================================================
# ATTENDANCE
# =========================================================

elif page == "Attendance & Engagement":

    st.markdown(
        '<div class="section-heading">'
        "Attendance & Engagement"
        "</div>",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Average Attendance",
        f"{average_attendance:.1f}%",
    )

    c2.metric(
        "Median Attendance",
        f"{median_attendance:.1f}%",
    )

    c3.metric(
        "Avg Mentor Meetings",
        f"{average_mentor:.2f}",
    )

    c4.metric(
        "Low Attendance",
        len(low_attendance),
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        data = (
            filtered.assign(
                Attendance_Group=pd.cut(
                    filtered["Attendance %"],
                    bins=[
                        0,
                        69.999,
                        79.999,
                        89.999,
                        100,
                    ],
                    labels=[
                        "<70%",
                        "70–79%",
                        "80–89%",
                        "90–100%",
                    ],
                    include_lowest=True,
                )
            )
            .groupby(
                "Attendance_Group",
                observed=True,
            )
            .size()
            .reset_index(name="Interns")
        )

        fig = px.bar(
            data,
            x="Attendance_Group",
            y="Interns",
            text_auto=True,
            title="Attendance Groups",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    with right:

        data = (
            filtered.groupby("Department")
            ["Attendance %"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            data,
            x="Department",
            y="Attendance %",
            text_auto=".1f",
            title="Average Attendance by Department",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    left, right = st.columns(2)

    with left:

        fig = px.box(
            filtered,
            x="Mode",
            y="Attendance %",
            title="Attendance by Internship Mode",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    with right:

        data = (
            filtered.groupby("Completed")
            ["Mentor Meetings"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            data,
            x="Completed",
            y="Mentor Meetings",
            text_auto=".2f",
            title="Mentor Meetings by Completion",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    st.subheader(
        "Attendance vs Mentor Meetings"
    )

    fig = px.scatter(
        filtered,
        x="Mentor Meetings",
        y="Attendance %",
        color="Completed",
        hover_data=[
            "Intern ID",
            "Name",
            "Department",
        ],
        title="Attendance and Mentor Engagement",
    )

    st.plotly_chart(
        style_figure(fig),
        use_container_width=True,
    )

    st.subheader(
        f"Interns Below {attendance_threshold}% Attendance"
    )

    st.dataframe(
        low_attendance[
            [
                "Intern ID",
                "Name",
                "Department",
                "Mode",
                "Attendance %",
                "CGPA",
                "Mentor Meetings",
                "Completed",
                "Stipend",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# CGPA
# =========================================================

elif page == "CGPA Analytics":

    st.subheader(
        "CGPA Analytics"
    )

    st.info(
        "CGPA is an academic indicator in the source dataset. "
        "It is not a formal internship performance score."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Average CGPA",
        f"{average_cgpa:.2f}",
    )

    c2.metric(
        "Median CGPA",
        f"{median_cgpa:.2f}",
    )

    c3.metric(
        "Minimum CGPA",
        f"{filtered['CGPA'].min():.2f}",
    )

    c4.metric(
        "Maximum CGPA",
        f"{filtered['CGPA'].max():.2f}",
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        groups = pd.cut(
            filtered["CGPA"],
            bins=[
                0,
                2.49,
                2.99,
                3.49,
                4.00,
            ],
            labels=[
                "<2.50",
                "2.50–2.99",
                "3.00–3.49",
                "3.50–4.00",
            ],
            include_lowest=True,
        )

        data = (
            groups.value_counts()
            .sort_index()
            .reset_index()
        )

        data.columns = [
            "CGPA Group",
            "Interns",
        ]

        fig = px.bar(
            data,
            x="CGPA Group",
            y="Interns",
            text_auto=True,
            title="CGPA Distribution",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    with right:

        data = (
            filtered.groupby("Department")
            ["CGPA"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            data,
            x="Department",
            y="CGPA",
            text_auto=".2f",
            title="Average CGPA by Department",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    left, right = st.columns(2)

    with left:

        fig = px.box(
            filtered,
            x="Mode",
            y="CGPA",
            title="CGPA by Internship Mode",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    with right:

        data = (
            filtered.groupby("University")
            ["CGPA"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            data,
            x="University",
            y="CGPA",
            text_auto=".2f",
            title="Average CGPA by University",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    st.subheader(
        "Attendance vs CGPA"
    )

    fig = px.scatter(
        filtered,
        x="Attendance %",
        y="CGPA",
        color="Department",
        hover_data=[
            "Intern ID",
            "Name",
            "Completed",
        ],
        title="Attendance vs Academic Indicator",
    )

    st.plotly_chart(
        style_figure(fig),
        use_container_width=True,
    )


# =========================================================
# STIPEND
# =========================================================

elif page == "Stipend Analytics":

    st.subheader(
        "Stipend Analytics"
    )

    st.caption(
        "Stipend — source unit unspecified"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Average Stipend",
        f"{average_stipend:,.0f}",
    )

    c2.metric(
        "Median Stipend",
        f"{median_stipend:,.0f}",
    )

    c3.metric(
        "Minimum",
        f"{minimum_stipend:,.0f}",
    )

    c4.metric(
        "Maximum",
        f"{maximum_stipend:,.0f}",
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Zero-Stipend Records",
        zero_stipend_count,
    )

    c2.metric(
        "Zero-Stipend Rate",
        f"{zero_stipend_rate:.1f}%",
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        fig = px.histogram(
            filtered,
            x="Stipend",
            nbins=12,
            title="Stipend Distribution",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    with right:

        fig = px.box(
            filtered,
            x="Department",
            y="Stipend",
            title="Stipend by Department",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    left, right = st.columns(2)

    with left:

        data = (
            filtered.groupby("Mode")
            ["Stipend"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            data,
            x="Mode",
            y="Stipend",
            text_auto=".0f",
            title="Average Stipend by Mode",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    with right:

        data = (
            filtered.groupby("University")
            ["Stipend"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            data,
            x="University",
            y="Stipend",
            text_auto=".0f",
            title="Average Stipend by University",
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

    st.subheader(
        "Attendance vs Stipend"
    )

    fig = px.scatter(
        filtered,
        x="Attendance %",
        y="Stipend",
        color="Department",
        hover_data=[
            "Intern ID",
            "Name",
            "CGPA",
            "Completed",
        ],
        title="Attendance vs Stipend",
    )

    st.plotly_chart(
        style_figure(fig),
        use_container_width=True,
    )

    st.info(
        "Zero stipend values are retained as observed source "
        "values and are not treated as missing data."
    )

    st.subheader(
        "Zero-Stipend Interns"
    )

    zero = filtered[
        filtered["Stipend"] == 0
    ]

    st.dataframe(
        zero[
            [
                "Intern ID",
                "Name",
                "Department",
                "University",
                "Mode",
                "Completed",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# COMPLETION
# =========================================================

elif page == "Completion Analysis":

    st.subheader(
        "Completion Analysis"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Interns",
        total_interns,
    )

    c2.metric(
        "Completed",
        completed_count,
    )

    c3.metric(
        "Non-Completed",
        non_completed_count,
    )

    c4.metric(
        "Completion Rate",
        f"{completion_rate:.1f}%",
    )

    st.divider()

    summary = pd.DataFrame(
        {
            "Status": [
                "Completed",
                "Non-Completed",
            ],
            "Interns": [
                completed_count,
                non_completed_count,
            ],
        }
    )

    fig = px.bar(
        summary,
        x="Status",
        y="Interns",
        text_auto=True,
        title="Completion Summary",
    )

    st.plotly_chart(
        style_figure(fig),
        use_container_width=True,
    )

    comparisons = [
        (
            "Department",
            "Observed Completion Rate by Department",
        ),
        (
            "Mode",
            "Observed Completion Rate by Mode",
        ),
        (
            "University",
            "Observed Completion Rate by University",
        ),
        (
            "Gender",
            "Observed Completion Rate by Gender",
        ),
        (
            "Duration (Weeks)",
            "Observed Completion Rate by Duration",
        ),
    ]

    for column, title in comparisons:

        result = completion_by(column)

        fig = px.bar(
            result,
            x=column,
            y="Completion Rate",
            text_auto=".1f",
            title=title,
        )

        fig.update_layout(
            yaxis_title="Completion Rate (%)"
        )

        st.plotly_chart(
            style_figure(fig),
            use_container_width=True,
        )

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# INTERN DIRECTORY
# =========================================================

elif page == "Intern Directory":

    st.subheader(
        "Intern Directory"
    )

    search = st.text_input(
        "Search by Intern ID or Name",
        placeholder="Type an Intern ID or name...",
    )

    directory = filtered.copy()

    if search.strip():

        query = search.strip()

        mask = (
            directory["Intern ID"]
            .astype(str)
            .str.contains(
                query,
                case=False,
                na=False,
            )
            |
            directory["Name"]
            .astype(str)
            .str.contains(
                query,
                case=False,
                na=False,
            )
        )

        directory = directory[mask]

    st.write(
        f"Showing **{len(directory)}** interns"
    )

    display_columns = [
        "Intern ID",
        "Name",
        "Gender",
        "University",
        "Department",
        "Mode",
        "Duration (Weeks)",
        "Mentor Meetings",
        "Attendance %",
        "CGPA",
        "Stipend",
        "Completed",
    ]

    st.dataframe(
        directory[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    if not directory.empty:

        st.divider()

        selected_id = st.selectbox(
            "Select an Intern",
            directory["Intern ID"].tolist(),
        )

        selected = directory[
            directory["Intern ID"]
            == selected_id
        ].iloc[0]

        st.subheader(
            f"{selected['Name']} — {selected['Intern ID']}"
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Attendance",
            f"{selected['Attendance %']:.1f}%",
        )

        c2.metric(
            "CGPA",
            f"{selected['CGPA']:.2f}",
        )

        c3.metric(
            "Stipend",
            f"{selected['Stipend']:,.0f}",
        )

        c4.metric(
            "Mentor Meetings",
            int(selected["Mentor Meetings"]),
        )

        left, right = st.columns(2)

        with left:

            st.markdown(
                f"""
                **University:** {selected['University']}

                **Department:** {selected['Department']}

                **Gender:** {selected['Gender']}

                **Mode:** {selected['Mode']}

                **Duration:** {selected['Duration (Weeks)']} weeks

                **Completion:** {selected['Completed']}
                """
            )

        with right:

            attendance_difference = (
                selected["Attendance %"]
                - filtered["Attendance %"].mean()
            )

            cgpa_difference = (
                selected["CGPA"]
                - filtered["CGPA"].mean()
            )

            stipend_difference = (
                selected["Stipend"]
                - filtered["Stipend"].mean()
            )

            mentor_difference = (
                selected["Mentor Meetings"]
                - filtered["Mentor Meetings"].mean()
            )

            st.markdown(
                "### Comparison with Filtered Dataset"
            )

            st.write(
                f"Attendance: "
                f"{'Above' if attendance_difference >= 0 else 'Below'} "
                f"average by "
                f"{abs(attendance_difference):.1f}"
            )

            st.write(
                f"CGPA: "
                f"{'Above' if cgpa_difference >= 0 else 'Below'} "
                f"average by "
                f"{abs(cgpa_difference):.2f}"
            )

            st.write(
                f"Stipend: "
                f"{'Above' if stipend_difference >= 0 else 'Below'} "
                f"average by "
                f"{abs(stipend_difference):,.0f}"
            )

            st.write(
                f"Mentor Meetings: "
                f"{'Above' if mentor_difference >= 0 else 'Below'} "
                f"average by "
                f"{abs(mentor_difference):.2f}"
            )

        st.info(
            "CGPA is an academic indicator and not a formal "
            "internship performance score."
        )


# =========================================================
# DATA QUALITY
# =========================================================

elif page == "Data Quality":

    st.subheader(
        "Data Quality & Dataset Information"
    )

    missing_values = int(
        df.isna().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    duplicate_ids = int(
        df["Intern ID"].duplicated().sum()
    )

    completeness = (
        100
        if df.size == 0
        else (
            1 - missing_values / df.size
        ) * 100
    )

    zero_stipend = int(
        (df["Stipend"] == 0).sum()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", len(df))
    c2.metric("Columns", len(df.columns))
    c3.metric("Missing Values", missing_values)
    c4.metric(
        "Data Completeness",
        f"{completeness:.1f}%",
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Duplicate Rows",
        duplicate_rows,
    )

    c2.metric(
        "Duplicate IDs",
        duplicate_ids,
    )

    c3.metric(
        "Zero-Stipend Records",
        zero_stipend,
    )

    st.divider()

    st.subheader(
        "Column Information"
    )

    column_info = pd.DataFrame(
        {
            "Column": df.columns,
            "Data Type": [
                str(df[column].dtype)
                for column in df.columns
            ],
            "Missing": [
                int(df[column].isna().sum())
                for column in df.columns
            ],
            "Unique Values": [
                int(df[column].nunique())
                for column in df.columns
            ],
        }
    )

    st.dataframe(
        column_info,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader(
        "Source Data Preview"
    )

    st.dataframe(
        df.head(20),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader(
        "Dataset Limitations"
    )

    st.markdown(
        """
        - The dataset contains 150 internship records.
        - There is no formal internship performance score.
        - CGPA is treated as an academic indicator.
        - No date fields are available for time-series analysis.
        - Stipend currency and payment cadence are unspecified.
        - Zero stipend values are retained as observed data.
        - Names are repeated, so Intern ID is the primary identifier.
        - The analysis is descriptive and does not establish causation.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Internship Performance, Attendance & Stipend Analytics Dashboard
        • Python • Pandas • Streamlit • Plotly
    </div>
    """,
    unsafe_allow_html=True,
)
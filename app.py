import streamlit as st
import pandas as pd
import calendar
from datetime import date


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Officer Mess Chhawla",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# GOOGLE SHEET
# ============================================================

SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1Kxbp6W4cb-_k9LD9V--ZJsysEDrcg3whYPj2TuHKfwU/edit"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .block-container {
        max-width: 1050px;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    [data-testid="stSidebar"],
    [data-testid="collapsedControl"] {
        display: none;
    }

    /*
       MOBILE CALENDAR
       --------------------------------------------------------
       Streamlit may stack st.columns on narrow screens.
       The keyed container is explicitly converted to a 7-column
       CSS grid so the calendar remains a real calendar on phones.
    */
    .st-key-calendar-grid [data-testid="stHorizontalBlock"],
    [data-testid="st-key-calendar-grid"] [data-testid="stHorizontalBlock"],
    .calendar-grid [data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(7, minmax(0, 1fr)) !important;
        grid-auto-flow: row !important;
        flex-direction: unset !important;
        flex-wrap: unset !important;
        width: 100% !important;
        max-width: 100% !important;
        gap: 0.3rem !important;
        align-items: stretch !important;
    }

    .st-key-calendar-grid [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    .st-key-calendar-grid [data-testid="stHorizontalBlock"] > [data-testid="column"],
    [data-testid="st-key-calendar-grid"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    [data-testid="st-key-calendar-grid"] [data-testid="stHorizontalBlock"] > [data-testid="column"],
    .calendar-grid [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    .calendar-grid [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        min-width: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        flex: none !important;
    }

    .st-key-calendar-grid [data-testid="stColumn"] > div,
    .st-key-calendar-grid [data-testid="column"] > div,
    [data-testid="st-key-calendar-grid"] [data-testid="stColumn"] > div,
    [data-testid="st-key-calendar-grid"] [data-testid="column"] > div {
        width: 100% !important;
        min-width: 0 !important;
    }

    /* Calendar cells */
    .calendar-grid div[data-testid="stButton"] {
        width: 100% !important;
    }

    .calendar-grid div[data-testid="stButton"] button {
        width: 100% !important;
        min-height: 52px !important;
        height: 52px !important;
        padding: 0 !important;
        border-radius: 10px !important;
        border: 1px solid #E2E8F0 !important;
        background: #FFFFFF !important;
        color: #334155 !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        box-shadow: none !important;
        transition: all 0.15s ease;
    }

    .calendar-grid div[data-testid="stButton"] button:hover {
        border-color: #94A3B8 !important;
        background: #F8FAFC !important;
        transform: translateY(-1px);
    }

    /*
       Fully available date marker.
       Render it as a real CSS dot instead of an emoji so iOS does not
       enlarge the marker or place it outside the date cell.
    */
    [class*="st-key-free-date-"] div[data-testid="stButton"] button {
        position: relative !important;
    }

    [class*="st-key-free-date-"] div[data-testid="stButton"] button::after {
        content: "";
        position: absolute;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #22C55E;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        pointer-events: none;
    }

    /* Free-date marker: keep the compact bullet subtle. */
    .st-key-calendar-grid div[data-testid="stButton"] button {
        letter-spacing: 0.01em;
    }

    /* Selected date: primary Streamlit button */
    .calendar-grid button[data-testid="stBaseButton-primary"] {
        background: #1E3A5F !important;
        color: #FFFFFF !important;
        border: 2px solid #1E3A5F !important;
        font-weight: 700 !important;
        box-shadow: 0 3px 10px rgba(30, 58, 95, 0.18) !important;
    }

    .calendar-grid button[data-testid="stBaseButton-primary"]:hover {
        background: #1E3A5F !important;
        color: #FFFFFF !important;
    }

    /* Past dates */
    .past-date {
        height: 52px;
        border: 1px solid #F1F5F9;
        border-radius: 10px;
        background: #F8FAFC;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #CBD5E1;
        font-size: 0.88rem;
        font-weight: 500;
    }

    /* Weekday labels */
    .weekday {
        text-align: center;
        color: #64748B;
        font-size: 0.72rem;
        font-weight: 650;
        padding-bottom: 0.3rem;
    }

    .calendar-heading {
        text-align: center;
        color: #172033;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0.1rem 0 0.55rem 0;
    }

    /* Navigation */
    .nav-button div[data-testid="stButton"] button {
        min-height: 40px !important;
        height: 40px !important;
        border-radius: 8px !important;
        font-size: 1.15rem !important;
    }

    /* Refresh */
    .refresh-button div[data-testid="stButton"] button {
        min-height: 40px !important;
        height: 40px !important;
        border-radius: 8px !important;
    }

    /* Calendar legend */
    .calendar-legend {
        text-align: center;
        margin: 0.55rem 0 0.9rem 0;
        color: #64748B;
        font-size: 0.78rem;
    }

    /* Booking results */
    .booking-item {
        font-size: 0.95rem;
        line-height: 1.55;
        color: #334155;
        margin: 0.35rem 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 0.72rem;
        padding-top: 1.5rem;
        padding-bottom: 0.3rem;
    }

    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 0.4rem;
            padding-right: 0.4rem;
            padding-top: 0.65rem;
        }

        .st-key-calendar-grid [data-testid="stHorizontalBlock"],
        [data-testid="st-key-calendar-grid"] [data-testid="stHorizontalBlock"],
        .calendar-grid [data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: repeat(7, minmax(0, 1fr)) !important;
            gap: 0.16rem !important;
            width: 100% !important;
            max-width: 100% !important;
        }

        .st-key-calendar-grid [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
        .st-key-calendar-grid [data-testid="stHorizontalBlock"] > [data-testid="column"],
        [data-testid="st-key-calendar-grid"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
        [data-testid="st-key-calendar-grid"] [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            min-width: 0 !important;
            width: 100% !important;
            max-width: 100% !important;
            flex: none !important;
        }

        .calendar-grid div[data-testid="stButton"] button {
            min-height: 43px !important;
            height: 43px !important;
            border-radius: 7px !important;
            font-size: 0.73rem !important;
        }

        [class*="st-key-free-date-"] div[data-testid="stButton"] button::after {
            width: 13px;
            height: 13px;
            right: 6px;
        }

        .past-date {
            height: 43px;
            border-radius: 7px;
            font-size: 0.73rem;
        }

        .weekday {
            font-size: 0.59rem;
            padding-bottom: 0.2rem;
        }

        .calendar-heading {
            font-size: 1.02rem;
            margin-bottom: 0.4rem;
        }

        .booking-item {
            font-size: 0.88rem;
            line-height: 1.5;
        }

        .calendar-legend {
            font-size: 0.72rem;
            margin-top: 0.45rem;
        }

        .footer {
            font-size: 0.68rem;
        }
    }

    /* Very narrow phones */
    @media (max-width: 360px) {

        .block-container {
            padding-left: 0.22rem;
            padding-right: 0.22rem;
        }

        .st-key-calendar-grid [data-testid="stHorizontalBlock"],
        [data-testid="st-key-calendar-grid"] [data-testid="stHorizontalBlock"],
        .calendar-grid [data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: repeat(7, minmax(0, 1fr)) !important;
            gap: 0.08rem !important;
        }

        .st-key-calendar-grid [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
        .st-key-calendar-grid [data-testid="stHorizontalBlock"] > [data-testid="column"],
        [data-testid="st-key-calendar-grid"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
        [data-testid="st-key-calendar-grid"] [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            min-width: 0 !important;
            width: 100% !important;
            flex: none !important;
        }

        .calendar-grid div[data-testid="stButton"] button {
            min-height: 39px !important;
            height: 39px !important;
            border-radius: 6px !important;
            font-size: 0.68rem !important;
        }

        [class*="st-key-free-date-"] div[data-testid="stButton"] button::after {
            width: 11px;
            height: 11px;
            right: 5px;
        }

        .past-date {
            height: 39px;
            border-radius: 6px;
            font-size: 0.68rem;
        }

        .weekday {
            font-size: 0.54rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD GOOGLE SHEET
# ============================================================

@st.cache_data(ttl=300)
def load_data():
    csv_url = SHEET_URL.replace(
        "/edit",
        "/export?format=csv"
    )
    return pd.read_csv(csv_url)


# ============================================================
# CLEAN DATA
# ============================================================

def clean_data(df):

    df = df.copy()
    df = df.dropna(how="all")

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
    )

    # Google Sheet uses DD.MM.YY / DD.MM.YYYY-style dates.
    # dayfirst=True prevents ambiguous dates being interpreted
    # incorrectly by pandas.
    df["From_Date"] = pd.to_datetime(
        df["From_Date"],
        errors="coerce",
        dayfirst=True
    )

    df["To_Date"] = pd.to_datetime(
        df["To_Date"],
        errors="coerce",
        dayfirst=True
    )

    df["To_Date"] = df["To_Date"].fillna(
        df["From_Date"]
    )

    df["Status"] = (
        df["Status"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    return df


# ============================================================
# FACILITY NORMALIZATION
# ============================================================

def extract_facilities(text):

    text = str(text).lower()
    facilities = []

    if "room" in text:
        facilities.append("Rooms")

    if "lounge" in text:
        facilities.append("Lounge")

    if "lawn" in text:
        facilities.append("Lawn")

    if "a mess" in text:
        facilities.append("A Mess")

    if "b mess" in text:
        facilities.append("B Mess")

    if "m hall" in text:
        facilities.append("M Hall")

    return facilities


def normalize_bookings(df):

    records = []

    for _, row in df.iterrows():

        facilities = extract_facilities(
            row.get(
                "Facility_Rooms",
                ""
            )
        )

        if not facilities:
            facilities = [
                str(
                    row.get(
                        "Facility_Rooms",
                        "Other"
                    )
                )
            ]

        for facility in facilities:

            records.append(
                {
                    "Booking_No": row.get(
                        "Booking_No",
                        ""
                    ),
                    "From_Date": row.get(
                        "From_Date"
                    ),
                    "To_Date": row.get(
                        "To_Date"
                    ),
                    "Facility": facility,
                    "Officer_Event": row.get(
                        "Officer_Event",
                        ""
                    ),
                    "Status": row.get(
                        "Status",
                        ""
                    ),
                    "Confirmation": row.get(
                        "Confirmation",
                        ""
                    ),
                    "Remarks": row.get(
                        "Remarks",
                        ""
                    )
                }
            )

    return pd.DataFrame(records)


# ============================================================
# LOAD / PREPARE DATA
# ============================================================

try:

    raw_df = load_data()
    df = clean_data(raw_df)
    normalized_df = normalize_bookings(df)

except Exception as e:

    st.error(
        "Could not load the Google Sheet."
    )

    st.exception(e)
    st.stop()


# ============================================================
# TODAY
# ============================================================

today = date.today()


# ============================================================
# SESSION STATE
# ============================================================

if "calendar_year" not in st.session_state:
    st.session_state.calendar_year = today.year

if "calendar_month" not in st.session_state:
    st.session_state.calendar_month = today.month

if "selected_date" not in st.session_state:
    st.session_state.selected_date = today


# ============================================================
# ORIGINAL RECORDS AFFECTING A DATE
# ============================================================

def original_records_for_date(selected_date):

    selected = pd.Timestamp(selected_date)

    records = df[
        (df["From_Date"] <= selected)
        &
        (df["To_Date"] >= selected)
        &
        (
            df["Status"].isin(
                [
                    "Booked",
                    "Blocked"
                ]
            )
        )
    ].copy()

    return records


# ============================================================
# HEADER
# ============================================================

header_col, refresh_col = st.columns(
    [5.5, 1.5],
    vertical_alignment="center"
)

with header_col:

    st.title(
        "🏨 Officer Mess Chhawla"
    )

    st.caption(
        "Booking & Occupancy Calendar"
    )

with refresh_col:

    st.markdown(
        '<div class="refresh-button">',
        unsafe_allow_html=True
    )

    if st.button(
        "↻ Refresh",
        use_container_width=True,
        help="Fetch the latest bookings from Google Sheets"
    ):

        load_data.clear()
        st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# MONTH NAVIGATION
# ============================================================

previous_col, month_col, next_col = st.columns(
    [1, 5, 1]
)

with previous_col:

    st.markdown(
        '<div class="nav-button">',
        unsafe_allow_html=True
    )

    if st.button(
        "‹",
        use_container_width=True,
        key="previous_month"
    ):

        if st.session_state.calendar_month == 1:

            st.session_state.calendar_month = 12
            st.session_state.calendar_year -= 1

        else:

            st.session_state.calendar_month -= 1

        st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


with month_col:

    month_name = calendar.month_name[
        st.session_state.calendar_month
    ]

    st.markdown(
        f"""
        <div class="calendar-heading">
            {month_name} {st.session_state.calendar_year}
        </div>
        """,
        unsafe_allow_html=True
    )


with next_col:

    st.markdown(
        '<div class="nav-button">',
        unsafe_allow_html=True
    )

    if st.button(
        "›",
        use_container_width=True,
        key="next_month"
    ):

        if st.session_state.calendar_month == 12:

            st.session_state.calendar_month = 1
            st.session_state.calendar_year += 1

        else:

            st.session_state.calendar_month += 1

        st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# CALENDAR
# ============================================================

weekdays = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun"
]

month_calendar = calendar.monthcalendar(
    st.session_state.calendar_year,
    st.session_state.calendar_month
)


# The calendar is wrapped in a keyed Streamlit container.
# CSS forces every horizontal week row to remain exactly
# seven columns even on narrow mobile screens.

with st.container(key="calendar-grid"):

    # --------------------------------------------------------
    # WEEKDAY HEADERS
    # --------------------------------------------------------

    header_cols = st.columns(
        7,
        gap="small"
    )

    for i, weekday in enumerate(weekdays):

        with header_cols[i]:

            st.markdown(
                f"""
                <div class="weekday">
                    {weekday}
                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # DATE GRID
    # --------------------------------------------------------

    for week_index, week in enumerate(month_calendar):

        cols = st.columns(
            7,
            gap="small"
        )

        for i, day_number in enumerate(week):

            with cols[i]:

                # Empty calendar cell
                if day_number == 0:

                    st.markdown(
                        '<div style="height:52px;"></div>',
                        unsafe_allow_html=True
                    )

                    continue


                current_date = date(
                    st.session_state.calendar_year,
                    st.session_state.calendar_month,
                    day_number
                )


                # ------------------------------------------------
                # PAST DATE
                # ------------------------------------------------

                if current_date < today:

                    st.markdown(
                        f"""
                        <div class="past-date">
                            {day_number}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    continue


                # ------------------------------------------------
                # DATE STATUS
                # ------------------------------------------------

                date_records = (
                    original_records_for_date(
                        current_date
                    )
                )

                is_free = date_records.empty

                is_selected = (
                    current_date
                    ==
                    st.session_state.selected_date
                )


                # ------------------------------------------------
                # BUTTON LABEL
                #
                # Green dot is part of the button itself.
                # ------------------------------------------------

                button_label = str(day_number)


                # ------------------------------------------------
                # SELECTED DATE
                #
                # type="primary" gives the selected date a
                # persistent native Streamlit highlight.
                # ------------------------------------------------

                # Give free dates a dedicated keyed wrapper so the
                # green marker can be drawn inside the date button.
                cell_key = (
                    f"free-date-{current_date}"
                    if is_free
                    else f"date-cell-{current_date}"
                )

                with st.container(key=cell_key):

                    if st.button(
                        button_label,
                        key=f"date_{current_date}",
                        use_container_width=True,
                        type=(
                            "primary"
                            if is_selected
                            else "secondary"
                        )
                    ):

                        st.session_state.selected_date = (
                            current_date
                        )

                        st.rerun()


# ============================================================
# CALENDAR LEGEND
# ============================================================

st.markdown(
    """
    <div class="calendar-legend">
        🟢 <strong>Fully available</strong>
        &nbsp;·&nbsp;
        No Booked or Blocked booking affects this date
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SELECTED DATE RESULTS
# ============================================================

selected_date = (
    st.session_state.selected_date
)

st.divider()

st.subheader(
    f"Availability for "
    f"{selected_date.strftime('%d %B %Y')}"
)


selected_records = (
    original_records_for_date(
        selected_date
    )
)


# ============================================================
# DISPLAY BOOKING RESULTS
# ============================================================

if selected_records.empty:

    st.success(
        "No bookings or blocks for this date."
    )

else:

    total_records = len(
        selected_records
    )

    for index, (_, row) in enumerate(
        selected_records.iterrows(),
        start=1
    ):

        facility_text = str(
            row.get(
                "Facility_Rooms",
                ""
            )
        ).strip()

        officer_event = str(
            row.get(
                "Officer_Event",
                ""
            )
        ).strip()

        status = str(
            row.get(
                "Status",
                ""
            )
        ).strip()

        from_date = row.get(
            "From_Date"
        )

        to_date = row.get(
            "To_Date"
        )

        start_text = (
            from_date.strftime(
                "%d.%m.%Y"
            )
            if pd.notna(from_date)
            else ""
        )

        end_text = (
            to_date.strftime(
                "%d.%m.%Y"
            )
            if pd.notna(to_date)
            else start_text
        )

        if facility_text and officer_event:

            description = (
                f"{facility_text} for "
                f"{officer_event}"
            )

        elif facility_text:

            description = facility_text

        elif officer_event:

            description = officer_event

        else:

            description = "Mess booking"


        # ----------------------------------------------------
        # NATIVE STREAMLIT MARKDOWN ONLY
        # No HTML spans or raw HTML in booking content.
        # ----------------------------------------------------

        if status.lower() == "blocked":

            st.markdown(
                f"**{index}.** "
                f"{description} "
                f"**:orange[(Blocked)]** "
                f"wef {start_text} "
                f"to {end_text}"
            )

        elif status.lower() == "booked":

            st.markdown(
                f"**{index}.** "
                f"{description} "
                f"**:red[(Booked)]** "
                f"wef {start_text} "
                f"to {end_text}"
            )

        else:

            st.markdown(
                f"**{index}.** "
                f"{description} "
                f"**({status})** "
                f"wef {start_text} "
                f"to {end_text}"
            )


        if index < total_records:
            st.divider()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Built by Rohit Kumar, Asstt Comdt
    </div>
    """,
    unsafe_allow_html=True
)

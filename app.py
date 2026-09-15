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
        padding-top: 1.2rem;
        padding-bottom: 1rem;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }


    /* ========================================================
       CALENDAR HEADING
       ======================================================== */

    .calendar-heading {
        text-align: center;
        color: #172033;
        font-size: 1.25rem;
        font-weight: 650;
        margin: 0.2rem 0 0.8rem 0;
    }


    /* ========================================================
       WEEKDAY HEADINGS
       ======================================================== */

    .weekday {
        text-align: center;
        color: #64748B;
        font-size: 0.72rem;
        font-weight: 650;
        padding-bottom: 0.35rem;
    }


    /* ========================================================
       CALENDAR DATE BUTTONS
       ======================================================== */

    div[data-testid="stButton"] button {
        min-height: 52px !important;
        height: 52px !important;
        border-radius: 10px !important;
        border: 1px solid #E2E8F0 !important;
        background: #FFFFFF !important;
        color: #334155 !important;
        font-size: 0.88rem !important;
        font-weight: 550 !important;
        transition: all 0.15s ease;
    }

    div[data-testid="stButton"] button:hover {
        border-color: #94A3B8 !important;
        background: #F8FAFC !important;
        transform: translateY(-1px);
    }


    /* ========================================================
       MONTH NAVIGATION
       ======================================================== */

    .nav-button div[data-testid="stButton"] button {
        min-height: 40px !important;
        height: 40px !important;
        border-radius: 8px !important;
        font-size: 1.2rem !important;
    }


    /* ========================================================
       SELECTED DATE
       ======================================================== */

    button[data-testid="stBaseButton-primary"] {
        background: #1E3A5F !important;
        color: #FFFFFF !important;
        border: 2px solid #1E3A5F !important;
        font-weight: 700 !important;
        box-shadow: 0 3px 10px rgba(30, 58, 95, 0.18);
    }

    button[data-testid="stBaseButton-primary"]:hover {
        background: #1E3A5F !important;
        color: #FFFFFF !important;
    }


    /* ========================================================
       TODAY
       ======================================================== */


    /* ========================================================
       PAST DATES
       ======================================================== */

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
    }


    /* ========================================================
       REFRESH BUTTON
       ======================================================== */

    div[data-testid="stButton"] button[kind="secondary"] {
        border-radius: 9px !important;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 0.35rem;
            padding-right: 0.35rem;
            padding-top: 0.7rem;
        }

        .calendar-heading {
            font-size: 1.05rem;
        }

        .weekday {
            font-size: 0.62rem;
        }

        div[data-testid="stButton"] button {
            min-height: 44px !important;
            height: 44px !important;
            border-radius: 8px !important;
            font-size: 0.75rem !important;
            padding: 0 !important;
        }

        .past-date {
            height: 44px;
            border-radius: 8px;
            font-size: 0.75rem;
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

    # --------------------------------------------------------
    # DATE COLUMNS
    # --------------------------------------------------------

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

    # If To_Date is empty, treat it as a single-day booking.

    df["To_Date"] = df["To_Date"].fillna(
        df["From_Date"]
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    df["Status"] = (
        df["Status"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    return df


# ============================================================
# FACILITY NORMALIZATION
#
# Kept for existing booking/facility logic.
# Displayed results still use ORIGINAL rows.
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
# LOAD DATA
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
#
# IMPORTANT:
# This works on ORIGINAL Google Sheet rows.
# Therefore one original row remains one displayed item.
# ============================================================

def original_records_for_date(selected_date):

    selected = pd.Timestamp(
        selected_date
    )

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

header_col, refresh_col = st.columns([6, 1], vertical_alignment="center")

with header_col:
    st.title(
        "🏨 Officer Mess Chhawla"
    )

    st.caption(
        "Booking & Occupancy Calendar"
    )

with refresh_col:
    if st.button(
        "↻ Refresh",
        use_container_width=True,
        help="Fetch the latest bookings from Google Sheets"
    ):
        load_data.clear()
        st.rerun()


# ============================================================
# MONTH NAVIGATION
# ============================================================

previous_col, month_col, next_col = st.columns(
    [1, 5, 1]
)


# ------------------------------------------------------------
# PREVIOUS MONTH
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# MONTH/YEAR
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# NEXT MONTH
# ------------------------------------------------------------

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
# WEEKDAY HEADERS
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

header_cols = st.columns(7)

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


# ============================================================
# CALENDAR
# ============================================================

month_calendar = calendar.monthcalendar(
    st.session_state.calendar_year,
    st.session_state.calendar_month
)


for week in month_calendar:

    cols = st.columns(7)

    for i, day_number in enumerate(week):

        with cols[i]:

            # ------------------------------------------------
            # EMPTY CELL
            # ------------------------------------------------

            if day_number == 0:

                st.write("")

                continue


            # ------------------------------------------------
            # CURRENT DATE
            # ------------------------------------------------

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
            # CHECK WHETHER DATE IS COMPLETELY FREE
            #
            # A date is free only when there are ZERO
            # Booked/Blocked original rows overlapping it.
            # ------------------------------------------------

            date_records = original_records_for_date(
                current_date
            )

            # ------------------------------------------------
            # DATE STATE
            # ------------------------------------------------

            is_selected = (
                current_date
                ==
                st.session_state.selected_date
            )

            # A green dot is shown ONLY for future dates with
            # absolutely no Booked or Blocked record affecting them.
            is_free_future_date = (
                current_date > today
                and date_records.empty
            )

            # ------------------------------------------------
            # DATE BUTTON
            # ------------------------------------------------

            # The green indicator is part of the button label,
            # so it stays INSIDE the date block.
            if is_free_future_date:
                button_label = f"{day_number}  🟢"
            else:
                button_label = str(day_number)

            if st.button(
                button_label,
                key=f"date_{current_date}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):

                st.session_state.selected_date = current_date

                st.rerun()


# ============================================================
# GREEN DOT EXPLANATION
# ============================================================

st.markdown(
    """
    <div class="availability-note">
        🟢 <strong>Fully available</strong>
        &nbsp;·&nbsp;
        No Booked or Blocked booking affects this date
    </div>
    """,
    unsafe_allow_html=True,
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


# ============================================================
# ORIGINAL BOOKINGS/BLOCKS
# ============================================================

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

        if status.casefold() == "blocked":
            status_text = "**:orange[(Blocked)]**"
        elif status.casefold() == "booked":
            status_text = "**:red[(Booked)]**"
        else:
            status_text = f"**({status})**"

        st.markdown(
            f"**{index}.** {description} "
            f"{status_text} wef {start_text} to {end_text}"
        )

        if index < len(selected_records):
            st.divider()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Built by Rohit Kumar, Asstt Comdt"
)
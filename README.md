# Officer Mess Chhawla — Booking & Occupancy Dashboard

A lightweight Streamlit dashboard for viewing upcoming Officer Mess Chhawla bookings and blocks through an interactive calendar.

## Features

- Interactive monthly calendar
- Future-date selection
- Selected date highlighting
- 🟢 Green indicator for completely available future dates
- Booking/block details shown immediately below the calendar
- Preserves original Google Sheet booking descriptions
- Supports multi-day bookings
- Automatically checks date overlaps
- Live Google Sheet data source
- Manual refresh button for latest data
- Mobile-friendly interface
- Simple, professional UI

## How It Works

The dashboard uses the Google Sheet as its live data source.

```text
Google Sheet
     ↓
Streamlit Dashboard
     ↓
Interactive Calendar
     ↓
Select a Date
     ↓
View Bookings / Blocks
```

A future date receives a green indicator when there are **no Booked or Blocked records overlapping that date**.

If one or more bookings/blocks affect a date, no green indicator is shown. Selecting the date displays the relevant records below the calendar.

## Data Source

The application reads booking information directly from the configured Google Sheet.

The Google Sheet should remain publicly viewable so that the deployed Streamlit application can read the data.

Do not hard-code booking information into `app.py`.

## Expected Data

The application expects the Google Sheet to contain the existing booking fields used by the dashboard, including:

- `From_Date`
- `To_Date`
- `Facility_Rooms`
- `Officer_Event`
- `Status`

Additional columns may be present as supported by the existing application.

### Booking Status

The dashboard currently considers these statuses when determining occupancy:

- `Booked`
- `Blocked`

## Running Locally

### 1. Install Python

Install Python 3.10+ if it is not already installed.

### 2. Install dependencies

```bash
pip install streamlit pandas
```

### 3. Run the dashboard

From the repository folder:

```bash
streamlit run app.py
```

The dashboard will open in your browser.

## Deployment

This application can be deployed using **Streamlit Community Cloud**.

Basic deployment flow:

```text
GitHub Repository
        ↓
Streamlit Community Cloud
        ↓
Live Dashboard URL
```

Select:

- Repository: this repository
- Main file: `app.py`

## Updating Bookings

Bookings do not need to be added to the Python code.

To add a booking:

1. Open the Google Sheet.
2. Add the booking as a new row.
3. The row does not need to be in chronological order.
4. Save the Google Sheet.
5. Open the dashboard.
6. Click **↻ Refresh**.

The dashboard will reload the latest Google Sheet data.

## Project Structure

```text
officer-mess-chhawla/
│
├── app.py
└── README.md
```

## Design Principle

The dashboard is intentionally focused on one task:

> **CLICK DATE → SEE BOOKINGS/BLOCKS AFFECTING THAT DATE**

It does not include unnecessary analytics, charts, KPIs, filters, or administrative features.

## Author

**Rohit Kumar, Asstt Comdt**

Officer Mess Chhawla Booking & Occupancy Dashboard

import os
import re
from datetime import datetime, timedelta

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def extract_dates(text):
    """
    Extracts date-like strings from user input.
    Currently supports:
      - 'YYYY-MM-DD'
      - 'DD/MM/YYYY' or 'MM/DD/YYYY'
      - 'Month DD' (e.g., March 15)
      - Relative terms: 'today', 'tomorrow', 'next Monday', etc. (limited)
    Returns a list of date strings in 'YYYY-MM-DD' format if possible.
    """
    # Pattern for YYYY-MM-DD
    iso_dates = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", text)
    if iso_dates:
        return iso_dates

    # Pattern for DD/MM/YYYY or MM/DD/YYYY
    slash_dates = re.findall(r"\b\d{1,2}/\d{1,2}/\d{4}\b", text)
    result_dates = []
    for d in slash_dates:
        parts = d.split("/")
        # Try both DD/MM/YYYY and MM/DD/YYYY
        for fmt in ("%d/%m/%Y", "%m/%d/%Y"):
            try:
                dt = datetime.strptime(d, fmt)
                result_dates.append(dt.strftime("%Y-%m-%d"))
                break
            except ValueError:
                continue

    # "March 15" or "15 March"
    month_day = re.findall(r"\b([A-Za-z]+)\s(\d{1,2})\b", text)
    for mon, day in month_day:
        try:
            dt = datetime.strptime(f"{mon} {day} {datetime.now().year}", "%B %d %Y")
            result_dates.append(dt.strftime("%Y-%m-%d"))
        except ValueError:
            continue

    # Relative dates: today, tomorrow, next Monday, etc.
    text = text.lower()
    today = datetime.now()
    if "today" in text:
        result_dates.append(today.strftime("%Y-%m-%d"))
    if "tomorrow" in text:
        result_dates.append((today + timedelta(days=1)).strftime("%Y-%m-%d"))
    days_of_week = [
        "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
    ]
    for idx, day in enumerate(days_of_week):
        if f"next {day}" in text:
            days_ahead = (idx - today.weekday() + 7) % 7
            if days_ahead == 0:
                days_ahead = 7
            result_dates.append((today + timedelta(days=days_ahead)).strftime("%Y-%m-%d"))
        elif day in text and f"next {day}" not in text:
            # This week (or today if matches)
            days_ahead = (idx - today.weekday()) % 7
            result_dates.append((today + timedelta(days=days_ahead)).strftime("%Y-%m-%d"))

    # ISO dates first, then others
    return iso_dates + result_dates

def validate_date(date_str):
    """
    Checks if a date string is valid and in the future.
    Returns True/False.
    """
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.date() >= datetime.now().date()
    except Exception:
        return False

def parse_int_from_text(text):
    """
    Extracts the first integer from a string.
    Returns int or None.
    """
    match = re.search(r"\b\d+\b", text)
    return int(match.group()) if match else None
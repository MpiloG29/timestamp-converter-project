from datetime import datetime

import numpy as np
import pandas as pd


def convert_date(timestamp_string):
    """
    Implement a function to take in a string timestamp and convert that to an encoded string.
    Input strings are in the following format 'YYYY-MM-DD HH:MM:SS'

    The output string is in 4 components:
        1. Shift  (A, B or C)
            Shift A is between the hours of 07:00 to 15:00(exclusive)
            Shift B ""                   "" 15:00 to 23:00(exclusive)
            Shift C ""                   "" 23:00 to 07:00(exclusive)

        2. Day of month in two digits e.g. (01, 02, ..., 31)

        3. Month encoded as a letter:
            Jan -> 'A'
            Feb -> 'B'
            Mar -> 'C'
            *NB the letters used to replace the months of January to December skip 'I'
            [ABCDEFGHJKLM]

        4 Last two digits of the year:
            2019 -> 19

    Examples
    --------
    >>> convert_date('2019-07-15 22:03:16')
    'B15G19'
    
    >>> convert_date('2015-01-05 07:00:01')
    'A05A15'
    
    >>> convert_date('2021-05-02 11:20:01')
    'A02E21'
    
    >>> convert_date('2023-12-25 23:30:00')
    'C25M23'

    Parameters:
    ----------
    timestamp_string : str
        A string timestamp in the format 'YYYY-MM-DD HH:MM:SS'

    Returns:
    -------
    str
        Encoded timestamp string in format: Shift + Day + MonthLetter + YearLastTwoDigits
    
    Raises:
    ------
    ValueError
        If the input string is not in the correct format
    """
    # Parse the timestamp string
    dt = datetime.strptime(timestamp_string, '%Y-%m-%d %H:%M:%S')
    
    # 1. Determine shift
    hour = dt.hour
    if 7 <= hour < 15:
        shift = 'A'
    elif 15 <= hour < 23:
        shift = 'B'
    else:  # 23:00-06:59 or hour == 23
        shift = 'C'
    
    # 2. Day of month in two digits
    day_str = f"{dt.day:02d}"
    
    # 3. Month encoded as a letter (skipping 'I')
    # Define mapping for months to letters
    month_mapping = {
        1: 'A',   # January
        2: 'B',   # February
        3: 'C',   # March
        4: 'D',   # April
        5: 'E',   # May
        6: 'F',   # June
        7: 'G',   # July
        8: 'H',   # August
        9: 'J',   # September (skipping I)
        10: 'K',  # October
        11: 'L',  # November
        12: 'M'   # December
    }
    month_letter = month_mapping[dt.month]
    
    # 4. Last two digits of year
    year_str = f"{dt.year % 100:02d}"
    
    # Combine all components
    return f"{shift}{day_str}{month_letter}{year_str}"

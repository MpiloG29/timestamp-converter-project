import pytest
from datetime_converter import convert_date


def test_convert_date():
    """Test cases for convert_date function"""
    
    # Test case 1: Example from documentation
    assert convert_date('2019-07-15 22:03:16') == 'B15G19'
    
    # Test case 2: Example from documentation
    assert convert_date('2015-01-05 07:00:01') == 'A05A15'
    
    # Test case 3: Example from documentation
    assert convert_date('2021-05-02 11:20:01') == 'A02E21'
    
    # Additional test cases
    
    # Test shift boundaries
    # Shift A: 07:00 to 14:59
    assert convert_date('2021-01-01 07:00:00') == 'A01A21'
    assert convert_date('2021-01-01 14:59:59') == 'A01A21'
    
    # Shift B: 15:00 to 22:59
    assert convert_date('2021-01-01 15:00:00') == 'B01A21'
    assert convert_date('2021-01-01 22:59:59') == 'B01A21'
    
    # Shift C: 23:00 to 06:59
    assert convert_date('2021-01-01 23:00:00') == 'C01A21'
    assert convert_date('2021-01-01 06:59:59') == 'C01A21'
    
    # Test month encoding (skipping I)
    test_months = [
        ('2021-01-15 12:00:00', 'A15A21'),  # January -> A
        ('2021-02-15 12:00:00', 'A15B21'),  # February -> B
        ('2021-03-15 12:00:00', 'A15C21'),  # March -> C
        ('2021-04-15 12:00:00', 'A15D21'),  # April -> D
        ('2021-05-15 12:00:00', 'A15E21'),  # May -> E
        ('2021-06-15 12:00:00', 'A15F21'),  # June -> F
        ('2021-07-15 12:00:00', 'A15G21'),  # July -> G
        ('2021-08-15 12:00:00', 'A15H21'),  # August -> H
        ('2021-09-15 12:00:00', 'A15J21'),  # September -> J (skip I)
        ('2021-10-15 12:00:00', 'A15K21'),  # October -> K
        ('2021-11-15 12:00:00', 'A15L21'),  # November -> L
        ('2021-12-15 12:00:00', 'A15M21'),  # December -> M
    ]
    
    for timestamp, expected in test_months:
        assert convert_date(timestamp) == expected, f"Failed for {timestamp}"
    
    # Test day formatting
    assert convert_date('2021-12-01 12:00:00') == 'A01M21'  # Single digit day
    assert convert_date('2021-12-31 12:00:00') == 'A31M21'  # Double digit day
    
    # Test year formatting
    assert convert_date('2000-01-01 12:00:00') == 'A01A00'  # Year 2000
    assert convert_date('1999-01-01 12:00:00') == 'A01A99'  # Year 1999
    assert convert_date('2022-01-01 12:00:00') == 'A01A22'  # Year 2022
    
    # Test edge cases
    assert convert_date('2023-12-31 23:59:59') == 'C31M23'  # End of year
    assert convert_date('2023-01-01 00:00:00') == 'C01A23'  # Start of year
    
    print("✓ All tests passed!")


if __name__ == "__main__":
    test_convert_date()

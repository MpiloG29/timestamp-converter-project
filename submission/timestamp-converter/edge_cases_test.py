from datetime_converter import convert_date

print("Edge Cases Test")
print("=" * 60)

edge_cases = [
    # Boundary times
    ('2023-01-01 00:00:00', 'C01A23'),  # Midnight
    ('2023-01-01 06:59:59', 'C01A23'),  # Just before shift A
    ('2023-01-01 07:00:00', 'A01A23'),  # Start of shift A
    ('2023-01-01 14:59:59', 'A01A23'),  # Just before shift B
    ('2023-01-01 15:00:00', 'B01A23'),  # Start of shift B
    ('2023-01-01 22:59:59', 'B01A23'),  # Just before shift C
    ('2023-01-01 23:00:00', 'C01A23'),  # Start of shift C
    
    # Month boundaries
    ('2023-01-31 12:00:00', 'A31A23'),  # End of January
    ('2023-02-28 12:00:00', 'A28B23'),  # End of February (non-leap)
    ('2024-02-29 12:00:00', 'A29B24'),  # End of February (leap year)
    ('2023-03-31 12:00:00', 'A31C23'),  # End of March
    ('2023-04-30 12:00:00', 'A30D23'),  # End of April
    ('2023-12-31 12:00:00', 'A31M23'),  # End of December
    
    # Year boundaries
    ('2023-12-31 23:59:59', 'C31M23'),  # Last second of year
    ('2024-01-01 00:00:00', 'C01A24'),  # First second of new year
    
    # Month encoding verification
    ('2023-01-15 12:00:00', 'A15A23'),  # Jan -> A
    ('2023-09-15 12:00:00', 'A15J23'),  # Sep -> J (skipping I)
    ('2023-12-15 12:00:00', 'A15M23'),  # Dec -> M
]

print(f"{'Timestamp':<25} {'Expected':<10} {'Got':<10} {'Status':<6}")
print("-" * 60)

all_passed = True
for timestamp, expected in edge_cases:
    try:
        result = convert_date(timestamp)
        status = "✓" if result == expected else "✗"
        if result != expected:
            all_passed = False
        print(f"{timestamp:<25} {expected:<10} {result:<10} {status:<6}")
    except Exception as e:
        print(f"{timestamp:<25} {expected:<10} ERROR: {e}")
        all_passed = False

print("=" * 60)
if all_passed:
    print("✅ All edge cases passed!")
else:
    print("❌ Some edge cases failed!")

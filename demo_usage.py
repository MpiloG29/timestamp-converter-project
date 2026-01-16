from datetime_converter import convert_date

print("Timestamp Converter Demo")
print("=" * 50)

# Examples from the documentation
examples = [
    '2019-07-15 22:03:16',
    '2015-01-05 07:00:01',
    '2021-05-02 11:20:01',
    '2023-12-25 23:30:00',
    '2023-06-15 14:59:59',  # Just before shift B
    '2023-06-15 15:00:00',  # Start of shift B
    '2023-06-15 22:59:59',  # Just before shift C
    '2023-06-15 23:00:00',  # Start of shift C
    '2023-06-15 06:59:59',  # Just before shift A
]

print(f"{'Input Timestamp':<25} {'Output':<10} {'Shift':<5}")
print("-" * 50)
for timestamp in examples:
    result = convert_date(timestamp)
    shift = result[0]
    shift_desc = {
        'A': '07:00-15:00',
        'B': '15:00-23:00', 
        'C': '23:00-07:00'
    }[shift]
    print(f"{timestamp:<25} {result:<10} {shift_desc:<5}")

print("\nMonth Encoding Examples:")
print("-" * 50)
# Show all months
for month in range(1, 13):
    timestamp = f'2023-{month:02d}-15 12:00:00'
    result = convert_date(timestamp)
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    print(f"{month_names[month-1]:<12} -> {result[3]} (as in {result})")

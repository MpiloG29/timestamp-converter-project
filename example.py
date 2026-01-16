from datetime_converter import convert_date

# Test the examples from the documentation
examples = [
    '2019-07-15 22:03:16',
    '2015-01-05 07:00:01',
    '2021-05-02 11:20:01',
    '2023-12-25 23:30:00',
    '2023-06-15 14:59:59',
    '2023-06-15 15:00:00',
]

print("Timestamp Converter Examples:")
print("-" * 40)
for timestamp in examples:
    result = convert_date(timestamp)
    print(f"{timestamp} -> {result}")
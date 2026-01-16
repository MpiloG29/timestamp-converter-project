from datetime_converter import convert_date

print("Interactive Timestamp Converter")
print("=" * 50)
print("Enter timestamps in format: YYYY-MM-DD HH:MM:SS")
print("Type 'quit' to exit")
print("=" * 50)

while True:
    user_input = input("\nEnter timestamp: ").strip()
    
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("Goodbye!")
        break
    
    if user_input.lower() == 'now':
        from datetime import datetime
        user_input = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Using current time: {user_input}")
    
    try:
        result = convert_date(user_input)
        print(f"Result: {result}")
        
        # Break down the result
        print(f"  Shift: {result[0]} ", end="")
        if result[0] == 'A':
            print("(07:00 to 15:00)")
        elif result[0] == 'B':
            print("(15:00 to 23:00)")
        else:
            print("(23:00 to 07:00)")
        
        print(f"  Day: {result[1:3]}")
        
        month_map = {
            'A': 'January', 'B': 'February', 'C': 'March',
            'D': 'April', 'E': 'May', 'F': 'June',
            'G': 'July', 'H': 'August', 'J': 'September',
            'K': 'October', 'L': 'November', 'M': 'December'
        }
        print(f"  Month: {result[3]} ({month_map.get(result[3], 'Unknown')})")
        print(f"  Year: 20{result[4:6]}")
        
    except ValueError as e:
        print(f"Error: Invalid format! Use: YYYY-MM-DD HH:MM:SS")
        print(f"Example: 2023-12-25 14:30:00")
    except Exception as e:
        print(f"Error: {e}")

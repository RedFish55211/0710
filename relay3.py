from datetime import time

# Create a time object for 2:30:00 AM
t1 = time(hour=2, minute=30)

# Create a time object for 15:45:30 with 500 microseconds
t2 = time(hour=15, minute=45, second=30, microsecond=500)

# Create a time object for 9:15:00 AM with timezone information (Eastern Time)
from datetime import timezone, timedelta
tzinfo = timezone(timedelta(hours=-5))  # UTC-5 (Eastern Time)
t3 = time(hour=9, minute=15, tzinfo=tzinfo)

print(t1)  # Output: 02:30:00
print(t2)  # Output: 15:45:30.000500
print(t3)  # Output: 09:15:00-05:00 (with timezone information)

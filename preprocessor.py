
import re
import pandas as pd

def preprocess(data):
    # Pattern to extract dates and times, handling both two-digit and four-digit years
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # Split the data based on the pattern (which finds date-time stamps)
    messages = re.split(pattern, data)[1:]  # Skip the first element, which is not a message
    dates = re.findall(pattern, data)  # Extract date-time stamps

    # Create a DataFrame with messages and corresponding dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date to datetime, handling two-digit and four-digit years
    df['message_date'] = pd.to_datetime(
        df['message_date'], 
        format='%d/%m/%y, %H:%M - ',  # Handle two-digit year
        dayfirst=True,                # Interpret day first
        errors='coerce'               # Coerce invalid formats to NaT
    )

    # Rename message_date to date
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Initialize lists for users and messages
    users = []
    messages = []

    # Extract user names and messages
    for message in df['user_message']:
        # Split message based on username pattern (username: message)
        entry = re.split(r'([\w\W]+?):\s', message)
        
        # If the message is from a user (not a system notification)
        if entry[1:]:
            users.append(entry[1])  # Username
            messages.append(" ".join(entry[2:]))  # Message content
        else:
            users.append('group_notification')  # System message (no user)
            messages.append(entry[0])  # Whole message is the system message

    # Add user and message columns to the DataFrame
    df['user'] = users
    df['message'] = messages

    # Drop the temporary 'user_message' column
    df.drop(columns=['user_message'], inplace=True)

    # Add date and time components for further analysis
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Generate time periods (e.g., "23-00", "00-01")
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-01")
        else:
            period.append(f"{hour}-{hour + 1}")

    df['period'] = period

    return df

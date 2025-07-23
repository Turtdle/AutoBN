import subprocess
import datetime

def set_system_time_ahead(hours):
    try:
        # Get current time and add the specified hours
        current_time = datetime.datetime.now()
        new_time = current_time + datetime.timedelta(hours=hours)
        
        # Format time for Windows time command (HH:MM:SS)
        time_str = new_time.strftime("%H:%M:%S")
        
        # Set the system time
        result = subprocess.run(['time', time_str], 
                              capture_output=True, 
                              text=True, 
                              shell=True)
        
        if result.returncode == 0:
            print(f"System time successfully changed to: {time_str}")
        else:
            print(f"Failed to change system time: {result.stderr}")
            
    except Exception as e:
        print(f"Error: {e}")

# Change system time 7 hours ahead
set_system_time_ahead(5)
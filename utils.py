import pytz

def convert_utc_to_local(utc_dt, timezone_str):
    if utc_dt.tzinfo is None:  
        utc_dt = pytz.utc.localize(utc_dt)
    
    local_tz = pytz.timezone(timezone_str)
    return utc_dt.astimezone(local_tz)

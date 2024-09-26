from datetime import timedelta

def calculate_uptime_downtime(polls, business_hours, time_delta):
    total_uptime = timedelta()
    total_downtime = timedelta()

    polls.sort(key=lambda x: x.timestamp_utc)

    if polls:
        start_time = polls[-1].timestamp_utc - time_delta
    else:
        return total_uptime, total_downtime

    relevant_polls = [poll for poll in polls if poll.timestamp_utc >= start_time]

    if not relevant_polls:
        return total_uptime, total_downtime

    for i in range(1, len(relevant_polls)):
        prev_poll = relevant_polls[i - 1]
        current_poll = relevant_polls[i]

        time_delta_between = current_poll.timestamp_utc - prev_poll.timestamp_utc

        if prev_poll.status == 'active': 
            total_uptime += time_delta_between
        else:
            total_downtime += time_delta_between

    return total_uptime, total_downtime

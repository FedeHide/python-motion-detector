from datetime import datetime


def handle_state_change(status_list, times, status):
    """
    handle state change between 'motion detected' and 'no motion'.
    Saves the time when the state change occurs.

    Args:
        status_list (list): list of states (0 or 1).
        times (list): list of times when the state change occurs.
        status (int): current state (0 or 1).

    Returns:
        tuple: updated status_list and times.
    """
    if len(status_list) > 1:
        if status == 1 and status_list[-2] == 0:
            times.append(datetime.now())
        elif status == 0 and status_list[-2] == 1:
            times.append(datetime.now())

    status_list.append(status)

    return status_list, times

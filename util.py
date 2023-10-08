def abs_time(years, days, hours, mins):
    return years + days / 365 + hours / 24 / 365 + mins / 24 / 60 / 365

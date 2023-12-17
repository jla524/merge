from merge.process import hours


def historical() -> None:
    members = hours.get_active_members()
    timecards = hours.get_timecards(members, days=1460)
    hours_detail = hours.get_hours_detail(timecards)
    hours.send_hours_detail(hours_detail)


def weekly() -> None:
    members = hours.get_active_members()
    timecards = hours.get_timecards(members, days=7)
    live_hours = hours.get_live_hours(timecards)
    hours.send_live_hours(live_hours)


if __name__ == "__main__":
    weekly()

from merge.process import hours


def historical() -> None:
    members = hours.get_active_members()
    timecards = hours.get_timecards(members, days=1460)
    hours_detail = hours.get_hours_detail(timecards)
    opportunities = hours.get_current_opportunities()
    hours.send_hours_detail(hours_detail)


def weekly() -> None:
    members = hours.get_active_members()
    #timecards = hours.get_timecards(members, days=7)
    timecards = hours.get_timecards(members, days=60)  # temporary
    timecards = hours.impute_signout_time(timecards)
    live_hours = hours.get_live_hours(timecards)
    hours.send_live_hours(live_hours)


if __name__ == "__main__":
    weekly()

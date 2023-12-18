from datetime import datetime, timedelta
from merge import Config
from merge.api.ragic import Ragic
from merge.api.opentimeclock import OpenTimeClock
from merge.common.helpers import JSON
from merge.common.enums import HoursDetail, LiveHours
from merge.logger.pkg_logger import Logger


def get_active_members() -> list[JSON]:
    ragic = Ragic()
    route = Config.ragic_attendance_route()
    result = ragic.get_data(route).json()
    entries = []
    for record in result.values():
        if record["Timeclock Status"] == "Open":
            Logger.info(f"Found active member {str(record)}")
            entries.append(record)
    return entries


def get_timecards(members: list[JSON], days: int = 7) -> list[JSON]:
    open_time_clock = OpenTimeClock()
    entries = []
    for member in members:
        route = Config.otc_timecards_route()
        start_time = datetime.today() - timedelta(days=days)
        params = {
            "nextRecord": 0,
            "dateTimeFrom": start_time.strftime("%Y-%m-%d %H:%m:%S"),
            "dateTimeTo": datetime.today().isoformat(),
            "userFullName": member["Full Name2"],
        }
        result = open_time_clock.get_data(route, params).json()
        for record in result.get("data", []):
            if record["employeeNumber"] == member["Membership ID"]:
                Logger.info(f"Found matching timecard {str(record)}")
                entries.append({**member, **record})
    return entries


def get_hours_detail(data: list[JSON]) -> list[JSON]:
    entries = []
    for row in data:
        entry = {
            HoursDetail.EMPLOYEE_NUMBER: row["employeeNumber"],
            HoursDetail.IN_IP: row["inIp"],
            HoursDetail.OUT_IP: row["outIp"],
            HoursDetail.EMPLOYEE_NAME: row["userFullName"],
            HoursDetail.IN_DATE_TIME: row["inDateTime"],
            HoursDetail.OUT_DATE_TIME: row["outDateTime"],
            HoursDetail.IN_DEVICE_ID: row["inDeviceId"],
            HoursDetail.OUT_DEVICE_ID: row["outDeviceId"],
            HoursDetail.IN_DATE_TIME_RAW: row.get("In date time raw", ""),
            HoursDetail.OUT_DATE_TIME_RAW: row.get("Out date time raw", ""),
            HoursDetail.MEMBERSHIP_ID_SDK: row["Membership ID_SDK"],
            HoursDetail.EVENT_ID: row["Event ID"],
            HoursDetail.FIRST_NAME: row["First Name"],
            HoursDetail.OPPORTUNITY: row["jobName"],
            HoursDetail.LAST_NAME: row["Last Name"],
            HoursDetail.EID: row["EID"],
            HoursDetail.USER_NAME: row["userName"],
            HoursDetail.MANAGER_COMMENT: row["managerComment"],
            HoursDetail.EMPLOYEE_NOTE: row["employeeNote"],
            HoursDetail.SHIFT: row["shiftName"],
        }
        entries.append(entry)
    return entries


def send_hours_detail(payloads: list[JSON]) -> None:
    ragic = Ragic()
    route = Config.ragic_hours_detail_route()
    for payload in payloads:
        Logger.info(f"Sending payload {str(payload)}")
        result = ragic.send_data(route, data=payload).json()
        Logger.info(f"Received result {str(result)}")


def get_live_hours(data: list[JSON]) -> list[JSON]:
    entries = []
    for row in data:
        entry = {
            LiveHours.EMPLOYEE_NUMBER: row["employeeNumber"],
            LiveHours.JOB_ABSENCE: row["jobName"],
            LiveHours.EMPLOYEE_NAME: row["userFullName"],
            LiveHours.IN_DATE_TIME: row["inDateTime"],
            LiveHours.OUT_DATE_TIME: row["outDateTime"],
            LiveHours.FIRST_NAME: row["First Name"],
            LiveHours.LAST_NAME: row["Last Name"],
            LiveHours.EID: row["EID"],
        }
        entries.append(entry)
    return entries


def send_live_hours(payloads: list[JSON]) -> None:
    ragic = Ragic()
    route = Config.ragic_live_hours_route()
    for payload in payloads:
        partial_fields = {LiveHours.EMPLOYEE_NUMBER, LiveHours.IN_DATE_TIME}
        filters = [f"{k},eq,{payload[k]}" for k in payload.keys() & partial_fields]
        result = ragic.get_data(route, params={"where": filters}).json()
        if not result:
            Logger.info(f"Sending payload {str(payload)}")
            result = ragic.send_data(route, data=payload).json()
            Logger.info(f"Received result {str(result)}")
            continue
        for record_id, record in result.items():
            if record["Out date time"] == payload[LiveHours.OUT_DATE_TIME]:
                Logger.info("Duplicate found, skipping update")
            else:
                for field in (LiveHours.IN_DATE_TIME, LiveHours.OUT_DATE_TIME):
                    payload[field] = payload[field].replace("-", "/")
                Logger.info(f"Updating payload {str(payload)}")
                result = ragic.send_data(f"{route}/{record_id}", data=payload).json()
                Logger.info(f"Received result {str(result)}")

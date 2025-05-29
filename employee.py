from datetime import datetime
from utils import validate_date

class LeaveBalance:
    def __init__(self, sick=0, annual=0, maternity=0):
        self.balances = {
            "Sick Leave": sick,
            "Annual Leave": annual,
            "Maternity Leave": maternity
        }
    
    def deduct(self, leave_type, days):
        if leave_type in self.balances and self.balances[leave_type] >= days:
            self.balances[leave_type] -= days
            return True
        return False

    def add(self, leave_type, days):
        if leave_type in self.balances:
            self.balances[leave_type] += days

    def get(self, leave_type):
        return self.balances.get(leave_type, 0)

    def to_dict(self):
        return dict(self.balances)

    @staticmethod
    def from_dict(data):
        return LeaveBalance(
            sick=data.get("Sick Leave", 0),
            annual=data.get("Annual Leave", 0),
            maternity=data.get("Maternity Leave", 0)
        )

class LeaveRequest:
    def __init__(self, leave_type, days, start_date, status="Pending", request_date=None):
        self.leave_type = leave_type
        self.days = days
        self.start_date = start_date  # String (e.g., "2025-06-01")
        self.status = status          # "Pending", "Approved", "Denied", "Cancelled"
        self.request_date = request_date or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "leave_type": self.leave_type,
            "days": self.days,
            "start_date": self.start_date,
            "status": self.status,
            "request_date": self.request_date
        }

    @staticmethod
    def from_dict(data):
        return LeaveRequest(
            leave_type=data["leave_type"],
            days=data["days"],
            start_date=data["start_date"],
            status=data.get("status", "Pending"),
            request_date=data.get("request_date")
        )

class Employee:
    def __init__(self, name, leave_balance=None, leave_history=None, is_manager=False):
        self.name = name
        self.leave_balance = leave_balance or LeaveBalance()
        self.leave_history = leave_history or []
        self.is_manager = is_manager

    def request_leave(self, leave_type, days, start_date):
        if not validate_date(start_date):
            return False, "Invalid or past date. Please provide a valid future date."
        if self.leave_balance.get(leave_type) < days:
            return False, "Insufficient leave balance."
        new_request = LeaveRequest(leave_type, days, start_date)
        self.leave_history.append(new_request)
        self.leave_balance.deduct(leave_type, days)
        return True, "Leave request submitted."

    def cancel_leave(self, leave_type, start_date):
        for req in self.leave_history:
            if (req.leave_type == leave_type and req.start_date == start_date 
                and req.status in ("Pending", "Approved")):
                req.status = "Cancelled"
                self.leave_balance.add(leave_type, req.days)
                return True, "Leave cancelled."
        return False, "No matching leave request found."

    def get_leave_history(self, year=None):
        if year is None:
            return self.leave_history
        return [req for req in self.leave_history if req.start_date.startswith(str(year))]

    def to_dict(self):
        return {
            "leave_balance": self.leave_balance.to_dict(),
            "leave_history": [req.to_dict() for req in self.leave_history],
            "is_manager": self.is_manager
        }

    @staticmethod
    def from_dict(name, data):
        balance = LeaveBalance.from_dict(data.get("leave_balance", {}))
        history = [LeaveRequest.from_dict(r) for r in data.get("leave_history", [])]
        is_manager = data.get("is_manager", False)
        return Employee(name, balance, history, is_manager)
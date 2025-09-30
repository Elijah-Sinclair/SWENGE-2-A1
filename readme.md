![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Commands

## Staff Commands
### Create Staff Member
flask staff create <username> <password>

### Clock In
flask staff clock-in <username>


### Clock Out
flask staff clock-out <username>

### View Combined Roster

flask staff view-roster <username> <start_date> <end_date> [--detailed]
#### Parameters:

start_date: Format YYYY-MM-DD

end_date: Format YYYY-MM-DD

### Check Current Shift Status
flask staff current-shift <username>

## Admin Commands
### Create Admin User

flask admin create <username> <password>

### Schedule Shift
flask admin schedule-shift <staff_username> <shift_date> <start_time> <end_time>
#### Parameters:

shift_date: Format YYYY-MM-DD

start_time: Format HH:MM

end_time: Format HH:MM

#### Example:
flask admin schedule-shift john 2024-01-15 09:00 17:00
### Delete Shift

flask admin delete-shift <shift_id>

### Generate Shift Report

flask admin generate-report <start_date> <end_date>

### List Staff Shifts

flask admin list-shifts <staff_username> <start_date> <end_date>

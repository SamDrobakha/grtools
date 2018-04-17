# calculates lived_years based on provided year of birth
import datetime

today_date = datetime.date.today()
bday = int(input('provide bday year'))
lived_years = today_date.year - bday
print(lived_years)

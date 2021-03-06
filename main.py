import Config
import Model
import Tools

users = []
users += Model.Contestant.get_data()
users += Model.Organizer.get_data()
users += Model.Volunteer.get_data()
users += Model.Company.get_data()
users += Model.Guest.get_data()
users += Model.Assistant.get_data()

Tools.create_dir(Config.OUT_PATH)
Tools.empty_dir(Config.OUT_PATH)

for u in users:
	u.generate_card()
	u.save()

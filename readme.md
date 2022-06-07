# Promineo Tech LMS Uploads

This Python script is designed to clean and preprocess our student data from our shared Google sheet workspace and format it to be uploaded into the learning management system, without any manual transfer of data.

The data comes directly from a specified sheet, via **gspread** - a Python api that allows for creating new or editing existing Google sheets. The preprocessing however is done entirely in Pandas. Information is taken from the sheet and programmatically formatted into a csv file ready to be read and processed by Moodle.

With this script, we can automate a large section of the student onboarding process - eliminating the manual copy/paste, drag/drop operations of the past - without sacrificing the routine of our admissions teams' input experience.
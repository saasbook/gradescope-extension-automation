# Extension automation tool for Gradescope
This tool aims to automate the process of granting extensions for exams administered on Gradescope

## Setup
Please download [Selenium](https://www.selenium.dev/) and the web driver (e.g. [Chrome webdriver](https://chromedriver.chromium.org/)) corresponding to the version of your browser. You also need to install all the libraries used in the tool.

## Example use
1. Create a Google form to collect extension requests from the students. The form needs to have a timestamp, email, and the requested timeslot. The requested timeslots should be numbered using "#1", "#2", etc. Ex) Alternate Timing #3 - Wednesday, December 15, 2021, from 8am to 11am
2. Download the Google form as a csv file. Suppose it is called `requests.csv`
3. Modify the timeslot setting inside the `run` function.
4. Run `python3 extension_automation.py requests.csv -c <course_id> -a <assignment_id>`. You can get the course_id and assignment_id from the url on Gradescope.
5. A browser window should pop up. Log in with your instructor account.
6. Wait for the tool to automatically fill in the details of extensions.
7. Check the terminal window for failed cases.
8. Since the tool is quite crude now, check the extension list on Gradescope against the Google form.

## Known issues
This tool is quite crude. It cannot
1. Update existing extension
2. Extend due time for DSP students
3. Handle duplicate requests
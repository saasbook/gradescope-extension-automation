from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import click
from datetime import datetime

MAX_WAIT = 10

def javascript_css_click(driver, q):
    if q[0] == "#" and " " not in q:
        return javascript_id_click(driver, q[1:])
    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.CSS_SELECTOR, q)))
    elem = driver.find_element_by_css_selector(q)
    ActionChains(driver).move_to_element(elem).perform()
    driver.execute_script("arguments[0].click();", elem)

def javascript_id_click(driver, id):
    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.ID, id)))
    elem = driver.find_element_by_id(id)
    ActionChains(driver).move_to_element(elem).perform()
    driver.execute_script("arguments[0].click();", elem)

def id_click(driver, id):
    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.ID, id)))
    elem = driver.find_element_by_id(id)
    ActionChains(driver).move_to_element(elem).perform()
    elem.click()

def css_click(driver, q):
    if q[0] == "#" and " " not in q:
        return id_click(driver, q[1:])
    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.CSS_SELECTOR, q)))
    elem = driver.find_element_by_css_selector(q)
    ActionChains(driver).move_to_element(elem).perform()
    elem.click()

def css_fill(driver, q, text):
    WebDriverWait(driver, MAX_WAIT).until(EC.visibility_of_element_located((By.CSS_SELECTOR, q)))
    elem = driver.find_element_by_css_selector(q)
    elem.clear()
    elem.send_keys(text)

def css_checkbox(driver, q, check):
    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.CSS_SELECTOR, q)))
    elem = driver.find_element_by_css_selector(q)
    ActionChains(driver).move_to_element(elem).click().perform()
    if (check and not elem.is_selected()) or (not check and elem.is_selected()):
        elem.click()

def create_extension(driver, assignment_url, email, release_time, due_time):
    driver.get(assignment_url)

    # Wait for sign-in
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, "main-content")))

    css_click(driver, "button.actionBar--action")
    css_fill(driver, "#downshift-0-input", email)

    elem = driver.find_element_by_id("downshift-0-item-0")
    elem.click()

    javascript_id_click(driver, "override_settings_enabled_releaseDate")


    release_date = datetime.fromisoformat(release_time)
    release_date = release_date.strftime("%b %d %Y %I:%M %p")
    css_fill(driver, "#override_settings_releaseDate_value", release_date)

    javascript_id_click(driver, "override_settings_enabled_dueDate")

    due_date = datetime.fromisoformat(due_time)
    due_date = due_date.strftime("%b %d %Y %I:%M %p")
    css_fill(driver, "#override_settings_dueDate_value", due_date)

    javascript_css_click(driver, "button[type='submit']")

    return "SUCCESS"

@click.command()
@click.argument('file', type=click.File('r'))
@click.option('-c', '--course', default=0, type=int, help="The ID of a course")
@click.option('-a', '--assignment', default=0, type=int, help="The ID of an assignment")
def run(course, assignment, file):
    request_reader = csv.reader(file)
    next(request_reader) # skip header row

    driver = webdriver.Chrome()
    assignment_url = f"https://www.gradescope.com/courses/{course}/assignments/{assignment}/extensions"
    
    for row in request_reader:
        if row:
            email, name, timeslot = row[1], row[2], row[3]
            
            if "#1" in timeslot:
                release_time = "2021-12-14T18:00:00"
                due_time = "2021-12-14T21:00:00"
            elif "#2" in timeslot:
                release_time = "2021-12-15T06:00:00"
                due_time = "2021-12-15T09:00:00"
            elif "#3" in timeslot:
                release_time = "2021-12-15T08:00:00"
                due_time = "2021-12-15T11:00:00"
            else:
                continue

            try:
                create_extension(driver, assignment_url, email, release_time, due_time)
                print(f"Extension for {name} ({email}) created.")
            except Exception as e:
                print(f"Failed to create extension for {name} ({email}): {e}")


if __name__ == '__main__':
    run()
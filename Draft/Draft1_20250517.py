"""
RPA to insert link in Monitor 


-Prompt for the Elentra even ID code to go to
-Save under elentra_event_id_input
"https://ntu.elentra.cloud/events?id="+ elentra_event_id_input

-Prompt for the LAMS Lesson ID code to go to
-Save under LAMS_lesson_id_input

-Open Web Browser 

-pause for 2 seconds

-drmatically insert each character of the URL link

-Open URL link

-pause for 2 seconds

-Check on the checkbox 
# <img src="/images/checkbox-on.gif" alt="">
/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/ul/li[2]/a/img

-click on content 
/html/body/div[1]/div/div[3]/div/div[2]/ul/li[2]/a

-Pause for 1 seconds

-scroll down to the bottom of the page

-Pause for 1 seconds

-click on No Time Frame
/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[3]/ul/li[4]/a

-Pause for 1 seconds

-Click on Button "Add a Resource"
/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[3]/div[1]/a

-Pause for 1 seconds

-Click on Checkbox "Link"
/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div/label[6]

-Pause for 1 seconds

-Click on Button "Next Step"
/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]

-Pause for 1 seconds

-Click on Checkbox "Optional"
/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[1]/label[1]

-Pause for 1 seconds

-Click on Button "Next Step"
/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]

-Pause for 1 seconds

-Click on Checkbox "Hide this resource from learners"
/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[3]/label[2]

-Pause for 1 seconds

-Click on Button "Next Step"
/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]

-Pause for 1 seconds

-Under "Please provide the full URL of the link"
/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[2]/div/input
-drmatically insert each character the Monitor URL which is "https://ilams.lamsinternational.com/lams/monitoring/monitoring/monitorLesson.do?lessonID="+ LAMS_lesson_id_input

-Pause for 1 seconds

-Under "You can optionally provide a different title for this link"
/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[3]/div/input
-drmatically insert each character of the Monitor Title

-Pause for 1 seconds

-Under "Please provide a description for this link"
/html/body

-drmatically insert each character of the Monitor Title

-Pause for 1 seconds

-Click on Button "Save Resource"
/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]

-Print "Resource added successfully"

-Execption handling, Print "Resource not added successfully"

-close the browser

"""

import sys
print(sys.executable)

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Specify the path to the Edge WebDriver (use the correct macOS path)
edge_driver_path = '/Users/neltontan/Driver/edgedriver_mac64_m1/msedgedriver'

# Create a Service object
service = Service(executable_path=edge_driver_path)

# Pass the Service object to the Edge WebDriver
driver = webdriver.Edge(service=service)

# Open the target URL
driver.get("https://opensource-demo.orangehrmlive.com/")

# Wait for the username input to be visible and interactable
WebDriverWait(driver, 100).until(
    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[1]/div/div[2]/input"))
)

# Find and interact with the login elements
driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[1]/div/div[2]/input").send_keys("Admin")
driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[2]/div/div[2]/input").send_keys("admin123")
driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[3]/button").click()

# If you're trying to click a button, ensure the XPath is correctly written
# Example (assuming the XPath is correct):
# driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div/div[1]/div/div[2]/div[2]/form/div[3]/button").click()

# Verify if login is successful

act_title = driver.title
exp_title = "OrangeHRM"

if act_title == exp_title:
    print("Login Test passed")
else:
    print("Login Test failed")

# Close the driver
driver.close()


#!/usr/local/bin/python3
# shift cmd P to select 3.13 
# DO NOT USE !/usr/bin/env python3

r""""
python3 -V to check version

pip3 install --upgrade pip
pip3 install --upgrade selenium
pip3 install --upgrade tk

python3 - << 'EOF'
import sys, tkinter
print("Python executable:", sys.executable)
print("Tk version:", tkinter.TkVersion)
print("Tcl patchlevel:", tkinter.Tcl().eval('info patchlevel'))
EOF

should see: 
Python executable: /Library/Frameworks/Python.framework/Versions/3.11/bin/python3
Tk version: 8.6
Tcl patchlevel: 8.6.13
"""

# Ensure you have started Chrome with:
r"""
MAC:
open -a "Google Chrome" --args \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/chrome-debug-profile"
then
curl http://127.0.0.1:9222/json

WINDOWS:
& 'C:\Program Files\Google\Chrome\Application\chrome.exe' `
  --remote-debugging-port=9222 `
  --user-data-dir="C:\Users\Neone\chrome-debug-profile"
then
curl http://127.0.0.1:9222/json

"""

import sys
import os
if os.name == "nt":        # Windows
    os.system("cls")
else:                      # Linux / macOS
    os.system("clear")

import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.scrolledtext import ScrolledText

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
ui_log_var = None
ui_root    = None

"""
# 1) Path to your matching ChromeDriver
chrome_driver_path = r"C:\\Users\\Neone\\Driver\\chromedriver.exe"  
service = Service(chrome_driver_path)

# 2) Tell Selenium to hook into the existing Chrome debug port
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# 3) Create the driver (this will *not* open a new browser window)
driver = webdriver.Chrome(service=service, options=options)

# 4) Confirm it s attached by printing the current title and URL
print("Attached to browser:", driver.title, driver.current_url)

"""
# Check which Python interpreter is in use
print("Using Python executable:", sys.executable)
print("⏳ Waiting for user input ⏳")

time_sleep = 0 #1 sec or 0.05 sec # wait x seconds between actions, for presentation purposes
time_out = 10 #wait up to x seconds for element to be clickable
#highlight_duration = 0.05 set in def highlight ()

def ui_log(message: str):
    """Append `message` + newline to the ScrolledText, keeping it read-only."""
    log_widget.config(state="normal")
    log_widget.insert("end", message + "\n")
    log_widget.see("end")
    log_widget.config(state="disabled")

# function for left to right typing animation
def dramatic_input(element, text, delay=1):
    """Type each character with a small pause to mimic a human."""
    for ch in text:
        element.send_keys(ch)
        # time.sleep(delay)

# function for highlight element in red, for presentation purposes 1 sec or 0.1 sec, value to be lower than time_sleep
def highlight(el, highlight_duration =0.1, color='clear', border="4px solid red"):
    # 1) Scroll the element into view
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
    # 2) Save its current style so we can restore later
    original_style = el.get_attribute("style") or ""
    # 3) Overwrite with our highlight style
    highlight_style = f"background: {color} !important; border: {border} !important; {original_style}"
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", el, highlight_style)
    # 4) Pause so you can actually *see* it
    time.sleep(highlight_duration) #declared in main
    # 5) Restore original style
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", el, original_style)

# function for Wait until clickable
def wait_and_click(driver, xpath, timeout, highlight_fn, message, sleep_after):
    """
    Wait up to `timeout` seconds for an element to be clickable, highlight it, click it, print `message`, sleep, and return the element.
    If it never becomes clickable, logs an error and re-raises.
    """
    global ui_log_var, ui_root
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        if highlight_fn:
            highlight_fn(el)
        el.click()
        if message:
            ui_log(message)
            ui_root.update() #better ui_root.update_idletasks()
            
        if sleep_after:
            time.sleep(sleep_after) # time sleep declared in main
        return el

    except TimeoutException:
        print("❌ Element never became clickable: %s", xpath)
        logger.error("Element never became clickable: %s", xpath) # re-raise so outer code can catch it if desired
        raise

#main function
def run_automation(event_id, lesson_id, lesson_title, use_mon, use_stu):
    start_time = time.time()  
     
    # 1) Request for inputs 
    elentra_event_id   = event_id
    elentra_event_name = None
    lams_lesson_id     = lesson_id
    lams_lesson_title  = lesson_title
    use_monitor        = use_mon
    use_student        = use_stu

    #print("Choices:", elentra_event_id, lams_lesson_id,lams_lesson_title, use_monitor, use_student)
    print("✅ ID input")
    ui_log("✅ ID input")

    # 2) Build URLs & Title
    elentra_event_url   = f"https://ntu.elentra.cloud/events?id={elentra_event_id}"
    #elentra_event_name = f"Elentra {elentra_event_id}"
    lams_monitor_title = f"LAMS {lams_lesson_title} (Facilitator/CE)"
    lams_monitor_url   = f"https://ilams.lamsinternational.com/lams/monitoring/monitoring/monitorLesson.do?lessonID={lams_lesson_id}"
    lams_student_title = f"LAMS {lams_lesson_title}"
    lams_student_url   = f"https://ilams.lamsinternational.com/lams/home/learner.do?lessonID={lams_lesson_id}"
    print("✅ URL input")
    ui_log("✅ URL input")
    
    # 3) Setup Chrome WebDriver to attach to existing debug session
    #macos-----
    chrome_driver_path = "/Users/neltontan/Driver/chromedriver-mac-arm64/chromedriver"
    #windows-----
    # chrome_driver_path = "C:\WebDrivers\chromedriver-win64\chromedriver.exe"

    global driver
    service = Service(executable_path=chrome_driver_path)
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(service=service, options=options)
    print("✅ Chrome WebDriver started")
    ui_log("✅ Chrome WebDriver started")
    
    try:
        # 4) Navigate to Elentra Event Page
        if True: #to group the lines of code
            driver.get(elentra_event_url)
            print("✅ Navigated to Elentra event page")
            ui_log("✅ Navigated to Elentra event page")
            time.sleep(time_sleep)

        # 5) Administrator checkbox
        wait_and_click(
            driver,
            "/html/body/div[1]/div/div[2]/div[2]/div[3]/div[2]/ul/li[2]/a/span",
            timeout=time_out,
            highlight_fn=highlight,
            message="✅ Administrator checkbox clicked",
            sleep_after=time_sleep
        )

        # 6) Content tab
        wait_and_click(
            driver,
            "/html/body/div[1]/div/div[3]/div/div[2]/ul/li[2]/a",
            timeout=time_out,
            highlight_fn=highlight,
            message="✅ Content link clicked",
            sleep_after=time_sleep
        )

        # event name
        if True: #to group the lines of code
        # a) wait for the H1 to be present
            h1 = WebDriverWait(driver, time_out).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div/h1[1]"))
            )
            highlight(h1)
            # b) extract its text
            elentra_event_name = h1.text
            print("✅ Page title is:", elentra_event_name)
            ui_log("✅ Page title is: "+ elentra_event_name)

        ui_log("⏳ Inserting MONITOR URL⏳")
        print("⏳ Inserting MONITOR URL⏳")
        if use_monitor:
            # 7) Scroll down page
            if True: #to group the lines of code
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print("✅ Scrolled to bottom")
                ui_log("✅ Scrolled to bottom")
                time.sleep(time_sleep)

            # 8) No Time Frame
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[3]/ul/li[4]/a",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ No Time Frame link clicked",
                sleep_after=time_sleep
            )
            
            # 9) Add a Resource
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[3]/div[1]/a",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Add a Resource link clicked",
                sleep_after=time_sleep
            )

            # 10) 'Link' Resource checkbox
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div/label[6]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Link checkbox selected",
                sleep_after=time_sleep
            )

            # 11) Next Step
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Next Step Button clicked",
                sleep_after=time_sleep
            ) 
            
            #** 12) Optional 
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[1]/label[1]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Optional selected",
                sleep_after=time_sleep
            )
            
            # 13) No Timeframe
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[2]/label[4]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ No Timeframe link clicked",
                sleep_after=time_sleep
            )
            
            # 14) Next Step
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Next step (to Hide)",
                sleep_after=time_sleep
            )
            
            # 15) No, this resource is accessible any time
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[1]/label[1]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ No, this resource is accessible any time selected",
                sleep_after=time_sleep
            )
            
            #** 16) Hide this resource from learners
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[3]/label[2]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Hide this resource from learners selected",
                sleep_after=time_sleep
            )
            
            # 17) Published
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[4]/label[1]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Published selected",
                sleep_after=time_sleep
            )
            
            # 18) Next Step
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Final Next Step clicked",
                sleep_after=time_sleep
            )
            
            # 18.5) No, the proxy isnt required to be enabled selected
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[1]/div/label[1]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ No, the proxy isnt required to be enabled selected",
                sleep_after=time_sleep
            )

            print("⏳ Inserting LAMS title & URL now ⏳")
            ui_log("⏳ Inserting LAMS title & URL now ⏳")
            
            #*** 19) Enter Monitor URL
            if True:
                time.sleep(0.5)
                el = WebDriverWait(driver, time_sleep).until(
                    EC.visibility_of_element_located((By.XPATH,
                        "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[2]/div/input"
                    ))
                )
                highlight(el)
                el.clear()
                el.send_keys(lams_monitor_url)
                #dramatic_input(el, lams_monitor_url)
                print("✅ Monitor URL entered")
                ui_log("✅ Monitor URL entered")
                time.sleep(time_sleep)
            
            #*** 20) Enter Lesson Title
            if True: #to group the lines of code
                el = WebDriverWait(driver, time_sleep).until(
                    EC.visibility_of_element_located((By.XPATH,
                        "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[3]/div/input"
                    ))
                )
                highlight(el)
                el.clear()
                el.send_keys(lams_monitor_title)
                #dramatic_input(el, LAMS_Lesson_Title_2)
                print("✅ Title entered")
                ui_log("✅ Title entered")
                time.sleep(time_sleep)

            #*** 21) Scroll the message box to the bottom
            if True: #to group the lines of code
                modal = WebDriverWait(driver, time_out).until(
                    EC.presence_of_element_located((By.ID, "event-resource-modal"))
                )
                highlight(modal)
                driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight;",
                    modal
                )
                print("✅ Modal scrolled to bottom")
                ui_log
                time.sleep(time_sleep)
                  
            #*** 22) Enter Description
            time.sleep(0.5)
            if True: #to group the lines of code
                iframe = driver.find_element(
                    By.CSS_SELECTOR,
                    "#cke_event-resource-link-description iframe.cke_wysiwyg_frame"
                )
                driver.switch_to.frame(iframe)
                print("✅ Switched to iframe")
                ui_log("✅ Switched to iframe")

                editor_body = driver.find_element(
                    By.CSS_SELECTOR,
                    "body[contenteditable='true']"
                )
                highlight(editor_body)
                try:
                    editor_body.clear()
                except:
                    editor_body.send_keys(Keys.COMMAND + "a", Keys.DELETE)
                
                editor_body.send_keys(lams_monitor_title)
                #dramatic_input(editor_body, LAMS_Lesson_Title_2)
                driver.switch_to.default_content()
                print("✅ Description added")
                ui_log("✅ Description added")

                time.sleep(time_sleep)

            # 23) Save Resource
            time.sleep(0.5)
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Resource saved",
                sleep_after=time_sleep
            )

            # 24) Close
            time.sleep(0.5)
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[1]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Closed attachment dialog",
                sleep_after=time_sleep,
                
            )
        
        ui_log("⏳ Inserting STUDENT URL⏳")
        print("⏳ Inserting STUDENT URL⏳")
        if use_student:
            # 7) Scroll down page
            if True: #to group the lines of code
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print("✅ Scrolled to bottom")
                ui_log("✅ Scrolled to bottom")
                time.sleep(time_sleep)

            #  Nelton: cuz button grayout, so cannot click 
            # # 8) No Time Frame
            # wait_and_click(
            #     driver,
            #     "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[3]/ul/li[4]/a",
            #     timeout=time_out,
            #     highlight_fn=highlight,
            #     message="✅ No Time Frame link clicked",
            #     sleep_after=time_sleep
            # )

            # 9) Add a Resource
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[3]/div[1]/a",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Add a Resource link clicked",
                sleep_after=time_sleep
            )

            # 10) 'Link' Resource checkbox
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div/label[6]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Link checkbox selected",
                sleep_after=time_sleep
            )

            # 11) Next Step
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Next Step Button clicked",
                sleep_after=time_sleep
            ) 
            
            #** 12) Required 
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[1]/label[2]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Optional selected",
                sleep_after=time_sleep
            )
            
            # 13) No Timeframe
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[2]/label[4]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ No Timeframe link clicked",
                sleep_after=time_sleep
            )
            
            # 14) Next Step
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Next step (to Hide)",
                sleep_after=time_sleep
            )
            
            # 15) No, this resource is accessible any time
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[1]/label[1]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ No, this resource is accessible any time selected",
                sleep_after=time_sleep
            )
            
            #** 16) Hide this resource from learners
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[3]/label[1]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Allow learners to view this resource selected",
                sleep_after=time_sleep
            )
            
            # 17) Published
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[4]/label[1]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Published selected",
                sleep_after=time_sleep
            )
            
            # 18) Next Step
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Final Next Step clicked",
                sleep_after=time_sleep
            )
            
            # 18.5) No, the proxy isnt required to be enabled selected
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[1]/div/label[1]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ No, the proxy isnt required to be enabled selected",
                sleep_after=time_sleep
            )
            
            print("⏳ Inserting LAMS title & URL now ⏳")
            ui_log("⏳ Inserting LAMS title & URL now ⏳")
            
            #*** 19) Enter Monitor URL
            if True:
                time.sleep(0.5)
                el = WebDriverWait(driver, time_sleep).until(
                    EC.visibility_of_element_located((By.XPATH,
                        "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[2]/div/input"
                    ))
                )
                highlight(el)
                el.clear()
                el.send_keys(lams_student_url)
                #dramatic_input(el, lams_monitor_url)
                print("✅ Monitor URL entered")
                ui_log("✅ Monitor URL entered")
                time.sleep(time_sleep)
            
            #*** 20) Enter Lesson Title
            if True: #to group the lines of code
                el = WebDriverWait(driver, time_sleep).until(
                    EC.visibility_of_element_located((By.XPATH,
                        "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[3]/div/input"
                    ))
                )
                highlight(el)
                el.clear()
                el.send_keys(lams_student_title)
                #dramatic_input(el, LAMS_Lesson_Title_2)
                print("✅ Title entered")
                time.sleep(time_sleep)

            #*** 21) Scroll the message box to the bottom
            if True: #to group the lines of code
                modal = WebDriverWait(driver, time_out).until(
                    EC.presence_of_element_located((By.ID, "event-resource-modal"))
                )
                highlight(modal)
                driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight;",
                    modal
                )
                print("✅ Modal scrolled to bottom")
                ui_log("✅ Modal scrolled to bottom")
                time.sleep(time_sleep)
                time.sleep(0.5)
            
            #*** 22) Enter Description
            time.sleep(0.5)
            if True: #to group the lines of code
                iframe = driver.find_element(
                    By.CSS_SELECTOR,
                    "#cke_event-resource-link-description iframe.cke_wysiwyg_frame"
                )
                driver.switch_to.frame(iframe)
                print("✅ Switched to iframe")
                ui_log("✅ Switched to iframe")

                editor_body = driver.find_element(
                    By.CSS_SELECTOR,
                    "body[contenteditable='true']"
                )
                highlight(editor_body)
                try:
                    editor_body.clear()
                except:
                    editor_body.send_keys(Keys.COMMAND + "a", Keys.DELETE)
                
                editor_body.send_keys(lams_student_title)
                #dramatic_input(editor_body, LAMS_Lesson_Title_2)
                driver.switch_to.default_content()
                print("✅ Description added")
                ui_log("✅ Description added")
                time.sleep(time_sleep)

            # 23) Save Resource
            time.sleep(0.5)
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Resource saved",
                sleep_after=time_sleep
            )

            # 24) Close
            time.sleep(0.5)
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[1]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Closed attachment dialog",
                sleep_after=time_sleep
            )

        # Final summary
        print("🎉 Resource added successfully for ⬇️")
        print("   Elentra Event Name: "+ elentra_event_name)
        print("   Elentra Event URL : "+ elentra_event_url)

        ui_log("🎉 Resource added successfully for ⬇️")
        ui_log("   Elentra Event Name: "+ elentra_event_name)
        ui_log("   LAMS Lesson ID    : "+ lams_lesson_id)
        
        if use_monitor:
            print("   LAMS Lesson Title  : "+ lams_monitor_title)
            print("   LAMS Monitor URL  : "+ lams_monitor_url)
            ui_log("   LAMS Lesson Title : "+ lams_monitor_title)
            ui_log("   LAMS Monitor URL  : "+ lams_monitor_url)

        if use_student:
            print("   LAMS Student Title : "+ lams_student_title)
            print("   LAMS Student URL  : "+ lams_student_url)
            ui_log("   LAMS Student Title : "+ lams_student_title)
            ui_log("   LAMS Student URL  : "+ lams_student_url)

    except Exception as e:
            print("❌ Resource not added successfully:", e)
            ui_log(f"❌ Resource not added successfully:,{e}")

    finally:
            # driver.quit()
            elapsed = time.time() - start_time
            print(f"⏱ Total elapsed time: {elapsed:.1f} seconds")
            ui_log(f"⏱ Total elapsed time: {elapsed:.1f} seconds")
            for w in (eid_entry, lid_entry, title_entry, mon_chk, stu_chk, ok_btn, close_btn):
                w.config(state="normal")

# function for UI message box and to get user input
def get_user_choices(
    event_default="1696",
    lesson_default="37655",
    lesson_title_default="(RPA test)FM_MiniQuiz_WomanHealth_DDMMYY"
):
    # 1) Create the ui_root window and show it immediately
    global ui_log_var, ui_root
    ui_root = tk.Tk()
    ui_root.title("Resource Upload Options")
    ui_root.resizable(True, True)
    ui_root.minsize(800, 600)

    # Make column 0 (labels) fixed size, column 1 (entries) stretchy
    ui_root.grid_columnconfigure(0, weight=0)
    ui_root.grid_columnconfigure(1, weight=1)

    # 2) Variables
    global eid_var, lid_var, title_var, mon_var, stu_var    
    eid_var   = tk.StringVar(value=event_default)
    lid_var   = tk.StringVar(value=lesson_default)
    title_var = tk.StringVar(value=lesson_title_default)
    mon_var   = tk.BooleanVar(value=True)
    stu_var   = tk.BooleanVar(value=True)

    # 3) layout inputs
    global eid_entry, lid_entry, title_entry, mon_chk, stu_chk
    pad = dict(padx=8, pady=6)
    tk.Label(ui_root, text="Elentra Event ID:").grid(row=0, column=0, **pad)
    eid_entry = tk.Entry(ui_root, textvariable=eid_var);     
    eid_entry.grid(row=0, column=1, sticky="ew", **pad)

    tk.Label(ui_root, text="LAMS Lesson ID:").grid(row=1, column=0, **pad)
    lid_entry = tk.Entry(ui_root, textvariable=lid_var);     
    lid_entry.grid(row=1, column=1, sticky="ew", **pad)

    tk.Label(ui_root, text="LAMS Lesson Title:").grid(row=2, column=0, **pad)
    title_entry = tk.Entry(ui_root, textvariable=title_var); 
    title_entry.grid(row=2, column=1, sticky="ew", **pad)

    # **Assign** your checkbuttons to variables:
    mon_chk = tk.Checkbutton(ui_root, text="Upload Monitor URL",  variable=mon_var)
    mon_chk.grid(row=3, columnspan=2, sticky="w", **pad)

    stu_chk = tk.Checkbutton(ui_root, text="Upload Student URL", variable=stu_var)
    stu_chk.grid(row=4, columnspan=2, sticky="w", **pad)

    # 4) replace Label+StringVar with a ScrolledText
    global log_widget
    log_widget = ScrolledText(
        ui_root,
        wrap="word",     # wrap long lines
        height=10,       # show 10 lines by default
        state="disabled" # start read-only
    )
    log_widget.grid( row=5, column=0, columnspan=2, sticky="nsew", padx=8, pady=(0,4)
    )
    ui_root.grid_rowconfigure(5, weight=1)
    ui_root.grid_columnconfigure(1, weight=1)

    # — when OK is pressed, disable inputs, queue the automation, but do NOT destroy
    def on_ok():
        # 1) make sure at least one of the two URLs is requested
        if not (mon_var.get() or stu_var.get()):
            messagebox.showerror(
            "Selection error",
            "Please select at least one of:\n"
            "  • Upload Monitor URL\n"
            "  • Upload Student URL"
            )
            return

    # 2) make sure none of the three text fields is blank
        if not eid_var.get().strip() \
        or not lid_var.get().strip() \
        or not title_var.get().strip():
            messagebox.showerror(
                "Input error",
                "Please fill in:\n"
                "  • Elentra Event ID\n"
                "  • LAMS Lesson ID\n"
                "  • LAMS Lesson Title"
            )
            return

    # 3) everything’s valid, so disable inputs and kick off the robot
        for w in (eid_entry, lid_entry, title_entry, mon_chk, stu_chk, ok_btn, close_btn):
            w.config(state="disabled") 
        
        ui_log("🏁 I want to end my work early....")
        # ui_log_var.set("🏁 Starting Clifford Bot…\n")
        ui_root.after(100, lambda: run_automation(
            eid_var.get().strip(),
            lid_var.get().strip(),
            title_var.get().strip(),
            mon_var.get(),
            stu_var.get()
        ))

    def on_cancel():
        ui_root.destroy()
        print("❌ Operation cancelled by user")
        sys.exit("❌ Operation cancelled by user")
    
    # 5) buttons: OK kicks off automation, Close actually destroys the window
    global ok_btn, close_btn
    btnf = tk.Frame(ui_root)
    btnf.grid(row=6, column=0, columnspan=2, pady=8, sticky="s")
    ok_btn    = tk.Button(btnf, text="OK",    width=10, command=on_ok) 
    close_btn = tk.Button(btnf, text="Close", width=10, command=on_cancel)
    ok_btn.pack(side="left",  padx=8)
    close_btn.pack(side="left", padx=8)
    ui_root.mainloop()

    # 7) center & start
    ui_root.update_idletasks()
    w, h = ui_root.winfo_width(), ui_root.winfo_height()
    x = (ui_root.winfo_screenwidth()  - w) // 2
    y = (ui_root.winfo_screenheight() - h) // 2
    ui_root.geometry(f"{w}x{h}+{x}+{y}")
       
if __name__ == "__main__":
    eid, lid, title, use_mon, use_stu = get_user_choices()
    run_automation(eid, lid, title, use_mon, use_stu)

# last updated June 2025

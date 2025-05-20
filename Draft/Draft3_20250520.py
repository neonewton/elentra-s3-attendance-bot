#!/usr/bin/env python3

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

os.environ["TK_SILENCE_DEPRECATION"] = "1"
from tkinter import simpledialog
import tkinter as tk
from tkinter import simpledialog, messagebox

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

def get_user_choices(
    event_default="1696",
    lesson_default="37655",
    lesson_title_default="(test)FM_MiniQuiz_WomanHealth_DDMMYY"
):
    # 1) Create the root window and show it immediately
    root = tk.Tk()
    root.title("Resource Upload Options")
    root.resizable(False, False)

    # 2) Variables
    eid_var   = tk.StringVar(value=event_default)
    lid_var   = tk.StringVar(value=lesson_default)
    title_var = tk.StringVar(value=lesson_title_default)
    mon_var   = tk.BooleanVar(value=True)
    stu_var   = tk.BooleanVar(value=True)
    result    = {}

    # — variables
    eid_var    = tk.StringVar(value=event_default)
    lid_var    = tk.StringVar(value=lesson_default)
    title_var  = tk.StringVar(value=lesson_title_default)
    mon_var    = tk.BooleanVar(value=True)
    stu_var    = tk.BooleanVar(value=True)
    result     = {}

    # 3) Layout
    pad = dict(padx=8, pady=6)
    tk.Label(root, text="Elentra Event ID:").grid( row=0, column=0, sticky="e", **pad)
    tk.Entry(root, textvariable=eid_var, width=30) .grid( row=0, column=1,       **pad)

    tk.Label(root, text="LAMS Lesson ID:").grid(  row=1, column=0, sticky="e", **pad)
    tk.Entry(root, textvariable=lid_var, width=30) .grid( row=1, column=1,       **pad)

    tk.Label(root, text="LAMS Lesson Title:").grid(row=2, column=0, sticky="e", **pad)
    tk.Entry(root, textvariable=title_var, width=50).grid(row=2, column=1,       **pad)

    tk.Checkbutton(root, text="Upload Monitor URL",  variable=mon_var).grid(row=3, columnspan=2, sticky="w", **pad)
    tk.Checkbutton(root, text="Upload Student URL", variable=stu_var).grid(row=4, columnspan=2, sticky="w", **pad)

    # — callbacks
    def on_ok():
        result.update({
            "event_id":            eid_var.get().strip(),
            "lesson_id":           lid_var.get().strip(),
            "lams_lesson_title":   title_var.get().strip(),
            "use_monitor":         mon_var.get(),
            "use_student":         stu_var.get()
        })
        root.destroy()

    def on_cancel():
        root.destroy()
        sys.exit("❌ Operation cancelled by user")

    btnf = tk.Frame(root)
    btnf.grid(row=5, columnspan=2, pady=(0,10))
    tk.Button(btnf, text="OK",     width=10, command=on_ok).pack(side="left", padx=8)
    tk.Button(btnf, text="Cancel", width=10, command=on_cancel).pack(side="left", padx=8)

    # 5) Center the window on screen
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    x = (root.winfo_screenwidth()  - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    # 6) Run the form
    root.mainloop()

    return (
        result["event_id"],
        result["lesson_id"],
        result["lams_lesson_title"],
        result["use_monitor"],
        result["use_student"]
    )


def dramatic_input(element, text, delay=0.01):
    """Type each character with a small pause to mimic a human."""
    for ch in text:
        element.send_keys(ch)
        time.sleep(delay)

def highlight(el, duration=2, color='clear', border="4px solid red"):
    # 1) Scroll the element into view
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
    # 2) Save its current style so we can restore later
    original_style = el.get_attribute("style") or ""
    # 3) Overwrite with our highlight style
    highlight_style = f"background: {color} !important; border: {border} !important; {original_style}"
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", el, highlight_style)
    # 4) Pause so you can actually *see* it
    time.sleep(duration)
    # 5) Restore original style
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", el, original_style)

def main():
    time_sleep = 0.5

    # 1) Request for inputs 
    (
      elentra_event_id,
      lams_lesson_id,
      lams_lesson_title,
      use_monitor,
      use_student
    ) = get_user_choices()

    print("Choices:",
          elentra_event_id,
          lams_lesson_id,
          lams_lesson_title,
          use_monitor,
          use_student)
    print("✅ ID input")

    # 2) Build URLs & Title
    elentra_event_name = f"{elentra_event_id}"
    elentra_event_url   = f"https://ntu.elentra.cloud/events?id={elentra_event_id}"
    
    LAMS_Lesson_Title_2 = f"LAMS {lams_lesson_title} (Facilitator/CE)"
    lams_monitor_url   = f"https://ilams.lamsinternational.com/lams/monitoring/monitoring/monitorLesson.do?lessonID={lams_lesson_id}"
    
    lams_student_title = f"LAMS {lams_lesson_title}"
    lams_student_url   = f"https://ilams.lamsinternational.com/lams/home/learner.do?lessonID={lams_lesson_id}"
    

    print("✅ URL input")
    
    # 3) Setup Chrome WebDriver to attach to existing debug session
    #macos
    # chrome_driver_path = "/Users/neltontan/Driver/chromedriver-mac-arm64/chromedriver"
    #windows
    chrome_driver_path = "C:\WebDrivers\chromedriver-win64\chromedriver.exe"
    service = Service(executable_path=chrome_driver_path)

    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    global driver
    driver = webdriver.Chrome(service=service, options=options)
    print("✅ Chrome WebDriver started")
    
    try:
        
        # 4) Navigate to Elentra Event Page
        driver.get(elentra_event_url)
        print("✅ Navigated to Elentra event page")
        time.sleep(time_sleep)

        # 5) Wait for the Administrator checkbox link to be clickable, then click
        btn = driver.find_element(By.XPATH,
            "/html/body/div[1]/div/div[2]/div[2]/div[3]/div[2]/ul/li[2]/a/span"
        )
        highlight(btn)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                "/html/body/div[1]/div/div[2]/div[2]/div[3]/div[2]/ul/li[2]/a/span"
            ))
        ).click()
        print("✅ Administrator checkbox clicked")

        # 6) Click “Content”
        btn = driver.find_element(By.XPATH,
            "/html/body/div[1]/div/div[3]/div/div[2]/ul/li[2]/a"
        )
        highlight(btn)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                "/html/body/div[1]/div/div[3]/div/div[2]/ul/li[2]/a"
            ))
        ).click()
        print("✅ Content link clicked")
        time.sleep(time_sleep)

        # 7) Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("✅ Scrolled to bottom")
        time.sleep(time_sleep)

        # 8) Click “No Timeframe”
        btn = driver.find_element(By.XPATH,
            "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[3]/ul/li[4]/a"
        )
        highlight(btn)
        btn.click()
        print("✅ No Time Frame link clicked")
        time.sleep(time_sleep)

        print("⏳ Inserting LAMS Lesson Title now ⏳")
        
        # 9) Click “Add a Resource”
        btn = driver.find_element(By.XPATH,
            "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[3]/div[1]/a"
        )
        highlight(btn)
        btn.click()
        print("✅ Add a Resource link clicked")
        time.sleep(time_sleep)

        # 10) Select “Link” checkbox
        btn = driver.find_element(By.XPATH,
            "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div/label[6]"
        )
        highlight(btn)
        btn.click()
        print("✅ Link checkbox selected")
        time.sleep(time_sleep)

        # 11) Three “Next Step” clicks with intermediate checkboxes
        # → Next (then “Optional”)
        btn = driver.find_element(By.XPATH,
            "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]"
        )
        highlight(btn)
        btn.click()
        time.sleep(time_sleep)
        btn = driver.find_element(By.XPATH,
            "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[1]/label[1]"
        )
        highlight(btn)
        btn.click()
        time.sleep(time_sleep)

        # → Next (then “Hide this resource”)
        btn = driver.find_element(By.XPATH,
            "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]"
        )
        highlight(btn)
        btn.click()
        time.sleep(time_sleep)
        btn = driver.find_element(By.XPATH,
            "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[3]/label[2]"
        )
        highlight(btn)
        btn.click()
        time.sleep(time_sleep)

        # → Final Next
        btn = driver.find_element(By.XPATH,
            "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]"
        )
        highlight(btn)
        btn.click()
        time.sleep(time_sleep)

        # 12) Enter Monitor URL
        if use_monitor:
            url_input = driver.find_element(By.XPATH,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[2]/div/input"
            )
            highlight(url_input)
            url_input.clear()
            dramatic_input(url_input, lams_monitor_url)
            time.sleep(time_sleep)

        # 13) Enter Lesson Title
        title_input = driver.find_element(By.XPATH,
            "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[3]/div/input"
        )
        highlight(title_input)
        dramatic_input(title_input, LAMS_Lesson_Title_2)
        time.sleep(time_sleep)
        
        # scroll instantly to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 14) Enter Lesson Description
        # 1) Locate the editor iframe and switch into it
        iframe = driver.find_element(
            By.CSS_SELECTOR,
            "#cke_event-resource-link-description iframe.cke_wysiwyg_frame"
        )
        driver.switch_to.frame(iframe)

        # 2) Now target the editable <body> inside the iframe
        editor_body = driver.find_element(
            By.CSS_SELECTOR,
            "body[contenteditable='true']"
        )

        # 3) Clear any existing content
        try:
            editor_body.clear()
        except:
            editor_body.send_keys(Keys.COMMAND + "a", Keys.DELETE)

        # 4) Type your new description
        dramatic_input(editor_body, lams_lesson_title)

        # 5) Switch back to the main document
        driver.switch_to.default_content()
        print("✅ Description added")

        # 15) Save Resource
        btn = driver.find_element(By.XPATH,
            "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]"
        )
        highlight(btn)
        btn.click()
        time.sleep(time_sleep)
        
        # 16) Close or Attach another Resource
        btn = driver.find_element(By.XPATH,
            "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[1]"
        )
        highlight(btn)
        btn.click()
        time.sleep(time_sleep)
        
        print("✅ Resource added successfully for⬇️")
        print("   Elentra Lesson Title  : "+ elentra_event_name)
        print("   Elentra Event URL  : "+ elentra_event_url)
        
        print("   LAMS Lesson Title : "+ LAMS_Lesson_Title_2)
        print("   LAMS Monitor URL   : "+ lams_monitor_url)

        #try

        # if use_student:
        # # **NEW**: repeat the “Add Resource” wizard steps,
        # # then clear & dramatic_input(student_url) into the URL field.
        # # For example:
        # driver.find_element(By.XPATH, ADD_RESOURCE_BUTTON_XPATH).click()
        # # … do the same Next-Step/checkbox flow …
        # stu_input = driver.find_element(By.XPATH, STUDENT_URL_XPATH)
        # stu_input.clear()
        # dramatic_input(stu_input, student_url)

        print("⏳ Inserting Student Title now ⏳")
        print("✅ Resource added successfully for⬇️")
        print("   LAMS Student Title : "+ lams_student_title)
        print("   LAMS Student URL   : "+ lams_student_url)

    except Exception as e:
        print("❌ Resource not added successfully:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

# shift cmd P to select 3.13 !/usr/local/bin/python3
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

from tkinter import simpledialog
import tkinter as tk
from tkinter import simpledialog, messagebox

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# function for left to right typing animation
def dramatic_input(element, text, delay=0.05):
    """Type each character with a small pause to mimic a human."""
    for ch in text:
        element.send_keys(ch)
        time.sleep(delay)

# function for highlight element in red
def highlight(el, highlight_duration:float, color='clear', border="4px solid red"):
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
def wait_and_click(
    driver,
    xpath: str,
    timeout: float, #declared in main
    highlight_fn,
    message: str,
    sleep_after: float #declared in main
):
    """
    Wait up to `timeout` seconds for an element to be clickable,
    optionally highlight it, click it, print `message`, sleep, and return the element.
    If it never becomes clickable, logs an error and re-raises.
    """
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        if highlight_fn:
            highlight_fn(el)
        el.click()
        if message:
            print(message)
            ui_log_var.set(ui_log_var.get() + message + "\n")
        if sleep_after:
            time.sleep(sleep_after) # time sleep declared in main
        return el

    except TimeoutException:
        logger.error("Element never became clickable: %s", xpath) # re-raise so outer code can catch it if desired
        raise

# function for UI message box and to get user input
def get_user_choices(
    event_default="1696",
    lesson_default="37655",
    lesson_title_default="(test)FM_MiniQuiz_WomanHealth_DDMMYY"
):
    # 1) Create the root window and show it immediately
    root = tk.Tk()
    root.title("Resource Upload Options")
    root.resizable(True, True)
    root.minsize(700, 300)

    # Make column 0 (labels) fixed size, column 1 (entries) stretchy
    root.grid_columnconfigure(0, weight=0)
    root.grid_columnconfigure(1, weight=1)

    # 2) Variables
    eid_var   = tk.StringVar(value=event_default)
    lid_var   = tk.StringVar(value=lesson_default)
    title_var = tk.StringVar(value=lesson_title_default)
    mon_var   = tk.BooleanVar(value=True)
    stu_var   = tk.BooleanVar(value=True)

    # 3) layout inputs
    pad = dict(padx=8, pady=6)
    tk.Label(root, text="Elentra Event ID:")\
      .grid(row=0, column=0, sticky="w", **pad)
    eid_entry = tk.Entry(root, textvariable=eid_var)
    eid_entry.grid(row=0, column=1, sticky="ew", **pad)

    tk.Label(root, text="LAMS Lesson ID:")\
      .grid(row=1, column=0, sticky="w", **pad)
    lid_entry = tk.Entry(root, textvariable=lid_var)
    lid_entry.grid(row=1, column=1, sticky="ew", **pad)

    tk.Label(root, text="LAMS Lesson Title:")\
      .grid(row=2, column=0, sticky="w", **pad)
    title_entry = tk.Entry(root, textvariable=title_var)
    title_entry.grid(row=2, column=1, sticky="ew", **pad)

    tk.Checkbutton(root, text="Upload Monitor URL",  variable=mon_var)\
      .grid(row=3, columnspan=2, sticky="w", **pad)
    tk.Checkbutton(root, text="Upload Student URL", variable=stu_var)\
      .grid(row=4, columnspan=2, sticky="w", **pad)

    # 4) log area
    log_var = tk.StringVar(value="")  
    global ui_log_var
    ui_log_var = log_var

    tk.Label(root, textvariable=log_var,
             justify="left", anchor="nw",
             relief="sunken", height=8)\
      .grid(row=5, column=0, columnspan=2,
            sticky="nsew", padx=8, pady=(0,4))
    root.grid_rowconfigure(5, weight=1)

    # 5) buttons: OK kicks off automation, Close actually destroys the window
    btnf = tk.Frame(root)
    btnf.grid(row=6, column=0, columnspan=2, sticky="s", pady=8)
    ok_btn    = tk.Button(btnf, text="OK",    width=10, command=lambda: on_ok())
    close_btn = tk.Button(btnf, text="Close", width=10, command=root.destroy)
    ok_btn.pack(side="left",  padx=8)
    close_btn.pack(side="left", padx=8)

    # — when OK is pressed, disable inputs, queue the automation, but do NOT destroy
    def on_ok():
        # enforce at least one checkbox
        if not (mon_var.get() or stu_var.get()):
            mon_var.set(True)
            stu_var.set(True)

        # disable everything so user can’t re-edit mid-run
        for w in (eid_entry, lid_entry, title_entry, ok_btn):
            w.config(state="disabled")

        ui_log_var.set("🏁 Starting…\n")
        # schedule the automation to run 100ms later on the same event loop
        root.after(100, lambda: run_automation(
            eid_var.get().strip(),
            lid_var.get().strip(),
            title_var.get().strip(),
            mon_var.get(),
            stu_var.get()
        ))

    def on_cancel():
        root.destroy()
        print("❌ Operation cancelled by user")
        sys.exit("❌ Operation cancelled by user")
    

    # Now give *row 5* weight so it expands to fill all extra vertical space
    root.grid_rowconfigure(5, weight=1)
    # Create your button‐frame in row 5, sticky south
    btnf = tk.Frame(root)
    btnf.grid(row=5, column=0, columnspan=2, sticky="s", pady=(0,10))
    tk.Button(btnf, text="OK",     width=10, command=on_ok).pack(side="left", padx=8)
    tk.Button(btnf, text="Cancel", width=10, command=on_cancel).pack(side="left", padx=8)

    #main function
    def run_automation(event_id, lesson_id, lesson_title, use_mon, use_stu):

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
        #macos-----
        chrome_driver_path = "/Users/neltontan/Driver/chromedriver-mac-arm64/chromedriver"
        #windows-----
        # chrome_driver_path = "C:\WebDrivers\chromedriver-win64\chromedriver.exe"

        service = Service(executable_path=chrome_driver_path)
        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        global driver
        driver = webdriver.Chrome(service=service, options=options)
        print("✅ Chrome WebDriver started")
        
        try:
            time_sleep = 0.5 # wait x seconds between actions
            time_out = 10 #wait up to x seconds for element to be clickable
            highlight_duration = 0.5 # wait x seconds to red border the element

            # 4) Navigate to Elentra Event Page
            driver.get(elentra_event_url)
            ui_log_var.set(ui_log_var.get() + "✅ Navigated to Elentra event page\n")
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

            # 7) Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("✅ Scrolled to bottom")
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

            # 11) Parameters:
            # Next Step
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]",
                timeout=time_out,
                highlight_fn=highlight,
                sleep_after=time_sleep
            ) 
            # Optional 
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[1]/label[1]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Optional selected",
                sleep_after=time_sleep
            )
            # No Timeframe
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[2]/label[4]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ No Timeframe link clicked",
                sleep_after=time_sleep
            )
            
            # Next Step
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Next step (to Hide)",
                sleep_after=time_sleep
            )
            # No, this resource is accessible any time
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[1]/label[1]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Next step (to Hide)",
                sleep_after=time_sleep
            )
            # Hide this resource from learners.
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[3]/label[2]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Hide this resource selected",
                sleep_after=time_sleep
            )
            # Published
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[4]/label[1]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Hide this resource selected",
                sleep_after=time_sleep
            )
            # Next Step
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Final Next",
                sleep_after=time_sleep
            )

            # 12) Enter Monitor URL
            if use_monitor:
                el = WebDriverWait(driver, time_sleep).until(
                    EC.visibility_of_element_located((By.XPATH,
                        "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[2]/div/input"
                    ))
                )
                highlight(el)
                el.clear()
                dramatic_input(el, lams_monitor_url)
                print("✅ Monitor URL entered")
                time.sleep(time_sleep)
            # 13) Enter Lesson Title
            print("⏳ Inserting LAMS title & URL now ⏳")
            el = WebDriverWait(driver, time_sleep).until(
                EC.visibility_of_element_located((By.XPATH,
                    "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[2]/form/div[2]/div[3]/div/input"
                ))
            )
            highlight(el)
            el.clear()
            dramatic_input(el, LAMS_Lesson_Title_2)
            print("✅ Title entered")
            time.sleep(time_sleep)

            # 14.1) Scroll the message box to the bottom
            modal = WebDriverWait(driver, time_out).until(
                EC.presence_of_element_located((By.ID, "event-resource-modal"))
            )
            highlight(modal)
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight;",
                modal
            )
            print("✅ Modal scrolled to bottom")
            time.sleep(time_sleep)

            # 14.2) Enter Description
            iframe = driver.find_element(
                By.CSS_SELECTOR,
                "#cke_event-resource-link-description iframe.cke_wysiwyg_frame"
            )
            driver.switch_to.frame(iframe)
            print("✅ Switched to iframe")

            editor_body = driver.find_element(
                By.CSS_SELECTOR,
                "body[contenteditable='true']"
            )
            highlight(editor_body)
            try:
                editor_body.clear()
            except:
                editor_body.send_keys(Keys.COMMAND + "a", Keys.DELETE)

            dramatic_input(editor_body, LAMS_Lesson_Title_2)
            driver.switch_to.default_content()
            print("✅ Description added")
            time.sleep(time_sleep)

            # 15) Save Resource
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[3]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Resource saved",
                sleep_after=time_sleep
            )

            # 16) Close dialog
            wait_and_click(
                driver,
                "/html/body/div[1]/div/div[3]/div/div[7]/div[1]/div[6]/div/div/div/div[3]/button[1]",
                timeout=time_out,
                highlight_fn=highlight,
                message="✅ Closed attachment dialog",
                sleep_after=time_sleep
            )

            # Final summary
            ui_log_var.set(ui_log_var.get() + "🎉 Resource added successfully for ⬇️\n")
            ui_log_var.set(ui_log_var.get() + "   Elentra Event ID  : "+ elentra_event_id + "\n")
            ui_log_var.set(ui_log_var.get() + "   LAMS Lesson ID    : "+ lams_lesson_id + "\n")
            if use_monitor:
                ui_log_var.set(ui_log_var.get() + "   LAMS Lesson Title : "+ lams_lesson_title + "\n")
                ui_log_var.set(ui_log_var.get() + "   LAMS Monitor URL  : "+ lams_monitor_url + "\n")



            print("⏳ Inserting Student Title now ⏳")
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


            if use_student:
                ui_log_var.set(ui_log_var.get() + "   LAMS Student Title : "+ lams_student_title + "\n")
                ui_log_var.set(ui_log_var.get() + "   LAMS Student URL  : "+ lams_student_url + "\n")

                print("   LAMS Lesson Title : "+ LAMS_Lesson_Title_2)
                print("   LAMS Monitor URL   : "+ lams_monitor_url)
        except Exception as e:
                ui_log_var.set(ui_log_var.get() + f"❌ Resource not added successfully:,{e}\n")


    # 7) center & start
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    x = (root.winfo_screenwidth()  - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.mainloop()

if __name__ == "__main__":
    get_user_choices()

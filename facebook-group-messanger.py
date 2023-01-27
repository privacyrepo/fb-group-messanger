import logging
import argparse
from datetime import datetime, timedelta
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

logging.basicConfig(filename="fb_output.log", level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("--email", type=str, required=True)
parser.add_argument("--password", type=str, required=True)
parser.add_argument("--group_id", type=str, required=True)
args = parser.parse_args()


def check_time(given_time):
    # Convert the input string to a datetime object
    if datetime.strptime(given_time, "%a %I:%M %p"):
        return False
    else:
        time_object = datetime.strptime(given_time, "%I:%M %p")

        # Get the current time
        now = datetime.now()

        # Combine the current date and time
        result = datetime.combine(now.date(), time_object.time())
    
        # Format the datetime object in the desired format
        result_formatted = result.strftime("%Y-%m-%d %H:%M:%S")

        # Calculate 30 minutes ago
        thirty_minutes_ago = now - timedelta(minutes=30)

        # Compare the given time to 30 minutes ago
        if result_formatted >= str(thirty_minutes_ago):
            return True
        else:
            return False


# Replace this with the URL of the Facebook group you want to send messages to
group_url = "https://www.facebook.com/groups/{}/".format(args.group_id)
session_num = 9
session_directory = "./chrome_test{}".format(session_num)


# Create a webdriver object and log in to Facebook
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={session_directory}")
# driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://www.facebook.com")

try:
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "pass")
    login_button = driver.find_element(By.NAME, "login")

    email_field.send_keys(args.email)
    password_field.send_keys(args.password)
    login_button.click()
    if driver.find_element(By.ID, "approvals_code").is_displayed():
        logging.info("NEED FOR DOUBLE AUTHENTICATION AGAIN. YOU HAVE 90 SEC")
        sleep(90)
except Exception as e:
    logging.error("Cant login:", e)
    pass

# Navigate to the group page
sleep(5)
driver.get(group_url)
logging.info("NO NEED FOR DOUBLE AUTHENTICATION AGAIN")

# Click the "Members" tab
sleep(5)
members_tab = driver.find_element(By.PARTIAL_LINK_TEXT, "members")
members_tab.click()

# Wait for the members list to load
sleep(5)

gauge_list = []

# Find All Members

message_button = driver.find_elements(By.XPATH, "//div[@aria-label='Message' and @role='button']")
message_button_list = list(set(message_button))

for item in message_button_list:
    try:
        time_tmp_list = []
        username_tmp_list = []
        user_name = ""
        first_name = ""
        sleep(5)
        item.click()
        sleep(5)
        chat_box = driver.find_element(By.XPATH, "//div[@role='textbox']")
        sleep(5)
        if chat_box.is_displayed():
            try:
                for name_item in chat_box.find_elements(By.XPATH,
                                                        "//span[@class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft']"):
                    tmp_name = name_item.text
                    if tmp_name != "Active now":
                        username_tmp_list.append(tmp_name)
                user_name = username_tmp_list[-1]
                first_name = user_name.split()[0]
            except Exception as e:
                logging.error("Cant find a name: Error", e)
            if chat_box.find_element(By.XPATH, "//span[@class='xk50ysn']").is_displayed():
                for time_item in chat_box.find_elements(By.XPATH, "//span[@class='xk50ysn']"):
                    tmp_time = time_item.text
                    time_tmp_list.append(tmp_time)
                last_message = time_tmp_list[-1]
                if check_time(last_message) is False:
                    message = "Hello {}! This is a test message from a Facebook Page.".format(first_name)
                    chat_box.send_keys(message)
                    chat_box.send_keys(Keys.RETURN)
                    logging.info("Message Sent to user {}".format(user_name))
            else:
                first_message = "Hello {}! This is a test message from a Facebook Page.".format(first_name)
                chat_box.send_keys(first_message)
                chat_box.send_keys(Keys.RETURN)
                logging.info("Message Sent to user {}".format(user_name))
            sleep(10)
            # Close the webdriver
            driver.find_element(By.XPATH, "//div[@aria-label='Close chat']").click()
    except:
        sleep(5)
        logging.error("Message not Sent to user {}: user received a message from you for the last 30 min".format(
            user_name))
        driver.find_element(By.XPATH, "//div[@aria-label='Close chat']").click()

logging.info("END")
driver.quit()


from selenium import webdriver
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU usage in headless
chrome_options.add_argument("--enable-unsafe-webgl")  # Enable unsafe WebGL
chrome_options.add_argument(
    "--enable-unsafe-swiftshader"
)  # Optional: avoid issues in some setups

# Initialize the WebDriver with Chrome options
# driver = webdriver.Chrome()
driver = webdriver.Chrome(options=chrome_options)


def addCookie():
    driver.add_cookie({"name": "JSESSIONID", "value": '"ajax:1707200517968142314"'})
    driver.add_cookie(
        {
            "name": "li_at",
            "value": "AQEDAThJHhYC2Z7yAAABkuIMwvQAAAGTK09QmU4AcXFuh736f5WyqPDJD6WxRRncX2xTnBA9JN5GCO3J6ekWzthl_oC514flNVO5QFRDnE-oI94tsrokAygxl4ie-YQOIjBSkFOlLWYOPp9XWwG8T5L2",
        }
    )


def extractUsersProfile():
    try:
        post_list = driver.find_elements(
            By.XPATH, '//*[@data-id[starts-with(.,"urn:li:activity")]]'
        )
        time.sleep(random.uniform(2, 5))
        # print(f'👌{element.text}')
        for post_item in post_list:
            if (
                "UI/UX" in post_item.text.lower()
            ):  # Use lower() to ensure case-insensitivity
                continue
            try:
                button = post_item.find_element(
                    By.CSS_SELECTOR, '[data-reaction-details=""]'
                )
                if (
                    button.text.isdigit() and int(button.text) > 10
                ):  # Ensure the text is numeric
                    print(f"Skipping post due to reaction count > 10: {button.text}")
                    continue
            except NoSuchElementException:
                continue
            except Exception as e:
                print(e)

        button.click()

        # time.sleep(random.uniform(2, 5))
        time.sleep(random.uniform(2, 5))
        dialog_box = driver.find_element(By.CSS_SELECTOR, '[data-test-modal=""]')

        profile_links_elements = dialog_box.find_elements(By.TAG_NAME, "a")

        profile_links = [link.get_attribute("href") for link in profile_links_elements]

        # for profile_link in profile_links:
        #     print(profile_link.get_attribute('href'))

        print("Successfully clicked on like button")
    except Exception as e:
        print(e)
        exit()

    return profile_links


def goToUserProfile(profile_links):
    try:
        print("i am working on user's profile")
        for profile_link in profile_links:
            driver.get(profile_link)
            time.sleep(random.uniform(2, 5))
            # WebDriverWait(driver,10).until(EC.presence_of_element_located(By.CLASS_NAME,'artdeco-card pv-profile-card break-words'))

            try:
                # experience_section_element = driver.find_element(By.ID,'experience')

                experience_section = driver.find_element(
                    By.XPATH, "//div[@id='experience']/.."
                )

                agency_links_elements = experience_section.find_elements(
                    By.XPATH,
                    './/*[@data-field[starts-with(.,"experience_company_logo")]]',
                )

                agency_links = [
                    link.get_attribute("href") for link in agency_links_elements
                ]

                print(f"👌{agency_links}")
                time.sleep(random.uniform(2, 5))
                handleMessageWorking(agency_links)
                # exit()
            except NoSuchElementException:
                continue
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)
import random

def handleMessageWorking(agency_links):
    for single_link in agency_links:
        driver.get(single_link)
        time.sleep(random.uniform(2, 5))

        try:
            message_button = driver.find_element(
                By.XPATH, '//*[@data-test-message-page-button[starts-with(.,"")]]'
            )

            if message_button is None:
                continue  # Skip if the button is not found

            message_button.click()
            time.sleep(random.uniform(2, 5))

            dropdown = driver.find_element(By.ID, "org-message-page-modal-conversation-topic")
            print("Dropdown found successfully")
            select = Select(dropdown)
            select.select_by_visible_text("Careers")
            print("Career selection found successfully")

            textarea = driver.find_element(By.ID, "org-message-page-modal-message")
            textarea.send_keys(
                "I am Abhishek Kumar, a detail-oriented UI/UX Designer with a background in Frontend developer and wordpress developer . Currently pursuing a Bachelor's in Computer Science, I have hands-on experience in designing user-centric interfaces, improving website functionality, and enhancing user engagement. Through internships at companies like Metaphile Pvt. Ltd. and UigGeeks Pvt. Ltd. I've gained expertise in UI/UX design, WordPress development, and front-end technologies such as HTML, CSS Tailwind, React-JS, Figma and Wordpress. I am passionate about creating intuitive, responsive designs that drive user satisfaction and system performance."
            )

            print("Text message set successfully")
            time.sleep(random.uniform(2, 5))

            span_element = driver.find_element(By.XPATH, "//span[text()='Send message']")
            button = span_element.find_element(By.XPATH, "..")  # Get parent button
            button.click()
            time.sleep(4)

        except NoSuchElementException:
            print("Message button or other element not found, skipping to next link.")
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

driver.get("https://www.linkedin.com/")

addCookie()

driver.refresh()
time.sleep(random.uniform(2, 5))


print("successfully done")

profile_links = extractUsersProfile()

print(profile_links)

time.sleep(random.uniform(2, 5))

goToUserProfile(profile_links)


# time.sleep(random.uniform(2, 5))

driver.quit()

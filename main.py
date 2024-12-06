from selenium import webdriver
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import json
import random

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU usage in headless
chrome_options.add_argument("--enable-unsafe-webgl")  # Enable unsafe WebGL
chrome_options.add_argument(
    "--enable-unsafe-swiftshader"
)  # Optional: avoid issues in some setups

with open("config.json", "r") as file:
    data = json.load(file)
# Initialize the WebDriver with Chrome options
# driver = webdriver.Chrome()
driver = webdriver.Chrome(options=chrome_options)



def addCookie():
    driver.add_cookie({"name": "JSESSIONID", "value": data["JSESSIONID"]})
    driver.add_cookie(
        {
            "name": "li_at",
            "value": data["li_at"],
        }
    )

def extractUsersProfile():
    try:
        profile_links = set()  # Use a set to avoid duplicate links
        
        # Locate posts
        post_list = driver.find_elements(By.XPATH, '//*[@data-id[starts-with(.,"urn:li:activity:")]]')
        time.sleep(random.uniform(1, 3))

        # Use a dictionary to ensure uniqueness based on `data-id`
        unique_posts = {}
        for post in post_list:
            try:
            # Extract the unique `data-id` for each post
                data_id = post.get_attribute("data-id")
                # print(data_id)
                if data_id and data_id not in unique_posts:
                    unique_posts[data_id] = post
                    print(data_id)
                    # print(post.text)
            except Exception as e:
                print(f"Error processing post: {e}")

            # Retrieve the unique posts as a list
            unique_post_list = list(unique_posts.values())

            # Print the number of unique posts
        print(f"Total unique posts: {len(unique_post_list)}")
        for post_item in unique_post_list:
            # print(data["Interest"].lower())
            # # print(post_item.text.)
            # print(data["Interest"].lower() not in post_item.text.lower())
            # if data["Interest"].lower() not in post_item.text.lower():
            #     print("Interest not found, proceeding with logic.")
            #     # Your code to process the post
            #     continue
            # else:
            #     print("Interest found, skipping post.")
            
            # print(post_item.)
            try:
                # Find the like button
                
                # Click the like button
                try:
                    button = WebDriverWait(post_item, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-reaction-details=""]'))
                    )
                
                    # if button.text.isdigit() and int(button.text) < 10:  # Numeric validation
                    #     print(f"Skipping post due to reaction count < 10: {button.text}")
                    #     continue
                    # print(f"Reaction Count > 10:")
                    button.click()
                except Exception as e:
                    print("Arre phir se vhi error . button click hone ka")   
                print("Successfully clicked on like button")
                time.sleep(random.uniform(1, 3))
                
                # Locate the dialog box
                dialog_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[role="dialog"]'))
                )
                # dialog_box = driver.find_element(By.CSS_SELECTOR, '[role="dialog"]')
                
                # Extract profile links
                profile_links_elements = dialog_box.find_elements(By.TAG_NAME, "a")
                profile_links.update(link.get_attribute("href") for link in profile_links_elements if link.get_attribute("href"))
                print(f"profile_links extracted {len(profile_links)} ")
                if(len(profile_links) > data["Total_Profiles"]):
                    print("profile_links extraction limit reached")
                    break
                time.sleep(random.uniform(1,3))
                dialog_close_button = dialog_box.find_element(By.TAG_NAME, "use")
                dialog_close_button.click()
                time.sleep(random.uniform(1,3))
            except NoSuchElementException as e:
                print(f"Element not found: {e}")
                continue
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
        
        if not profile_links:
            print("No profile links found.")
        
    except Exception as e:
        print(f"Critical error in extractUsersProfile: {e}")
        exit()

    return list(profile_links)  # Return as a list for better flexibility

def goToUserProfile(profile_links):
    try:
        print("i am working on user's profile")
        for profile_link in profile_links:
            driver.get(profile_link)
            time.sleep(random.uniform(1, 3))
            # WebDriverWait(driver,10).until(EC.presence_of_element_located(By.CLASS_NAME,'artdeco-card pv-profile-card break-words'))

            try:
                # experience_section_element = driver.find_element(By.ID,'experience')
                # search_words = data["Words"]

                # # Extracting the `bio_words` text
                # bio_words = driver.find_element(
                #     By.XPATH,
                #     './/*[@data-generated-suggestion-target[starts-with(.,"urn:li:fsu_profileActionDelegate")]]',
                # ).text

                # # Finding all words from the list that are in `bio_words`
                # found_words = [word for word in search_words if word in bio_words]

                # # Printing the results
                # if found_words:
                #     print(f"Found words: {found_words}")
                # else:
                #     print("No words from the list were found in the bio_words.")
                #     continue

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
                time.sleep(random.uniform(1, 3))
                handleMessageWorking(agency_links)
                # exit()
            except NoSuchElementException:
                continue
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)


def handleMessageWorking(agency_links):
    for single_link in agency_links:
        driver.get(single_link)
        time.sleep(random.uniform(1, 3))

        try:
            print("starting setting message stuff")
            message_button = driver.find_element(
                By.XPATH, '//*[@data-test-message-page-button[starts-with(.,"")]]'
            )

            if message_button is None:
                continue  # Skip if the button is not found

            print("-----")
            message_button.click()
            print("-----")
            time.sleep(random.uniform(1, 3))
            print("-----")

            dropdown = driver.find_element(
                By.ID, "msg-shared-modals-msg-page-modal-presenter-conversation-topic"
            )
            print("Dropdown found successfully")
            select = Select(dropdown)
            select.select_by_visible_text("Careers")
            print("Career selection found successfully")

            textarea = driver.find_element(By.ID, "org-message-page-modal-message")
            textarea.send_keys(data["Message"])

            print("Text message set successfully")
            time.sleep(random.uniform(1, 3))

            span_element = driver.find_element(
                By.XPATH, "//span[text()='Send message']"
            )
            button = span_element.find_element(By.XPATH, "..")  # Get parent button
            button.click()
            time.sleep(2)

        except NoSuchElementException:
            print("Message button or other element not found, skipping to next link.")
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            continue


driver.get("https://www.linkedin.com/")

addCookie()

driver.refresh()
time.sleep(random.uniform(1, 3))


print("successfully done")

print("ashish")
profile_links = extractUsersProfile()

print(profile_links)

time.sleep(random.uniform(1, 3))

goToUserProfile(profile_links)


# time.sleep(random.uniform(1, 3))

driver.quit()

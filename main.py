from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU usage in headless
chrome_options.add_argument("--enable-unsafe-webgl")  # Enable unsafe WebGL
chrome_options.add_argument("--enable-unsafe-swiftshader")  # Optional: avoid issues in some setups

# Initialize the WebDriver with Chrome options
driver = webdriver.Chrome(options=chrome_options)


def addCookie():
    driver.add_cookie({
        "name" : "JSESSIONID",
        "value": "\"ajax:-5419834528488810090\""
    })
    driver.add_cookie({
        "name" : 'li_at',
        "value": "AQEDAThW5cEDtVQkAAABkhq21mUAAAGTC0f2eU4AYV4qxu0ubkxBKWnbQPc8GrKC4RmN0Ypl_CpcNs2ZOFt73WwIvwRfJtEeacKG7EETYN-_4pRKX-O_YOGOTbgSSLrzwhSFmfLGOsHN5ulWYGqXKCUQ"
    })

def extractUsersProfile():
    try:
        post_list = driver.find_elements(By.XPATH,'//*[@data-id[starts-with(.,"urn:li:activity")]]')
        time.sleep(2)
    # print(f'👌{element.text}')
        for post_item in post_list:
            if 'flutter' in post_item.text.lower():  # Use lower() to ensure case-insensitivity
                continue
            try:
                button = post_item.find_element(By.CSS_SELECTOR,'[data-reaction-details=""]')
                if button.text.isdigit() and int(button.text) > 10:  # Ensure the text is numeric
                        print(f'Skipping post due to reaction count > 10: {button.text}')
                        continue
            except NoSuchElementException:
                continue
            except Exception as e:
                print(e)    
    
    

        button.click()        

    # time.sleep(5)
        time.sleep(2)
        dialog_box = driver.find_element(By.CSS_SELECTOR,'[data-test-modal=""]')

        profile_links_elements = dialog_box.find_elements(By.TAG_NAME,'a')

        profile_links = [link.get_attribute('href') for link in profile_links_elements]

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
            time.sleep(5)
            # WebDriverWait(driver,10).until(EC.presence_of_element_located(By.CLASS_NAME,'artdeco-card pv-profile-card break-words'))

            try:
                # experience_section_element = driver.find_element(By.ID,'experience')

                experience_section = driver.find_element(By.XPATH,"//div[@id='experience']/..")
            
                agency_links_elements = experience_section.find_elements(By.XPATH,'.//*[@data-field[starts-with(.,"experience_company_logo")]]')

                agency_links = [link.get_attribute('href') for link in agency_links_elements]

                print(f'👌{agency_links}')
                time.sleep(3)
                handleMessageWorking(agency_links)
                # exit()
            except NoSuchElementException:
                continue
            except Exception as e :
                print(e)
    


    except Exception as e:
        print(e)    


def handleMessageWorking(agency_links):
    for single_link in agency_links :
        driver.get(single_link)

        time.sleep(2)

        message_button = driver.find_element(By.XPATH,'//*[@data-test-message-page-button[starts-with(.,"")]]')

        message_button.click()

        time.sleep(2)

        dropdown = driver.find_element(By.ID,'org-message-page-modal-conversation-topic')
        print("dropdown found successfully ")
        select = Select(dropdown)

        select.select_by_visible_text('Careers')

        print("career selection found successfully")

        textarea = driver.find_element(By.ID,'org-message-page-modal-message')

        textarea.send_keys(
        "Hello, my name is Ashish Sharma, and I’m currently in my final year of B.Tech in Computer Science at IIMT Engineering College, Meerut. "
        "I have hands-on experience in mobile app development, particularly using Flutter, where I’ve successfully built 5 large-scale projects for different agencies. "
        "These projects have sharpened my skills in UI/UX design, state management, and integrating backend services like Firebase.\n\n"
        "Although most of my experience is in Flutter, I am also passionate about Java development, which aligns with my computer science background. "
        "I have a solid understanding of core Java concepts such as OOP, data structures, and algorithms, and I’m excited to apply my problem-solving and software development skills in this position."
    )

        print("text message set successfully")

        time.sleep(2)

        span_element = driver.find_element(By.XPATH, "//span[text()='Send message']")

# Find the parent button using the span element's XPath
        button = span_element.find_element(By.XPATH, '..')  # '..' refers to the parent element (the button)

# Click the button
        button.click()

        
        time.sleep(4)


driver.get("https://www.linkedin.com/")

addCookie()

driver.refresh()
time.sleep(2)


print("successfully done")

profile_links = extractUsersProfile()

print(profile_links)

time.sleep(2)

goToUserProfile(profile_links)


# time.sleep(5)

driver.quit()


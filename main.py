import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

email = "a.thomas@ecole-ipssi.net"
password = "es3$Hian_B@hHwM"

url_base = "https://business.global-exam.com/"


def login(local_driver):
    input_email = WebDriverWait(local_driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    input_email.send_keys(email)
    input_password = WebDriverWait(local_driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    input_password.send_keys(password)
    btn_login = WebDriverWait(local_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div/div/div/div/div/form/div[3]/button')))
    btn_login.click()


def got_to_orga(local_driver, orga="IPSSI"):
    parent_element = local_driver.find_elements(By.XPATH, "//div[contains(h3, '%s')]" % orga)[0]
    parent_element.click()


def get_stats(local_driver):
    local_driver.get("https://business.global-exam.com/")
    stats_element = WebDriverWait(local_driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div/main/div[2]/div/div/div[2]/div[1]/div[3]/div[1]/p[1]")))
    return int(stats_element.text.replace("h", ""))


def go_to_actual_module(local_driver):
    x_path = "/html/body/div[1]/div/main/div[2]/div/div/div[1]/div[1]/div[2]/div[3]/a"
    btn_actual_module = WebDriverWait(local_driver, 10).until(EC.presence_of_element_located((By.XPATH, x_path)))
    try :
        btn_actual_module.click()
    except:
        href = btn_actual_module.get_attribute('href')
        local_driver.get(href)


def play(local_driver):
    if get_terminate_situation(local_driver) > 0:
        go_to_situation(local_driver)
        answer_to_question(local_driver)
    else:
        if get_terminate_module(local_driver) > 0:
            go_to_next_module(local_driver)
        else:
            print("Module ended")


def get_terminate_situation(local_driver):
    actual_xpath = '//*[@id="index"]/div/main/div[2]/div[2]/div[2]/div/div/div[2]/p[2]/span[1]'
    max_xpath = '//*[@id="index"]/div/main/div[2]/div[2]/div[2]/div/div/div[2]/p[2]/span[2]'
    actual = WebDriverWait(local_driver, 10).until(EC.presence_of_element_located((By.XPATH, actual_xpath)))
    max = WebDriverWait(local_driver, 10).until(EC.presence_of_element_located((By.XPATH, max_xpath)))
    return int(max.text.replace("/ ", "")) - int(actual.text)


def get_terminate_module(local_driver):
    actual_xpath = '/html/body/div[1]/div/main/div[2]/div[2]/div[2]/div/div/div[2]/p[1]/span[1]'
    max_xpath = '/html/body/div[1]/div/main/div[2]/div[2]/div[2]/div/div/div[2]/p[1]/span[2]'
    actual = WebDriverWait(local_driver, 10).until(EC.presence_of_element_located((By.XPATH, actual_xpath)))
    max = WebDriverWait(local_driver, 10).until(EC.presence_of_element_located((By.XPATH, max_xpath)))
    return int(max.text.replace("/ ", "")) - int(actual.text)


def go_to_next_module(local_driver):

    time.sleep(5)

    actual_xpath = '/html/body/div[1]/div/main/div[2]/div[2]/div[2]/div/div/div[2]/p[1]/span[1]'
    actual = WebDriverWait(local_driver, 10).until(EC.presence_of_element_located((By.XPATH, actual_xpath)))
    number = int(actual.text)

    parent_xpath = "/html/body/div[1]/div/main/div[2]/div[2]/div[2]/div/div/div[3]"
    parent = WebDriverWait(local_driver, 10).until(EC.presence_of_element_located((By.XPATH, parent_xpath)))

    a_tag = parent.find_element(By.TAG_NAME, "a")

    href = a_tag.get_attribute("href")

    content_id = href.split("/")[6]
    industry_id = href.split("/")[4]

    local_driver.get(url_base + "industry/" + industry_id + "/content/" + str(int(content_id) + number))

    time.sleep(5)
    play(local_driver)





def go_to_situation(local_driver):
    css_selector = "button-solid-primary-medium"
    list_btn = local_driver.find_elements(By.CLASS_NAME, css_selector)
    desired_text = ["Continuer", "Commencer"]
    for btn in list_btn:
        if btn.text in desired_text:
            btn.click()
            break


def get_type_question(local_driver):
    css_selector = "button-solid-primary-large"
    list_btn = local_driver.find_elements(By.CLASS_NAME, css_selector)
    desired_text = ["Commencer"]
    for btn in list_btn:
        if btn.text in desired_text:
            return "Start"

    try:
        x_path_true_or_false = "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[2]/ul"
        ul_true_or_false = local_driver.find_element(By.XPATH, x_path_true_or_false)

        if ul_true_or_false is not None:
            li_elements = driver.execute_script("return arguments[0].getElementsByTagName('li')", ul_true_or_false)
            if len(li_elements) == 2:
                return "True or False"
    except:
        pass

    try:
        x_path_multiple_choice = "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[2]/ul"
        ul_multiple_choice = local_driver.find_element(By.XPATH, x_path_multiple_choice)

        if ul_multiple_choice is not None:
            li_elements = driver.execute_script("return arguments[0].getElementsByTagName('li')", ul_multiple_choice)
            if len(li_elements) > 2:
                return "Multiple Choice"
    except:
        pass

    try:
        x_path_bad_answer = "/html/body/div[1]/div[2]/div[1]/div[2]/p"
        bad_answer = local_driver.find_element(By.XPATH, x_path_bad_answer)

        if bad_answer is not None:
            return "Bad Answer"
    except:
        pass

    try:
        blank_words = local_driver.find_element(By.ID, "recon1")
        if blank_words is not None:
            return "Blank Words"
    except:
        pass

    try:
        is_drag_and_drop_selector = "vue-draggable-answers-list"
        is_drag_and_drop = local_driver.find_element(By.CLASS_NAME, is_drag_and_drop_selector)
        if is_drag_and_drop is not None:
            return "Drag and Drop"
    except:
        pass

    try:
        center_text_xpath = "/html/body/div[1]/div/div[2]/div[1]/div/div/p"
        center_text = local_driver.find_element(By.XPATH, center_text_xpath).text
        if center_text is not None:
            if center_text.startswith("Match"):
                return "Match words"
    except:
        pass

    try:
        center_text_xpath = "/html/body/div[1]/div/div[2]/div[1]/div/div/p"
        center_text = local_driver.find_element(By.XPATH, center_text_xpath).text
        if center_text is not None:
            if center_text.startswith("Place the words in the correct order"):
                return "Order words"
    except:
        pass

    try:
        transcript_button = "/html/body/div[1]/div/div[2]/div[1]/div[2]/div[1]/button[2]"
        transcript = local_driver.find_element(By.XPATH, transcript_button)
        if transcript is not None:
            if transcript.text == "Transcript":
                return "Transcript"
    except:
        pass

    return "End"


def answer_to_question(local_driver):
    time.sleep(55)

    continue_situation = True

    while continue_situation:

        time.sleep(5)

        type_question = get_type_question(local_driver)
        print(type_question)

        if type_question == "Start":
            start_answer(local_driver)
        elif type_question == "True or False":
            true_or_false_answer(local_driver)
        elif type_question == "Multiple Choice":
            multiple_choice_answer(local_driver)
        elif type_question == "Bad Answer":
            go_to_next_question(local_driver)
        elif type_question == "Blank Words":
            blank_words_answer(local_driver)
        elif type_question == "Drag and Drop":
            drag_and_drop_answer(local_driver)
        elif type_question == "Match words":
            match_words_answer(local_driver)
        elif type_question == "Order words":
            order_words_answer(local_driver)
        elif type_question == "Transcript":
            go_to_next_question(local_driver)
        elif type_question == "End":
            is_end = go_to_next_question(local_driver)
            try :
                xpath_end = "/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div/a[2]"
                end = local_driver.find_element(By.XPATH, xpath_end)
                if end is not None:
                    end.click()
                    continue_situation = False
            except:
                pass




def start_answer(local_driver):
    css_selector = "button-solid-primary-large"
    list_btn = local_driver.find_elements(By.CLASS_NAME, css_selector)
    desired_text = ["Commencer"]
    for btn in list_btn:
        if btn.text in desired_text:
            btn.click()
            break


def true_or_false_answer(local_driver):
    print("true or false")
    go_to_next_question(local_driver)


def blank_words_answer(local_driver):
    technical_words = [
        "Compute", "Device", "Mouse", "Keyboard", "Monitor",
        "Printer", "Router", "Modem", "Speaker", "Microphone",
        "Webcam", "USB", "Hard drive", "Memory", "RAM",
        "Processor", "Operating system", "Software", "Application", "File",
        "Folder", "Browser", "Website", "Link", "Download",
        "Upload", "Password", "Email", "Wireless", "Bluetooth",
        "Wi-Fi", "Ethernet", "Firewall", "Virus", "Backup",
        "Data", "Cloud", "Social media", "Chat", "Gaming",
        "Interface", "Error", "Update", "Plug and play", "Driver",
        "Resolution", "Pixel", "Scroll", "Search", "Click"
    ]

    input_elements = local_driver.find_elements(By.CSS_SELECTOR, "input[id^='recon']")
    for input_element in input_elements:
        input_element.send_keys(random.choice(technical_words))
        time.sleep(0.5)

    go_to_next_question(local_driver)


def drag_and_drop_answer(local_driver):
    selector_drag_and_drop = "vue-draggable-answers-list"
    drag_and_drop = local_driver.find_element(By.CLASS_NAME, selector_drag_and_drop)

    if drag_and_drop is not None:
        span_elements = local_driver.execute_script("return arguments[0].getElementsByTagName('span')", drag_and_drop)
        while len(span_elements) > 0:
            number = random.randint(0, len(span_elements) - 1)
            span_elements[number].click()
            time.sleep(1)
            span_elements = local_driver.execute_script("return arguments[0].getElementsByTagName('span')",
                                                        drag_and_drop)

    go_to_next_question(local_driver)


def match_words_answer(local_driver):
    ul_parent_xpath = "/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/ul"
    ul_parent = local_driver.find_element(By.XPATH, ul_parent_xpath)

    if ul_parent is not None:
        li_elements = local_driver.execute_script("return arguments[0].getElementsByTagName('li')", ul_parent)
        for li_element in li_elements:
            local_driver.execute_script("arguments[0].classList.remove('hidden')", li_element)

        while len(li_elements) > 0:
            number = random.randint(0, len(li_elements) - 1)
            li_elements[number].click()
            time.sleep(1)
            li_elements = local_driver.execute_script("return arguments[0].getElementsByTagName('li')", ul_parent)

    go_to_next_question(local_driver)


def order_words_answer(local_driver):
    parent_xpath = "/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/div"
    parent = local_driver.find_element(By.XPATH, parent_xpath)

    if parent is not None:
        div_elements = local_driver.execute_script("return arguments[0].getElementsByTagName('div')", parent)
        while len(div_elements) > 0:
            number = random.randint(0, len(div_elements) - 1)
            div_elements[number].click()
            time.sleep(1)
            div_elements = local_driver.execute_script("return arguments[0].getElementsByTagName('div')", parent)

    go_to_next_question(local_driver)


def multiple_choice_answer(local_driver):
    x_path_multiple_choice = "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[2]/ul"
    ul_multiple_choice = local_driver.find_element(By.XPATH, x_path_multiple_choice)

    if ul_multiple_choice is not None:
        li_elements = driver.execute_script("return arguments[0].getElementsByTagName('li')", ul_multiple_choice)
        number = random.randint(0, len(li_elements) - 1) + 1
        for i in range(number):
            li_elements[i].click()
            time.sleep(0.5)

    go_to_next_question(local_driver)


def go_to_next_question(local_driver):
    time.sleep(10)
    css_selector = "button-solid-primary-large"
    list_btn = local_driver.find_elements(By.CLASS_NAME, css_selector)
    desired_text = ["Suivant", "Terminer"]
    if len(list_btn) == 0 :
        time.sleep(5)
        return "end"
    for btn in list_btn:
        if btn.text in desired_text:
            btn.click()
            break


if __name__ == '__main__':
    driver = uc.Chrome(use_subprocess=False)
    driver.get(url_base)
    try:
        login(driver)
        try:
            got_to_orga(driver)
        except :
            pass
        try:
            nbr_hours = get_stats(driver)
            while True:
                go_to_actual_module(driver)
                play(driver)
        except Exception as e:
            print(e)
    except:
        print("Unable to login")

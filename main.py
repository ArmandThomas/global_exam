import undetected_chromedriver as uc
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from dotenv import dotenv_values

env_vars = dotenv_values('.env.local')

email = env_vars['EMAIL']
password = env_vars['PASSWORD']

if (not email or not password):
    print("Please add your credentials in .env.local")
    exit()

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
    try:
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
            go_to_new_module(local_driver)


def get_terminate_situation(local_driver):
    actual_xpath = '//*[@id="index"]/div/main/div[2]/div[2]/div[2]/div/div/div[2]/p[2]/span[1]'
    max_xpath = '//*[@id="index"]/div/main/div[2]/div[2]/div[2]/div/div/div[2]/p[2]/span[2]'
    actual = WebDriverWait(local_driver, 10).until(EC.presence_of_element_located((By.XPATH, actual_xpath)))
    max = WebDriverWait(local_driver, 10).until(EC.presence_of_element_located((By.XPATH, max_xpath)))
    return int(max.text.replace("/ ", "")) - int(actual.text)


def go_to_new_module(local_driver):
    xpath = "/html/body/div[1]/div/main/div[2]/div[1]/div[2]/a"
    btn_new_module = WebDriverWait(local_driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    btn_new_module.click()

    array_module = ["Immobilier", "Restauration", "Jeux vidéo", "Gestion d'un spa", "Design", "Santé", "Bâtiment",
                    "Banque & Finance", "Météo et climat"]

    if 'MODULE' in env_vars:
        array_module = env_vars['MODULE'].split(",")

    cards = WebDriverWait(local_driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-tab")))

    for card in cards:
        if "is-selected" in card.get_attribute("class"):
            if card.text in array_module:
                array_module.remove(card.text)

    if len(array_module) == 0:
        print("All modules have been done")
        exit()

    random_module = random.choice(array_module)
    if 'MODULE' in env_vars:
        random_module = random_module[0]

    for card in cards:
        if card.text == random_module:
            card.click()
            break

    btn_start_xpath = "/html/body/div[1]/div/main/div[2]/div[2]/div[2]/span/div/div[2]/div[2]/a"
    btn_start = WebDriverWait(local_driver, 10).until(EC.presence_of_element_located((By.XPATH, btn_start_xpath)))
    btn_start.click()

    time.sleep(2)
    play(local_driver)


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

    a_tag = parent.find_elements(By.TAG_NAME, "a")

    a_tag[number].click()

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
    time.sleep(2)

    continue_situation = True

    context = []

    while continue_situation:

        time.sleep(5)

        type_question = get_type_question(local_driver)

        if type_question == "Start":
            start_answer(local_driver)
        elif type_question == "True or False":
            true_or_false_answer(local_driver, context)
        elif type_question == "Multiple Choice":
            multiple_choice_answer(local_driver, context)
        elif type_question == "Bad Answer":
            go_to_next_question(local_driver)
        elif type_question == "Blank Words":
            blank_words_answer(local_driver, context)
        elif type_question == "Drag and Drop":
            drag_and_drop_answer(local_driver, context)
        elif type_question == "Match words":
            match_words_answer(local_driver, context)
        elif type_question == "Order words":
            order_words_answer(local_driver, context)
        elif type_question == "Transcript":
            transcript_type(local_driver, context)
        elif type_question == "End":
            go_to_next_question(local_driver)
            try:
                xpath_end = "/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div/a[2]"
                end = local_driver.find_element(By.XPATH, xpath_end)
                if end is not None:
                    end.click()
                    continue_situation = False
            except:
                pass


def transcript_type(local_driver, context) :

    print("Transcript type")


def start_answer(local_driver):
    css_selector = "button-solid-primary-large"
    list_btn = local_driver.find_elements(By.CLASS_NAME, css_selector)
    desired_text = ["Commencer"]
    for btn in list_btn:
        if btn.text in desired_text:
            btn.click()
            break


def true_or_false_answer(local_driver, context):
    xpath = "/html/body/div[1]/div/div[2]/div[1]/div/div/div/div/div[2]/ul/li[2]"
    true_or_false = local_driver.find_element(By.XPATH, xpath)
    true_or_false.click()
    go_to_next_question(local_driver)


def blank_words_answer(local_driver, context):

    print("Blank words")
    go_to_next_question(local_driver)


def drag_and_drop_answer(local_driver, context):

    xpath_parent_list_answer = "/html/body/div[1]/div/div[2]/div[1]/div/div[2]"
    parent_list_answer = WebDriverWait(local_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_parent_list_answer))
    )

    list_words = []

    if parent_list_answer is not None:
        list_spans = local_driver.execute_script("return arguments[0].getElementsByTagName('span')", parent_list_answer)
        for span in list_spans:
            list_words.append(span.text)

    xpath_text = "/html/body/div[1]/div/div[2]/div[1]/div/div[1]"
    text = WebDriverWait(local_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_text))
    )
    inner_html = text.get_attribute("innerHTML")

    prompt = "Will be very usefull on answer me only the array not text with this," \
             "Please interprete the html i give you and answer me my problem by responding only a array like ['word1', 'word2' etc...]" \
             " For each word : %s give number of index sort by blank in the text, for example if the word %s should complete the first blank represented by div with data-row-name start with recon return me, the word %s should blank the second div, the return should be ['%s','%s', '%s'] : The html of text to complete is : %s " % (
    ', '.join(list_words), list_words[0], list_words[2], list_words[0], list_words[2], list_words[1], inner_html)

    try :
        response = ask_question_to_gpt3(local_driver, prompt)

        # response expect something like "Based on the HTML provided, here is the array of words that should fill in the blanks, sorted by the index of the corresponding blank:['to bring it into conformity', 'seasonal rentals', 'furniture']Explanation:Therefore, the array ['to bring it into conformity', 'seasonal rentals', 'furniture'] represents the words that should be used to fill in the respective blanks in the given HTML text, sorted by the index of the blanks." retrive the array of words by split by [
        response = response.split("[")[1]
        response = response.split("]")[0]
        response = response.split(",")
        response = [word.replace("'", "").strip() for word in response]

        # response is like ['seasonal rentals', 'to bring it into conformity', 'furniture']
        # get span elements and click them in the order of response
        if len(response) == len(list_words):
            for word in response:
                xpath_span = "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/span[text()='%s']" % word
                span = local_driver.find_element(By.XPATH, xpath_span)
                span.click()
                time.sleep(1)

    except:
        pass

    #go_to_next_question(local_driver)






def match_words_answer(local_driver, context):
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


def order_words_answer(local_driver, context):
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


def multiple_choice_answer(local_driver, context):
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
    if len(list_btn) == 0:
        time.sleep(5)
        return "end"
    for btn in list_btn:
        if btn.text in desired_text:
            btn.click()
            break

def ask_question_to_gpt3(local_driver, question):

    get_answer_gpt = False

    switch_to_new_tab(local_driver, 1)
    time.sleep(2)
    text_area_xpath = "/html/body/div[1]/div[1]/div[2]/div/main/div[3]/form/div/div/textarea"
    text_area = WebDriverWait(local_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, text_area_xpath)))
    text_area.send_keys(question)

    btn_send_xpath = "/html/body/div[1]/div[1]/div[2]/div/main/div[3]/form/div/div/button"
    btn_send = WebDriverWait(local_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, btn_send_xpath)))
    btn_send.click()

    time.sleep(10)

    answer = None

    while not get_answer_gpt :
        x_path_status = "/html/body/div[1]/div[1]/div[2]/div/main/div[3]/form/div/div[1]/div/button"
        btn_status = WebDriverWait(local_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, x_path_status)))
        if btn_status.text == "Regenerate response":

            parent_all_answer = "/html/body/div[1]/div[1]/div[2]/div/main/div[2]/div/div/div"
            all_answer = WebDriverWait(local_driver, 10).until(
                EC.presence_of_element_located((By.XPATH, parent_all_answer)))
            if all_answer is not None:
                selector = "text-base"
                div_answer = local_driver.execute_script("return arguments[0].getElementsByClassName(arguments[1])",all_answer, selector)
                if len(div_answer) > 0:
                    # get all p tag in div

                    # get me last div in div_answer
                    div = div_answer[len(div_answer) - 1]

                    p_elements = local_driver.execute_script("return arguments[0].getElementsByTagName('p')", div)

                    text = ""
                    for p in p_elements:
                        text += p.text
                    answer = text
                    if answer is not None:
                        get_answer_gpt = True
                        break

    switch_to_new_tab(local_driver, 0)
    return answer

def switch_to_new_tab(local_driver, tab):
    time.sleep(2)
    local_driver.switch_to.window(local_driver.window_handles[tab])
    time.sleep(2)


if __name__ == '__main__':
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-popup-blocking")
    driver = uc.Chrome(options=chrome_options)
    driver.get(url_base)

    # make new tab
    driver.execute_script("window.open('https://chat.openai.com/', 'new_tab');")
    time.sleep(2)

    switch_to_new_tab(driver, 1)

    # wait user to login to openai

    is_connected_To_openai = False

    while not is_connected_To_openai:
        xpath_user_ai = "/html/body/div[1]/div[1]/div[1]/div/div/div/nav/div[4]/div/button"
        time.sleep(2)
        print("Waiting for user to login to openai")
        try:
            user_ai = driver.find_element(By.XPATH, xpath_user_ai)
            is_connected_To_openai = True
        except:
            pass

    switch_to_new_tab(driver, 0)

    try:
        login(driver)
        try:
            got_to_orga(driver)
        except:
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

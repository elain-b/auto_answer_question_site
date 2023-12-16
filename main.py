import time

import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import pyautogui

# executable_path=r"/Users/taniteiko/Documents/auto-ans-q/chromedriver"
# driver = webdriver.Chrome()
# driver.get('https://infoq.jp/')
# login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='spLoginBtn login-button index--header_login modal-syncer']")))
# login_button.click()

# pyautogui.moveTo(100, 100)
# pyautogui.moveTo(1797, 857)

# x, y = pyautogui.position()
# print(f"カーソルの現在位置: {x}, {y}")


email="tteiko.55@gmail.com"
password="qy2kvdPSkSHNJ2d"

executable_path=r"/Users/taniteiko/Documents/auto-ans-q/chromedriver"
service = Service(executable_path=executable_path)
driver = webdriver.Chrome(service=service)
driver.get('https://infoq.jp/')
# login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".spLoginBtn")))
# login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='spLoginBtn login-button index--header_login modal-syncer']")))
# login_button = driver.find_element(By.CSS_SELECTOR, ".login-button")
# login_button.click()
# print(login_button.text)

elements = driver.find_elements(By.CSS_SELECTOR, ".header-buttons > *")
for element in elements:
    # print(element.get_attribute("innerHTML"))
    if "ログイン" in element.text:
        element.click()
        break

email_input = driver.find_element(By.ID, "AccountEmail")
email_input.clear()
email_input.send_keys(email)
passward_input = driver.find_element(By.ID, "AccountPassword")
passward_input.clear()
passward_input.send_keys(password)
login_button = driver.find_element(By.ID, "modal_login_button")
login_button.click()

current_window_handle = driver.current_window_handle
# print(current_window_handle)


new_window_handle = None
# target_texts = ["商社", "その他", "女性", "応募しない", "同居している人はいない", "スマートフォン"]
# nxt_btn = "次へ"

# def click_element_with_text(driver, text):
#     # elements = driver.find_elements(By.XPATH, "//*[contains(text(), '{}')]".format(text))
#     # elements = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '{}')]".format(text))))
#     # elements = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[contains(text(), '{}')]".format(text))))
#     elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(), '{}')]".format(text))))
#     print(elements[0])
#     if elements:
#         element = elements[0]
#         element.click()
#         return True
#     return False

# アンケートリンク
# element = driver.find_element_by_class_name("contentLine2_title")
# print(element.text)

enq_links = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#enquete-list-active_jp li.right-enqList_list a")))
# element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.contentLine2_title')))
# enq_links_list = [link.get_attribute("href") for link in enq_links]



target_texts = ["女性", "30", "正社員", "その他の業種", "未婚", "フルタイム", "文字4"]

# ページ内にradioタグ、checkbox、またはtextboxが存在するか判定する関数
def check_elements_exist():
    radio_elements = driver.find_elements(By.XPATH, "//input[@type='radio']")
    checkbox_elements = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    textbox_elements = driver.find_elements(By.XPATH, "//input[@type='text']")
    
    if radio_elements or checkbox_elements or textbox_elements:
        print("ラジオかテキストかドロップダウンがありました")
        return True  # 要素が存在する場合はTrueを返す
    else:
        return False  # 要素が存在しない場合はFalseを返す

# 「次」という文字を探してクリックする関数
def click_next_element():
    next_button = driver.find_element(By.XPATH, "//*[contains(text(), '次')]")
    next_button.click()

# アンケート回答後次のページに移動する用の関数
def go_to_next_page():
    # next_button = driver.find_element(By.XPATH, "//*[contains(text(), '次')]")
    next_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
    next_button.click()
    # ページ遷移後の待機や処理を記述する（必要に応じて追加する）
    print("次へクリック")

# ページ内にtextboxがあり、「歳」という文字があるかを判定して処理を行う関数
def check_textbox_and_input():
    textbox_elements = driver.find_elements(By.XPATH, "//input[@type='tel']")
    yearold_element = driver.find_element(By.XPATH, "//*[contains(text(), '歳')]")
    for textbox in textbox_elements:
        if yearold_element:
            textbox.send_keys("32")
            return True  # 「歳」という文字が含まれるtextboxに入力した場合はTrueを返す
    return False  # 該当するtextboxが見つからなかった場合はFalseを返す

# ページ内にドロップダウンがあり、「東京」という文字があるかを判定して処理を行う関数
def check_dropdown_and_select():
    dropdown_elements = driver.find_elements(By.XPATH, "//select")
    for dropdown in dropdown_elements:
        options = dropdown.find_elements(By.XPATH, ".//option")
        for option in options:
            if "東京" in option.text:
                dropdown.click()
                option.click()
                return True  # 「東京」という文字を含むドロップダウンを選択した場合はTrueを返す
    return False  # 該当するドロップダウンが見つからなかった場合はFalseを返す

# 全てのアンケートリンクが格納されたリストを回す
for link in enq_links:
    while True:
        try:
            time.sleep(2)
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "contentLine2_title")))
            print("アンケートページを開く")
            element.click()


            # 別ウィンドウにフォーカス
            all_window_handles = driver.window_handles
            for handle in all_window_handles:
                if handle != current_window_handle:
                    new_window_handle = handle
                    break
            driver.switch_to.window(new_window_handle)

            #  回答スタートボタンクリック
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "enqueteStartBtn")))
            button.click()
            print("アンケート開始")

            # 2個目の回答スタートボタンクリック
            # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="次へ進む"]')))
            # element.click()

            # 2個目の回答スタートボタンクリック
            if not check_elements_exist():
                click_next_element()
            else:
                print("2個目の回答スタートボタンがありませんでした")

            while True:
                # ページ内にtextboxがあり、「歳」という文字があるかを判定
                if check_textbox_and_input():
                    print("Textboxに入力しました")
                else:
                    print("Textboxが存在しないか、条件に該当する要素が見つかりませんでした")

                # ページ内にドロップダウンがあり、「東京」という文字があるかを判定
                if check_dropdown_and_select():
                    print("ドロップダウンを選択しました")
                else:
                    print("ドロップダウンが存在しないか、条件に該当する要素が見つかりませんでした")

                # リスト内の文字を探すループ処理
                for text in target_texts:
                    try:
                        element = driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
                        element.click()
                        # クリック後の処理を記述する（必要に応じて追加する）
                        
                        # 次へのボタンを押して次のページに遷移
                        go_to_next_page()
                        time.sleep(5)
                    except NoSuchElementException:
                        print(f"ページ内に'{text}'が見つかりませんでした")
                        # 見つからなかった場合の処理を記述する（必要に応じて追加する）
                break
                
            # ページ内の次の文字を探す前に、最後のページでないかをチェック
            if not driver.find_elements(By.XPATH, "//*[contains(text(), '次')]"):
                break
            
            # 1ページ分の回答が終わったら次のページに移動
            click_next_element()

            time.sleep(10)
            # ウィンドウを閉じる
            driver.close()
            # ウィンドウのフォーカスを元に戻す
            driver.switch_to.window(current_window_handle)
            time.sleep(10)
        except NoSuchElementException:
            print("アンケートリンクが見つかりませんでした")
            # ウィンドウを閉じる
            driver.close()
            # ウィンドウのフォーカスを元に戻す
            driver.switch_to.window(current_window_handle)
            break
# try:
#     p = pyautogui.locateOnScreen("./img/1.png")
#     x, y = pyautogui.center(p)
#     pyautogui.click(x, y)
#     time.sleep(1)
# except:
#     pass

# try:
#     p = pyautogui.locateOnScreen("./img/2.png")
#     x, y = pyautogui.center(p)
#     pyautogui.click(x, y)
#     time.sleep(5)
# except:
#     pass
# try:
#     p = pyautogui.locateOnScreen("./img/3.png", grayscale=True, confidence=.6)
#     x, y = pyautogui.center(p)
#     pyautogui.click(x, y)
#     print(x, y)
#     time.sleep(5)
# except:
#     pass

# 2個目の回答スタートボタンクリック
# element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="次へ進む"]')))
# element.click()

# 全てのアンケートリンクが格納されたリストを回す
# for link in enq_links:
# while True:
#     try:
        # time.sleep(2)
        # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "contentLine2_title")))
        # print("アンケート回答開始")
        # element.click()
    

        # # 別ウィンドウにフォーカス
        # all_window_handles = driver.window_handles
        # for handle in all_window_handles:
        #     if handle != current_window_handle:
        #         new_window_handle = handle
        #         break
        # driver.switch_to.window(new_window_handle)
        # print(new_window_handle)

        # try:
            #  回答スタートボタンクリック
            # button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "enqueteStartBtn")))
            # button.click()


            # 2個目の回答スタートボタンクリック
            # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="次へ進む"]')))
            # element.click()

            # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[value='"その他"']')))
            # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[text()='その他']")))
            # print(element)

            # try:
                # disagree_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '終了')]")))
                # next_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '次')]")))
                # checkboxes = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']")))
                # radiobuttons = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='radio']")))

                # if disagree_element:
                #     disagree_element.click()
                # elif next_element:
                #     next_element.click()
                # elif checkboxes or radiobuttons:
                #     print("ある")
                # else:
                #     print("ない")
            # except NoSuchElementException:
            #     driver.close()
            #     continue

            # elements = driver.find_elements(By.XPATH, "//*")

            # for element in elements:
            #     if "終了" in element.text:
            #         target_element = element
            #         break
            #     if "開始" in element.text:
            #         target_element = element
            #         break
            #     if "次" in element.text:
            #         target_element = element
            #         print('次へ見つかった')
            #         break

            # if target_element:
            #     element = target_element.find_element(By.TAG_NAME, "a")
            #     print(element.get_attribute('innerHTML'))
            #     if target_element.tag_name == "button":
            #         target_element.click()
            #     if target_element.tag_name == "a":
            #         target_element.click()
            #     if target_element.tag_name == "input":
            #         target_element.click()
            #     else:
            #         print("要素がありません")
                # time.sleep(5)
            # else:
            #     print("要素が見つかりませんでした")

            # あらかじめ格納した回答リストを回す
            # for text in target_texts:
            #     time.sleep(5)
            #     elements = driver.find_elements(By.XPATH, "//*[contains(text(), '{}')]".format(text))
            #     if elements:
            #         for element in elements:
            #             print(element.text)

            #             element_type = element.get_attribute("type") 
                        
            #             if element_type == "text":
            #                 actions = ActionChains(driver)
            #                 actions.move_to_element(element).perform()

            #                 element.clear()
            #                 element.send_keys("32")
                        
            #             elif element_type == "radio":
            #                 element.click()
                        
            #             time.sleep(1)
            #             # break
            #     else:
            #         print("要素が見つかりません")
                
            #     # 回答後次へをクリック
            #     element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"]')))
            #     element.click()
                
            #     # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "finishButton")))
            #     # if "次へ" in element.get_attribute("value"):
            #     #     element.click()


            #     time.sleep(2)
            #     break
        # except Exception as e:
            # エラーが発生した場合の処理
            # print("エラーが発生しました:", e)
            # continue

        # time.sleep(2)

        # # ウィンドウを閉じる
        # driver.close()

        # # ウィンドウのフォーカスを元に戻す
        # driver.switch_to.window(current_window_handle)

        # time.sleep(10)

        # table_element = driver.find_elements(By.XPATH, "//table")
        # print(table_element)

        # table = driver.find_element_by_xpath("//table[@class='answerChoiceTable']")
        # rows = table.find_elements_by_xpath(".//tr")
        # for row in rows:
        #     label = row.find_element_by_xpath(".//label")
        #     text = label.text
        #     if any(target_text in text for target_text in target_texts):
        #         # 要素が見つかった場合の処理
        #         element = row.find_element_by_xpath(".//input[@type='radio']")
        #         element.click()
        #         break
        # else:
        #     print("要素が見つからなかった")


        # for text in target_texts:
        #     elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(), '{}')]".format(text))))
        #     print(elements)
        #     time.sleep(5)
            # if click_element_with_text(driver, text):
            #     break
            # else:
            #     print("要素が見つからなかった")

        # break
    # except NoSuchElementException:
    #     print("アンケートリンクが見つかりませんでした")
    #     break


# browser_pid = driver.service.process.pid
# print(f"ブラウザのプロセスID: {browser_pid}")

# ans_element = driver.find_element(By.XPATH, "//span[text()='あなたご自身に関するアンケート']")
# ans_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='あなたご自身に関するアンケート']")))
# ans_element.click()

# options.add_argument("--remote-debugging-port=9222")
# options.add_argument("--user-data-dir=/Users/taniteiko/Library/Application Support/Google/Chrome/Default")




# wait = WebDriverWait(driver, 10)

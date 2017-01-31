
#this will start selenium and set chrome as the active browser

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import datetime
def find_date_time():
    #find date/time
    date_time = ' {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    return date_time

driver = webdriver.Chrome()

url = 'https://app.sproutsocial.com/login'
tweet_text = 'Test tweet from Selenium'+find_date_time()
login_username = 'qatests+homework2@sproutsocial.com'
login_password = 'LbEWMDjuRNaEtDy4Q.G9jrfvEWqt'
reply_txt = 'Thanks for the tweet!'+find_date_time()
driver.get(url)
wait = WebDriverWait(driver, 10);

#sign into application
try:
    username_box = wait.until(EC.presence_of_element_located(('id','signin-email')))
    password_box = wait.until(EC.presence_of_element_located(('id','signin-pw')))
    submit_btn = wait.until(EC.presence_of_element_located(('css selector', '.button._largesubmit._loader.js-login-button')))
    username_box.send_keys(login_username)
    password_box.send_keys(login_password)
    submit_btn.click()
except TimeoutException:
    print('The login page elements were not able to be found within 10 seconds')


#these test cases can be run after login is completed successfully
# 1 - compose tweet and send from home page
try:
    compose_btn = wait.until(EC.element_to_be_clickable(('css selector','.menu-item.third.remainder.compose')))
    compose_btn.click()
except TimeoutException:
    print('The compose button elements were not able to be found within 10 seconds')

try:
    compose_msg = wait.until(EC.presence_of_element_located(('xpath','//*[@id="compose-form"]/div[2]/article/div[1]/div[2]/textarea')))
    compose_submit = wait.until(EC.element_to_be_clickable(('css selector','.primary-action.js-submit-message.js-primary.action._main-compose-action')))
    compose_msg.send_keys(tweet_text)
    compose_submit.click()
except:
    print('The compose message elements were not able to be found within 10 seconds')


# 2 - view messages and reply with comments and also just retweet

messages_btn = wait.until(EC.element_to_be_clickable(('css selector','.menu-item-link.messages')))
messages_btn.click()
element = wait.until(EC.presence_of_element_located(('xpath','//*[@id="recent_msgs"]/div/section[1]/article/div[3]/span[1]')))
if element.get_attribute('innerHTML') != tweet_text:
    print('Latest tweet did not get posted: %s' %tweet_text)

#find latest tweet and reply/retweet
latest_tweet = driver.find_element_by_xpath('//*[@id="recent_msgs"]/div[1]/section[1]/article/section/ul/li[1]/a')
hover = ActionChains(driver).move_to_element(latest_tweet)
hover.perform()
latest_tweet.click()
#input reply message and click button to post
reply_msg = wait.until(EC.presence_of_element_located(('xpath','//*[@id="compose-form"]/div[2]/article/div[1]/div[2]/textarea')))
reply_msg.send_keys(reply_txt)
driver.find_element_by_css_selector('.primary-action.js-submit-message.js-primary.action._main-compose-action').click()
#this click is for a pop-up that asks whether I'm sure I want to reply/retweet my own tweet (in reality this might not always apply)
driver.find_element_by_css_selector('.action.primary-action.js-submit').click()



# 3 - Use calendar to set tweet for future date (this one has not been completed yet)
"""
publishing_tab = wait.until(EC.presence_of_element_located(('css selector','.menu-item-link.publishing')))
publishing_tab.click()
schedule_msg = wait.until(EC.presence_of_element_located(('css selector','.auxcontent-action.action.primary-action.js-schedule-message')))
schedule_msg.click()

next_month = driver.find_element_by_css_selector('.ui-icon.ui-icon-circle-triangle-e')
hover = ActionChains(driver).move_to_element(next_month)
hover.perform()
next_month.click()

"""

driver.close()

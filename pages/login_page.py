from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, email, pw):
        self.driver.get('https://www.traceparts.com/de/sign-in')
        self.driver.maximize_window()

        cookie_button = self.driver.find_element(By.ID, 'didomi-notice-agree-button')
        cookie_button.click()
        self.driver.find_element(By.ID, 'Email').send_keys(email)
        self.driver.find_element(By.ID, 'Password').send_keys(pw)
        self.driver.find_element(By.ID, 'signin-btn').click()

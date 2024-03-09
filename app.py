from flask import Flask, request, jsonify
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import re
import time
import os

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    # Define the login URL within the function
    login_url = 'https://catalogue.bibliothequedequebec.qc.ca/client/fr_CA/general/search/patronlogin/https:$002f$002fcatalogue.bibliothequedequebec.qc.ca$002fclient$002ffr_CA$002fgeneral$002fsearch$002faccount/search.Login.Failed?dt=list'

    # Get username and password from the request
    username = request.json.get('username')
    password = request.json.get('password')

    # Set up Firefox options
    options = FirefoxOptions()
    options.add_argument("--headless")


    #Geckodriver path
    geckodriver_path = 'PATH FOR GECKODRIVER'
    os.environ['PATH'] += os.pathsep + geckodriver_path
    # Create a Firefox WebDriver instance with headless option
    driver = webdriver.Firefox(options=options)

    try:
        # Open the login page
        driver.get(login_url)

        # Wait for the username field to be visible
        username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'j_username')))
        # Find the username field and enter the username
        username_field.send_keys(username)

        # Find the password field using its ID and enter the password
        password_field = driver.find_element(By.ID, 'j_password')
        password_field.send_keys(password)

        # Find and click the login button
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'submit_0')))
        login_button.click()

        # Wait for the login process to complete
        WebDriverWait(driver, 10).until(EC.url_changes(login_url))

        data_to_extract = request.json.get('data_to_extract')

        extracted_data = {}

        # Extract welcome message and selected value
        if 'user_name' in data_to_extract:
            try:
                welcome_message_element = driver.find_element(By.CLASS_NAME, 'welcome')
                welcome_message = welcome_message_element.text
        # Remove "Bienvenue" from the welcome message
                welcome_message = welcome_message.replace("Bienvenue", "").strip()
                extracted_data['welcome_message'] = welcome_message
            except NoSuchElementException:
                extracted_data['welcome_message'] = None

        #email
        if 'email' in data_to_extract:
            time.sleep(2)  # Add a delay to allow time for the element to load
            try:
                email_element = driver.find_element(By.CLASS_NAME, 'email')
                email_value = email_element.get_attribute('value')
                extracted_data['email'] = email_value
            except NoSuchElementException:
                extracted_data['email'] = None


        if 'biblio_pref' in data_to_extract:
            try:
                dropdown_element = driver.find_element(By.ID, 'pickupLibrary')
                selected_value = dropdown_element.get_attribute('value')
                extracted_data['selected_value'] = selected_value
            except NoSuchElementException:
                extracted_data['selected_value'] = None


        # Extract total prêts
        if 'total_prets' in data_to_extract:
            try:
                pret_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ui-id-12')))
                pret_link.click()
                total_prets_div = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "Total des prêts :")]')))
                total_prets_text = total_prets_div.text
                total_prets_value = re.search(r'\d+', total_prets_text).group()
                extracted_data['total_prets_value'] = total_prets_value
            except NoSuchElementException:
                extracted_data['total_prets_value'] = None


        # Extract documents en retard
        if 'docs_retard' in data_to_extract:
            try:
                pret_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ui-id-12')))
                pret_link.click()
                documents_en_retard_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'verticalCenterSingleLine')))
                documents_en_retard_text = documents_en_retard_element.text
                documents_en_retard_value = re.search(r'\d+', documents_en_retard_text).group()
                extracted_data['docs_retard_value'] = documents_en_retard_value
            except NoSuchElementException:
                extracted_data['docs_retard_value'] = None


        # Extract frais table
        if 'frais_table' in data_to_extract:
            try:
                frais_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ui-id-14')))
                frais_tab.click()
                frais_table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "payFinesTable")))
                frais_table_html = frais_table.get_attribute("outerHTML")
                extracted_data['frais_table_html'] = frais_table_html
            except NoSuchElementException:
                extracted_data['frais_table_html'] = None


        # Extract payment history table
        if 'payment_history_table' in data_to_extract:
            try:
                frais_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ui-id-14')))
                frais_tab.click()
                payment_history_table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "paymentHistoryTable")))
                payment_history_table_html = payment_history_table.get_attribute("outerHTML")
                extracted_data['payment_history_table_html'] = payment_history_table_html
            except NoSuchElementException:
                extracted_data['payment_history_table_html'] = None


        return jsonify(extracted_data)

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})

    finally:
        # Close the browser window after 10 seconds
        time.sleep(1)
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)

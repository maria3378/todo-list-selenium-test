from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import logging
import os

# Configure logging
logging.basicConfig(filename='test_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Setup Chrome options
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Uncomment for CI/CD or headless testing

# Setup ChromeDriver
service = Service()
driver = webdriver.Chrome(service=service, options=options)

try:
    # Load the Todo List App locally
    filepath = f"file://{os.path.abspath('index.html')}"
    driver.get(filepath)
    logging.info("Loaded Todo List App.")

    # Locate input and button
    task_input = driver.find_element(By.ID, "taskInput")
    add_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Add Task')]")

    # Add task
    task_text = "Buy groceries"
    task_input.send_keys(task_text)
    add_button.click()
    logging.info(f"Sent task: {task_text}")

    # Wait for task to appear
    wait = WebDriverWait(driver, 5)
    new_task = wait.until(EC.presence_of_element_located((By.XPATH, f"//ul[@id='taskList']/li[contains(text(), '{task_text}')]")))

    # Assert
    assert task_text in new_task.text
    logging.info("Task successfully added and verified.")

except (AssertionError, TimeoutException) as e:
    logging.error("Test failed", exc_info=True)
    driver.save_screenshot("error_screenshot.png")
finally:
    driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

service = Service("C:/Users/aryan/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")  # Update with your path to chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_soup(url):
    driver.get(url)
    try:
        # Wait for the presence of a specific element that indicates the page has fully loaded
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-hook='review']")))
    except Exception as e:
        print(f"Error while waiting for page to load: {e}")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_reviews(soup):
    review_containers = soup.find_all('div', {'data-hook': 'review'})
    if not review_containers:
        print("No review containers found.")
    with open("C:/Users/aryan/Downloads/amazon_reviews.txt", 'a', encoding='utf-8') as f:
        for review in review_containers:
            try:
                review_text = review.find('span', {'data-hook': 'review-body'}).text.strip()
                review_rating = float(review.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip())
                print(review_rating)
                print(review_text)
                f.write(f'Rating: {review_rating}\n')
                f.write(f'Review: {review_text}\n\n')
            except Exception as e:
                print(f"Error while processing review: {e}")

link = "https://www.amazon.com/Mighty-Patch-Hydrocolloid-Absorbing-count/product-reviews/B074PVTPBW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
link = link.replace("&reviewerType=all_reviews", "")
x = 1
with open("C:/Users/aryan/Downloads/amazon_reviews.txt", 'w', encoding='utf-8') as f:
    f.write("Reviews: \n")

while x < 4:
    soup = get_soup(link + f"&reviewerType=all_reviews&pageNumber={x}")
    print(f'Getting page: {x}')
    get_reviews(soup)
    x += 1

driver.quit()
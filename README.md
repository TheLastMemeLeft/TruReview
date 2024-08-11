Project Name: Sentiment Analysis of Product Reviews
Overview
This project performs sentiment analysis on product reviews using Google's Generative AI model. It processes both historical and recent reviews, visualizes sentiment data using pie charts, and provides detailed insights into positive and negative factors affecting the product.

Project Structure
amznscraper.py: A web scraping script that collects reviews from Amazon.
sentiment_analysis.py: The main script that performs sentiment analysis and generates visualizations.
amazon_reviews.txt: A file containing historical reviews.
amazon_recent_reviews.txt: A file containing recent reviews.
chromedriver_amzn_scraper.py: A substitute scraper that uses chromedriver instead of docker (less effective)

1. Prerequisites
Docker Desktop: Install Docker Desktop from Docker's official website.

Follow the instructions to install splash:
https://splash.readthedocs.io/en/stable/

or follow this simple video tutorial:
https://www.youtube.com/watch?v=8q2K41QC2nQ


Make sure you have the following Python packages installed:

google-generativeai
Pillow
matplotlib
re
textwrap

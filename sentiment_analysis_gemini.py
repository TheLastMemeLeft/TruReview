key = ""  # PUT YOUR API KEY HERE






import google.generativeai as genai
import PIL.Image
import os
import time
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
from textwrap import wrap




# Set API key
genai.configure(api_key=key)

# Load reviews with UTF-8 encoding
with open("amazon_reviews.txt", 'r', encoding='utf-8') as f:
    txt = f.read()

# Generate sentiment analysis for most relevant reviews
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content([
    "Perform a sentiment analysis on the product using the reviews. Your response should follow the response structure shown:",
    "**Positive:** (percentage of positive reviews)",
    "**Neutral:** (Percentage of neutral reviews)", 
    "**Negative:** (Percentage of Negative reviews)",
    "**Positive Factors:** (list of positive factors)",
    "**Negative Factors:** (list of negative factors)",
    "**Overall:** (Overall sentiment analysis)", txt])

time.sleep(30)  # Sleep to avoid monetary charges from Gemini

genai.configure(api_key=key)

# Load recent reviews with UTF-8 encoding
with open("amazon_recent_reviews.txt", 'r', encoding='utf-8') as g:
    txt2 = g.read()

# Generate sentiment analysis for recent reviews
response2 = model.generate_content([
    "Perform a sentiment analysis on the product using the reviews. Your response should follow the response structure shown:",
    "**Positive:** (percentage of positive reviews)",
    "**Neutral:** (Percentage of neutral reviews)", 
    "**Negative:** (Percentage of Negative reviews)",
    "**Positive Factors:** (list of positive factors)",
    "**Negative Factors:** (list of negative factors)",
    "**Overall:** (Overall sentiment analysis)", txt2])


print(response.text)
print(response2.text)

# Function to extract sentiment data and factors (Improved)
def extract_sentiment_data(raw_text):
    sentiment_data = {'Positive': 0.0, 'Neutral': 0.0, 'Negative': 0.0} 
    positive_factors, negative_factors, overall_summary = [], [], ""
    positive_match = re.search(r"\*\*Positive:\*\* (\d+\.?\d*)%", raw_text)
    neutral_match = re.search(r"\*\*Neutral:\*\* (\d+\.?\d*)%", raw_text)
    negative_match = re.search(r"\*\*Negative:\*\* (\d+\.?\d*)%", raw_text)

    if positive_match and neutral_match and negative_match:
        sentiment_data = {
            'Positive': float(positive_match.group(1)),
            'Neutral': float(neutral_match.group(1)),
            'Negative': float(negative_match.group(1))
        }
    else:
        print("Error: Unable to extract sentiment percentages. Please check the input format.")
        sentiment_data = None

# Extract positive factors
    positive_factors_match = re.search(r"\*\*Positive Factors:\*\*\n(.*?)\n\n", raw_text, re.DOTALL)
    if positive_factors_match:
        positive_factors = positive_factors_match.group(1).strip().split('\n* ')
        positive_factors = [factor.replace('* **', '').replace(':**', ':') for factor in positive_factors]
    else:
        print("Error: Unable to extract positive factors. Please check the input format.")
        positive_factors = []

    # Extract negative factors
    negative_factors_match = re.search(r"\*\*Negative Factors:\*\*\n(.*?)\n\n", raw_text, re.DOTALL)
    if negative_factors_match:
        negative_factors = negative_factors_match.group(1).strip().split('\n* ')
        negative_factors = [factor.replace('* **', '').replace(':**', ':') for factor in negative_factors]
    else:
        print("Error: Unable to extract negative factors. Please check the input format.")
        negative_factors = []

    # Extract overall summary
    overall_match = re.search(r"\*\*Overall:\*\*\s*([\s\S]*)", raw_text)
    if overall_match:
        overall_summary = overall_match.group(1).strip()
    else:
        print("Error: Unable to extract overall summary. Please check the input format.")
        overall_summary = "No overall summary available."

    return sentiment_data, positive_factors, negative_factors, overall_summary

# Extract data for both relevant and recent reviews
sentiment_data_relevant, positive_factors_relevant, negative_factors_relevant, overall_summary_relevant = extract_sentiment_data(response.text)
sentiment_data_recent, positive_factors_recent, negative_factors_recent, overall_summary_recent = extract_sentiment_data(response2.text)

# Wrap text for formatting
def wrap_text(text, width):
    wrapped_lines = []
    for line in text.split('\n'):
        wrapped_lines.extend(wrap(line, width=width))
    return '\n'.join(wrapped_lines)

# Wrapped text for relevant reviews
positive_factors_text_relevant = wrap_text('Positive Factors:\n' + '\n'.join(positive_factors_relevant), width=100)
negative_factors_text_relevant = wrap_text('Negative Factors:\n' + '\n'.join(negative_factors_relevant), width=100)
overall_summary_text_relevant = wrap_text('Overall:\n' + overall_summary_relevant, width=100)

# Wrapped text for recent reviews
positive_factors_text_recent = wrap_text('Positive Factors:\n' + '\n'.join(positive_factors_recent), width=100)
negative_factors_text_recent = wrap_text('Negative Factors:\n' + '\n'.join(negative_factors_recent), width=100)
overall_summary_text_recent = wrap_text('Overall:\n' + overall_summary_recent, width=100)

# Choose mode: "dark" or "light"
mode = "light"  # Change to "light" for light mode

# Set colors based on mode
if mode == "dark":
    background_color = '#2b2c30'
    text_color = 'white'
    pie_colors = ['#ab9ff3', '#ffa07a', '#ff6347']  # rgb(171,160,243), orange, red
elif mode == "light":
    background_color = 'white'
    text_color = 'black'
    pie_colors = ['#4682b4', '#ff6347', '#ffa500']  # blue, red, orange

# Path to your font file
font_path = "C:/Users/aryan/Downloads/Sentiment Analysis/fonts/Nunito/static/Nunito-Light.ttf" # Update with your path

# Load the custom font
font_properties = fm.FontProperties(fname=font_path)

# Ensure explode length matches data length
explode_relevant = (0.1, 0, 0)[:len(sentiment_data_relevant)]
explode_recent = (0.1, 0, 0)[:len(sentiment_data_recent)]

# Create figure and subplots for pie charts
fig, axs = plt.subplots(2, 2, figsize=(18, 16), gridspec_kw={'height_ratios': [1, 1]})
fig.patch.set_facecolor(background_color)  # Set background color

# Pie chart for relevant reviews
axs[0, 0].pie(sentiment_data_relevant.values(), explode=explode_relevant, 
              labels=sentiment_data_relevant.keys(), colors=pie_colors,
              autopct='%1.1f%%', shadow=True, startangle=140, 
              textprops={'color': text_color, 'fontproperties': font_properties})
axs[0, 0].patch.set_facecolor(background_color) 
axs[0, 0].set_title("Most Relevant Reviews", color=text_color, fontproperties=font_properties)

# Text underneath the relevant reviews pie chart
axs[1, 0].axis('off')
text_relevant = f"{positive_factors_text_relevant}\n\n{negative_factors_text_relevant}\n\n{overall_summary_text_relevant}"
axs[1, 0].text(0.5, 0.05, text_relevant, fontsize=10, va='bottom', ha='center', color=text_color, fontproperties=font_properties, 
             bbox={'facecolor': 'lightgray', 'alpha': 0.5, 'pad': 10}) 

# Pie chart for recent reviews
axs[0, 1].pie(sentiment_data_recent.values(), explode=explode_recent,
              labels=sentiment_data_recent.keys(), colors=pie_colors, 
              autopct='%1.1f%%', shadow=True, startangle=140, 
              textprops={'color': text_color, 'fontproperties': font_properties})
axs[0, 1].patch.set_facecolor(background_color)
axs[0, 1].set_title("Most Recent Reviews", color=text_color, fontproperties=font_properties)

# Text underneath the recent reviews pie chart
axs[1, 1].axis('off')
text_recent = f"{positive_factors_text_recent}\n\n{negative_factors_text_recent}\n\n{overall_summary_text_recent}"
axs[1, 1].text(0.5, 0.05, text_recent, fontsize=10, va='bottom', ha='center', color=text_color, fontproperties=font_properties, 
             bbox={'facecolor': 'lightgray', 'alpha': 0.5, 'pad': 10})

plt.tight_layout()
plt.show()



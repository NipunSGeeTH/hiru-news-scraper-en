import requests
from bs4 import BeautifulSoup
import time 
import json


def scrape_hirunews_page(url):
    """Scrapes news articles from a single page of Hiru News."""

    response = requests.get(url)
    response.raise_for_status()  

    soup = BeautifulSoup(response.content, 'lxml')

    articles = []
    article_elements = soup.find_all('div', class_='row', style='margin-bottom:10px') 

    for article_element in article_elements:
        try:
            title_element = article_element.find('div', class_='all-section-tittle').find('a')
            title = title_element.text.strip() if title_element else "N/A"
            link = title_element['href'] if title_element else "N/A"
            news_id = link.split("/")[-2] if link else "N/A"

            date_time_element = article_element.find('div', class_='middle-tittle-time')
            date_time = date_time_element.text.strip() if date_time_element else "N/A"

            # Extract image link
            image_element = article_element.find('div', class_='sc-image').find('img')
            image_link = image_element['src'] if image_element else "N/A" 

            

            articles.append({
                'news_id': news_id,
                'title': title,
                'link': link, 
                'date_time': date_time,
                'image_link': image_link
               

            })
        except Exception as e:
            print(f"Error scraping article: {e}")

    return articles

if __name__ == '__main__':
    base_url = 'https://www.hirunews.lk/english/local-news.php?pageID='
    num_pages = 1  # Scrape the first 1 pages (adjust as needed)

    all_articles = []

    for page in range(1, num_pages + 1):
        url = f"{base_url}{page}"
        print(f"Scraping page: {url}")
        all_articles.extend(scrape_hirunews_page(url))
        time.sleep(1)  


    with open("HiruNews_articles_headlines.json", "w", encoding='utf-8') as json_file:
        json.dump(all_articles, json_file, ensure_ascii=False, indent=4)

    # Output or further process the scraped data
for article in all_articles:
    print("News ID:", article['news_id'])
    print("Title:", article['title'])
    print("Link:", article['link'])
    print("Date/Time:", article['date_time'])
    print("Image:", article['image_link'])
    print("\n")




    # Load the news articles
with open('HiruNews_articles_headlines.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Find new articles
new_articles = [article for article in articles]

# Display and save new articles
if new_articles:
    Full_News_With_Contents = []
    for article in new_articles:



        url=article['link']
            

        

        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.content, 'lxml')
        paragraph_div = soup.find('div', id='article-phara2')

        if paragraph_div:
            for br in paragraph_div.find_all("br\br"):
                br.replace_with("\n")  
            paragraph_text = paragraph_div.get_text(separator="\n")
            paragraph_text = paragraph_text.strip()
            paragraph_text = paragraph_text
            print(paragraph_text)
        else:
            print("Paragraph not found") 




        news_item = {
            "ID": article['news_id'],
            "Title": article['title'],
            "Link": article['link'],
            "Date": article['date_time'],
            "Image": article['image_link'],
            "Paragraph" : paragraph_text
        }
        Full_News_With_Contents.append(news_item)
        

    # Save the new articles to Full_News_With_Contents.json
    with open('Full_News_With_Contents.json', 'w', encoding='utf-8') as f:  # 'w' mode overwrites the file
        json.dump(Full_News_With_Contents, f, ensure_ascii=False, indent=4)

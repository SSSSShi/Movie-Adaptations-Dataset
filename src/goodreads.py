import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import csv

def clean_number(text):
    """Remove commas and convert to number"""
    try:
        return int(text.replace(',', ''))
    except:
        return 0

def clean_name(name):
    """Remove quotes from beginning and end of name"""
    return name.strip('"')

def get_page_url(base_url, page):
    """Generate URL for each page"""
    if page == 1:
        return base_url
    return f"{base_url}?page={page}"

def extract_float_safely(match):
    """Safely extract float from regex match"""
    if match:
        try:
            return float(match.group(1))
        except:
            return 0.0
    return 0.0

def scrape_goodreads_list(base_url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        all_books = []
        page = 1
        
        while True:
            url = get_page_url(base_url, page)
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            book_items = soup.find_all('tr', {'itemtype': 'http://schema.org/Book'})
            
            if not book_items:  # No more books found
                break
                
            for item in book_items:
                try:
                    # Get book title
                    title_element = item.find('a', {'class': 'bookTitle'})
                    if not title_element:
                        continue
                    name = clean_name(title_element.text.strip())
                    
                    # Get author
                    author_text = item.find('span', {'itemprop': 'author'})
                    if not author_text or not author_text.find('a'):
                        continue
                    author = author_text.find('a').text.strip()
                    
                    # Get rating information
                    rating_span = item.find('span', {'class': 'greyText'})
                    rating_text = rating_span.text.strip() if rating_span else ""
                    
                    # Extract average rating
                    avg_rating_match = re.search(r'(\d+\.\d+)\s*avg', rating_text)
                    avg_rating = extract_float_safely(avg_rating_match)
                    
                    # Extract rating count
                    rating_count_match = re.search(r'[—–]\s*([\d,]+)\s*ratings', rating_text)
                    rating_count = clean_number(rating_count_match.group(1)) if rating_count_match else 0
                    
                    # Get score
                    score_text = item.find(text=lambda t: t and ('score:' in t.lower() or 'score' in t.lower()))
                    score_match = re.search(r'score:?\s*([\d,]+)', score_text) if score_text else None
                    score = float(score_match.group(1).replace(',', '')) if score_match else 0.0
                    
                    # Get vote count
                    votes_text = item.find(text=lambda t: t and 'people voted' in t)
                    votes_match = re.search(r'(\d+)\s*people voted', votes_text) if votes_text else None
                    vote_count = int(votes_match.group(1)) if votes_match else 0
                    
                    all_books.append({
                        'Name': name,
                        'Author': author,
                        'Avg Rating': round(avg_rating, 2),  # Round to 2 decimal places
                        'Rating Count': rating_count,
                        'Score': round(score, 1),  # Round to 1 decimal place
                        'Vote Count': vote_count
                    })
                    
                    print(f"Processed: {name}")
                    
                except Exception as e:
                    print(f"Error processing book '{name if 'name' in locals() else 'unknown'}': {str(e)}")
                    continue
            
            print(f"Completed page {page}")
            page += 1
            time.sleep(1)  # Delay between pages
        
        if all_books:
            df = pd.DataFrame(all_books)
            
            # Save to CSV without quotes
            with open('best_movie_adaptations.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, 
                                      fieldnames=['Name', 'Author', 'Avg Rating', 'Rating Count', 'Score', 'Vote Count'],
                                      quoting=csv.QUOTE_NONE,
                                      escapechar='\\')
                writer.writeheader()
                for book in all_books:
                    writer.writerow(book)
            
            print(f"\nSuccessfully scraped {len(all_books)} books and saved to best_movie_adaptations.csv")
            
            return df
        else:
            print("No books were successfully processed.")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {str(e)}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None


base_url = "https://www.goodreads.com/list/show/17956.Best_Movie_Adaptations"
df = scrape_goodreads_list(base_url)
if df is not None:
    print("\nFirst few entries:")
    print(df.head())
else:
    print("\nFailed to create dataset.")
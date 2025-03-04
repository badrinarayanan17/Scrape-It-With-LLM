# Tried with psaw

import os
import praw
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timezone
from psaw import PushshiftAPI
import time

# Load environment variables
load_dotenv()

def scrape_reddit_data(subreddit_name, limit=10000, start_year=2019, end_year=2024, min_comments=10):
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )
    
    api = PushshiftAPI(reddit)
    
    start_epoch = int(datetime(start_year, 1, 1).timestamp())
    end_epoch = int(datetime(end_year, 12, 31, 23, 59, 59).timestamp())
    
    posts = []
    count = 0
    
    try:
        for submission in api.search_submissions(subreddit=subreddit_name,
                                                 after=start_epoch,
                                                 before=end_epoch,
                                                 filter=['id', 'title', 'selftext', 'url', 'author', 
                                                         'score', 'num_comments', 'created_utc', 'subreddit',
                                                         'permalink', 'is_self', 'is_video', 'over_18', 
                                                         'spoiler', 'stickied'],
                                                 limit=limit):
            if submission.num_comments >= min_comments:
                posts.append({
                    'id': submission.id,
                    'title': submission.title,
                    'selftext': submission.selftext,
                    'url': submission.url,
                    'author': str(submission.author),
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'created_utc': datetime.fromtimestamp(submission.created_utc, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                    'subreddit': submission.subreddit.display_name,
                    'permalink': submission.permalink,
                    'is_self': submission.is_self,
                    'is_video': submission.is_video,
                    'over_18': submission.over_18,
                    'spoiler': submission.spoiler,
                    'stickied': submission.stickied
                })
                count += 1
                if count % 100 == 0:
                    print(f"Scraped {count} posts...")
                if count >= limit:
                    break
    except Exception as e:
        print(f"An error occurred while scraping: {e}")
    
    # Sort posts by number of comments in descending order
    posts.sort(key=lambda x: x['num_comments'], reverse=True)
    
    return posts

def save_reddit_data_to_excel(data, output_folder='output'):
    os.makedirs(output_folder, exist_ok=True)
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Reorder columns
    columns_order = ['id', 'title', 'selftext', 'url', 'author', 'score', 'num_comments', 
                     'created_utc', 'subreddit', 'permalink', 'is_self', 'is_video', 
                     'over_18', 'spoiler', 'stickied']
    df = df[columns_order]
    
    # Generate timestamp for the filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save as Excel
    excel_output_path = os.path.join(output_folder, f'reddit_data_15/10/24{timestamp}.xlsx')
    
    with pd.ExcelWriter(excel_output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Posts', index=False)
        
        # Adjust column widths
        worksheet = writer.sheets['Posts']
        for idx, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).map(len).max(), len(col))
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)  # limit to 50 for readability
    
    print(f"Reddit data saved to Excel at {excel_output_path}")

if __name__ == "__main__":
    try:
        subreddit_name = input("Enter the subreddit name to scrape (e.g., 'ADHD'): ")
        limit = int(input("Enter the number of posts to scrape (default is 10000): ") or 10000)
        start_year = int(input("Enter the start year for filtering (default is 2019): ") or 2019)
        end_year = int(input("Enter the end year for filtering (default is 2024): ") or 2024)
        min_comments = int(input("Enter the minimum number of comments for a post to be included (default is 10): ") or 10)
        
        print(f"Scraping data from r/{subreddit_name}...")
        start_time = time.time()
        reddit_data = scrape_reddit_data(subreddit_name, limit, start_year, end_year, min_comments)
        end_time = time.time()
        
        print(f"Scraping completed. Total posts scraped: {len(reddit_data)}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        
        print("Saving data to Excel...")
        save_reddit_data_to_excel(reddit_data)
        
        print("Data scraping and saving complete!")
    
    except Exception as e:
        print(f"An error occurred: {e}")
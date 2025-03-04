# Scraping the ADHD related data from reddit social media

import os
import praw
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timezone
import time

load_dotenv()

# Creating Reddit Instance
def create_reddit_instance(): 
    return praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )

# This function will scrape the reddit data
def scrape_reddit_data(subreddit_name, limit=6000, start_year=2019, end_year=2024, min_comments=90):
    reddit = create_reddit_instance()
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    start_date = datetime(start_year, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(end_year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

    print(f"Scraping posts from r/{subreddit_name} between {start_date} and {end_date}")

    # List of sorting methods to try
    sort_methods = ['top', 'hot', 'new', 'controversial']
    time_filters = ['all', 'year', 'month', 'week', 'day']

    for sort_method in sort_methods:
        for time_filter in time_filters:
            if len(posts) >= limit:
                break

            print(f"Trying {sort_method} posts, time filter: {time_filter}")
            
            try:
                if sort_method == 'top' or sort_method == 'controversial':
                    submission_stream = getattr(subreddit, sort_method)(time_filter=time_filter, limit=None)
                elif sort_method == 'hot':
                    submission_stream = subreddit.hot(limit=None)
                else:  # 'new'
                    submission_stream = subreddit.new(limit=None)

                for post in submission_stream:
                    post_date = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
                    
                    if start_date <= post_date <= end_date and post.num_comments >= min_comments:
                        if post.id not in [p['id'] for p in posts]:  # Avoid duplicates
                            posts.append({
                                'id': post.id,
                                'title': post.title,
                                'selftext': post.selftext,
                                'url': post.url,
                                'author': str(post.author),
                                'score': post.score,
                                'num_comments': post.num_comments,
                                'created_utc': post_date.strftime('%Y-%m-%d %H:%M:%S'),
                                'subreddit': post.subreddit.display_name,
                                'permalink': post.permalink,
                                'is_self': post.is_self,
                                'is_video': post.is_video,
                                'over_18': post.over_18,
                                'spoiler': post.spoiler,
                                'stickied': post.stickied
                            })
                        
                        if len(posts) % 100 == 0:
                            print(f"Scraped {len(posts)} posts so far...")
                        
                        if len(posts) >= limit:
                            break
                    
                    if post_date < start_date:
                        break  

            except Exception as e:
                print(f"Error during scraping {sort_method} posts: {e}")

            time.sleep(1)  # Delay
            
    posts.sort(key=lambda x: x['num_comments'], reverse=True)

    return posts


# This function is to save the results in a excel file
def save_reddit_data_to_excel(data, output_folder='output'):
    if not data:
        print("No data to save. Skipping Excel file creation.")
        return

    os.makedirs(output_folder, exist_ok=True)
    
    # Creating a DataFrame
    df = pd.DataFrame(data)
    
    columns_order = ['id', 'title', 'selftext', 'url', 'author', 'score', 'num_comments', 
                     'created_utc', 'subreddit', 'permalink', 'is_self', 'is_video', 
                     'over_18', 'spoiler', 'stickied']
    df = df[columns_order]

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    excel_output_path = os.path.join(output_folder, f'reddit_data_Insomnia{timestamp}.xlsx')
    
    with pd.ExcelWriter(excel_output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Posts', index=False)
        
        worksheet = writer.sheets['Posts']
        for idx, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).map(len).max(), len(col))
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)  # limit to 50 for readability
    
    print(f"Reddit data saved to Excel at {excel_output_path}")

if __name__ == "__main__":
    try:
        subreddit_name = input("Enter the subreddit name to scrape (e.g., 'ADHD'): ")
        limit = int(input("Enter the number of posts to scrape (default is 6000): ") or 6000)
        start_year = int(input("Enter the start year for filtering (default is 2019): ") or 2019)
        end_year = int(input("Enter the end year for filtering (default is 2024): ") or 2024)
        min_comments = int(input("Enter the minimum number of comments for a post to be included (default is 90): ") or 90)

        print(f"Scraping data from r/{subreddit_name}...")
        reddit_data = scrape_reddit_data(subreddit_name, limit, start_year, end_year, min_comments)

        print(f"Total posts scraped: {len(reddit_data)}")

        if reddit_data:
            print("Saving data to Excel...")
            save_reddit_data_to_excel(reddit_data)
            print("Data scraping and saving complete!")
        else:
            print("No data was scraped. Please check your input parameters and try again.")

    except Exception as e:
        print(f"An error occurred: {e}")
        
# Conclusion - As a end result, this script will scrape the data using PRAW (Python Reddit API Wrapper)that is related to ADHD in reddit social media. Extracted posts are filtered between 2019 - 2024. Further analysis can be done with this data. 
        

import streamlit as st
import feedparser
import pandas as pd

# Function to scrape news articles from an RSS feed URL
def scrape_news_from_feed(feed_url):
    articles = []
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        articles.append({
            'title': entry.title,
            'author': entry.get('author', 'N/A'),
            'publish_date': entry.get('published', 'N/A'),
            'link': entry.link,
            'summary': entry.summary
        })
    return articles

# Main function to run the Streamlit app
def main():
    st.title("News Scraper")

    # Input field for RSS feed URL
    feed_url = st.text_input("Enter the RSS feed URL", 'http://feeds.bbci.co.uk/news/rss.xml')

    # Container for buttons
    button_container = st.empty()
    col1, col2 = button_container.columns([1, 1])
    
    # Placeholder for download button, initially empty
    download_button = col2.empty()
    
    # Scrape News button
    scrape_button = col1.button("Scrape News")
    
    if scrape_button:
        with st.spinner("Scraping articles..."):
            articles = scrape_news_from_feed(feed_url)
            st.success("Scraping completed!")
            
            # Display articles
            for article in articles:
                st.subheader(article['title'])
                st.write(f"**Author:** {article['author']}")
                st.write(f"**Publish Date:** {article['publish_date']}")
                st.write(f"**Summary:** {article['summary']}")
                st.write(f"[Read more]({article['link']})")
                st.write("---")
            
            # Save articles to CSV
            df = pd.DataFrame(articles)
            csv = df.to_csv(index=False).encode('utf-8')
            
            # Activate download button
            download_button.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='news_articles.csv',
                mime='text/csv',
            )

if __name__ == '__main__':
    main()

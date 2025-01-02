#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
import requests
import pandas as pd


# In[3]:


url = "https://www.airlinequality.com/airline-reviews/british-airways/?sortby=post_date%3ADesc&pagesize=100"


# In[4]:


page = requests.get(url)


# In[5]:


soup = BeautifulSoup(page.text, "html")


# In[11]:


Review_Header = soup.find_all("h2", class_="text_header")

#To extract just the text from the review_header
Clean_Review_Header = [header.get_text().strip() for header in Review_Header]

#print the review_headers
print(Clean_Review_Header)


# In[13]:


df = pd.DataFrame(Clean_Review_Header)
print(df)


# In[14]:


df.to_csv(r'C:\Users\KEHINDE FAITH A\Downloads\BA_Practice\BA_Review_Header.csv', index=False)


# In[22]:


Review_Sub_Header = soup.find_all("h3", class_="text_sub_header userStatusWrapper")

#Extract the desired info
text_Sub_Header = []
for header in Review_Sub_Header:
    # Extract name
    name = header.find("span", itemprop="name").get_text().strip()
    
    # Extract country from the text by splitting after the closing tag of <span>
    country = header.get_text().split(')')[0].split('(')[-1].strip()
    
    # Extract datetime and datePublished
    time_tag = header.find("time", itemprop="datePublished")
    datetime = time_tag['datetime']
    date_published = time_tag.get_text().strip()

    # Append the extracted information to the data list
    text_Sub_Header.append({"name": name, "country": country, "datetime": datetime, "date_published": date_published})
    
    print(text_Sub_Header)


# In[23]:


df1 = pd.DataFrame(text_Sub_Header)
print(df1)


# In[26]:


df1.to_csv(r'C:\Users\KEHINDE FAITH A\Downloads\BA_Practice\BA_Sub_Header.csv', index=False)


# In[28]:


Review_Content = soup.find_all("div", class_="text_content")
Cleaned_Review_Content = [f"{index}. {header.get_text().strip()}" for index, header in enumerate(Review_Content, start=1)]
print(Cleaned_Review_Content)


# In[30]:


#Save in dataframe
df2 = pd.DataFrame(Cleaned_Review_Content)


# In[31]:


# Download and Save the file in a csv format"
df2.to_csv(r'C:\Users\KEHINDE FAITH A\Downloads\BA_Practice\BA_Review_Content.csv', index=False)


# In[33]:


# extract individual ratings

ratings = []
for table in soup.find_all('table', class_='review-ratings'):
    rating = {}
    for row in table.find_all('tr'):
        header = row.find('td', class_='review-rating-header')
        value = row.find('td', class_='review-value')
        stars = row.find('td', class_='review-rating-stars')
        if header and value:
            rating[header.get_text(strip=True)] = value.get_text(strip=True)
        elif header and stars:
            rating_value = len(stars.find_all('span', class_='fill'))
            rating[header.get_text(strip=True)] = rating_value
    ratings.append(rating)
    
print(ratings)


# In[36]:


df3 = pd.DataFrame(ratings)
print(df3)


# In[37]:


df3.to_csv(r'C:\Users\KEHINDE FAITH A\Downloads\BA_Practice\BA_Ratings.csv', index=False)


# In[ ]:





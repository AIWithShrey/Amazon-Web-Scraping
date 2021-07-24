from selenium import webdriver
from bs4 import BeautifulSoup
import csv

#function to retrieve url of product page

def my_url(keyword):
    temp = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_1'
    keyword = keyword.replace(' ', '+')
    
    # Add Term Query To URL
    url = temp.format(keyword)
    
    # Add Page Query Placeholder
    url += '&page{}'
    
    return url

#function to extract each record of the product
def extract_record(obj):
    try:
        atag = obj.h2.a
        description = atag.text.strip()
        url = 'https://www.amazon.in' + atag.get('href')
    except AttributeError:
        return
    
    #it is possible that some items on amazom.com might not be having one of the items we are looking for(e.g. some items might not be having ratings or price), we will be getting error if we dont take care of that. We will therefore add some error handlers
    #if there are no price,probably the item is out of stock or not available, then we will ignore the item, but if there are no reviews yet, it's fine, we will still want to extract the item.
    try:
        parent=obj.find('span','a-price')
        price=parent.find('span','a-offscreen').text
    except AttributeError: #we are excepting the error if it occurs so that we can move to extract the next item, else the program will stop running and gives error
        return
    
    try:
        rate=obj.i.text
        counts_review = obj.find('span', {'class': 'a-size-base'}).text
    except AttributeError:
        #assigning empty string to ratings and 
        rate = ''
        counts_review = ''
    
    image = obj.find('img', {'class': 's-image'}).get('src') 
    
    #let's create a tuple that will contain all these items and assign it to a result variable
    result = (description, price, rate, counts_review, url,image)
    return result

'''Run Main Program Routine'''
#function to bring previous functions and run the main program
def main(keyword):
    # Startup The Webdriver
    driver = webdriver.Safari()
#     options = EdgeOptions()
#     options.use_chromium =True
#     driver = Edge(options=options)
    
    records = []  #an empty records list to contain all of our extracted records
    url =my_url(keyword)
    
    for page in range(1, 50):
        driver.get(url.format(page))
        soup =BeautifulSoup(driver.page_source, 'html.parser')
        results=soup.find_all('div',{'data-component-type':'s-search-result'})
#         results=soup.find_all('div',{'data-component-type': 's-search-result'}) #same as we did above

        
#we will like to check if what we have return from the extract_record function is empty or not
        for item in results:
            record = extract_record(item) 
            if record: #if the record has something in it append to records list
                records.append(record) 
                
#         driver.quit()
    
#     # Save Results To CSV File
        with open('Results.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Description', 'Price', 'Rating', 'Reviews Count', 'URL','Image link'])
            writer.writerows(records)

product = str(input("What are you looking for today? "))
main(product)
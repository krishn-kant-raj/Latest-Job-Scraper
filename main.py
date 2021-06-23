# import important libraries
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date
from lxml import html
import requests
import os

choice = None

# Empty list to store the fianl data
AlljobTitle = []
AlljobLinks = []
LastApply = []
# Temporary lists to cleanup data
Links = []
Title = []
Filter = []
ApplyDate = []
FinalDates = []
FinalTitle = []
# define a menu function
def menu():
    AlljobTitle.clear()
    AlljobLinks.clear()
    Links.clear()
    LastApply.clear()
    Title.clear()
    Filter.clear()
    ApplyDate.clear()
    FinalDates.clear()
    FinalTitle.clear()
    try:
        global choice
        os.system('cls')
        print("1 Latest Jobs\n2 Admissions\n3 Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:    
            url = "https://www.sarkariresult.com/latestjob/"
            return url
        elif choice == 2:    
            url= "https://www.sarkariresult.com/admission/"
            return url
        elif choice == 3:
            exit(0)
    except ValueError:
        print('Enter the valid choice in number')


def scrap_info(url):
    if url == None:
        menu()
    if choice==1:
        print("[INFO] Loading latest job for you...")
    if choice==2:
        print("[INFO] Loading latest admissions for you...")
    
    page = requests.get(url)
    tree = html.fromstring(page.content)
    htmlContent = page.content
    soup = BeautifulSoup(htmlContent, 'html.parser')

    print("[INFO] Please wait for a while...\n")
    
    # Extract all <li> tag contents and all links from Anchor '<a>' tag
    li_text = soup.find_all('li')
    job_links = soup.find_all('a')
    
    for i in range(len(li_text)):
        xpathLastApply = f'//*[@id="post"]/ul[{i}]/li/text()'
        ApplyDate.append(tree.xpath(xpathLastApply))
        xpathTitle = f'//*[@id="post"]/ul[{i}]/li/a/text()'
        Title.append(tree.xpath(xpathTitle))
    # Cleaning of Title String
    for t in Title:
        ttl = str(t).replace("['",'')
        ttl = ttl.replace("']",'')
        FinalTitle.append(ttl)
        
    # Cleaning Date String    
    for i in ApplyDate:
        lstdt = str(i).replace("']",'')
        lstdt = lstdt.replace("[' ",'')
        FinalDates.append(lstdt)

    # Extract all job title with latest date <= today
    for dt in range(0,len(FinalDates)):
        try:
            today = date.today()
            today = today.strftime("%d/%m/%Y")
            today = datetime.strptime(today, '%d/%m/%Y')
            if FinalDates[dt][-2:] == 'NA':
                continue
            date_str = FinalDates[dt][-10:]
            dt_obj = datetime.strptime(date_str, '%d/%m/%Y')
            if (FinalDates[dt][-4:] == '2021' and (dt_obj >= today) == True):
                Filter.append(dt)
        except ValueError:
            continue
        
    # Extract all links from page of latest job
    # Apply some condition to remove unwanted links
    if choice==1:
        for link in job_links[21:]:
            linkText = link.get('href')
            Links.append(linkText)
    if choice==2:
        for link in job_links[20:]:
            linkText = link.get('href')
            Links.append(linkText)
    
    for indx in Filter:
        if choice==1:
            AlljobTitle.append(FinalTitle[indx].replace('Online Form 2021','').strip())
        if choice==2:
            AlljobTitle.append(FinalTitle[indx].replace('Admission Online Form 2021','').strip())
        AlljobLinks.append(Links[indx])
        LastApply.append(FinalDates[indx])
    #LastApply = [FinalDates[i] for i in Filter]
    #LastApply = map(FinalDates.__getitem__, Filter)

def show_jobs():
    # Display the Job Title with there corresponding link to apply
    if choice==1:
        for num in range(len(Filter)):
            print(f"Job Title: {AlljobTitle[num]} \n{LastApply[num]} \nApply Link: {AlljobLinks[num]}\n")
    if choice==2:
        for num in range(len(Filter)):
            print(f"Collage Name: {AlljobTitle[num]} \n{LastApply[num]} \nApply Link: {AlljobLinks[num]}\n")
    # Exit the program after pressing 'E' or 'e'
    star = '*****'
    line = star.center(90, "-")
    print(line)
    ch = input("Enter 'E/e' to exit and 'C/c' to continue: ")
    print(line)
    if ch == 'E' or ch == 'e':
        exit(0)
    elif ch=='C' or ch == 'c':
        pass
        
while True:           

    scrap_info(menu())
    show_jobs()

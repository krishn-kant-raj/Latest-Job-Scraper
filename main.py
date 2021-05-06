# import important libraries
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date
import os
choice = None
exit_count = 0
# define a menu function
def menu():
    try:
        global choice
        global exit_count
        os.system('cls')
        print("1 for Latest Jobs\n2 for Admissions")
        choice = int(input("Enter your choice: "))
        if choice==1:    
            url = "https://www.sarkariresult.com/latestjob.php"
            return url
        elif choice==2:    
            url= "https://www.sarkariresult.com/admission.php"
            return url
        else:
            print('Invalid input!! Please enter the valid choice.')
            exit_count+=1
            if exit_count==3:
                print('Sorry! Your Maximum Limit Exists.')
                exit(0)
            else:
                menu()
    except ValueError:
        print('Enter the valid choice in number')
        exit_count+=1
        if exit_count==3:
            print('Sorry! Your Maximum Limit Exists.')
            exit(0)
        else:
            menu()

def scrap_info(url):
    if url==None or choice>2:
        menu()
    print("[INFO] Loading latest job for you...")
    print("\n[INFO] Please wait for a while...\n\n")
    
    r = requests.get(url)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, 'html.parser')

    # Extract all <li> tag contents and all links from Anchor '<a>' tag
    li_text = soup.find_all('li')
    job_links = soup.find_all('a')

    # Empty list to store the Title and Links of latest job
    AlljobTitle = []
    AlljobLinks = []

    # Extract all job title with latest date <= today
    for title in li_text:
        try:
            text = title.text
            today = date.today()
            today = today.strftime("%d/%m/%Y")
            today = datetime.strptime(today, '%d/%m/%Y')
            date_str = text[-10:]
            dt_obj = datetime.strptime(date_str, '%d/%m/%Y')
            if text[-4:] == '2021' and (dt_obj >= today) == True:
                AlljobTitle.append(text)
        except ValueError:
            pass

    latest_job_count = len(AlljobTitle)
    job_count = 0

    # Extract all links from page of latest job
    # Apply some condition to remove unwanted links
    for link in job_links:
        linkText = link.get('href')
        if job_count == latest_job_count:
            break
        if linkText[-4:] == 'com/':
            continue
        elif 'answerkey' in linkText or 'syllabus' in linkText:
            continue
        elif 'latestjob.php' in linkText:
            continue
        elif 'admitcard' in linkText or 'result.php' in linkText or '#' in linkText:
            continue
        elif 'store' in linkText or 'apps' in linkText or 'apple' in linkText:
            continue
        elif '20' in linkText or '19' in linkText or '18' in linkText or '17' in linkText or '16' in linkText:
            continue
        elif linkText[-10:] == 'upsssc.php':
            continue
        elif linkText[-7:] == 'all.php':
            continue
        else:
            AlljobLinks.append(linkText)
            job_count += 1

    # Display the Job Title with there corresponding link to apply
    for i in range(0, len(AlljobLinks)):
        print(f'Job Title: {AlljobTitle[i]} \nApply Link: {AlljobLinks[i]}')
        print()

    # Exit the program after pressing 'E' or 'e'
        star = '*****'
        line = star.center(90, "-")
        print(line)
        ch = input("Enter 'E' or 'e' to exit and 'C' or 'c' to continue: ")
        print(line)
        if ch == 'E' or ch == 'e':
            exit(0)
        elif ch=='C' or ch=='c':
            menu()
while True:           
    url = menu()
    scrap_info(url)

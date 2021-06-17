from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date
import streamlit as st
import pandas as pd 
import numpy as np
import requests
import base64


def main():
    header_text="""
    <style>
    .column {
      float: left;
      width: 33.33%;
      padding: 5px;
    }

    .row::after {
      content: "";
      clear: both;
      display: table;
    }

    .row {
      display: flex;
    }

    .column {
      flex: 33.33%;
      padding: 5px;
    }
    </style>

    <div class="row">
      <div class="column">
        <a href ="https://github.com/krishn-kant-raj/Latest-Job-Scraper">
        <img src="https://pngimg.com/uploads/github/github_PNG28.png" alt="GitHub" style="width:10%">
        <b style="font-size:18px; color:#289ede; font-family:Georgia, serif">  GitHub</b></a>
      </div>
      <div class="column">
        <a href="https://www.linkedin.com/in/krishnkantraj/">
        <img src="https://pngimg.com/uploads/linkedIn/linkedIn_PNG38.png" alt="Krishn Kant Raj Linkedin" style="width:13%">
        <b style="font-size:26px; color:#289ede; font-family:'Brush Script MT', cursive;">Krishn Kant Raj</b></a>
      </div>
    </div>
    """
    
    st.markdown(header_text,unsafe_allow_html=True)
    st.sidebar.markdown("### Choice")
    activities = ["Select Option","Latest Job","Admissions"]    
    choice = st.sidebar.selectbox("Select Activities",activities)
    if choice=='Select Option':
        st.info("_**Please Select an Option in sidebar**_")
        about="""
            # Advantages of this Web-App
            
             ### ✔ Get all **Latest Jobs** and **Admissions** posted on [Sarkari Result Website](sarkariresul.com)

             ### ✔ Totally Add free! Web-App.

             ### ✔ No need to search more in huge list of jobs

             ### ✔ You will get the only details of _**Job**_ or _**Admissions**_ whose apply date is Live.
            ***

             > _**Desclamer:**_ This is not authorised by the [Sarkari Result Admin](sarkariresult.com).
                                I have not taken any permissions to scrap this mensioned websites to the
                                Admin. I am taking all responsibilities that this web app will not harm
                                the mensioned website any how. This web-app is only created to get the
                                meaningful informations from the sarkariresul.com website.
            """
        st.markdown(about)
        
    if choice=='Latest Job':
        st.title('Scraping All Latest Jobs')
        
        url = "https://www.sarkariresult.com/latestjob.php"
        r = requests.get(url)
        htmlContent = r.content
        soup = BeautifulSoup(htmlContent, 'html.parser')
        # Extract all <li> tag contents and all links from Anchor '<a>' tag
        li_text = soup.find_all('li')
        job_links = soup.find_all('a')

        # Empty list to store the Title and Links of latest job
        AlljobTitle = []
        AlljobLinks = []
        LastDate = []

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
                    AlljobTitle.append(text[:-40])
                    LastDate.append(text[-10:])
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
                
        data = {'Job_Title':AlljobTitle,
                'Last_apply_date':LastDate,
                'Job_link':AlljobLinks
                }
        data = pd.DataFrame(data)
        
        # Display the Job Title with there corresponding link to apply
        for i in range(0, len(AlljobLinks)):
            st.write('**Job Title:**', AlljobTitle[i])
            st.write('**Last Apply Date:**',LastDate[i])
            st.write('**Apply Link:**', AlljobLinks[i])
            st.markdown("-----")
        filename = str(today)+'-Jobs'+'.csv'
        csv = data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  
        button = f'<a href="data:file/csv;base64,{b64}" download="{filename}"><b style="font-size:30px; color:#28d4a3; font-family:verdana">✔ Download Data in .CSV format</b></a>'
        st.markdown(button,unsafe_allow_html=True)
        st.balloons()
        
    elif choice=='Admissions':
        st.title('Scraping All Latest Admissions')
        url= "https://www.sarkariresult.com/admission.php"
        r = requests.get(url)
        htmlContent = r.content
        soup = BeautifulSoup(htmlContent, 'html.parser')
        # Extract all <li> tag contents and all links from Anchor '<a>' tag
        li_text = soup.find_all('li')
        job_links = soup.find_all('a')

        # Empty list to store the Title and Links of latest job
        AlljobTitle = []
        AlljobLinks = []
        LastDate = []

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
                    if ('Admission' in text):
                        text = text.replace('Admission','')
                    AlljobTitle.append(text[:-40])
                    LastDate.append(text[-10:])
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
                
        data = {'Collage_name':AlljobTitle,
                'Last_apply_date':LastDate,
                'Apply_link':AlljobLinks
                }
        data = pd.DataFrame(data)
        
        # Display the Job Title with there corresponding link to apply
        for i in range(0, len(AlljobLinks)):
            st.write('**Collage Name:**', AlljobTitle[i])
            st.write('**Last Apply Date:**',LastDate[i])
            st.write('**Apply Link:**', AlljobLinks[i])
            st.markdown("-----")
        filename = str(today)+'-Admissions'+'.csv'
        csv = data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  
        button = f'<a href="data:file/csv;base64,{b64}" download="{filename}"><b style="font-size:30px; color:#d47f24; font-family:verdana">✔ Download Data in .CSV format</b></a>'
        st.markdown(button,unsafe_allow_html=True)
        st.balloons()
        
if __name__ == '__main__':
    main()

from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date
import streamlit as st
from lxml import html
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
        page = requests.get(url)
        tree = html.fromstring(page.content)
        htmlContent = page.content
        soup = BeautifulSoup(htmlContent, 'html.parser')
        # Extract all <li> tag contents and all links from Anchor '<a>' tag
        li_text = soup.find_all('li')
        job_links = soup.find_all('a')

        # Empty list to store the Title and Links of latest job
        AlljobTitle = []
        AlljobLinks = []
        LastDate = []
        # Temporary lists to cleanup data
        LastApply = []
        Links = []
        Title = []
        Filter = []
        ApplyDate = []
        FinalDates = []
        FinalTitle = []
        # Extract all job title with latest date <= today

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
        for link in job_links[21:]:
            linkText = link.get('href')
            Links.append(linkText)

        for indx in Filter:
            text = FinalTitle[indx].replace('Online Form','').strip()
            text = text.replace('2021','').strip()
            AlljobTitle.append(text)
            AlljobLinks.append(Links[indx])
            LastApply.append(FinalDates[indx])    
        data = {'Job_Title':AlljobTitle,
                'Last_apply_date':LastApply,
                'Job_link':AlljobLinks
                }
        data = pd.DataFrame(data)
        
        # Display the Job Title with there corresponding link to apply
        for i in range(0, len(AlljobLinks)):
            st.write('**Job Title:**', AlljobTitle[i])
            st.write('**Last Apply Date:**',LastApply[i])
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
        page = requests.get(url)
        tree = html.fromstring(page.content)
        htmlContent = page.content
        soup = BeautifulSoup(htmlContent, 'html.parser')
        # Extract all <li> tag contents and all links from Anchor '<a>' tag
        li_text = soup.find_all('li')
        job_links = soup.find_all('a')

        # Empty list to store the Title and Links of latest job
        AlljobTitle = []
        AlljobLinks = []
        LastDate = []
        # Temporary lists to cleanup data
        LastApply = []
        Links = []
        Title = []
        Filter = []
        ApplyDate = []
        FinalDates = []
        FinalTitle = []

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
        for link in job_links[20:]:
            linkText = link.get('href')
            Links.append(linkText)

        for indx in Filter:
            text = FinalTitle[indx].replace('Online Form','').strip()
            text = text.replace('2021','').strip()
            if ('Admission' in text):
                AlljobTitle.append(text.replace('Admission','').strip())
            else:
                AlljobTitle.append(text)
            AlljobLinks.append(Links[indx])
            LastApply.append(FinalDates[indx])    
        data = {'College_name':AlljobTitle,
                'Last_apply_date':LastApply,
                'Job_link':AlljobLinks
                }
        data = pd.DataFrame(data)
        
        # Display the Job Title with there corresponding link to apply
        for i in range(0, len(AlljobLinks)):
            st.write('**Collage Name:**', AlljobTitle[i])
            st.write('**Last Apply Date:**',LastApply[i])
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

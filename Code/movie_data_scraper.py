import lxml
import re
import csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from requests import get

class IMDB(object):
    """
    Class to contain all the methods required to scrape the dataset from IMDB website.
    """
    def __init__(self, url):
        """
        Constructor to initialize the URL from where data has to be scraped. 
        """
        super(IMDB, self).__init__()
        page = get(url)

        self.soup = BeautifulSoup(page.content, 'lxml')

    def articleTitle(self):
        """
        Method to return title name.
        """
        return self.soup.find("h1", class_="header").text.replace("\n","")

    def bodyContent(self):
        """
        Method to return movie data.
        """
        content = self.soup.find(id="main")
        return content.find_all("div", class_="lister-item mode-advanced")

    def movieData(self):
        """
        Method to return the list of all the movie details.
        """
        movieFrame = self.bodyContent()
        movieTitle = []
        movieDate = []
        movieRunTime = []
        movieGenre = []
        movieRating = []
        movieScore = []
        movieDescription = []
        movieDirector = []
        movieStars = []
        movieVotes = []
        movieGross = []
        
        for movie in movieFrame:
            movieFirstLine = movie.find("h3", class_="lister-item-header")
            movieTitle.append(movieFirstLine.find("a").text)
            movieDate.append(re.sub(r"[()]","", movieFirstLine.find_all("span")[-1].text))
            try:
                movieRunTime.append(movie.find("span", class_="runtime").text[:-4])
            except:
                movieRunTime.append(np.nan)
            movieGenre.append(movie.find("span", class_="genre").text.rstrip().replace("\n","").split(","))
            try:
                movieRating.append(movie.find("strong").text)
            except:
                movieRating.append(np.nan)
            try:
                movieScore.append(movie.find("span", class_="metascore unfavorable").text.rstrip())
            except:
                movieScore.append(np.nan)
            movieDescription.append(movie.find_all("p", class_="text-muted")[-1].text.lstrip())
            movieCast = movie.find("p", class_="")

            try:
                casts = movieCast.text.replace("\n","").split('|')
                casts = [x.strip() for x in casts]
                casts = [casts[i].replace(j, "") for i,j in enumerate(["Director:", "Stars:"])]
                movieDirector.append(casts[0])
                movieStars.append([x.strip() for x in casts[1].split(",")])
            except:
                casts = movieCast.text.replace("\n","").strip()
                movieDirector.append(np.nan)
                movieStars.append([x.strip() for x in casts.split(",")])

            movieNumbers = movie.find_all("span", attrs={"name": "nv"})

            if len(movieNumbers) == 2:
                movieVotes.append(movieNumbers[0].text)
                movieGross.append(movieNumbers[1].text)
            elif len(movieNumbers) == 1:
                movieVotes.append(movieNumbers[0].text)
                movieGross.append(np.nan)
            else:
                movieVotes.append(np.nan)
                movieGross.append(np.nan)

        moviesz = pd.DataFrame({
            'movieTitle':movieTitle,
            'movieDate':movieDate,
            'movieRunTime':movieRunTime,
            'movieGenre':movieGenre,
            'movieRating':movieRating,
            'movieScore':movieScore,
            'movieDescription':movieDescription,
            'movieDirector':movieDirector,
            'movieStars':movieStars,
            'movieVotes':movieVotes,
            'movieGross':movieGross
        })
        #moviesz.to_csv('movies1.csv')
        return moviesz

if __name__ == "__main__":
    """
    Main Function to define the number of pages to be scraped from the IMDB website. 
    """
    pages = np.arange(1, 30010, 100)
    filenumber=0
    for page in pages:
        print("Processed Movies :"+ str(page))
        url = "https://www.imdb.com/search/title/?title_type=feature,tv_series&count=100&start="+str(page)+"&ref_=adv_nxt"
        im = IMDB(url)
        x = im.movieData()
        x.to_csv('movies1.csv')

        file1 = open('final_dataset.csv','a',newline="",encoding="utf8")
        writer = csv.writer(file1)
        rownumber=0
        with open('movies1.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            for row in reader:
                if filenumber==0:
                    filenumber = 1
                    writer.writerow(row)
                    continue
                if rownumber == 0:
                    rownumber = 1
                    continue
                writer.writerow(row)
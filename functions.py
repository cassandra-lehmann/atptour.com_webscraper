#-------------------------------------------------------------------------------------
#                             GET PLAYER'S COUNTRY                               
#-------------------------------------------------------------------------------------
def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return "error"
    

#-------------------------------------------------------------------------------------
#                                    WEBSCRAPER                               
#-------------------------------------------------------------------------------------
def scrape(date, urlpattern):
    from bs4 import BeautifulSoup
    import requests
    import re
    import pandas as pd
    
    url = urlpattern.format(date)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    #Ranking
    ranking = soup.find_all("td", {"class": "rank-cell"})
    ranking = [item.get_text().strip() for item in ranking]
    
    #Move
    move = soup.find_all("div", {"class": "move-text"})
    move = [item.get_text().strip() for item in move]
    
    #Country
    country = soup.find_all("div", {"class": "country-item"})
    country = [item.find("img", {"alt": True}) for item in country]
    country_list = []

    for item in country:
        current_item = find_between(str(item), '"', '"' )
        country_list.append(current_item)
    
    #Player
    player = soup.find_all("td", {"class": "player-cell"})
    player = [item.get_text().strip() for item in player]
    
    #Age
    age = soup.find_all("td", {"class": "age-cell"})
    age = [item.get_text().strip() for item in age]
    
    #Points
    points = soup.find_all("a", {"data-ga-label": "rankings-breakdown"})
    points = [item.get_text().strip() for item in points]
    
    #Tournaments
    tournaments = soup.find_all("td", {"class": "tourn-cell"})
    tournaments = [item.get_text().strip() for item in tournaments]
    
    #Points dropping
    points_dropping = soup.find_all("td", {"class": "pts-cell"})
    points_dropping = [item.get_text().strip() for item in points_dropping]
    
    #Next best
    next_best = soup.find_all("td", {"class": "next-cell"})
    next_best = [item.get_text().strip() for item in next_best]

    #Create datafame for link
    df = pd.DataFrame({
                    "ranking": ranking,
                    "move": move,
                    "country": country_list,
                    "player": player,
                    "age": age,
                    "points": points,
                    "tournaments": tournaments,
                    "points_dropping": points_dropping,
                    "next_best": next_best
                })
    #Date
    df["date"] = date
    
    return df

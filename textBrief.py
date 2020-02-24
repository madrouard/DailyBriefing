from bs4 import BeautifulSoup
from twilio.rest import Client
import requests

# These variables are related to the horoscope website
horoscope = requests.get('https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=3')
horosoup = BeautifulSoup(horoscope.text, 'html.parser')
main_horoscope = (horosoup.find('p').getText())  # The daily horoscope

# These variables are related to hackernews
res = requests.get('https://news.ycombinator.com/')
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.select('.storylink')
subtext = soup.select('.subtext')


# This function takes all the front page stories and finds the one with the most votes
def highest_post(links, subtext):
    largest = 0
    hTitle = ''
    hLink = ''
    for idx, item in enumerate(links):
        title = links[idx].getText()
        link = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points >= largest:
                largest = points
                hTitle = title
                hLink = link
    return "Title: " + hTitle + "\n Link: " + hLink


daily_post = highest_post(links, subtext)

account_sid = 'REPLACE WITH OWN ID'
auth_token = 'REPLACE WITH OWN TOKEN'
client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='Bot's number',
    body=(daily_post + '\n' + main_horoscope),
    to='My Number'
)

print(message.sid)

import requests
from bs4 import BeautifulSoup
from time import sleep
from csv import writer
from random import choice


BASE_URL = "http://quotes.toscrape.com"

def scrape_quotes():
	all_quotes = []
	url = "/page/1"
	while url:
		response = requests.get(f"{BASE_URL}{url}")
		soup = BeautifulSoup(response.text, "html.parser")
		quotes = soup.find_all(class_="quote")
		
		for quote in quotes:
			all_quotes.append({
				"text": quote.find(class_ = "text").get_text(),
				"author": quote.find(class_= "author").get_text(),
				"bio-link": quote.find("a")["href"]
				})
		next_button = soup.find(class_="next")
		url = next_button.find("a")["href"] if next_button else None
		sleep(1)
	return all_quotes
def start_game(quotes):

	quote = choice(quotes)
	remain_guesses = 4
	print("Here's a quote: ")
	print(quote["text"])
	print(quote["author"])
	guess = ""
	while guess.lower() != quote["author"].lower() and remain_guesses > 0:
		guess = input(f"Who said this quote? Guesses reamining: {remain_guesses}\n")
		if guess.lower() == quote["author"].lower():
			print("You got it!")
			break
		remain_guesses -= 1
		if remain_guesses == 3:
			response = requests.get(f"{BASE_URL}{quote['bio-link']}")
			soup = BeautifulSoup(response.text, "html.parser")
			birth_date = soup.find(class_ = "author-born-date").get_text()
			birth_place = soup.find(class_ = "author-born-location").get_text()
			print(f"Here's a hint: the author was born on {birth_date} {birth_place}")
		elif remain_guesses == 2:
			print(f"Here is a hint. Author's first name starts with {quote['author'][0]}")
		elif remain_guesses == 1: 
			last_initial = quote["author"].split(" ")[1][0]
			print(f"Here is a hint. Author's last name starts with {last_initial}")
		else:
			print(f"Sorry you ran out of guesses. The author was: {quote['author']} ")
	again = ''
	while again.lower() not in ('y', 'yes' , 'n', 'no'):
		again = input("Would you like to play again (y/n)? ")
	if again.lower() in ('yes', 'y'):
		print("Okay, again it is.")
		return start_game(quotes)
	else:
		print("Ok. Goodbye!")
quotes = scrape_quotes()
start_game(quotes)
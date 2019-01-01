# COPYRIGHT Robert Davis - http://www.robertdavis.co.uk
import praw
import config
import time
import requests
import json

cache = []

def main():

	print("\nLogging in")
	# Initialise Reddit instance and Log In
	reddit = praw.Reddit(username = config.username,
					 	 password = config.password, 
					 	 client_id = config.client_id,
					 	 client_secret = config.client_secret, 
					 	 user_agent = config.user_agent)
	print("Logged in\n")

	# List of domains to check
	domains = ["dailymail.co.uk"]
	# Number of reddit posts/submissions returned, for each domain
	submission_limit = 4

	# Process a search for each domain
	for domain in domains:
		domain_search = process_search(reddit, domain, submission_limit)
		# Process each submission in each search
		for submission in domain_search:
			process_submission(submission)

	print("\nFinished pass")
	print("-------------\n")

def process_search(reddit, domain, submission_limit):

	# Processing a reddit search for each domain
	print("-------------\nSearching reddit for posts with domain: " + domain)
	domain_search = reddit.domain(domain).new(limit=submission_limit)
	return domain_search

def process_submission(submission):

	# Processing each submission within each search
	post_title = submission.title
	post_url = submission.url
	searchResults = []

	if len(post_title) > 15:
		print("\n" + post_title + " / " + post_url)
		formatted_post_title = format_post_title(post_title)
		searchResults = web_search(formatted_post_title, post_url)
		submit_comment(submission)
		cache.append(submission.url)

def format_post_title(post_title):
	# TO-DO processing of the post title here
	print("\nFormatting post title")
	# 1. Remove any domains / domain names eg [facebook.com]
	post_title = post_title.replace("http://","")
	post_title = post_title.replace("www.","")
	post_title = post_title.replace(".com","")
	post_title = post_title.replace(".co.uk","")
	# 2. Remove basic punctuation eg ( ) [ ] { } &  \ < > . _ + / * - = @ ! ^ ~ ` : ; | " " 
	post_title = post_title.translate({ord(c): None for c in '()[]&\{\}\\&<>_+/*-=@!^~`:;|}""'})
	# 3. Streamline the post title down to only it's key words

	# 4. Emphasise key numbers with " " for more reliable/relevant google search results eg. "200,000"
	# for word in post_title.split():
	# 	if word.isupper():
	# 		print("")
	# 5. Output and return
	formatted_post_title = post_title
	print("Searching the web with results matching: " + formatted_post_title)
	return formatted_post_title

def web_search(formatted_post_title, post_url):
	# Getting search data from Google Custom Search API
	response = requests.get("https://www.googleapis.com/customsearch/v1?key="+config.search_key+"&cx="+config.search_engine+"&q="+formatted_post_title)
	# Formatting json Data
	searchUrl = response.json()
	searchResults = []

	#TO-DO output all results from google search
	
	if (searchUrl["searchInformation"]["totalResults"] != "0"):
		for i in range(0, 4):
			searchResults.append(searchUrl["items"][i]["title"])
			print(searchUrl["items"][i]["displayLink"] + " / " + searchUrl["items"][i]["title"] + " / " + searchUrl["items"][i]["link"])
	else:
		print("\tNO RESULTS FOUND: Continuing to next post")

def compare_titles_to_results(formatted_post_title, searchResults):
	# TO-DO Compare the post titles to the article titles
	# If they share a certain number of words, submit a comment
	matchedResults = []
	tempString = ""

	# for i in range(0,10):
	# 	for word in searchResults[i]:
	# 		tempString.append(word)
	# 	for word in formatted_post_title: 
	# 		matchedResults.append(word)

	# number_of_matches = len(matchedResults)

	# if (number_of_matches >= 3):
	# 	for i in range(0, number_of_matches+1):
	# 		print(matchedResults[i])
		

def create_reply():
	#print("Creating reply text")
	reply_text = """## Alternate and related sources for this article.

|**Source**|**Article**|
|:-|:-|
|Daily Mail""" + """|Article URL|

* &#x200B;

^(BEEP) ^(BOOP:) ^(This) ^(comment) ^(was) ^(automatically) ^(generated) ^(by) ^(a) ^(bot) ^(on) ^(a) ^(limited) ^(trial) ^(run.) ^(This) ^(bot) ^(is) ^(in) ^(an) ^(alpha) ^(stage) ^(of) ^(development.) ^(Results) ^(may) ^(be) ^(incorrect) ^(or) ^(inaccurate.) ^(If) ^(you) ^(notice) ^(any) ^(wrong) ^(or) ^(unusual) ^(results) ^(please) ^(message) ^(the) ^(author) ^/u/Houstons-Problem^(.)"""
	return reply_text

def submit_comment(submission):
	#print("Replying to submission\n")
	reply_text = create_reply()
	#submission.reply(reply_text)
	#print("Replied to submission")

def debug_format_json(searchUrl):
	print("")
	# Formats Google Custom Search JSON Data for debugging purposes
	# jsonData = json.dumps(searchUrl)
	# print(jsonData+"\n")

while True:
	main()
	# Runs every 100 seconds
	time.sleep(100)
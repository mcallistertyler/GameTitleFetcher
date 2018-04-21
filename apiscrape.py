import requests
import json
import csv
import _mysql
apikey = ""
testlist = []
parameters = {"results":0}
#user agent needed for get otherwise 403 error produced
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

print("Giant Bomb Title Searcher")

def csvify(titles):
	with open('new_file.csv', 'w+') as myfile:
		csvWriter = csv.writer(myfile, delimiter=',')
		csvWriter.writerow(['game_title', 'game_system'])
		csvWriter.writerows(titles)

def quotify(letters):
	letters = "\"" + letters + "\""
	return letters

def dbInsert(titles):
	db = _mysql.connect(host="xxx.xxx.xxx.xxxx", user="", passwd="", db="", port=3306)
	for x in range(0, len(titles)):
			gameTitle = titles[x][0]#2d list, 0 is title, 1 is system
			gameSystem = titles[x][1]
			db.query("""INSERT INTO Games(game_title, game_system) VALUES ("""+quotify(gameTitle)+""", """+quotify(gameSystem)+""") """)

def fetchTitles():
	title = input("Enter the title of the series you want to search.")
	gamesearchlink = "https://www.giantbomb.com/api/search/?api_key=" + apikey + "&format=json&query=%22" + title.lower() + "%22&resources=game"
	response = requests.get(gamesearchlink, headers=header, params=parameters)
	data = response.json()
	if(response.status_code == 200):
		if data['results']:
			try:
				for i in data['results']:
					for j in i['platforms']:
						testlist.append([i['name'], j['name']])
				csvify(testlist)
			except:
				pass
		else:
			print("No titles found")
	else:
		print("Error, returned status code: " + response.status_code)
	dbInsert(testlist)	

fetchTitles()

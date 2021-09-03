Scripts to get reviews from restaurant of a given city (tripadvisor)

Depencencies
	python3
	bs4==0.0.1
	lxml==4.5.2
	requests==2.24.0
	urllib3==1.25.10
	tqdm

Go to the code folder
	clone the utils repository
		git clone https://github.com/dannysv/utils.git
	run 
		- python 1get_pagination_rests.py link_restaurant_city folderout numberpages
		example:
		python 1get_pagination_rests.py https://www.tripadvisor.de/Restaurants-g187323-Berlin.html berlin 200
		- python 2get_links_restaurants.py berlin
		- python 3get_pagination_revs.py berlin 300
		- python 4pagination_to_links.py berlin
		- python 5get_reviews.py berlin

Output
	the list of reviews are placed in folder data_berlin
	Final output : ../data_berlin/reviews.json

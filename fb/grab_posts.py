import facebook
import login_fb as l

from pymongo import MongoClient
from pprint import pprint as pretty


mongo = MongoClient()
db = mongo['predict-news-posts']
collection = db['friends-posts-links']


access_token = l.login(l.ACCESS_TOKEN)
print "Access_token: ", access_token

graph = facebook.GraphAPI(access_token)
profile = graph.get_object("me")
friends = graph.get_connections("me", "friends")

for friend in friends['data']:
	friend_post = {}
	
	feed = graph.get_connections(friend['id'], 'links')
	friend_post['name'] = friend['name']

	links = []
	for feed_obj in feed['data']:

		doc = {
				'description': feed_obj['description'] if 'description' in feed_obj else "",
				'link': feed_obj['link'] if 'link' in feed_obj else "",
				'name': feed_obj['name'] if 'name' in feed_obj else "",
				'message': feed_obj['message'] if 'message' in feed_obj else ""
			}
		links.append(doc)
	friend_post['links'] = links

	collection.insert(friend_post)


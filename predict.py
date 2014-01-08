import sys
import scipy as sp
from pymongo import MongoClient
from datetime import datetime

# mongo setup
mongo = MongoClient()
db = mongo['predict-news-posts']
collection = db['friends-posts-links']
calculations = db['calculations']

# calculate Euclidean distance, of new post with the old posts
def dist_raw(v1, v2):
	delta = v1 - v2
	return sp.linalg.norm(delta.toarray())


# # calculate the vector distance
def dist_norm(v1, v2):
	v1_normalized = v1 / sp.linalg.norm(v1.toarray())
	v2_normalized = v2 / sp.linalg.norm(v2.toarray())
	delta = v1_normalized - v2_normalized
	return sp.linalg.norm(delta.toarray())


# get posts for each friend
def get_all_posts():
	all_posts = {}

	friend_posts = collection.find({})

	for friend_post in list(friend_posts):
		link_titles = []

		for l in friend_post['links']:
			if l['name'] and not l['name'] == 'Timeline Photos' and 'https://' not in l['name'] and 'http://' not in l['name']:
				link_titles.append(l['name'])
		all_posts[friend_post['name']] = link_titles

	return all_posts

# now to find out the distances for each friend's posts
def calculate_distances(all_posts, vectorizer, content):
	for name, posts in all_posts.iteritems():

		if len(posts) > 0:
			for article_name in content:
				print '{0}: for {1} -> article "{2}"'.format(datetime.now(), name.encode('utf-8'), article_name.encode('utf-8'))
				X_train = vectorizer.fit_transform(posts)
				num_samples, num_features = X_train.shape
				
				article_name_vec = vectorizer.transform([article_name])
				article_post_array = article_name_vec.toarray()

				best_doc = None
				best_dist = sys.maxint
				best_i = None

				for i in range(0, num_samples):
					post = posts[i]
					if post == article_name:
						continue
					post_vec = X_train.getrow(i)
					d = dist_norm(post_vec, article_name_vec)
					# d = dist_raw(post_vec, article_name_vec)
					# print "=== Post {0} with dist={1}: {2}".format(i, d, post.encode('utf-8'))
					if d < best_dist:
						best_doc = post
						best_dist = d
						best_i = i
				if best_dist > 0.0:
					calculations.insert({'name': name, 'content-test': article_name, 'best-post': best_doc, 'best-distance': best_dist})

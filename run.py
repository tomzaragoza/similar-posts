import fb
from stemming import StemmedCountVectorizer
from predict import *
from bson import Binary, Code
from bson.json_util import dumps, loads


mongo = MongoClient()
db = mongo['predict-news-posts']
collection = db['calculations']

if __name__ == "__main__":

	answer = raw_input("Want to retrieve you friend's link posts? (y/n) ")
	if answer.lower() in ['y', 'yes']:
		fb.grab_posts()

	vectorizer = StemmedCountVectorizer(min_df=1, stop_words="english") # minimum document frequency
	content = [	"The Brain, in Exquisite Detail", 
				"Asian Factories See Sense and Savings in Environmental Certification",
				"Rangers Bury the Maple Leafs Beneath 7 Goals",
				"Steep Penalties Taken in Stride by JPMorgan Chase",
				"Weight-Loss Companies Charged With Fraud",
				"What Your Cat Is Thinking",
				"Missing a Cancer Diagnosis"]

	all_posts = get_all_posts()
	calculate_distances(all_posts, vectorizer, content)

	print 
	for article in content:
		calculation = collection.find({'content-test': article}).sort('best-distance', 1).limit(1).next()
		print "{0}: {1}'s post '{2}' with a distance of {3}".format(article, calculation['name'], calculation['best-post'], calculation['best-distance'])

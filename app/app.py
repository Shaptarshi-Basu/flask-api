#coding: utf-8

from flask import Flask, request, jsonify
import pymongo
from bson import ObjectId





app = Flask(__name__)


@app.route('/songs')
def getSongs():
	offset = 0
	limit = 5
	if 'offset' in request.args:
		offset_value = request.args.get('offset')
		if not offset_value.isnumeric():
			return jsonify({"error": "offset value should be numeric and postive"})
		offset = int(offset_value)
	if 'limit' in request.args:
		limit_value = request.args.get('limit')
		if not limit_value.isnumeric():
			return jsonify({"error": "limit value should be numeric"})
		limit = int(limit_value)
	mycol = getCollection()
	staring_id = mycol.find().sort('_id',pymongo.ASCENDING)
	try:
		last_id = staring_id[offset]['_id']
	except IndexError as e:
		return jsonify({"error":"index out of bound for offset"})
	mydoc = mycol.find({ '_id': { '$gte': last_id } }).sort('_id', pymongo.ASCENDING).limit(limit)
	output = []
	for x in mydoc:
		x["_id"] = str(x["_id"])
		output.append(x)
	next_url = "http://localhost:5000/songs?limit="+str(limit) + '&offset=' + str(offset + limit)
	prev_url = "http://localhost:5000/songs?limit="+str(limit) + '&offset=' + str(offset - limit)	
	return jsonify({"next_url":next_url,"prev_url": prev_url, "messages":output})


def getCollection():
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["yousician"]
	mycol = mydb["songs"]
	return mycol


@app.route('/songs/avg/difficulty')
def getAvgDifficulty():
    # parameter 'varname' is specified
    # parameter 'varname' is NOT specified
    mycol = getCollection()
    mydoc = mycol.find().sort('_id', pymongo.ASCENDING)
    difficulty = 0
    count = 0
    if 'level' in request.args:
    	level = request.args.get('level')
    else:
    	level = 0
    if not level.isnumeric():
    	return jsonify({"error": "level value should be numeric"})
    for x in mydoc:
    	if x['difficulty'] > float(level):
    		print(x['difficulty'])
    		difficulty =difficulty + x['difficulty']
    		count = count + 1
    if count != 0:
    	avg = difficulty / count
    	return jsonify({"average Value": str(avg)})
    else:
    	return jsonify({"error": "No value above that level"})	       

@app.route('/songs/search')
def getSearchResults():
    mycol = getCollection()
    mydoc = mycol.find().sort('_id', pymongo.ASCENDING)
    song_list = []
    if 'message' not in request.args:
    	return jsonify({"error": "Search parameter should be present"})
    searchCtr = request.args.get('message')
    if len(searchCtr) == 0 :
    	return jsonify({"error": "Search parameter cannot be empty"})
    for x in mydoc:
    	if  searchCtr.lower() in x['artist'].lower() or searchCtr.lower() in x['title'].lower() :
    		x["_id"]= str(x["_id"])
    		song_list.append(x)
    return jsonify(song_list)

@app.route('/songs/rating', methods = ['POST'])
def addRatings():
    mycol = getCollection()
    if 'song_id' in request.args:
    	songid = request.args.get('song_id')
    else:
    	 return jsonify({"error":"mandatory parameter song_id not added"})
    if 'rating' in request.args:
    	rating = request.args.get('rating')
    else:
    	return jsonify({"error":"mandatory parameter rating not added"})
    starting_ind = mycol.find( { "_id": ObjectId(songid) } )
    new_ratings = [rating]
    for el in starting_ind:
    	if 'ratings' in el.keys():
    		ratings = el['ratings']
    		for oldr in ratings:
    			new_ratings.append(str(oldr))
    			new_ratings.sort()
    		mycol.update({ "_id" : ObjectId(songid) },{ "$set": { "ratings" : new_ratings } });

    	else:
    		mycol.update({ "_id" : ObjectId(songid) },{ "$set": { "ratings" : new_ratings } });
    return jsonify({"updated":str(songid)})

@app.route("/songs/avg/rating/<song_id>")
def data(song_id):
	mycol = getCollection()
	least_rating = 0
	max_rating = 0
	avg_rating = 0
	count = 0
	starting_ind = mycol.find( { "_id": ObjectId(song_id) } )
	for el in starting_ind:
		least_rating = el['ratings'][0]
		max_rating = el['ratings'][len(el['ratings'])-1]
		ratings = el ['ratings']
		for rating in ratings:
			avg_rating = avg_rating + int(rating)
			count = count + 1
		avg_rating = avg_rating / count	
	return jsonify({"least_rating":least_rating, "max_rating": max_rating,"avg rating":avg_rating})

 
if __name__ == '__main__':
	app.run(debug=False,host='0.0.0.0')



# test_hello_add.py
from app import app
from flask import json

def test_getSongs():
    response = app.test_client().get(
        '/songs',
        data=json.dumps({"artist": "The Yousicians","title": "Lycanthropic Metamorphosis","difficulty": 14.6,"level":13,"released": "2016-10-26", "_id":"111fd34" }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
def test_getSongsGetDifficulty():
    response = app.test_client().get(
        '/songs/avg/difficulty',
        data=json.dumps({"average Value": "11"}),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
def test_getSongsPostRatings():
    response = app.test_client().post(
        '/songs/rating?song_id=5ef8c0161b46f1f375c99b4e&rating=3',
        data=json.dumps({"updated":"5ef8c0161b46f1f375c99b4e"}),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
def test_getSongsBySearchString():
    response = app.test_client().get(
        '/songs/search?message=hello',
        data=json.dumps({"artist": "The Yousicians","title": "Lycanthropic Metamorphosis","difficulty": 14.6,"level":13,"released": "2016-10-26", "_id":"111fd34" }),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
def test_getAvgDifficultyWithLevel():
    response = app.test_client().get(
        '/songs/avg/difficulty?level=2',
        data=json.dumps({"average Value": "11"}),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
def test_getRatingsOfSong():
    response = app.test_client().get(
        '/songs/avg/rating/5ef8c0161b46f1f375c99b4e',
        data=json.dumps({"average Value": "11"}),
        content_type='application/json',
    )
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
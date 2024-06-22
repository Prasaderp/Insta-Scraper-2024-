from pymongo import MongoClient

client = MongoClient('mongodb+srv://tilt_studio123:tilt_studio123@instadata.gqcj0yu.mongodb.net/?retryWrites=true&w=majority&appName=InstaData')
db = client['instagramData']

profile_col = db['profiles']
hashtag_posts_col = db['hashtagPosts']

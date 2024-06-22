import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [username, setUsername] = useState('');
  const [hashtag, setHashtag] = useState('');
  const [profileData, setProfileData] = useState(null);
  const [hashtagPosts, setHashtagPosts] = useState([]);

  const fetchProfileData = async () => {
    try {
      const response = await axios.post(`http://localhost:8000/profile/${username}`);
      setProfileData(response.data);
    } catch (error) {
      console.error("Error fetching profile data:", error);
    }
  };

  const fetchHashtagPosts = async () => {
    try {
      const response = await axios.post(`http://localhost:8000/hashtag/${hashtag}`);
      setHashtagPosts(response.data);
    } catch (error) {
      console.error("Error fetching hashtag posts:", error);
    }
  };

  return (
    <div className="App">
      <h1>Instagram Scraper</h1>
      
      <div>
        <h2>Profile Data</h2>
        <input 
          type="text" 
          placeholder="Enter Instagram username" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
        />
        <button onClick={fetchProfileData}>Search</button>
        {profileData && (
          <div>
            <h3>Profile Details</h3>
            <p>Username: {profileData.username}</p>
            <p>No. of Posts: {profileData["No. of Posts"]}</p>
            <p>Followers: {profileData.followers}</p>
            <p>Following: {profileData.following}</p>
          </div>
        )}
      </div>
      
      <div>
        <h2>Hashtag Posts</h2>
        <input 
          type="text" 
          placeholder="Enter hashtag" 
          value={hashtag} 
          onChange={(e) => setHashtag(e.target.value)} 
        />
        <button onClick={fetchHashtagPosts}>Search</button>
        {hashtagPosts.length > 0 && (
          <div>
            <h3>Posts Details</h3>
            {hashtagPosts.map((post, index) => (
              <div key={index}>
                <p>Post URL: <a href={post.post_url} target="_blank" rel="noopener noreferrer">{post.post_url}</a></p>
                <p>Account: {post.account_name}</p>
                <p>Likes Count: {post.likes_count}</p>
                <p>Date: {post.date}</p>
                <p>Full Caption: {post.full_caption}</p>
                <p>Hashtags: {post.hashtags ? post.hashtags.join(', ') : 'No hashtags'}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

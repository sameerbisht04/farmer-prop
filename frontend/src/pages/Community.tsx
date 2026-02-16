import React, { useState } from 'react';

const Community: React.FC = () => {
  const [newPost, setNewPost] = useState('');
  
  const posts = [
    {
      id: 1,
      author: 'Rajesh Kumar',
      location: 'Punjab',
      time: '2 hours ago',
      title: 'Wheat Harvesting Tips',
      content: 'Sharing some effective wheat harvesting techniques that have worked well for me this season. The key is timing and proper equipment maintenance.',
      likes: 12,
      comments: 5
    },
    {
      id: 2,
      author: 'Priya Sharma',
      location: 'Haryana',
      time: '4 hours ago',
      title: 'Organic Pest Control Methods',
      content: 'Has anyone tried neem oil for pest control? I found it very effective for aphids on my cotton crop. Would love to hear your experiences.',
      likes: 8,
      comments: 3
    },
    {
      id: 3,
      author: 'Amit Singh',
      location: 'Uttar Pradesh',
      time: '6 hours ago',
      title: 'Weather Alert - Heavy Rains Expected',
      content: 'Farmers in our area, please be prepared for heavy rains in the next 2 days. Protect your crops and check drainage systems.',
      likes: 15,
      comments: 8
    }
  ];

  const handleSubmitPost = (e: React.FormEvent) => {
    e.preventDefault();
    if (newPost.trim()) {
      // Handle post submission
      setNewPost('');
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Farmer Community</h1>
        
        {/* Create Post */}
        <div className="bg-gray-50 rounded-lg p-4 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Share Your Experience</h2>
          <form onSubmit={handleSubmitPost}>
            <textarea
              value={newPost}
              onChange={(e) => setNewPost(e.target.value)}
              placeholder="Share your farming experiences, ask questions, or provide tips to fellow farmers..."
              className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
              rows={4}
            />
            <div className="flex justify-end mt-3">
              <button
                type="submit"
                className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                Post
              </button>
            </div>
          </form>
        </div>
        
        {/* Community Posts */}
        <div className="space-y-4">
          {posts.map((post) => (
            <div key={post.id} className="bg-white border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white font-semibold">
                    {post.author.charAt(0)}
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">{post.author}</h3>
                    <p className="text-sm text-gray-500">{post.location} • {post.time}</p>
                  </div>
                </div>
              </div>
              
              <h4 className="font-medium text-gray-900 mb-2">{post.title}</h4>
              <p className="text-gray-700 mb-4">{post.content}</p>
              
              <div className="flex items-center space-x-4 text-sm text-gray-500">
                <button className="flex items-center space-x-1 hover:text-green-600">
                  <span>👍</span>
                  <span>{post.likes}</span>
                </button>
                <button className="flex items-center space-x-1 hover:text-green-600">
                  <span>💬</span>
                  <span>{post.comments}</span>
                </button>
                <button className="hover:text-green-600">Share</button>
              </div>
            </div>
          ))}
        </div>
        
        {/* Community Stats */}
        <div className="mt-8 bg-green-50 border border-green-200 rounded-lg p-4">
          <h3 className="font-medium text-green-800 mb-2">Community Statistics</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-green-700">
            <div>
              <span className="font-medium">Active Farmers:</span> 1,247
            </div>
            <div>
              <span className="font-medium">Posts This Week:</span> 89
            </div>
            <div>
              <span className="font-medium">Questions Answered:</span> 156
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Community;
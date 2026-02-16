import React from 'react';

const Notifications: React.FC = () => {
  const notifications = [
    {
      id: 1,
      type: 'irrigation',
      title: 'Irrigation Reminder',
      message: 'Time to water your wheat crop. Optimal time is between 5-7 PM.',
      time: '2 hours ago',
      isRead: false
    },
    {
      id: 2,
      type: 'pest_control',
      title: 'Pest Alert',
      message: 'Aphid infestation detected in your area. Consider preventive measures.',
      time: '1 day ago',
      isRead: false
    },
    {
      id: 3,
      type: 'weather',
      title: 'Weather Warning',
      message: 'Heavy rainfall expected in next 24 hours. Protect your crops.',
      time: '2 days ago',
      isRead: true
    },
    {
      id: 4,
      type: 'market',
      title: 'Price Update',
      message: 'Wheat prices have increased by 5% in your local market.',
      time: '3 days ago',
      isRead: true
    },
    {
      id: 5,
      type: 'fertilizer',
      title: 'Fertilizer Application',
      message: 'Time to apply nitrogen fertilizer to your rice crop.',
      time: '4 days ago',
      isRead: true
    }
  ];

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'irrigation': return '💧';
      case 'pest_control': return '🐛';
      case 'weather': return '🌧️';
      case 'market': return '📈';
      case 'fertilizer': return '🌱';
      default: return '📢';
    }
  };

  const getNotificationColor = (type: string) => {
    switch (type) {
      case 'irrigation': return 'bg-blue-100 text-blue-800';
      case 'pest_control': return 'bg-red-100 text-red-800';
      case 'weather': return 'bg-yellow-100 text-yellow-800';
      case 'market': return 'bg-green-100 text-green-800';
      case 'fertilizer': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Notifications</h1>
          <button className="text-sm text-green-600 hover:text-green-700">
            Mark all as read
          </button>
        </div>
        
        {/* Notification Settings */}
        <div className="bg-gray-50 rounded-lg p-4 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Notification Settings</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label className="flex items-center">
              <input type="checkbox" defaultChecked className="mr-2" />
              <span className="text-sm text-gray-700">Irrigation reminders</span>
            </label>
            <label className="flex items-center">
              <input type="checkbox" defaultChecked className="mr-2" />
              <span className="text-sm text-gray-700">Pest alerts</span>
            </label>
            <label className="flex items-center">
              <input type="checkbox" defaultChecked className="mr-2" />
              <span className="text-sm text-gray-700">Weather warnings</span>
            </label>
            <label className="flex items-center">
              <input type="checkbox" defaultChecked className="mr-2" />
              <span className="text-sm text-gray-700">Market price updates</span>
            </label>
            <label className="flex items-center">
              <input type="checkbox" defaultChecked className="mr-2" />
              <span className="text-sm text-gray-700">Fertilizer reminders</span>
            </label>
            <label className="flex items-center">
              <input type="checkbox" defaultChecked className="mr-2" />
              <span className="text-sm text-gray-700">Community updates</span>
            </label>
          </div>
        </div>
        
        {/* Notifications List */}
        <div className="space-y-4">
          {notifications.map((notification) => (
            <div
              key={notification.id}
              className={`border rounded-lg p-4 ${
                notification.isRead 
                  ? 'bg-white border-gray-200' 
                  : 'bg-blue-50 border-blue-200'
              }`}
            >
              <div className="flex items-start space-x-3">
                <div className="text-2xl">
                  {getNotificationIcon(notification.type)}
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h3 className="font-medium text-gray-900">{notification.title}</h3>
                    <span className={`px-2 py-1 text-xs rounded-full ${getNotificationColor(notification.type)}`}>
                      {notification.type.replace('_', ' ')}
                    </span>
                  </div>
                  <p className="text-gray-700 mt-1">{notification.message}</p>
                  <p className="text-sm text-gray-500 mt-2">{notification.time}</p>
                </div>
                {!notification.isRead && (
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                )}
              </div>
            </div>
          ))}
        </div>
        
        {/* Notification Summary */}
        <div className="mt-8 bg-green-50 border border-green-200 rounded-lg p-4">
          <h3 className="font-medium text-green-800 mb-2">Notification Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-green-700">
            <div>
              <span className="font-medium">Unread:</span> {notifications.filter(n => !n.isRead).length}
            </div>
            <div>
              <span className="font-medium">This Week:</span> 12
            </div>
            <div>
              <span className="font-medium">Important:</span> 3
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Notifications;
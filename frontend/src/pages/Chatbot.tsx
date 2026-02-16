import React, { useState, useRef, useEffect } from 'react';
import toast from 'react-hot-toast';

interface Message {
  id: number;
  text: string;
  isUser: boolean;
  timestamp: Date;
  type?: 'text' | 'voice';
}

const Chatbot: React.FC = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: 'नमस्ते! मैं आपका AI कृषि सलाहकार हूं। आज आपकी क्या मदद कर सकता हूं? (Hello! I am your AI agriculture advisor. How can I help you today?)',
      isUser: false,
      timestamp: new Date()
    }
  ]);
  const [isListening, setIsListening] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('hi');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // AI Response Generator
  const generateAIResponse = (userMessage: string, language: string): string => {
    const message = userMessage.toLowerCase();
    
    // Hindi responses
    if (language === 'hi') {
      if (message.includes('सिंचाई') || message.includes('irrigation') || message.includes('पानी')) {
        return 'सिंचाई के लिए सुबह या शाम का समय सबसे अच्छा है। अपनी फसल के अनुसार पानी दें - गेहूं को सप्ताह में 2-3 बार, चावल को रोजाना पानी चाहिए।';
      }
      if (message.includes('कीट') || message.includes('pest') || message.includes('बीमारी')) {
        return 'कीट नियंत्रण के लिए नीम का तेल या जैविक कीटनाशक का उपयोग करें। नियमित रूप से पत्तियों की जांच करें और संक्रमित पौधों को तुरंत हटा दें।';
      }
      if (message.includes('खाद') || message.includes('fertilizer') || message.includes('उर्वरक')) {
        return 'खाद डालने का सही समय बुवाई के 15-20 दिन बाद है। NPK अनुपात 20:20:20 का उपयोग करें। मिट्टी की जांच के बाद ही खाद डालें।';
      }
      if (message.includes('मौसम') || message.includes('weather') || message.includes('बारिश')) {
        return 'आज का मौसम अच्छा है। तापमान 28°C है। अगले 2 दिनों में बारिश की संभावना है, इसलिए अपनी फसल की सुरक्षा करें।';
      }
      if (message.includes('फसल') || message.includes('crop') || message.includes('बीज')) {
        return 'सही फसल चुनने के लिए मिट्टी की जांच कराएं। रबी सीजन में गेहूं, सरसों, चना उगा सकते हैं। खरीफ सीजन में चावल, मक्का, कपास अच्छे विकल्प हैं।';
      }
      return 'मैं आपकी मदद करने के लिए यहां हूं। कृपया अपनी समस्या या सवाल विस्तार से बताएं। मैं आपको सबसे अच्छी सलाह दूंगा।';
    }
    
    // English responses
    if (language === 'en') {
      if (message.includes('irrigation') || message.includes('water') || message.includes('watering')) {
        return 'For irrigation, early morning or evening is the best time. Water according to your crop - wheat needs water 2-3 times a week, rice needs daily watering.';
      }
      if (message.includes('pest') || message.includes('disease') || message.includes('insect')) {
        return 'For pest control, use neem oil or organic pesticides. Regularly check leaves and remove infected plants immediately.';
      }
      if (message.includes('fertilizer') || message.includes('manure') || message.includes('nutrient')) {
        return 'The right time to apply fertilizer is 15-20 days after sowing. Use NPK ratio 20:20:20. Apply fertilizer only after soil testing.';
      }
      if (message.includes('weather') || message.includes('rain') || message.includes('temperature')) {
        return 'Today\'s weather is good. Temperature is 28°C. There is a chance of rain in the next 2 days, so protect your crops.';
      }
      if (message.includes('crop') || message.includes('seed') || message.includes('planting')) {
        return 'For choosing the right crop, get your soil tested. In Rabi season, you can grow wheat, mustard, gram. In Kharif season, rice, maize, cotton are good options.';
      }
      return 'I am here to help you. Please describe your problem or question in detail. I will give you the best advice.';
    }
    
    // Punjabi responses
    if (language === 'pa') {
      if (message.includes('ਸਿੰਚਾਈ') || message.includes('ਪਾਣੀ')) {
        return 'ਸਿੰਚਾਈ ਲਈ ਸਵੇਰ ਜਾਂ ਸ਼ਾਮ ਦਾ ਸਮਾਂ ਸਭ ਤੋਂ ਵਧੀਆ ਹੈ। ਆਪਣੀ ਫਸਲ ਦੇ ਅਨੁਸਾਰ ਪਾਣੀ ਦਿਓ - ਕਣਕ ਨੂੰ ਹਫ਼ਤੇ ਵਿੱਚ 2-3 ਵਾਰ, ਚੌਲਾਂ ਨੂੰ ਰੋਜ਼ਾਨਾ ਪਾਣੀ ਚਾਹੀਦਾ ਹੈ।';
      }
      if (message.includes('ਕੀਟ') || message.includes('ਰੋਗ')) {
        return 'ਕੀਟ ਨਿਯੰਤਰਣ ਲਈ ਨੀਮ ਦਾ ਤੇਲ ਜਾਂ ਜੈਵਿਕ ਕੀਟਨਾਸ਼ਕ ਦਾ ਉਪਯੋਗ ਕਰੋ। ਨਿਯਮਿਤ ਤੌਰ \'ਤੇ ਪੱਤਿਆਂ ਦੀ ਜਾਂਚ ਕਰੋ ਅਤੇ ਸੰਕਰਮਿਤ ਪੌਦਿਆਂ ਨੂੰ ਤੁਰੰਤ ਹਟਾ ਦਿਓ।';
      }
      return 'ਮੈਂ ਤੁਹਾਡੀ ਮਦਦ ਕਰਨ ਲਈ ਇੱਥੇ ਹਾਂ। ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਸਮਸਿਆ ਜਾਂ ਸਵਾਲ ਵਿਸਤਾਰ ਨਾਲ ਦੱਸੋ। ਮੈਂ ਤੁਹਾਨੂੰ ਸਭ ਤੋਂ ਵਧੀਆ ਸਲਾਹ ਦਵਾਂਗਾ।';
    }
    
    return 'I am here to help you. Please describe your problem or question in detail.';
  };

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      const newMessage: Message = {
        id: messages.length + 1,
        text: message,
        isUser: true,
        timestamp: new Date(),
        type: 'text'
      };
      setMessages(prev => [...prev, newMessage]);
      setMessage('');
      setIsTyping(true);
      
      // Simulate AI thinking time
      setTimeout(() => {
        const aiResponse = generateAIResponse(message, selectedLanguage);
        const aiMessage: Message = {
          id: messages.length + 2,
          text: aiResponse,
          isUser: false,
          timestamp: new Date(),
          type: 'text'
        };
        setMessages(prev => [...prev, aiMessage]);
        setIsTyping(false);
      }, 1500);
    }
  };

  const handleVoiceInput = () => {
    if (!isListening) {
      setIsListening(true);
      toast.success('Listening... Speak now');
      
      // Simulate voice recognition
      setTimeout(() => {
        const voiceMessage = "मुझे सिंचाई के बारे में जानकारी चाहिए";
        setMessage(voiceMessage);
        setIsListening(false);
        toast.success('Voice input received');
      }, 3000);
    } else {
      setIsListening(false);
      toast.error('Voice input stopped');
    }
  };

  const quickQuestions = [
    { text: 'सिंचाई कब करें?', lang: 'hi' },
    { text: 'कीट नियंत्रण कैसे करें?', lang: 'hi' },
    { text: 'खाद कब डालें?', lang: 'hi' },
    { text: 'मौसम कैसा है?', lang: 'hi' },
    { text: 'When to irrigate?', lang: 'en' },
    { text: 'How to control pests?', lang: 'en' },
    { text: 'When to apply fertilizer?', lang: 'en' },
    { text: 'What is the weather?', lang: 'en' }
  ];

  const handleQuickQuestion = (question: string) => {
    setMessage(question);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        {/* Header */}
        <div className="p-4 border-b border-gray-200 bg-green-50">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-semibold text-gray-900">🤖 AI Crop Advisor</h1>
              <p className="text-sm text-gray-600">Ask questions about crops, pests, diseases, and farming practices</p>
            </div>
            <div className="flex items-center space-x-2">
              <select
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="hi">हिंदी</option>
                <option value="en">English</option>
                <option value="pa">ਪੰਜਾਬੀ</option>
              </select>
            </div>
          </div>
        </div>
        
        {/* Quick Questions */}
        <div className="p-4 border-b border-gray-200 bg-gray-50">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Quick Questions:</h3>
          <div className="flex flex-wrap gap-2">
            {quickQuestions
              .filter(q => q.lang === selectedLanguage)
              .slice(0, 4)
              .map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleQuickQuestion(question.text)}
                  className="px-3 py-1 bg-white border border-gray-300 rounded-full text-sm hover:bg-green-50 hover:border-green-300 transition-colors"
                >
                  {question.text}
                </button>
              ))}
          </div>
        </div>
        
        {/* Messages */}
        <div className="h-96 overflow-y-auto p-4 space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  msg.isUser
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                <p className="text-sm">{msg.text}</p>
                <p className={`text-xs mt-1 ${
                  msg.isUser ? 'text-green-100' : 'text-gray-500'
                }`}>
                  {msg.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        {/* Input Form */}
        <form onSubmit={handleSendMessage} className="p-4 border-t border-gray-200">
          <div className="flex space-x-2">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder={
                selectedLanguage === 'hi' ? 'अपना सवाल यहाँ टाइप करें...' :
                selectedLanguage === 'pa' ? 'ਆਪਣਾ ਸਵਾਲ ਇੱਥੇ ਟਾਈਪ ਕਰੋ...' :
                'Type your question here...'
              }
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            />
            <button
              type="button"
              onClick={handleVoiceInput}
              className={`px-3 py-2 rounded-md transition-colors ${
                isListening 
                  ? 'bg-red-500 text-white hover:bg-red-600' 
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
              title={isListening ? 'Stop listening' : 'Start voice input'}
            >
              {isListening ? '🔴' : '🎤'}
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              Send
            </button>
          </div>
        </form>
        
        {/* Features Info */}
        <div className="p-4 bg-blue-50 border-t border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="flex items-center space-x-2">
              <span className="text-blue-600">🌐</span>
              <span className="text-blue-800">Multilingual Support</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-blue-600">🎤</span>
              <span className="text-blue-800">Voice Input</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-blue-600">🤖</span>
              <span className="text-blue-800">AI-Powered</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
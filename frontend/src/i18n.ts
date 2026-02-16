import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import Backend from 'i18next-http-backend';

// Translation resources
const resources = {
  hi: {
    translation: {
      // Common
      'common.loading': 'लोड हो रहा है...',
      'common.error': 'त्रुटि हुई है',
      'common.success': 'सफल',
      'common.cancel': 'रद्द करें',
      'common.save': 'सहेजें',
      'common.delete': 'हटाएं',
      'common.edit': 'संपादित करें',
      'common.back': 'वापस',
      'common.next': 'आगे',
      'common.previous': 'पिछला',
      'common.submit': 'जमा करें',
      'common.search': 'खोजें',
      'common.filter': 'फिल्टर',
      'common.sort': 'क्रमबद्ध करें',
      'common.refresh': 'रिफ्रेश करें',
      
      // Navigation
      'nav.home': 'होम',
      'nav.chatbot': 'AI सलाहकार',
      'nav.imageAnalysis': 'छवि विश्लेषण',
      'nav.marketPrices': 'बाजार भाव',
      'nav.community': 'समुदाय',
      'nav.notifications': 'सूचनाएं',
      'nav.profile': 'प्रोफाइल',
      'nav.logout': 'लॉग आउट',
      
      // Authentication
      'auth.login': 'लॉग इन करें',
      'auth.register': 'रजिस्टर करें',
      'auth.phoneNumber': 'फोन नंबर',
      'auth.otp': 'OTP',
      'auth.sendOTP': 'OTP भेजें',
      'auth.verifyOTP': 'OTP सत्यापित करें',
      'auth.name': 'नाम',
      'auth.email': 'ईमेल',
      'auth.state': 'राज्य',
      'auth.district': 'जिला',
      'auth.village': 'गांव',
      'auth.pincode': 'पिन कोड',
      'auth.farmSize': 'खेत का आकार (एकड़)',
      'auth.primaryCrops': 'मुख्य फसलें',
      'auth.farmingExperience': 'खेती का अनुभव (वर्ष)',
      'auth.preferredLanguage': 'पसंदीदा भाषा',
      
      // Home
      'home.welcome': 'स्वागत है',
      'home.getAdvice': 'AI सलाह प्राप्त करें',
      'home.uploadImage': 'छवि अपलोड करें',
      'home.checkPrices': 'बाजार भाव देखें',
      'home.joinCommunity': 'समुदाय में शामिल हों',
      'home.weatherUpdate': 'मौसम अपडेट',
      'home.todayAdvice': 'आज की सलाह',
      'home.quickActions': 'त्वरित कार्य',
      
      // Chatbot
      'chatbot.title': 'AI कृषि सलाहकार',
      'chatbot.placeholder': 'अपना सवाल पूछें...',
      'chatbot.voiceInput': 'आवाज इनपुट',
      'chatbot.voiceRecording': 'आवाज रिकॉर्ड हो रही है...',
      'chatbot.stopRecording': 'रिकॉर्डिंग रोकें',
      'chatbot.send': 'भेजें',
      'chatbot.typing': 'टाइप कर रहा है...',
      'chatbot.suggestions': 'सुझाव',
      'chatbot.clearChat': 'चैट साफ करें',
      
      // Image Analysis
      'imageAnalysis.title': 'छवि विश्लेषण',
      'imageAnalysis.uploadImage': 'छवि अपलोड करें',
      'imageAnalysis.dragDrop': 'छवि को यहां खींचें या क्लिक करें',
      'imageAnalysis.analyze': 'विश्लेषण करें',
      'imageAnalysis.diseaseDetection': 'रोग पहचान',
      'imageAnalysis.pestDetection': 'कीट पहचान',
      'imageAnalysis.cropClassification': 'फसल वर्गीकरण',
      'imageAnalysis.plantHealth': 'पौधे की सेहत',
      'imageAnalysis.results': 'परिणाम',
      'imageAnalysis.confidence': 'विश्वसनीयता',
      'imageAnalysis.treatment': 'उपचार',
      'imageAnalysis.prevention': 'रोकथाम',
      
      // Market Prices
      'marketPrices.title': 'बाजार भाव',
      'marketPrices.searchCrop': 'फसल खोजें',
      'marketPrices.selectMarket': 'बाजार चुनें',
      'marketPrices.priceRange': 'कीमत सीमा',
      'marketPrices.trend': 'ट्रेंड',
      'marketPrices.forecast': 'पूर्वानुमान',
      'marketPrices.setAlert': 'अलर्ट सेट करें',
      'marketPrices.priceHistory': 'कीमत इतिहास',
      
      // Community
      'community.title': 'किसान समुदाय',
      'community.postQuestion': 'सवाल पूछें',
      'community.shareExperience': 'अनुभव साझा करें',
      'community.recentPosts': 'हाल के पोस्ट',
      'community.trending': 'ट्रेंडिंग',
      'community.like': 'लाइक',
      'community.comment': 'कमेंट',
      'community.share': 'शेयर',
      'community.follow': 'फॉलो करें',
      
      // Notifications
      'notifications.title': 'सूचनाएं',
      'notifications.markAllRead': 'सभी पढ़े गए मार्क करें',
      'notifications.weatherAlert': 'मौसम चेतावनी',
      'notifications.priceAlert': 'कीमत अलर्ट',
      'notifications.diseaseAlert': 'रोग चेतावनी',
      'notifications.reminder': 'रिमाइंडर',
      
      // Profile
      'profile.title': 'प्रोफाइल',
      'profile.editProfile': 'प्रोफाइल संपादित करें',
      'profile.personalInfo': 'व्यक्तिगत जानकारी',
      'profile.farmInfo': 'खेत की जानकारी',
      'profile.preferences': 'प्राथमिकताएं',
      'profile.notificationSettings': 'सूचना सेटिंग्स',
      'profile.languageSettings': 'भाषा सेटिंग्स',
      'profile.privacySettings': 'गोपनीयता सेटिंग्स',
    }
  },
  en: {
    translation: {
      // Common
      'common.loading': 'Loading...',
      'common.error': 'An error occurred',
      'common.success': 'Success',
      'common.cancel': 'Cancel',
      'common.save': 'Save',
      'common.delete': 'Delete',
      'common.edit': 'Edit',
      'common.back': 'Back',
      'common.next': 'Next',
      'common.previous': 'Previous',
      'common.submit': 'Submit',
      'common.search': 'Search',
      'common.filter': 'Filter',
      'common.sort': 'Sort',
      'common.refresh': 'Refresh',
      
      // Navigation
      'nav.home': 'Home',
      'nav.chatbot': 'AI Advisor',
      'nav.imageAnalysis': 'Image Analysis',
      'nav.marketPrices': 'Market Prices',
      'nav.community': 'Community',
      'nav.notifications': 'Notifications',
      'nav.profile': 'Profile',
      'nav.logout': 'Logout',
      
      // Authentication
      'auth.login': 'Login',
      'auth.register': 'Register',
      'auth.phoneNumber': 'Phone Number',
      'auth.otp': 'OTP',
      'auth.sendOTP': 'Send OTP',
      'auth.verifyOTP': 'Verify OTP',
      'auth.name': 'Name',
      'auth.email': 'Email',
      'auth.state': 'State',
      'auth.district': 'District',
      'auth.village': 'Village',
      'auth.pincode': 'Pincode',
      'auth.farmSize': 'Farm Size (acres)',
      'auth.primaryCrops': 'Primary Crops',
      'auth.farmingExperience': 'Farming Experience (years)',
      'auth.preferredLanguage': 'Preferred Language',
      
      // Home
      'home.welcome': 'Welcome',
      'home.getAdvice': 'Get AI Advice',
      'home.uploadImage': 'Upload Image',
      'home.checkPrices': 'Check Prices',
      'home.joinCommunity': 'Join Community',
      'home.weatherUpdate': 'Weather Update',
      'home.todayAdvice': 'Today\'s Advice',
      'home.quickActions': 'Quick Actions',
      
      // Chatbot
      'chatbot.title': 'AI Agriculture Advisor',
      'chatbot.placeholder': 'Ask your question...',
      'chatbot.voiceInput': 'Voice Input',
      'chatbot.voiceRecording': 'Recording voice...',
      'chatbot.stopRecording': 'Stop Recording',
      'chatbot.send': 'Send',
      'chatbot.typing': 'Typing...',
      'chatbot.suggestions': 'Suggestions',
      'chatbot.clearChat': 'Clear Chat',
      
      // Image Analysis
      'imageAnalysis.title': 'Image Analysis',
      'imageAnalysis.uploadImage': 'Upload Image',
      'imageAnalysis.dragDrop': 'Drag and drop image here or click to select',
      'imageAnalysis.analyze': 'Analyze',
      'imageAnalysis.diseaseDetection': 'Disease Detection',
      'imageAnalysis.pestDetection': 'Pest Detection',
      'imageAnalysis.cropClassification': 'Crop Classification',
      'imageAnalysis.plantHealth': 'Plant Health',
      'imageAnalysis.results': 'Results',
      'imageAnalysis.confidence': 'Confidence',
      'imageAnalysis.treatment': 'Treatment',
      'imageAnalysis.prevention': 'Prevention',
      
      // Market Prices
      'marketPrices.title': 'Market Prices',
      'marketPrices.searchCrop': 'Search Crop',
      'marketPrices.selectMarket': 'Select Market',
      'marketPrices.priceRange': 'Price Range',
      'marketPrices.trend': 'Trend',
      'marketPrices.forecast': 'Forecast',
      'marketPrices.setAlert': 'Set Alert',
      'marketPrices.priceHistory': 'Price History',
      
      // Community
      'community.title': 'Farmer Community',
      'community.postQuestion': 'Post Question',
      'community.shareExperience': 'Share Experience',
      'community.recentPosts': 'Recent Posts',
      'community.trending': 'Trending',
      'community.like': 'Like',
      'community.comment': 'Comment',
      'community.share': 'Share',
      'community.follow': 'Follow',
      
      // Notifications
      'notifications.title': 'Notifications',
      'notifications.markAllRead': 'Mark All Read',
      'notifications.weatherAlert': 'Weather Alert',
      'notifications.priceAlert': 'Price Alert',
      'notifications.diseaseAlert': 'Disease Alert',
      'notifications.reminder': 'Reminder',
      
      // Profile
      'profile.title': 'Profile',
      'profile.editProfile': 'Edit Profile',
      'profile.personalInfo': 'Personal Information',
      'profile.farmInfo': 'Farm Information',
      'profile.preferences': 'Preferences',
      'profile.notificationSettings': 'Notification Settings',
      'profile.languageSettings': 'Language Settings',
      'profile.privacySettings': 'Privacy Settings',
    }
  },
  pa: {
    translation: {
      // Common
      'common.loading': 'ਲੋਡ ਹੋ ਰਿਹਾ ਹੈ...',
      'common.error': 'ਗਲਤੀ ਹੋਈ ਹੈ',
      'common.success': 'ਸਫਲ',
      'common.cancel': 'ਰੱਦ ਕਰੋ',
      'common.save': 'ਸੇਵ ਕਰੋ',
      'common.delete': 'ਮਿਟਾਓ',
      'common.edit': 'ਸੰਪਾਦਨ ਕਰੋ',
      'common.back': 'ਵਾਪਸ',
      'common.next': 'ਅੱਗੇ',
      'common.previous': 'ਪਿਛਲਾ',
      'common.submit': 'ਜਮ੍ਹਾ ਕਰੋ',
      'common.search': 'ਖੋਜੋ',
      'common.filter': 'ਫਿਲਟਰ',
      'common.sort': 'ਕ੍ਰਮਬੱਧ ਕਰੋ',
      'common.refresh': 'ਰਿਫਰੈਸ਼ ਕਰੋ',
      
      // Navigation
      'nav.home': 'ਘਰ',
      'nav.chatbot': 'AI ਸਲਾਹਕਾਰ',
      'nav.imageAnalysis': 'ਚਿੱਤਰ ਵਿਸ਼ਲੇਸ਼ਣ',
      'nav.marketPrices': 'ਬਾਜ਼ਾਰ ਭਾਅ',
      'nav.community': 'ਕਮਿਊਨਿਟੀ',
      'nav.notifications': 'ਸੂਚਨਾਵਾਂ',
      'nav.profile': 'ਪ੍ਰੋਫਾਈਲ',
      'nav.logout': 'ਲੌਗ ਆਉਟ',
      
      // Authentication
      'auth.login': 'ਲੌਗ ਇਨ ਕਰੋ',
      'auth.register': 'ਰਜਿਸਟਰ ਕਰੋ',
      'auth.phoneNumber': 'ਫੋਨ ਨੰਬਰ',
      'auth.otp': 'OTP',
      'auth.sendOTP': 'OTP ਭੇਜੋ',
      'auth.verifyOTP': 'OTP ਸਥਿਤੀ ਕਰੋ',
      'auth.name': 'ਨਾਮ',
      'auth.email': 'ਈਮੇਲ',
      'auth.state': 'ਰਾਜ',
      'auth.district': 'ਜ਼ਿਲ੍ਹਾ',
      'auth.village': 'ਪਿੰਡ',
      'auth.pincode': 'ਪਿੰਨ ਕੋਡ',
      'auth.farmSize': 'ਖੇਤ ਦਾ ਆਕਾਰ (ਏਕੜ)',
      'auth.primaryCrops': 'ਮੁੱਖ ਫਸਲਾਂ',
      'auth.farmingExperience': 'ਖੇਤੀ ਦਾ ਤਜਰਬਾ (ਸਾਲ)',
      'auth.preferredLanguage': 'ਪਸੰਦੀਦਾ ਭਾਸ਼ਾ',
      
      // Home
      'home.welcome': 'ਸਵਾਗਤ ਹੈ',
      'home.getAdvice': 'AI ਸਲਾਹ ਪ੍ਰਾਪਤ ਕਰੋ',
      'home.uploadImage': 'ਚਿੱਤਰ ਅਪਲੋਡ ਕਰੋ',
      'home.checkPrices': 'ਬਾਜ਼ਾਰ ਭਾਅ ਦੇਖੋ',
      'home.joinCommunity': 'ਕਮਿਊਨਿਟੀ ਵਿੱਚ ਸ਼ਾਮਲ ਹੋਵੋ',
      'home.weatherUpdate': 'ਮੌਸਮ ਅਪਡੇਟ',
      'home.todayAdvice': 'ਅੱਜ ਦੀ ਸਲਾਹ',
      'home.quickActions': 'ਤੇਜ਼ ਕਾਰਵਾਈਆਂ',
      
      // Chatbot
      'chatbot.title': 'AI ਖੇਤੀ ਸਲਾਹਕਾਰ',
      'chatbot.placeholder': 'ਆਪਣਾ ਸਵਾਲ ਪੁੱਛੋ...',
      'chatbot.voiceInput': 'ਆਵਾਜ਼ ਇਨਪੁੱਟ',
      'chatbot.voiceRecording': 'ਆਵਾਜ਼ ਰਿਕਾਰਡ ਹੋ ਰਹੀ ਹੈ...',
      'chatbot.stopRecording': 'ਰਿਕਾਰਡਿੰਗ ਰੋਕੋ',
      'chatbot.send': 'ਭੇਜੋ',
      'chatbot.typing': 'ਟਾਈਪ ਕਰ ਰਿਹਾ ਹੈ...',
      'chatbot.suggestions': 'ਸੁਝਾਅ',
      'chatbot.clearChat': 'ਚੈਟ ਸਾਫ਼ ਕਰੋ',
      
      // Image Analysis
      'imageAnalysis.title': 'ਚਿੱਤਰ ਵਿਸ਼ਲੇਸ਼ਣ',
      'imageAnalysis.uploadImage': 'ਚਿੱਤਰ ਅਪਲੋਡ ਕਰੋ',
      'imageAnalysis.dragDrop': 'ਚਿੱਤਰ ਨੂੰ ਇੱਥੇ ਖਿੱਚੋ ਜਾਂ ਕਲਿਕ ਕਰੋ',
      'imageAnalysis.analyze': 'ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ',
      'imageAnalysis.diseaseDetection': 'ਰੋਗ ਪਛਾਣ',
      'imageAnalysis.pestDetection': 'ਕੀਟ ਪਛਾਣ',
      'imageAnalysis.cropClassification': 'ਫਸਲ ਵਰਗੀਕਰਣ',
      'imageAnalysis.plantHealth': 'ਪੌਦੇ ਦੀ ਸਿਹਤ',
      'imageAnalysis.results': 'ਨਤੀਜੇ',
      'imageAnalysis.confidence': 'ਵਿਸ਼ਵਾਸ',
      'imageAnalysis.treatment': 'ਇਲਾਜ',
      'imageAnalysis.prevention': 'ਰੋਕਥਾਮ',
      
      // Market Prices
      'marketPrices.title': 'ਬਾਜ਼ਾਰ ਭਾਅ',
      'marketPrices.searchCrop': 'ਫਸਲ ਖੋਜੋ',
      'marketPrices.selectMarket': 'ਬਾਜ਼ਾਰ ਚੁਣੋ',
      'marketPrices.priceRange': 'ਕੀਮਤ ਸੀਮਾ',
      'marketPrices.trend': 'ਟ੍ਰੈਂਡ',
      'marketPrices.forecast': 'ਪੂਰਵਾਨੁਮਾਨ',
      'marketPrices.setAlert': 'ਅਲਰਟ ਸੈੱਟ ਕਰੋ',
      'marketPrices.priceHistory': 'ਕੀਮਤ ਇਤਿਹਾਸ',
      
      // Community
      'community.title': 'ਕਿਸਾਨ ਕਮਿਊਨਿਟੀ',
      'community.postQuestion': 'ਸਵਾਲ ਪੋਸਟ ਕਰੋ',
      'community.shareExperience': 'ਤਜਰਬਾ ਸਾਂਝਾ ਕਰੋ',
      'community.recentPosts': 'ਹਾਲ ਦੇ ਪੋਸਟ',
      'community.trending': 'ਟ੍ਰੈਂਡਿੰਗ',
      'community.like': 'ਲਾਈਕ',
      'community.comment': 'ਕਮੈਂਟ',
      'community.share': 'ਸ਼ੇਅਰ',
      'community.follow': 'ਫੌਲੋ ਕਰੋ',
      
      // Notifications
      'notifications.title': 'ਸੂਚਨਾਵਾਂ',
      'notifications.markAllRead': 'ਸਭ ਪੜ੍ਹੇ ਗਏ ਮਾਰਕ ਕਰੋ',
      'notifications.weatherAlert': 'ਮੌਸਮ ਚੇਤਾਵਨੀ',
      'notifications.priceAlert': 'ਕੀਮਤ ਅਲਰਟ',
      'notifications.diseaseAlert': 'ਰੋਗ ਚੇਤਾਵਨੀ',
      'notifications.reminder': 'ਰਿਮਾਈਂਡਰ',
      
      // Profile
      'profile.title': 'ਪ੍ਰੋਫਾਈਲ',
      'profile.editProfile': 'ਪ੍ਰੋਫਾਈਲ ਸੰਪਾਦਨ ਕਰੋ',
      'profile.personalInfo': 'ਵਿਅਕਤੀਗਤ ਜਾਣਕਾਰੀ',
      'profile.farmInfo': 'ਖੇਤ ਦੀ ਜਾਣਕਾਰੀ',
      'profile.preferences': 'ਤਰਜੀਹਾਂ',
      'profile.notificationSettings': 'ਸੂਚਨਾ ਸੈਟਿੰਗਜ਼',
      'profile.languageSettings': 'ਭਾਸ਼ਾ ਸੈਟਿੰਗਜ਼',
      'profile.privacySettings': 'ਗੁਪਤਤਾ ਸੈਟਿੰਗਜ਼',
    }
  }
};

i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    lng: 'hi', // default language
    fallbackLng: 'en',
    debug: process.env.NODE_ENV === 'development',
    
    interpolation: {
      escapeValue: false, // not needed for react as it escapes by default
    },
    
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage'],
    },
  });

export default i18n;

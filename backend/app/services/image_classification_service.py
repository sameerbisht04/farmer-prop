import cv2
import numpy as np
from PIL import Image
import io
import json
from typing import Dict, Any, List
import torch
import torchvision.transforms as transforms
from torchvision import models


class ImageClassificationService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Disease database
        self.disease_database = {
            "rice": {
                "bacterial_blight": {
                    "name": "बैक्टीरियल ब्लाइट",
                    "description": "चावल की पत्तियों पर पीले-भूरे रंग के धब्बे दिखाई देते हैं",
                    "treatment": "कॉपर ऑक्सीक्लोराइड 0.3% का छिड़काव करें",
                    "prevention": "स्वस्थ बीज का उपयोग करें और खेत में पानी का उचित प्रबंधन करें",
                    "severity": "high"
                },
                "blast": {
                    "name": "ब्लास्ट रोग",
                    "description": "पत्तियों और तनों पर भूरे रंग के धब्बे",
                    "treatment": "ट्राइसाइक्लाजोल 0.1% का छिड़काव करें",
                    "prevention": "नाइट्रोजन की मात्रा कम रखें और खेत को साफ रखें",
                    "severity": "high"
                }
            },
            "wheat": {
                "rust": {
                    "name": "रस्ट रोग",
                    "description": "पत्तियों पर नारंगी-भूरे रंग के धब्बे",
                    "treatment": "प्रोपिकोनाजोल 0.1% का छिड़काव करें",
                    "prevention": "प्रतिरोधी किस्मों का उपयोग करें",
                    "severity": "medium"
                },
                "powdery_mildew": {
                    "name": "पाउडरी मिल्ड्यू",
                    "description": "पत्तियों पर सफेद पाउडर जैसा दिखाई देता है",
                    "treatment": "सल्फर 0.2% का छिड़काव करें",
                    "prevention": "खेत में हवा का प्रवाह बनाए रखें",
                    "severity": "medium"
                }
            },
            "tomato": {
                "early_blight": {
                    "name": "अर्ली ब्लाइट",
                    "description": "पत्तियों पर भूरे रंग के धब्बे जो बढ़ते जाते हैं",
                    "treatment": "मैनकोजेब 0.2% का छिड़काव करें",
                    "prevention": "पौधों के बीच उचित दूरी रखें",
                    "severity": "medium"
                },
                "late_blight": {
                    "name": "लेट ब्लाइट",
                    "description": "पत्तियों और फलों पर काले धब्बे",
                    "treatment": "मेटालैक्सिल 0.1% का छिड़काव करें",
                    "prevention": "पानी का उचित प्रबंधन करें",
                    "severity": "high"
                }
            }
        }
        
        # Pest database
        self.pest_database = {
            "rice": {
                "brown_plant_hopper": {
                    "name": "भूरा प्लांट हॉपर",
                    "description": "चावल की पत्तियों को खाने वाला छोटा भूरा कीट",
                    "control": "इमिडाक्लोप्रिड 0.05% का छिड़काव करें",
                    "prevention": "खेत में पानी का उचित प्रबंधन करें",
                    "symptoms": "पत्तियां पीली हो जाती हैं और सूख जाती हैं"
                },
                "rice_leaf_folder": {
                    "name": "चावल पत्ती मोड़क",
                    "description": "पत्तियों को मोड़कर अंदर रहने वाला कीट",
                    "control": "कार्बोफ्यूरान 3G का उपयोग करें",
                    "prevention": "खेत को साफ रखें और प्राकृतिक शत्रुओं को बढ़ावा दें",
                    "symptoms": "पत्तियां मुड़ी हुई दिखाई देती हैं"
                }
            },
            "wheat": {
                "aphid": {
                    "name": "एफिड",
                    "description": "छोटे हरे या काले रंग के कीट जो पत्तियों का रस चूसते हैं",
                    "control": "डाइमेथोएट 0.03% का छिड़काव करें",
                    "prevention": "प्राकृतिक शत्रुओं को बढ़ावा दें",
                    "symptoms": "पत्तियां पीली हो जाती हैं और विकृत हो जाती हैं"
                }
            },
            "tomato": {
                "whitefly": {
                    "name": "व्हाइटफ्लाई",
                    "description": "छोटे सफेद रंग के कीट जो पत्तियों के नीचे रहते हैं",
                    "control": "एसिटामिप्रिड 0.01% का छिड़काव करें",
                    "prevention": "पीले चिपचिपे ट्रैप का उपयोग करें",
                    "symptoms": "पत्तियां पीली हो जाती हैं और वायरस फैलता है"
                }
            }
        }
        
        # Crop database
        self.crop_database = {
            "rice": {
                "name": "चावल",
                "description": "भारत की मुख्य खाद्य फसल",
                "growth_stages": ["seedling", "tillering", "flowering", "maturity"],
                "health_indicators": ["leaf_color", "plant_height", "tiller_count"]
            },
            "wheat": {
                "name": "गेहूं",
                "description": "रबी की मुख्य फसल",
                "growth_stages": ["germination", "tillering", "stem_elongation", "heading", "maturity"],
                "health_indicators": ["leaf_color", "plant_height", "tiller_count"]
            },
            "tomato": {
                "name": "टमाटर",
                "description": "महत्वपूर्ण सब्जी फसल",
                "growth_stages": ["seedling", "vegetative", "flowering", "fruiting", "maturity"],
                "health_indicators": ["leaf_color", "fruit_quality", "plant_vigor"]
            }
        }

    async def classify_crop_disease(self, image_data: bytes, crop_type: str = None) -> Dict[str, Any]:
        """
        Classify crop disease from image
        """
        try:
            # Preprocess image
            image = self._preprocess_image(image_data)
            
            # For now, return mock data based on image analysis
            # In production, this would use a trained ML model
            mock_result = self._mock_disease_classification(image, crop_type)
            
            return mock_result
            
        except Exception as e:
            print(f"Disease classification error: {e}")
            return self._get_default_disease_result()

    async def classify_pest(self, image_data: bytes, crop_type: str = None) -> Dict[str, Any]:
        """
        Classify pest from image
        """
        try:
            # Preprocess image
            image = self._preprocess_image(image_data)
            
            # For now, return mock data based on image analysis
            # In production, this would use a trained ML model
            mock_result = self._mock_pest_classification(image, crop_type)
            
            return mock_result
            
        except Exception as e:
            print(f"Pest classification error: {e}")
            return self._get_default_pest_result()

    async def classify_crop(self, image_data: bytes) -> Dict[str, Any]:
        """
        Classify crop type from image
        """
        try:
            # Preprocess image
            image = self._preprocess_image(image_data)
            
            # For now, return mock data based on image analysis
            # In production, this would use a trained ML model
            mock_result = self._mock_crop_classification(image)
            
            return mock_result
            
        except Exception as e:
            print(f"Crop classification error: {e}")
            return self._get_default_crop_result()

    async def analyze_plant_health(self, image_data: bytes, crop_type: str = None) -> Dict[str, Any]:
        """
        Comprehensive plant health analysis
        """
        try:
            # Preprocess image
            image = self._preprocess_image(image_data)
            
            # Analyze image for health indicators
            health_analysis = self._analyze_plant_health_indicators(image, crop_type)
            
            return health_analysis
            
        except Exception as e:
            print(f"Plant health analysis error: {e}")
            return self._get_default_health_result()

    def _preprocess_image(self, image_data: bytes) -> np.ndarray:
        """
        Preprocess image for analysis
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array
            image_array = np.array(image)
            
            # Resize image if needed
            if image_array.shape[0] > 512 or image_array.shape[1] > 512:
                image = image.resize((512, 512))
                image_array = np.array(image)
            
            return image_array
            
        except Exception as e:
            print(f"Image preprocessing error: {e}")
            return np.zeros((224, 224, 3), dtype=np.uint8)

    def _mock_disease_classification(self, image: np.ndarray, crop_type: str = None) -> Dict[str, Any]:
        """
        Mock disease classification (replace with actual ML model)
        """
        # Simple analysis based on image characteristics
        avg_color = np.mean(image, axis=(0, 1))
        
        # Determine crop type if not provided
        if not crop_type:
            crop_type = self._detect_crop_type_from_image(image)
        
        # Mock disease detection based on color analysis
        if avg_color[1] < 100:  # Low green component
            disease_key = "bacterial_blight" if crop_type == "rice" else "early_blight"
        else:
            disease_key = "blast" if crop_type == "rice" else "late_blight"
        
        disease_info = self.disease_database.get(crop_type, {}).get(disease_key, {})
        
        return {
            "disease_name": disease_info.get("name", "अज्ञात रोग"),
            "confidence": 0.75,
            "description": disease_info.get("description", "रोग की पहचान की गई है"),
            "treatment_advice": disease_info.get("treatment", "उपयुक्त दवा का छिड़काव करें"),
            "prevention_tips": disease_info.get("prevention", "खेत को साफ रखें"),
            "severity": disease_info.get("severity", "medium"),
            "crop_type": crop_type,
            "model_version": "v1.0"
        }

    def _mock_pest_classification(self, image: np.ndarray, crop_type: str = None) -> Dict[str, Any]:
        """
        Mock pest classification (replace with actual ML model)
        """
        # Determine crop type if not provided
        if not crop_type:
            crop_type = self._detect_crop_type_from_image(image)
        
        # Mock pest detection
        pest_key = "brown_plant_hopper" if crop_type == "rice" else "aphid"
        pest_info = self.pest_database.get(crop_type, {}).get(pest_key, {})
        
        return {
            "pest_name": pest_info.get("name", "अज्ञात कीट"),
            "confidence": 0.70,
            "description": pest_info.get("description", "कीट की पहचान की गई है"),
            "control_measures": pest_info.get("control", "उपयुक्त कीटनाशक का छिड़काव करें"),
            "prevention_tips": pest_info.get("prevention", "खेत को साफ रखें"),
            "damage_symptoms": pest_info.get("symptoms", "पत्तियों में नुकसान दिखाई देता है"),
            "crop_type": crop_type,
            "model_version": "v1.0"
        }

    def _mock_crop_classification(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Mock crop classification (replace with actual ML model)
        """
        # Simple analysis based on image characteristics
        avg_color = np.mean(image, axis=(0, 1))
        
        # Determine crop type based on color characteristics
        if avg_color[1] > 120:  # High green component
            crop_type = "rice"
        elif avg_color[1] > 100:
            crop_type = "wheat"
        else:
            crop_type = "tomato"
        
        crop_info = self.crop_database.get(crop_type, {})
        
        return {
            "crop_name": crop_info.get("name", "अज्ञात फसल"),
            "confidence": 0.80,
            "description": crop_info.get("description", "फसल की पहचान की गई है"),
            "growth_stage": "vegetative",
            "health_status": "healthy"
        }

    def _analyze_plant_health_indicators(self, image: np.ndarray, crop_type: str = None) -> Dict[str, Any]:
        """
        Analyze plant health indicators from image
        """
        # Determine crop type if not provided
        if not crop_type:
            crop_type = self._detect_crop_type_from_image(image)
        
        # Analyze color distribution
        avg_color = np.mean(image, axis=(0, 1))
        
        # Calculate health score based on color analysis
        green_ratio = avg_color[1] / (avg_color[0] + avg_color[1] + avg_color[2])
        health_score = min(1.0, green_ratio * 2)
        
        # Determine health status
        if health_score > 0.8:
            health_status = "healthy"
            issues = []
        elif health_score > 0.6:
            health_status = "moderate"
            issues = ["पत्तियों में हल्का पीलापन"]
        else:
            health_status = "poor"
            issues = ["पत्तियों में पीलापन", "संभावित रोग या कीट"]
        
        return {
            "overall_health_score": health_score,
            "health_status": health_status,
            "issues_detected": issues,
            "health_summary": f"पौधे की सेहत {health_status} है",
            "recommendations": self._get_health_recommendations(health_status, issues),
            "confidence": 0.75,
            "crop_type": crop_type,
            "model_version": "v1.0"
        }

    def _detect_crop_type_from_image(self, image: np.ndarray) -> str:
        """
        Detect crop type from image characteristics
        """
        # Simple heuristic based on image characteristics
        avg_color = np.mean(image, axis=(0, 1))
        
        if avg_color[1] > 120:  # High green component
            return "rice"
        elif avg_color[1] > 100:
            return "wheat"
        else:
            return "tomato"

    def _get_health_recommendations(self, health_status: str, issues: List[str]) -> str:
        """
        Get health recommendations based on status and issues
        """
        if health_status == "healthy":
            return "पौधे स्वस्थ हैं। नियमित देखभाल जारी रखें।"
        elif health_status == "moderate":
            return "पौधों में हल्की समस्या है। उर्वरक और पानी का उचित प्रबंधन करें।"
        else:
            return "पौधों में गंभीर समस्या है। तुरंत उपचार की आवश्यकता है।"

    def _get_default_disease_result(self) -> Dict[str, Any]:
        return {
            "disease_name": "रोग पहचान नहीं हो सका",
            "confidence": 0.0,
            "description": "कृपया स्पष्ट तस्वीर भेजें",
            "treatment_advice": "विशेषज्ञ से सलाह लें",
            "prevention_tips": "खेत को साफ रखें",
            "severity": "unknown"
        }

    def _get_default_pest_result(self) -> Dict[str, Any]:
        return {
            "pest_name": "कीट पहचान नहीं हो सका",
            "confidence": 0.0,
            "description": "कृपया स्पष्ट तस्वीर भेजें",
            "control_measures": "विशेषज्ञ से सलाह लें",
            "prevention_tips": "खेत को साफ रखें",
            "damage_symptoms": "लक्षण स्पष्ट नहीं हैं"
        }

    def _get_default_crop_result(self) -> Dict[str, Any]:
        return {
            "crop_name": "फसल पहचान नहीं हो सका",
            "confidence": 0.0,
            "description": "कृपया स्पष्ट तस्वीर भेजें",
            "growth_stage": "unknown",
            "health_status": "unknown"
        }

    def _get_default_health_result(self) -> Dict[str, Any]:
        return {
            "overall_health_score": 0.0,
            "health_status": "unknown",
            "issues_detected": [],
            "health_summary": "विश्लेषण नहीं हो सका",
            "recommendations": "कृपया स्पष्ट तस्वीर भेजें",
            "confidence": 0.0
        }

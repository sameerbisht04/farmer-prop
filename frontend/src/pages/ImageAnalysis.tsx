import React, { useState } from 'react';

const ImageAnalysis: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<string | null>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleAnalyze = () => {
    if (selectedFile) {
      // Simulate analysis
      setAnalysis('This appears to be a healthy wheat plant. No signs of disease or pest damage detected. Continue regular monitoring and maintain proper irrigation.');
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Image Analysis</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Upload Section */}
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Upload Image</h2>
            
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <input
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="hidden"
                id="image-upload"
              />
              <label
                htmlFor="image-upload"
                className="cursor-pointer block"
              >
                <div className="text-4xl mb-4">📷</div>
                <p className="text-gray-600 mb-2">Click to upload an image</p>
                <p className="text-sm text-gray-500">Supports JPG, PNG, GIF up to 10MB</p>
              </label>
            </div>
            
            {preview && (
              <div className="mt-4">
                <img
                  src={preview}
                  alt="Preview"
                  className="w-full h-64 object-cover rounded-lg"
                />
                <button
                  onClick={handleAnalyze}
                  className="mt-4 w-full bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  Analyze Image
                </button>
              </div>
            )}
          </div>
          
          {/* Analysis Results */}
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Analysis Results</h2>
            
            {analysis ? (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h3 className="font-medium text-green-800 mb-2">Analysis Complete</h3>
                <p className="text-green-700">{analysis}</p>
              </div>
            ) : (
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
                <div className="text-4xl mb-4">🔍</div>
                <p className="text-gray-600">Upload an image to get started with analysis</p>
              </div>
            )}
            
            {/* Tips */}
            <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="font-medium text-blue-800 mb-2">Tips for Better Analysis</h3>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• Take clear, well-lit photos</li>
                <li>• Focus on affected areas</li>
                <li>• Include leaves, stems, and roots if possible</li>
                <li>• Avoid blurry or dark images</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageAnalysis;
export interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  type?: string;
  confidence?: number;
  suggestions?: string[];
}

export interface ChatResponse {
  message: string;
  advisory_type: string;
  confidence: number;
  suggestions: string[];
  language: string;
  audio_response_url?: string;
  timestamp: Date;
}

export interface VoiceMessage {
  audio_data?: string;
  transcribed_text: string;
  language: string;
  audio_format: string;
}

export interface ChatHistory {
  id: number;
  title: string;
  content: string;
  type: string;
  created_at: string;
  is_read: boolean;
}

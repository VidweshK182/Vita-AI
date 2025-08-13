
'use client';

import { motion } from 'framer-motion';
import React, { useEffect, useState } from 'react';
import BackgroundPaths from '../components/BackgroundPaths';

const emojis = [
  '🧠', '💬', '📊', '😴', '💧', '😊', '📈', '🧪',
  '👨‍⚕️', '🤖', '📦', '🛠️', '💻', '🧬', '📅',
  '🧘‍♂️', '📚', '🧾', '⚙️', '🩺', '🧍‍♂️', '🚰', '🌙'
];

export default function InsightsPage() {
  const [isClient, setIsClient] = useState(false);
  const [currentEmojiIndex, setCurrentEmojiIndex] = useState(0);
  const [shuffledEmojis, setShuffledEmojis] = useState(emojis);
  const [insight, setInsight] = useState('');
  const [trendImage, setTrendImage] = useState('');
  const [chatOpen, setChatOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const isDev = process.env.NODE_ENV === 'development';

  const BACKEND_URL = isDev
    ? 'http://localhost:10000/upload-csv/'
    : 'https://healthinsightgenerator.onrender.com/upload-csv/';
  
  const CHATBOT_URL = isDev
    ? 'http://localhost:8501/'
    : 'https://streamlitchatbot.onrender.com';
  
  useEffect(() => {
    setIsClient(true);
    setShuffledEmojis([...emojis].sort(() => Math.random() - 0.5));
  }, []);

  useEffect(() => {
    if (!isClient) return;
    const interval = setInterval(() => {
      setCurrentEmojiIndex((prev) => (prev + 1) % shuffledEmojis.length);
    }, 2000);
    return () => clearInterval(interval);
  }, [isClient, shuffledEmojis.length]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedFile(e.target.files?.[0] || null);
  };

  const handleSubmitUpload = async () => {
    if (!selectedFile) return;

    const form = new FormData();
    form.append('file', selectedFile);
    setLoading(true);
    setInsight('');
    setTrendImage('');

    try {
      const res = await fetch(BACKEND_URL, {
        method: 'POST',
        body: form
      });

      if (!res.ok) {
        const text = await res.text();
        console.error('Upload failed:', text);
        throw new Error(text);
      }

      const data = await res.json();
      console.log('Received response:', data);

      setInsight(JSON.stringify(data.insights, null, 2));
      setTrendImage(`data:image/png;base64,${data.trend_image}`);
    } catch (err) {
      console.error('❌ Error uploading file:', err);
      setInsight("❌ Failed to generate insights.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="relative min-h-screen bg-white text-black overflow-x-hidden">
      <BackgroundPaths />

      <div className="relative container mx-auto px-4 py-6 sm:py-12 max-w-2xl">
        <motion.div
          className="flex flex-col items-center space-y-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className="bg-white/70 backdrop-blur-md rounded-lg shadow-md p-6 w-full">
            <motion.div
              className="text-center space-y-3"
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
            >
              <div className="text-4xl sm:text-5xl">{shuffledEmojis[currentEmojiIndex]}</div>
              <h1 className="text-2xl sm:text-3xl font-bold">Health Insight & Chatbot AI Intern Project</h1>
              <p className="text-gray-600 text-sm">
                VITA by ZML — AI-powered personalized health assistant using logs and chatbot interface
              </p>
            </motion.div>

            <div className="w-full mt-6">
              <h2 className="text-lg font-semibold mb-2">🧠 Insight Engine</h2>
              <p className="text-sm text-gray-700">
                Vita parses user logs (sleep, hydration, mood)
                in CSV format and generates human-friendly health advice.
                <br /><br />
                Input: Simulated health data<br />
                Output: Smart suggestions like "Increase your hydration", "Your sleep dropped this week"
                <br /><br />
                💬 Health Chatbot — Ask questions like “How’s my mood this week?” or “What’s my sleep trend?”
                <br /><br />
                📊 Visual Dashboard — Trend charts for sleep/hydration/mood.
                <br /><br />
                📂 Upload a CSV (date, sleep_hours, mood, steps, hydration_ml) 
              </p>
            </div>

            <div className="w-full mt-6 flex flex-col sm:flex-row gap-3 items-center">
              <input
                type="file"
                onChange={handleFileChange}
                className="flex-1 px-2 py-1 border rounded w-full sm:w-auto"
              />
              <button
                onClick={handleSubmitUpload}
                className="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700 transition"
              >
                Submit
              </button>
            </div>

            {loading && (
              <div className="flex flex-col items-center justify-center gap-2 mt-4">
                <div className="animate-pulse text-3xl">🔄</div>
                <p className="text-sm text-gray-600">Generating trends and insights... please wait.</p>
              </div>
            )}

            {insight && (
              <div className="w-full mt-4 bg-gray-100 p-4 rounded shadow max-h-72 overflow-auto">
                <h3 className="font-bold mb-2">🧠 Insights</h3>
                <pre className="text-sm whitespace-pre-wrap">{insight}</pre>
              </div>
            )}

            {trendImage && (
              <div className="w-full mt-6">
                <h3 className="font-bold mb-2">📊 Trends</h3>
                <img src={trendImage} alt="Trend Chart" className="rounded shadow w-full h-auto" />
              </div>
            )}
          </div>
        </motion.div>
      </div>

      <div className="fixed bottom-4 right-4 z-50 flex flex-col items-end">
        <button
          onClick={() => setChatOpen(!chatOpen)}
          className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-full shadow-lg transition duration-200"
        >
          {chatOpen ? 'Close Chat' : '💬 Open Chatbot'}
        </button>

        {chatOpen && (
          <div className="mt-2 w-[90vw] sm:w-[360px] h-[70vh] sm:h-[480px] bg-white rounded-xl overflow-hidden shadow-xl border">
            <iframe
              src={CHATBOT_URL}
              title="Sparkle Chatbot"
              className="w-full h-full"
              allow="clipboard-write"
              style={{ border: 'none' }}
            />
          </div>
        )}
      </div>
    </main>
  );
}

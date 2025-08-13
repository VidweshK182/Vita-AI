'use client';

import { AnimatePresence, motion } from 'framer-motion';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import { FaAddressCard, FaGithub, FaLinkedin, FaTwitter } from 'react-icons/fa';
import BackgroundPaths from './components/BackgroundPaths';

const emojis = ['🕷️', '🌚', '🐚', '🍄', '🌱', '🪽', '🐳', '🐬', '🐙', '🦄', '🐵', '🌀', '🔳', '🔲', '♠️', '♣️', '🃏', '🎴', '🀄️', '♦️', '♥️', '💭'];

const links = [
  {
    title: 'GitHub',
    url: 'https://github.com/VidweshK182',
    icon: <FaGithub size={20} className="sm:text-2xl" />
  },

  {
    title: 'LinkedIn',
    url: 'https://www.linkedin.com/in/vidwesh-kadarla',
    icon: <FaLinkedin size={20} className="sm:text-2xl" />
  }

];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1
  }
};

const emojiVariants = {
  hover: {
    scale: 1.2,
    rotate: [0, -10, 10, -10, 0],
    transition: {
      duration: 0.5
    }
  }
};

export default function Home() {
  const [isClient, setIsClient] = useState(false);
  const [currentEmojiIndex, setCurrentEmojiIndex] = useState(0);
  const [shuffledEmojis, setShuffledEmojis] = useState(emojis);
  const [showContactForm, setShowContactForm] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    setIsClient(true);
    setShuffledEmojis([...emojis].sort(() => Math.random() - 0.5));

    const checkMobile = () => {
      setIsMobile(window.innerWidth < 640);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  useEffect(() => {
    if (!isClient) return;

    const interval = setInterval(() => {
      setCurrentEmojiIndex((prev) => (prev + 1) % shuffledEmojis.length);
    }, 2000);

    return () => clearInterval(interval);
  }, [isClient, shuffledEmojis.length]);

  return (
    <main className="relative min-h-screen bg-white text-black overflow-hidden">
      <BackgroundPaths />

      <div className="relative container mx-auto px-4 py-4 sm:py-8 md:py-16 max-w-2xl">
        <motion.div
          className="flex flex-col items-center space-y-4 sm:space-y-6 md:space-y-8"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div
            className="text-center space-y-2 sm:space-y-3 md:space-y-4"
            variants={itemVariants}
          >
            <motion.div
              className="relative w-20 h-20 sm:w-24 sm:h-24 md:w-32 md:h-32 mx-auto flex items-center justify-center"
              variants={emojiVariants}
              whileHover="hover"
            >
              {isClient && (
                <AnimatePresence mode="wait">
                  <motion.span
                    key={currentEmojiIndex}
                    initial={{ opacity: 0, scale: 0.5 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.5 }}
                    transition={{ duration: 0.5 }}
                    className="text-4xl sm:text-5xl md:text-7xl"
                  >
                    {shuffledEmojis[currentEmojiIndex]}
                  </motion.span>
                </AnimatePresence>
              )}
              {!isClient && (
                <span className="text-4xl sm:text-5xl md:text-7xl">
                  {emojis[0]}
                </span>
              )}
            </motion.div>
            <div className="text-center">
              <h1 className="text-2xl sm:text-3xl md:text-5xl font-bold text-black">
                Kadarla Sri Vidwesh
              </h1>
              <p className="text-sm sm:text-base text-gray-600">
                Full Stack Developer | Tech Explorer
              </p>
            </div>
          </motion.div>

          <motion.div
            className="w-full px-2 sm:px-4"
            variants={containerVariants}
          >
            <Link href="/insights" passHref>
              <motion.div
                className="cursor-pointer flex items-center justify-center gap-2 p-3 mt-6 bg-blue-600 text-white rounded-lg text-base font-semibold hover:bg-blue-700 transition-all"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                🔍 Check Insights
              </motion.div>
            </Link>

            {/* 👇 Circular Social Icons + Contact */}
            <div className="flex justify-center gap-4 mt-6">
              {links.map((link, index) => (
                <motion.a
                  key={index}
                  href={link.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-3 bg-gray-50 rounded-full border border-gray-200 hover:bg-gray-100 group transition-all"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <span className="text-gray-700 group-hover:text-blue-600 transition-colors">
                    {link.icon}
                  </span>
                </motion.a>
              ))}

              <motion.button
                onClick={() => setShowContactForm(true)}
                className="p-3 bg-gray-50 rounded-full border border-gray-200 hover:bg-gray-100 group transition-all"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
              >
                <FaAddressCard size={20} className="text-gray-700 group-hover:text-blue-600 transition-colors" />
              </motion.button>
            </div>

            <AnimatePresence>
              {showContactForm && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center"
                >
                  <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    exit={{ scale: 0.8, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className="w-[90%] sm:w-[500px] h-[600px] bg-white rounded-lg shadow-xl relative overflow-hidden"
                  >
                    <button
                      onClick={() => setShowContactForm(false)}
                      className="absolute top-2 right-3 text-gray-600 hover:text-red-500 text-xl font-bold z-10"
                    >
                      ×
                    </button>

                    <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSe5xu-c140qAjGPuSDDo8PQtVHnoj4ALsC_0H3VIezYWGhr9w/viewform?embedded=true" 
                    width="800" 
                    height="800">Loading…
                    </iframe>

                  </motion.div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </motion.div>
      </div>
    </main>
  );
}

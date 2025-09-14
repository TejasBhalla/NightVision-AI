import { motion } from "framer-motion";
import UploadForm from "./components/UploadForm";
import VideoPlayer from "./components/VideoPlayer";
import screenshot from "./assets/nightvision-screenshot.png";

export default function App() {
  return (
    <div
      className="min-h-screen bg-black text-green-400 relative overflow-hidden"
      style={{
        backgroundImage:
          "url('https://plus.unsplash.com/premium_photo-1682629430351-2cbf66cff813?w=600&auto=format&fit=crop&q=60')",
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      {/* Dark overlay for night-vision effect */}
      <div className="absolute inset-0 bg-black/70"></div>

      {/* Main Content */}
      <div className="relative z-10 flex flex-col items-center p-10 pt-32">
  {/* Title */}
  <motion.h1
    initial={{ opacity: 0, y: -20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 1 }}
    className="text-4xl md:text-6xl font-extrabold text-green-400 drop-shadow-[0_0_10px_rgba(0,255,0,0.8)] mb-10"
  >
    🌙 NightVision AI Engine
  </motion.h1>


        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 1 }}
          className="text-lg md:text-xl text-green-300 mb-8 max-w-2xl text-center"
        >
          Enhance and analyze videos in low-light conditions with AI-powered
          night vision. Upload your video, enable detection, and see the magic ✨.
        </motion.p>

        {/* Upload Form */}
        <UploadForm />

        {/* Video Player */}
        <VideoPlayer />

        {/* About Section */}
<section className="mt-20 max-w-6xl text-center px-4">
  <motion.h2
    initial={{ opacity: 0, y: 30 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 1 }}
    className="text-3xl md:text-4xl font-bold text-green-400 mb-6 drop-shadow-[0_0_10px_rgba(0,255,0,0.7)]"
  >
    🔍 About NightVision AI Engine
  </motion.h2>

  <motion.p
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ delay: 0.3, duration: 1 }}
    className="text-green-200 max-w-3xl mx-auto mb-6 leading-relaxed text-lg md:text-xl"
  >
    The <span className="text-green-400 font-semibold">NightVision AI Engine</span> is a cutting-edge web platform designed to enhance and analyze videos captured in low-light or night-time conditions. It leverages <span className="text-green-400 font-semibold">AI-powered computer vision</span> to brighten scenes, detect objects, and provide real-time insights without losing details.
  </motion.p>

  <motion.p
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ delay: 0.5, duration: 1 }}
    className="text-green-200 max-w-3xl mx-auto mb-6 leading-relaxed text-lg md:text-xl"
  >
    With features like <span className="text-green-400 font-semibold">object detection, glow highlights</span>, and seamless video enhancement, users can transform dim footage into visually rich videos. The interface is built using <span className="text-green-400 font-semibold">React + TailwindCSS</span> for a smooth and responsive experience.
  </motion.p>

  <motion.p
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ delay: 0.7, duration: 1 }}
    className="text-green-200 max-w-3xl mx-auto mb-10 leading-relaxed text-lg md:text-xl"
  >
    The backend, powered by <span className="text-green-400 font-semibold">FastAPI</span> and <span className="text-green-400 font-semibold">OpenCV + YOLO</span>, ensures fast processing and accurate object detection. Whether for security, wildlife observation, or creative media, the NightVision AI Engine brings clarity to the darkest environments.
  </motion.p>

  {/* Optional Screenshot with Neon Labels */}
  <div className="relative flex justify-center items-center">
  {/* Screenshot */}
  <img
    src={screenshot}
    alt="Website UI"
    className="rounded-xl border-2 border-green-500 shadow-[0_0_25px_rgba(0,255,0,0.6)] max-h-[600px] object-contain"
  />

  {/* Anchor positions (transparent dots on features) */}
  {/* Choose File button anchor */}
  <div id="anchor-choosefile" className="absolute top-[180px] left-1/2 w-2 h-2 bg-green-400 rounded-full"></div>

  {/* Enhance/Detect/Glow anchor */}
  <div id="anchor-enhance" className="absolute top-[250px] left-1/2 w-2 h-2 bg-green-400 rounded-full"></div>

  {/* Original Video anchor */}
  <div id="anchor-original" className="absolute top-[430px] left-[320px] w-2 h-2 bg-green-400 rounded-full"></div>

  {/* Processing text anchor */}
  <div id="anchor-processing" className="absolute bottom-[80px] left-1/2 w-2 h-2 bg-green-400 rounded-full"></div>

  {/* Processed Video anchor */}
  <div id="anchor-processed" className="absolute top-[430px] right-[320px] w-2 h-2 bg-green-400 rounded-full"></div>

  {/* Labels + lines */}
  {/* Choose File */}
  <div className="absolute -top-10 left-1/2 -translate-x-1/2 text-green-400 font-bold flex flex-col items-center">
    📂 Choose File
    <div className="w-0 h-[60px] border-l-2 border-green-400"></div>
  </div>

  {/* Enhance/Detect/Glow */}
  <div className="absolute top-[250px] -left-56 text-green-400 font-bold flex items-center">
    ✨ Enhance / Detect / Glow
    <div className="ml-2 w-[220px] border-t-2 border-green-400"></div>
  </div>

  {/* Original Video */}
  <div className="absolute bottom-[160px] -left-56 text-green-400 font-bold flex items-center">
    🎥 Original Video
    <div className="ml-2 w-[220px] border-t-2 border-green-400"></div>
  </div>

  {/* Processing Feature */}
  <div className="absolute -bottom-14 left-1/2 -translate-x-1/2 text-green-400 font-bold flex flex-col items-center">
    ⚙️ Processing Feature
    <div className="w-0 h-[60px] border-l-2 border-green-400"></div>
  </div>

  {/* Processed Video */}
  <div className="absolute bottom-[160px] -right-64 text-green-400 font-bold flex flex-col items-start w-56">
    🪄 Processed Video 
    <span className="text-sm text-gray-300">(Auto-downloads to local storage)</span>
    <div className="w-[220px] border-t-2 border-green-400 mt-1"></div>
  </div>
</div>
</section>

      </div>
    </div>
  );
}

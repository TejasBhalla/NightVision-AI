import { motion } from "framer-motion";
import UploadForm from "./components/UploadForm";
import VideoPlayer from "./components/VideoPlayer";

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
      <div className="relative z-10 flex flex-col items-center p-10">
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
        <section className="mt-20 max-w-6xl text-center">
          <motion.h2
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1 }}
            className="text-3xl md:text-4xl font-bold text-green-400 mb-6 drop-shadow-[0_0_8px_rgba(0,255,0,0.6)]"
          >
            🔍 About the Website
          </motion.h2>

          <p className="text-green-200 max-w-3xl mx-auto mb-10">
            This section explains the components of the NightVision AI Engine
            interface and the technologies behind them.
          </p>

          {/* Website Screenshot with Labels */}
          <div className="relative flex justify-center">
            <img
              src="/website-screenshot.png" // replace with your screenshot
              alt="Website UI"
              className="rounded-xl border-2 border-green-500 shadow-[0_0_20px_rgba(0,255,0,0.6)] max-h-[500px] object-contain"
            />

            {/* Labels for UI parts */}
            <span className="absolute top-10 left-5 bg-green-900/80 px-3 py-1 rounded-lg text-sm border border-green-500">
              📂 Choose File Button <br /> (React + Tailwind for UI)
            </span>

            <span className="absolute top-24 right-5 bg-green-900/80 px-3 py-1 rounded-lg text-sm border border-green-500">
              ⏳ Upload & Processing <br /> (Zustand manages state + Axios API call)
            </span>

            <span className="absolute bottom-20 left-10 bg-green-900/80 px-3 py-1 rounded-lg text-sm border border-green-500">
              🎥 Original Video <br /> (Rendered with native HTML5 Video)
            </span>

            <span className="absolute bottom-20 right-10 bg-green-900/80 px-3 py-1 rounded-lg text-sm border border-green-500">
              ✨ Processed Video <br /> (Generated via FastAPI + OpenCV + YOLO)
            </span>
          </div>
        </section>
      </div>
    </div>
  );
}

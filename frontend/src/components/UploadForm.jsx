import { useVideoStore } from "../store/videoStore";
import { useState } from "react";
import { motion } from "framer-motion";
import { Car } from "lucide-react";

export default function UploadForm() {
  const { setVideoFile, processVideo, isProcessing } = useVideoStore();
  const [options, setOptions] = useState({
    enhance: true,
    detect: true,
    glow: true,
  });

  const handleFileChange = (e) => {
    setVideoFile(e.target.files[0]);
  };

  const handleProcess = () => {
    processVideo(options);
  };

  return (
    <div className="flex flex-col items-center gap-4 p-6 border rounded-xl shadow-md bg-gray-900 text-white">
      <input
        type="file"
        accept="video/*"
        onChange={handleFileChange}
        className="p-2 border rounded bg-gray-800"
      />

      {/* Toggle Options */}
      <div className="flex gap-4 text-sm">
        <label>
          <input
            type="checkbox"
            checked={options.enhance}
            onChange={() =>
              setOptions({ ...options, enhance: !options.enhance })
            }
          />{" "}
          Enhance
        </label>
        <label>
          <input
            type="checkbox"
            checked={options.detect}
            onChange={() =>
              setOptions({ ...options, detect: !options.detect })
            }
          />{" "}
          Detect
        </label>
        <label>
          <input
            type="checkbox"
            checked={options.glow}
            onChange={() => setOptions({ ...options, glow: !options.glow })}
          />{" "}
          Glow
        </label>
      </div>

      {/* Process Button with Car Animation */}
      <button
        onClick={handleProcess}
        disabled={isProcessing}
        className="relative overflow-hidden w-48 h-12 bg-green-600 rounded hover:bg-green-700 disabled:bg-gray-600 flex items-center justify-center"
      >
        {isProcessing ? (
          <motion.div
            className="absolute left-0"
            initial={{ x: 0 }}
            animate={{ x: 160 }} 
            transition={{
              repeat: Infinity,
              repeatType: "loop",
              duration: 1,
              ease: "linear",
            }}
          >
            <Car className="w-6 h-6 text-white" />
          </motion.div>
        ) : (
          "Process Video"
        )}
      </button>
    </div>
  );
}

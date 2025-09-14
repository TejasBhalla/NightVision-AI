import { useVideoStore } from "../store/videoStore";
import { useState, useEffect } from "react";

export default function VideoPlayer() {
  const { videoFile, processedVideoUrl, isProcessing } = useVideoStore();
  const [downloaded, setDownloaded] = useState(false);

  useEffect(() => {
    if (processedVideoUrl) {
      setDownloaded(true);
      const timer = setTimeout(() => setDownloaded(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [processedVideoUrl]);

  if (!videoFile) return null;

  const originalUrl = URL.createObjectURL(videoFile);

  const videoWidth = 800;
  const videoHeight = 500;

  return (
    <div className="flex flex-col items-center gap-6 w-full mt-6">
      {/* Original Video */}
      <h2 className="text-green-300 mb-2 text-lg font-semibold">🎥 Original</h2>
      <div
        className="flex items-center justify-center rounded-xl border border-green-500"
        style={{
          width: `${videoWidth}px`,
          height: `${videoHeight}px`,
          backgroundColor: "black",
        }}
      >
        <video
          src={originalUrl}
          controls
          style={{
            width: "100%",
            height: "100%",
            objectFit: "contain",
            borderRadius: "12px",
          }}
        />
      </div>

      {/* Processed Video */}
      {isProcessing && <p className="text-yellow-300 animate-pulse mt-4">Processing video…⏳</p>}

      {processedVideoUrl && (
        <>
          <h2 className="text-green-300 mt-4 mb-2 text-lg font-semibold">✨ Processed</h2>
          <div
            className="flex items-center justify-center rounded-xl border border-green-500"
            style={{
              width: `${videoWidth}px`,
              height: `${videoHeight}px`,
              backgroundColor: "black",
            }}
          >
            <video
              src={processedVideoUrl}
              controls
              style={{
                width: "100%",
                height: "100%",
                objectFit: "contain",
                borderRadius: "12px",
              }}
            />
          </div>
          {downloaded && (
            <p className="text-blue-400 mt-2 font-medium animate-pulse">
              ✅ Video downloaded
            </p>
          )}
        </>
      )}
    </div>
  );
}

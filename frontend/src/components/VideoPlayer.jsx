import { useVideoStore } from "../store/videoStore";

export default function VideoPlayer() {
  const { videoFile, processedVideoUrl } = useVideoStore();

  if (!videoFile && !processedVideoUrl) return null;

  const originalUrl = videoFile ? URL.createObjectURL(videoFile) : null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
      {/* Original Video */}
      {originalUrl && (
        <div className="flex flex-col items-center">
          <h2 className="text-green-300 mb-2">🎥 Original</h2>
          <video
            src={originalUrl}
            controls
            className="rounded-xl border border-green-500 shadow-[0_0_20px_rgba(0,255,0,0.4)]"
          />
        </div>
      )}

      {/* Processed Video */}
      {processedVideoUrl && (
        <div className="flex flex-col items-center">
          <h2 className="text-green-300 mb-2">✨ Processed</h2>
          <video
            src={processedVideoUrl}
            controls
            className="rounded-xl border border-green-500 shadow-[0_0_20px_rgba(0,255,0,0.8)]"
          />
        </div>
      )}
    </div>
  );
}

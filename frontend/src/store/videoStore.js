import { create } from "zustand";
import axios from "axios";

export const useVideoStore = create((set, get) => ({
  videoFile: null,
  processedVideoUrl: null,
  isProcessing: false,

  setVideoFile: (file) => set({ videoFile: file }),
  setProcessedVideoUrl: (url) => set({ processedVideoUrl: url }),
  setIsProcessing: (status) => set({ isProcessing: status }),

  processVideo: async (options = { enhance: true, detect: true, glow: true }) => {
    const { videoFile } = get();
    if (!videoFile) return;

    set({ isProcessing: true });

    const formData = new FormData();
    formData.append("video", videoFile);
    formData.append("enhance", options.enhance.toString());
    formData.append("detect", options.detect.toString());
    formData.append("glow", options.glow.toString());

    try {
      const response = await axios.post("http://localhost:8080/api/process/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        responseType: "arraybuffer",
      });

      const videoBlob = new Blob([response.data], { type: "video/mp4" });
      const url = URL.createObjectURL(videoBlob);

      set({ processedVideoUrl: url });
    } catch (error) {
      console.error("Processing failed:", error);
    } finally {
      set({ isProcessing: false });
    }
  },
}));

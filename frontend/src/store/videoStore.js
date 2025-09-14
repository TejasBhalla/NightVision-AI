import { create } from "zustand";
import axios from "axios";

export const useVideoStore = create((set, get) => ({
  videoFile: null,
  isProcessing: false,

  // Setters
  setVideoFile: (file) => set({ videoFile: file }),
  setIsProcessing: (status) => set({ isProcessing: status }),

  // Process and download video
  processVideo: async (options = { enhance: true, detect: true, glow: true }) => {
    const { videoFile } = get();
    if (!videoFile) return;

    set({ isProcessing: true });

    const formData = new FormData();
    formData.append("video", videoFile); // must match backend multer key
    formData.append("enhance", options.enhance.toString());
    formData.append("detect", options.detect.toString());
    formData.append("glow", options.glow.toString());

    try {
      const response = await axios.post(
        "http://localhost:8080/api/process/upload",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
          responseType: "arraybuffer", // receive binary video
        }
      );

      // Convert response to Blob and trigger download
      const blob = new Blob([response.data], { type: "video/mp4" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `processed_${videoFile.name}`; // download name
      document.body.appendChild(link);
      link.click();
      link.remove();

      alert("✅ Video processed and ready for download!");
    } catch (error) {
      console.error("Processing failed:", error);
      alert("❌ Video processing failed. Check backend logs.");
    } finally {
      set({ isProcessing: false });
    }
  },
}));

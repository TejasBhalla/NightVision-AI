import fs from "fs";
import path from "path";
import { sendToAI } from "../services/aiClient.js";
import { logger } from "../utils/logger.js";

export async function uploadAndProcess(req, res) {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "video file is required" });
    }

    const videoPath = req.file.path;

    // Process via Python AI
    const outPath = await sendToAI(videoPath, {
      enhance: true,
      detect: true,
      glow: true,
    });

    if (!fs.existsSync(outPath)) {
      return res.status(500).json({ error: "processed file not found" });
    }

    // ✅ Send file as download
    res.setHeader("Content-Type", "video/mp4");
    res.setHeader(
      "Content-Disposition",
      `attachment; filename="processed_${req.file.originalname}"`
    );

    const fileStream = fs.createReadStream(outPath);
    fileStream.pipe(res);

    fileStream.on("end", () => {
      logger.info(`✅ Processed video sent for download: ${outPath}`);
    });

    fileStream.on("error", (err) => {
      console.error("❌ File stream error:", err);
      res.status(500).json({ error: "Failed to send file", details: err.message });
    });
  } catch (err) {
    console.error("❌ Processing failed:", err);
    return res.status(500).json({ error: "processing failed", details: err.message });
  }
}

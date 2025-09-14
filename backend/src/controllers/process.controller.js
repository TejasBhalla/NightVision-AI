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

    const stat = fs.statSync(outPath);
    const fileSize = stat.size;
    const range = req.headers.range;

    res.setHeader("Content-Type", "video/mp4");

    // ✅ Handle streaming with range requests
    if (range) {
      const parts = range.replace(/bytes=/, "").split("-");
      const start = parseInt(parts[0], 10);
      const end = parts[1] ? parseInt(parts[1], 10) : fileSize - 1;

      const chunkSize = end - start + 1;
      const file = fs.createReadStream(outPath, { start, end });

      res.writeHead(206, {
        "Content-Range": `bytes ${start}-${end}/${fileSize}`,
        "Accept-Ranges": "bytes",
        "Content-Length": chunkSize,
        "Content-Type": "video/mp4",
      });

      file.pipe(res);
    } else {
      res.writeHead(200, {
        "Content-Length": fileSize,
        "Content-Type": "video/mp4",
      });
      fs.createReadStream(outPath).pipe(res);
    }

    logger.info(`✅ Sent processed video: ${outPath}`);
  } catch (err) {
    console.error("❌ Processing failed:", err);
    return res.status(500).json({ error: "processing failed", details: err.message });
  }
}

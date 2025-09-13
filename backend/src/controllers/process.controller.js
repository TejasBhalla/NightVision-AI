import fs from 'fs';
import path from 'path';
import { sendToAI } from '../services/aiClient.js';
import { logger } from '../utils/logger.js';

export async function uploadAndProcess(req, res) {
  try {
    if (!req.file) return res.status(400).json({ error: 'video file is required' });
    const videoPath = req.file.path;

    // Stream AI engine response back to client
    const aiStream = await sendToAI(videoPath, { enhance: true, detect: true, glow: true });

    res.setHeader('Content-Type', 'video/mp4');
    const outPath = path.join(path.dirname(videoPath), `processed_${path.basename(videoPath, path.extname(videoPath))}.mp4`);
    const write = fs.createWriteStream(outPath);

    aiStream.pipe(write);
    aiStream.pipe(res);

    write.on('finish', () => {
      logger.info('Saved processed file to', outPath);
      // Optional: clean up original after processing
      // fs.unlink(videoPath, () => {});
    });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: 'processing failed', details: err.message });
  }
}
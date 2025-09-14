import axios from 'axios';
import fs from 'fs';
import path from 'path';
import os from 'os';
import FormData from 'form-data';

export async function sendToAI(videoPath, options = {}) {
  const form = new FormData();
  form.append('file', fs.createReadStream(videoPath)); // must match FastAPI field name
  form.append('enhance', String(options.enhance ?? true));
  form.append('detect', String(options.detect ?? true));
  form.append('glow', String(options.glow ?? true));

  const resp = await axios.post('http://127.0.0.1:8000/process', form, {
    responseType: 'stream',
    headers: form.getHeaders(),
    maxBodyLength: Infinity,
    maxContentLength: Infinity,
  });

  // Save the streamed response to a temp file
  const outPath = path.join(os.tmpdir(), `processed_${Date.now()}.mp4`);
  const writer = fs.createWriteStream(outPath);

  await new Promise((resolve, reject) => {
    resp.data.pipe(writer);
    let error = null;
    writer.on('error', (err) => {
      error = err;
      writer.close();
      reject(err);
    });
    writer.on('close', () => {
      if (!error) resolve(true);
    });
  });

  return outPath; // return the path to Node backend
}

import axios from 'axios';
import fs from 'fs';
import FormData from 'form-data';

export async function sendToAI(videoPath, options = {}) {
  const form = new FormData();

  // FastAPI expects field name 'file', but in Node we called it 'video'
  form.append('file', fs.createReadStream(videoPath));  // map video -> file

  form.append('enhance', String(options.enhance ?? true));
  form.append('detect', String(options.detect ?? true));
  form.append('glow', String(options.glow ?? true));

  const resp = await axios.post('http://127.0.0.1:8000/process', form, {
    responseType: 'stream',
    headers: form.getHeaders(),
    maxBodyLength: Infinity,
    maxContentLength: Infinity,
  });

  return resp.data; // Readable stream
}

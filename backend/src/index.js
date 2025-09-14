import express from 'express';
import cors from 'cors';
import morgan from 'morgan';
import dotenv from 'dotenv';
import processRouter from './routes/process.route.js';
import { logger } from './utils/logger.js';

dotenv.config();

const app = express();
app.use(cors({
  origin: "http://localhost:5173", // frontend
  methods: ["GET", "POST"],
  allowedHeaders: ["Content-Type", "Authorization"]
}));
app.use(express.json({ limit: '5gb' }));
app.use(morgan('dev'));

app.get('/health', (req, res) => res.json({ ok: true }));
app.use('/api/process', processRouter);

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => logger.info(`Node backend running on :${PORT}`));
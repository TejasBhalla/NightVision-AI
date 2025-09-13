import { Router } from 'express';
import { upload } from '../middleware/upload.js';
import { uploadAndProcess } from '../controllers/process.controller.js';

const router = Router();

router.post('/upload', upload.single('video'), uploadAndProcess);

export default router;
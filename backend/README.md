md
# Night Vision Driving AI — Node Backend

## Run
cp .env.example .env
npm install
npm run dev

## API
POST /api/process/upload (multipart/form-data)
- field: video (file)
- returns: processed MP4 stream
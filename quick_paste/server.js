const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const cors = require('cors');

const app = express();
const PORT = 8000;

// Enable CORS
app.use(cors());
// Increase JSON limit for base64 images (50MB should be plenty)
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));

// Serve static files from src directory
app.use(express.static('src'));

// Ensure directories exist (data folder is at root, one level up)
const dataDir = path.join(__dirname, '..', 'data');
const toBeScannedDir = path.join(dataDir, 'to-be-scanned');
const alreadyScannedDir = path.join(dataDir, 'already-scanned');

[dataDir, toBeScannedDir, alreadyScannedDir].forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
});

// Configure multer for image uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, toBeScannedDir);
    },
    filename: function (req, file, cb) {
        const timestamp = Date.now();
        cb(null, `screenshot-${timestamp}.png`);
    }
});

const upload = multer({ 
    storage: storage,
    limits: { fileSize: 10 * 1024 * 1024 } // 10MB limit
});

// Upload endpoint
app.post('/api/upload', upload.single('image'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No image provided' });
    }
    
    res.json({ 
        success: true, 
        filename: req.file.filename,
        path: req.file.path 
    });
});

// Upload base64 image
app.post('/api/upload-base64', (req, res) => {
    const { imageData, filename } = req.body;
    
    if (!imageData) {
        return res.status(400).json({ error: 'No image data provided' });
    }
    
    // Remove data:image/png;base64, prefix
    const base64Data = imageData.replace(/^data:image\/\w+;base64,/, '');
    const buffer = Buffer.from(base64Data, 'base64');
    
    const finalFilename = filename || `screenshot-${Date.now()}.png`;
    const filepath = path.join(toBeScannedDir, finalFilename);
    
    fs.writeFile(filepath, buffer, (err) => {
        if (err) {
            console.error('Error saving file:', err);
            return res.status(500).json({ error: 'Failed to save image' });
        }
        
        res.json({ 
            success: true, 
            filename: finalFilename,
            path: filepath 
        });
    });
});

// List images
app.get('/api/images/:folder', (req, res) => {
    const folder = req.params.folder === 'scanned' ? alreadyScannedDir : toBeScannedDir;
    
    fs.readdir(folder, (err, files) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to list files' });
        }
        
        const images = files
            .filter(file => /\.(png|jpg|jpeg|gif|webp)$/i.test(file))
            .map(file => ({
                filename: file,
                path: path.join(folder, file),
                url: `/images/${req.params.folder}/${file}`
            }));
            
        res.json(images);
    });
});

// Move image from to-be-scanned to already-scanned
app.post('/api/move/:filename', (req, res) => {
    const filename = req.params.filename;
    const sourcePath = path.join(toBeScannedDir, filename);
    const destPath = path.join(alreadyScannedDir, filename);
    
    fs.rename(sourcePath, destPath, (err) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to move file' });
        }
        res.json({ success: true });
    });
});

// Delete image
app.delete('/api/images/:folder/:filename', (req, res) => {
    const folder = req.params.folder === 'scanned' ? alreadyScannedDir : toBeScannedDir;
    const filepath = path.join(folder, req.params.filename);
    
    fs.unlink(filepath, (err) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to delete file' });
        }
        res.json({ success: true });
    });
});

// Serve images
app.get('/images/to-be-scanned/:filename', (req, res) => {
    res.sendFile(path.join(toBeScannedDir, req.params.filename));
});

app.get('/images/scanned/:filename', (req, res) => {
    res.sendFile(path.join(alreadyScannedDir, req.params.filename));
});

app.listen(PORT, () => {
    console.log(`
╔══════════════════════════════════════════════════════════╗
║       QuickPaste Debug Interface - Node.js Server       ║
╚══════════════════════════════════════════════════════════╝

Server running at: http://localhost:${PORT}/

✅ Works with ALL browsers (including Brave!)
✅ No File System API needed
✅ Images save directly to disk

Open in your browser: http://localhost:${PORT}/

Press Ctrl+C to stop the server
    `);
});
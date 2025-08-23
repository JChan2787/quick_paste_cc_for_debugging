# QuickPaste Debug Interface

A lightweight, browser-based tool for quickly capturing and managing screenshots during debugging sessions. Paste images directly from your clipboard and have them automatically saved to disk for reference.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## Features

- **Quick Paste**: Paste screenshots with `Ctrl+V` or click the paste button
- **Drag & Drop**: Drop image files directly onto the browser window
- **Auto-Save**: Images automatically save to local disk storage
- **Visual Grid**: Clean, responsive grid layout for viewing pasted images
- **Cross-Browser**: Works with all modern browsers (Chrome, Firefox, Edge, Brave, Safari)
- **No Cloud Dependencies**: Completely local - your images never leave your machine
- **Platform Agnostic**: Works on Windows, macOS, and Linux
- **MCP Integration**: Model Context Protocol support for AI assistant workflows

## Quick Start

### Prerequisites

- Node.js (v14 or higher) - [Download](https://nodejs.org/)
- npm (comes with Node.js)
- Python 3.8+ (for MCP integration)

### Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd image-uploader-tool
```

2. Install dependencies:
```bash
cd quick_paste
npm install
cd ..
```

3. (Optional) Install MCP dependencies:
```bash
cd quick_paste-mcp
pip install -r requirements.txt
cd ..
```

### Running the Tool

#### Windows
Double-click `start.bat` or run:
```bash
start.bat
```

#### macOS/Linux
```bash
chmod +x start.sh  # First time only
./start.sh
```

The tool will:
1. Start a local server on port 8000
2. Open your default browser automatically
3. Create necessary directories (`data/to-be-scanned/`)

## Usage

### Pasting Images

1. Take a screenshot using your OS screenshot tool:
   - Windows: `Win + Shift + S`
   - macOS: `Cmd + Shift + 4`
   - Linux: `Print Screen` or screenshot tool

2. In the QuickPaste interface:
   - Click the "Paste Image" button, OR
   - Press `Ctrl+V` (or `Cmd+V` on macOS)

3. Your image appears in the grid and is automatically saved to `data/to-be-scanned/`

### Managing Images

- **Clear Display**: Removes images from the visual grid but keeps files on disk
- **View Files**: Check the `data/to-be-scanned/` folder for saved images

### File Organization

```
image-uploader-tool/
├── data/
│   ├── to-be-scanned/     # New screenshots saved here
│   └── already-scanned/   # Processed images (manually moved)
├── quick_paste/
│   ├── src/
│   │   └── index.html     # Main application file
│   ├── server.js          # Node.js backend server
│   ├── package.json       # Project dependencies
│   ├── start.bat          # Windows launcher (internal)
│   ├── start.sh           # Unix/macOS launcher (internal)
│   └── node_modules/      # Dependencies (auto-generated)
├── quick_paste-mcp/       # MCP integration
│   ├── src/
│   │   └── server.py      # MCP server implementation
│   ├── requirements.txt   # Python dependencies
│   ├── run_server.py      # MCP server runner
│   └── SETUP.md          # MCP setup instructions
├── start.bat              # Windows launcher (root)
├── start.sh               # Unix/macOS launcher (root)
├── README.md              # This file
├── LICENSE                # MIT License
└── .gitignore             # Git ignore rules
```

## Configuration

### Changing the Port

If port 8000 is already in use, edit these files:

1. In `quick_paste/server.js`:
```javascript
const PORT = 8000;  // Change to your preferred port
```

2. In `quick_paste/start.bat` (Windows):
```batch
rundll32 url.dll,FileProtocolHandler http://localhost:8000/
```

3. In `quick_paste/start.sh` (Unix/macOS):
```bash
URL="http://localhost:8000/"
```

### Image Storage

Images are saved with timestamp-based filenames:
- Format: `screenshot-{timestamp}.png`
- Location: `data/to-be-scanned/`

## Technical Details

### Architecture

- **Backend**: Node.js with Express
- **File Handling**: Multer for multipart uploads
- **Frontend**: Vanilla JavaScript with modern CSS
- **Storage**: Local file system (no database required)

### Browser Compatibility

| Browser | Supported | Notes |
|---------|-----------|-------|
| Chrome | ✅ | Full support |
| Firefox | ✅ | Full support |
| Edge | ✅ | Full support |
| Brave | ✅ | Full support |
| Safari | ✅ | Full support |

### Security

- Runs entirely on localhost
- No external network requests
- No telemetry or analytics
- Images never leave your machine
- CORS configured for local access only

## Troubleshooting

### Server won't start

- **Port in use**: Another application is using port 8000. Change the port number in configuration.
- **Node.js not installed**: Install Node.js from [nodejs.org](https://nodejs.org/)

### Can't paste images

- **Browser permissions**: Ensure your browser has clipboard access permissions
- **Image format**: Tool supports PNG, JPG, GIF, and WebP formats
- **File size**: Maximum image size is 50MB

### Images not saving

- **Directory permissions**: Ensure the tool has write permissions in its directory
- **Disk space**: Check available disk space
- **Server running**: Confirm the Node.js server is running (check terminal/console)

## Development

### Project Structure

```javascript
// Key endpoints
POST /api/upload-base64  // Handles pasted images
GET /api/images/:folder  // Lists saved images
DELETE /api/images/:folder/:filename  // (Reserved)
```

### Extending the Tool

The codebase is intentionally simple and hackable:

- `quick_paste/src/index.html` - All frontend code in one file
- `quick_paste/server.js` - Straightforward Express server
- No build process required
- No complex dependencies

## MCP Integration (Model Context Protocol)

The QuickPaste tool now includes MCP support for seamless integration with AI assistants like Claude. This allows AI assistants to automatically analyze screenshots for UI issues, bugs, and other observations.

### MCP Features

- **Automatic Screenshot Discovery**: AI assistants can query for unprocessed screenshots
- **Batch Analysis**: Process multiple screenshots in a single session
- **Organized Workflow**: Screenshots automatically move from `to-be-scanned` to `already-scanned` after analysis
- **Resource-based Access**: Clean API through MCP resources

### Setting Up MCP

**Step 1: Install MCP Server Dependencies**

```bash
cd quick_paste-mcp
pip install -r requirements.txt
```

**Step 2: Configure Claude Desktop** (or other MCP-compatible clients):

Add to your Claude configuration file:

```json
{
  "mcpServers": {
    "QuickPaste-MCP": {
      "command": "python",
      "args": ["/path/to/quick_paste-mcp/run_server.py"]
    }
  }
}
```

**Step 3: Run the MCP Server**

```bash
cd quick_paste-mcp
python run_server.py
```

### Using MCP with AI Assistants

Once configured, AI assistants can:

- Access screenshots via `@QuickPaste-MCP` mention
- Query `quickpaste://screenshots/to-be-scanned` for new screenshots
- Query `quickpaste://screenshots/already-scanned` for processed screenshots
- Automatically analyze UI issues and move files after processing

Example workflow:

1. Paste screenshots into QuickPaste web interface
2. Ask your AI assistant: "Check @QuickPaste-MCP for new screenshots"
3. AI analyzes images and provides feedback on UI issues
4. Screenshots automatically move to `already-scanned` folder

**Pro Tip**: For best results with Claude Code, use a direct prompt like:
> "I uploaded more screenshots. Use the QuickPaste MCP to look at them."

This ensures Claude Code properly invokes the MCP tool rather than attempting direct file access.

## Contributing

Feel free to fork and modify this tool for your needs. Some ideas for enhancement:

- Add image annotation capabilities
- Implement categories or tags
- Add image compression options
- Create keyboard shortcuts for common actions
- Add export functionality

## License

MIT License - See LICENSE file for details

---

**Note**: This tool was created for local development and debugging purposes. It is not intended for production deployment or public-facing use.

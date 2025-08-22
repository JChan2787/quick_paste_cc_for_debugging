# QuickPaste MCP Setup Guide for Claude Code

This guide will help you set up the QuickPaste MCP (Model Context Protocol) server to allow AI assistants to analyze your screenshots in Claude Code.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Claude Code (Anthropic's CLI)

## Installation Steps

### 1. Set Up Python Environment (Optional but Recommended)

If you have a preferred Python environment manager (conda, uv, venv), activate it first. Otherwise, you can install globally.

#### Using venv:
```bash
cd quick_paste-mcp
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Using conda:
```bash
conda create -n quickpaste python=3.10
conda activate quickpaste
```

### 2. Install Dependencies

```bash
cd quick_paste-mcp
pip install -r requirements.txt
```

### 3. Test the Server

Test that the server runs correctly:

```bash
python run_server.py
```

You should see output like:
```
Starting QuickPaste MCP Server
Data directory: C:\...\image-uploader-tool\data
```

Press `Ctrl+C` to stop the test.

### 4. Configure Claude Code

You need to add the MCP server to your Claude Code configuration file.

#### Finding Your Config File

**Windows**: `C:\Users\[YourUsername]\.claude.json`
**macOS/Linux**: `~/.claude.json`

#### Configuration Steps

1. Open your `.claude.json` file in a text editor

2. Find your project directory in the configuration. Look for something like:
```json
"C:\\Path\\To\\Your\\Project": {
```

3. In the `mcpServers` section of your project, add:

```json
"QuickPaste-MCP": {
  "type": "stdio",
  "command": "python",
  "args": [
    "C:/Full/Path/To/image-uploader-tool/quick_paste-mcp/run_server.py"
  ],
  "env": {}
}
```

**Important**: Replace `C:/Full/Path/To/` with the actual absolute path to your image-uploader-tool directory.

#### ⚠️ CRITICAL FOR VIRTUAL ENVIRONMENT USERS ⚠️

If you're using conda, venv, uv, or any Python virtual environment, you **MUST** use the FULL PATH to your environment's Python executable!

**Why?** Claude Code runs in a clean environment and has NO IDEA about your:
- Activated conda/venv environments  
- PATH modifications
- Shell configurations

##### For conda users:
```json
"QuickPaste-MCP": {
  "type": "stdio",
  "command": "C:/Users/YourName/miniconda3/envs/your-env-name/python.exe",
  "args": [
    "C:/Full/Path/To/image-uploader-tool/quick_paste-mcp/run_server.py"
  ],
  "env": {}
}
```

To find your conda Python path:
1. Activate your environment: `conda activate your-env-name`
2. Run: `where python` (Windows) or `which python` (macOS/Linux)  
3. Copy that EXACT path into the "command" field

##### For venv users:
```json
"QuickPaste-MCP": {
  "type": "stdio",
  "command": "C:/Full/Path/To/image-uploader-tool/quick_paste-mcp/venv/Scripts/python.exe",
  "args": [
    "C:/Full/Path/To/image-uploader-tool/quick_paste-mcp/run_server.py"
  ],
  "env": {}
}
```

#### Example Complete Entry:

```json
"C:\\Users\\YourName\\Documents\\Projects": {
  "allowedTools": [],
  "mcpServers": {
    "QuickPaste-MCP": {
      "type": "stdio",
      "command": "python",
      "args": [
        "C:/Users/YourName/Documents/Projects/image-uploader-tool/quick_paste-mcp/run_server.py"
      ],
      "env": {}
    }
  }
}
```

### 5. Restart Claude Code

After saving the configuration file, you may need to restart your Claude Code session for the changes to take effect. Start a new chat or reload your current project.

## Usage

Once configured, you can ask Claude to analyze your screenshots:

```
"Hey, check the screenshots I just took. The UI looks broken."
```

Claude will:
1. Access the `quickpaste://screenshots/to-be-scanned` resource
2. View and analyze each screenshot
3. Describe any UI issues found
4. Move the analyzed screenshots to the `already-scanned` folder

## Available Resources

The MCP server provides these resources:

- `quickpaste://screenshots/to-be-scanned` - Screenshots waiting for analysis
- `quickpaste://screenshots/already-scanned` - Previously analyzed screenshots  
- `quickpaste://info` - Server configuration information

## Troubleshooting

### Server doesn't appear in Claude

1. Check that the path in `.claude.json` is absolute and correct
2. Ensure Python is in your PATH or use the full path to python.exe
3. Check the Claude logs for errors

### Import errors

Make sure you've installed the dependencies:
```bash
pip install -r requirements.txt
```

### Permission errors

Ensure the MCP server has read/write access to the `data` directory.

## Logs

The MCP server creates a log file `quickpaste_mcp.log` in the `quick_paste-mcp` directory for debugging.
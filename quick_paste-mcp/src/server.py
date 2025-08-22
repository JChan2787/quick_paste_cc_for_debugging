#!/usr/bin/env python3
"""
QuickPaste MCP Server - FastMCP Implementation
Provides access to screenshot folders for AI assistants to analyze UI issues.
"""

import asyncio
import logging
import sys
import io
import json
import platform
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Fix Windows Unicode issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quickpaste_mcp.log'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("QuickPaste-MCP")

# Get the data directories (relative to the quick_paste-mcp folder)
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
TO_BE_SCANNED_DIR = DATA_DIR / "to-be-scanned"
ALREADY_SCANNED_DIR = DATA_DIR / "already-scanned"

def get_move_instructions() -> str:
    """
    Generate platform-specific move instructions for screenshots.
    """
    source = str(TO_BE_SCANNED_DIR.absolute())
    dest = str(ALREADY_SCANNED_DIR.absolute())
    
    system = platform.system()
    
    if system == "Windows":
        # For Windows, provide PowerShell command with proper escaping
        # Using forward slashes which PowerShell accepts
        source_clean = source.replace('\\', '/')
        dest_clean = dest.replace('\\', '/')
        return (
            "After analyzing all screenshots, please move them to the already-scanned folder. "
            f"On Windows, use PowerShell: Move-Item '{source_clean}/*.png' '{dest_clean}/' "
            "Or use individual file moves if wildcards don't work."
        )
    elif system == "Darwin":  # macOS
        return (
            "After analyzing all screenshots, please move them to the already-scanned folder. "
            f"On macOS, use: mv \"{source}\"/*.png \"{dest}/\""
        )
    else:  # Linux and others
        return (
            "After analyzing all screenshots, please move them to the already-scanned folder. "
            f"On Linux, use: mv \"{source}\"/*.png \"{dest}/\""
        )

@mcp.resource("quickpaste://screenshots/to-be-scanned")
async def get_unscanned_screenshots() -> str:
    """
    Returns a list of screenshots waiting to be analyzed.
    Includes instructions for the AI assistant to analyze and move them.
    """
    try:
        # Ensure directory exists
        if not TO_BE_SCANNED_DIR.exists():
            TO_BE_SCANNED_DIR.mkdir(parents=True, exist_ok=True)
            return json.dumps({
                "screenshots": [],
                "message": "No screenshots found in to-be-scanned folder.",
                "instructions": None
            }, indent=2)
        
        # Get all image files
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
        screenshots = []
        
        for file in TO_BE_SCANNED_DIR.iterdir():
            if file.is_file() and file.suffix.lower() in image_extensions:
                screenshots.append({
                    "filename": file.name,
                    "path": str(file.absolute()),
                    "size": file.stat().st_size,
                    "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                })
        
        if not screenshots:
            return json.dumps({
                "screenshots": [],
                "message": "No screenshots found in to-be-scanned folder.",
                "instructions": None
            }, indent=2)
        
        # Build response with instructions
        response = {
            "screenshots": screenshots,
            "count": len(screenshots),
            "to_be_scanned_path": str(TO_BE_SCANNED_DIR.absolute()),
            "already_scanned_path": str(ALREADY_SCANNED_DIR.absolute()),
            "analysis_instructions": (
                f"Please analyze these {len(screenshots)} screenshot(s) for UI issues, bugs, or other observations. "
                "Use the Read tool to view each image file, then describe what you see. "
                "Focus on any visual problems, layout issues, or unexpected behavior."
            ),
            "post_analysis_instructions": get_move_instructions()
        }
        
        return json.dumps(response, indent=2)
        
    except Exception as e:
        logger.error(f"Error getting unscanned screenshots: {e}")
        return json.dumps({
            "error": str(e),
            "screenshots": []
        }, indent=2)

@mcp.resource("quickpaste://screenshots/already-scanned")
async def get_scanned_screenshots() -> str:
    """
    Returns a list of screenshots that have already been analyzed.
    """
    try:
        # Ensure directory exists
        if not ALREADY_SCANNED_DIR.exists():
            ALREADY_SCANNED_DIR.mkdir(parents=True, exist_ok=True)
            return json.dumps({
                "screenshots": [],
                "message": "No screenshots in already-scanned folder."
            }, indent=2)
        
        # Get all image files
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
        screenshots = []
        
        for file in ALREADY_SCANNED_DIR.iterdir():
            if file.is_file() and file.suffix.lower() in image_extensions:
                screenshots.append({
                    "filename": file.name,
                    "path": str(file.absolute()),
                    "size": file.stat().st_size,
                    "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                })
        
        response = {
            "screenshots": screenshots,
            "count": len(screenshots),
            "already_scanned_path": str(ALREADY_SCANNED_DIR.absolute()),
            "message": f"Found {len(screenshots)} previously analyzed screenshot(s)."
        }
        
        return json.dumps(response, indent=2)
        
    except Exception as e:
        logger.error(f"Error getting scanned screenshots: {e}")
        return json.dumps({
            "error": str(e),
            "screenshots": []
        }, indent=2)

@mcp.resource("quickpaste://info")
async def get_server_info() -> str:
    """
    Returns information about the QuickPaste MCP server and its configuration.
    """
    info = {
        "server": "QuickPaste MCP",
        "version": "1.0.0",
        "description": "Provides access to screenshot folders for UI analysis",
        "directories": {
            "base": str(BASE_DIR.absolute()),
            "data": str(DATA_DIR.absolute()),
            "to_be_scanned": str(TO_BE_SCANNED_DIR.absolute()),
            "already_scanned": str(ALREADY_SCANNED_DIR.absolute())
        },
        "resources": [
            "quickpaste://screenshots/to-be-scanned - Get screenshots waiting for analysis",
            "quickpaste://screenshots/already-scanned - Get previously analyzed screenshots",
            "quickpaste://info - Server information"
        ]
    }
    return json.dumps(info, indent=2)

def main():
    """Main entry point for the server."""
    logger.info("Starting QuickPaste MCP Server")
    logger.info(f"Data directory: {DATA_DIR.absolute()}")
    logger.info(f"To-be-scanned: {TO_BE_SCANNED_DIR.absolute()}")
    logger.info(f"Already-scanned: {ALREADY_SCANNED_DIR.absolute()}")
    
    # Ensure directories exist
    TO_BE_SCANNED_DIR.mkdir(parents=True, exist_ok=True)
    ALREADY_SCANNED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Run the FastMCP server
    mcp.run()

if __name__ == "__main__":
    main()
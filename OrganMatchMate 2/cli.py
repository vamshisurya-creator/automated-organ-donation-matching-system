#!/usr/bin/env python
"""
CLI Entry point for the Organ Donation Matching System
"""
import os
import logging
from app import app

def main():
    """Main entry point for the application"""
    logging.basicConfig(level=logging.INFO)
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    # Inform the user about the running server
    logging.info(f"Starting Organ Donation Matching System on {host}:{port}")
    logging.info("Press CTRL+C to quit")
    
    app.run(host=host, port=port)

if __name__ == '__main__':
    main()
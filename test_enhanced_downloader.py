#!/usr/bin/env python3
"""
Test script for the enhanced downloader functionality
This script tests the enhanced downloader with a simple DOI
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the PyPaperBot module to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyPaperBot.Paper import Paper
from PyPaperBot.EnhancedDownloader import EnhancedDownloader

def test_enhanced_downloader():
    """Test the enhanced downloader with a sample paper"""
    print("Testing Enhanced Downloader with PySmartDL")
    print("=" * 50)
    
    # Create a test paper object (using a known open-access paper)
    test_paper = Paper(title="Test Paper - Machine Learning Applications")
    # Set DOI after initialization
    test_paper.DOI = "10.1371/journal.pone.0001234"  # Example DOI
    
    # Override canBeDownloaded for testing
    test_paper.canBeDownloaded = lambda: True
    
    # Create temporary directory for downloads
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")
        
        # Initialize enhanced downloader
        downloader = EnhancedDownloader(enable_progress=True)
        
        # Test single paper download
        print("\nTesting single paper download...")
        success, source, file_path = downloader.download_paper_enhanced(
            test_paper, temp_dir
        )
        
        if success:
            print(f"PASS: Single download test")
            print(f"   Source: {source}")
            print(f"   File: {file_path}")
            
            # Check if file exists
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"   File size: {file_size} bytes")
            else:
                print(f"   WARNING: File not found: {file_path}")
        else:
            print("FAIL: Single download test")
        
        # Test batch download
        print("\nTesting batch paper download...")
        test_papers = [test_paper]
        
        stats = downloader.download_papers_enhanced(
            test_papers, temp_dir, num_limit=1, scholar_results=1
        )
        
        print(f"\nBatch download results:")
        print(f"   Attempted: {stats['total_attempted']}")
        print(f"   Successful: {stats['successful_downloads']}")
        print(f"   Failed: {stats['failed_downloads']}")
        
        if stats['successful_downloads'] > 0:
            print("PASS: Batch download test")
        else:
            print("FAIL: Batch download test")


def test_backward_compatibility():
    """Test backward compatibility with original downloader interface"""
    print("\nTesting Backward Compatibility")
    print("=" * 50)
    
    try:
        from PyPaperBot.Downloader import downloadPapers
        print("Successfully imported downloadPapers function")
        
        # This should work with the enhanced downloader
        test_paper = Paper(title="Test Compatibility Paper")
        test_paper.canBeDownloaded = lambda: False  # Skip actual download
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = downloadPapers([test_paper], temp_dir, 1, 1, use_enhanced=True)
            print("PASS: Backward compatibility test")
            
    except Exception as e:
        print(f"FAIL: Backward compatibility test - {e}")


if __name__ == "__main__":
    print("PyPaperBot Enhanced Downloader Test Suite")
    print("=" * 60)
    
    # Test enhanced downloader
    test_enhanced_downloader()
    
    # Test backward compatibility
    test_backward_compatibility()
    
    print("\n" + "=" * 60)
    print("Test suite completed!")
    print("\nTips for contributing:")
    print("   1. The enhanced downloader provides better user experience")
    print("   2. Progress bars show real-time download progress")
    print("   3. Resume capability for interrupted downloads")
    print("   4. Better error handling and retry mechanisms")
    print("   5. Multi-threaded downloads for improved speed")
    print("\nUsage:")
    print("   python -m PyPaperBot --query='machine learning' --scholar-pages=1 --dwn-dir='./downloads'")
    print("   python -m PyPaperBot --classic-dl --query='ai' --scholar-pages=1 --dwn-dir='./downloads'  # Use classic downloader")

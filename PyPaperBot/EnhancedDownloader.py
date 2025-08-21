#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Downloader with PySmartDL support
Improves downloading experience with progress bars, resume capability, and better error handling
"""

import os
import time
import random
from pathlib import Path
from pySmartDL import SmartDL
import requests
from .HTMLparsers import getSchiHubPDF, SciHubUrls
from .NetInfo import NetInfo


class EnhancedDownloader:
    """Enhanced downloader using PySmartDL for better downloading experience"""
    
    def __init__(self, enable_progress=True, threads=5, timeout=10):
        """
        Initialize the enhanced downloader
        
        Args:
            enable_progress (bool): Show progress bars during download
            threads (int): Number of download threads (default: 5)
            timeout (int): Connection timeout in seconds (default: 10)
        """
        self.enable_progress = enable_progress
        self.threads = threads
        self.timeout = timeout
    
    def set_scihub_url(self):
        """Find and set working SciHub URL"""
        try:
            r = requests.get(NetInfo.SciHub_URLs_repo, headers=NetInfo.HEADERS, timeout=self.timeout)
            links = SciHubUrls(r.text)
            found = False

            print("\nSearching for working Sci-Hub instance...")
            for link in links:
                try:
                    r = requests.get(link, headers=NetInfo.HEADERS, timeout=5)
                    if r.status_code == 200:
                        found = True
                        NetInfo.SciHub_URL = link
                        break
                except Exception:
                    continue
            
            if found:
                print(f"✓ Using {NetInfo.SciHub_URL} as Sci-Hub instance")
            else:
                print("⚠ No working Sci-Hub instance found!")
                print("Consider using a VPN or proxy if Sci-Hub is blocked in your country")
                NetInfo.SciHub_URL = "https://sci-hub.st"
                
        except Exception as e:
            print(f"Error setting Sci-Hub URL: {e}")
            NetInfo.SciHub_URL = "https://sci-hub.st"

    def get_safe_filename(self, folder, filename):
        """
        Generate a safe filename that doesn't conflict with existing files
        
        Args:
            folder (str): Target folder path
            filename (str): Desired filename
            
        Returns:
            str: Safe file path
        """
        file_path = Path(folder) / filename
        counter = 1
        
        while file_path.exists():
            name_parts = filename.rsplit('.', 1)
            if len(name_parts) == 2:
                new_filename = f"{name_parts[0]}({counter}).{name_parts[1]}"
            else:
                new_filename = f"{filename}({counter})"
            file_path = Path(folder) / new_filename
            counter += 1
            
        return str(file_path)

    def download_with_smartdl(self, url, file_path, headers=None):
        """
        Download file using PySmartDL
        
        Args:
            url (str): Download URL
            file_path (str): Target file path
            headers (dict): HTTP headers
            
        Returns:
            bool: True if download successful, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Configure SmartDL
            dl = SmartDL(
                url, 
                file_path, 
                progress_bar=self.enable_progress,
                threads=self.threads,
                timeout=self.timeout
            )
            
            # Set custom headers if provided
            if headers:
                dl.headers = headers
            
            # Start download
            dl.start()
            
            # Check if download was successful
            if dl.isSuccessful():
                if self.enable_progress:
                    print(f"✓ Successfully downloaded: {os.path.basename(file_path)}")
                    print(f"  Size: {dl.get_dl_size(human=True)}")
                    print(f"  Speed: {dl.get_speed(human=True)}")
                return True
            else:
                if self.enable_progress:
                    print(f"✗ Download failed: {dl.get_errors()}")
                return False
                
        except Exception as e:
            if self.enable_progress:
                print(f"✗ Download error: {e}")
            return False

    def download_paper_enhanced(self, paper, download_dir, scihub_url=None):
        """
        Enhanced paper download with multiple fallback methods
        
        Args:
            paper: Paper object to download
            download_dir (str): Download directory
            scihub_url (str): Custom SciHub URL (optional)
            
        Returns:
            tuple: (success, download_source, file_path)
        """
        # Set SciHub URL
        if scihub_url:
            NetInfo.SciHub_URL = scihub_url
        elif not NetInfo.SciHub_URL:
            self.set_scihub_url()
        
        # Generate safe filename
        file_path = self.get_safe_filename(download_dir, paper.getFileName())
        
        # URL joining helper
        def url_join(*args):
            return "/".join(str(arg).rstrip('/') for arg in args)
        
        # Download strategies in order of preference
        strategies = []
        
        # Strategy 1: SciHub with DOI
        if paper.DOI:
            strategies.append({
                'url': url_join(NetInfo.SciHub_URL, paper.DOI),
                'source': 'SciHub (DOI)',
                'source_id': 1,
                'requires_pdf_extraction': True
            })
        
        # Strategy 2: SciHub with Scholar link
        if paper.scholar_link:
            strategies.append({
                'url': url_join(NetInfo.SciHub_URL, paper.scholar_link),
                'source': 'SciHub (Scholar)',
                'source_id': 1,
                'requires_pdf_extraction': True
            })
        
        # Strategy 3: Direct PDF from Scholar
        if paper.scholar_link and paper.scholar_link.endswith('.pdf'):
            strategies.append({
                'url': paper.scholar_link,
                'source': 'Scholar (Direct PDF)',
                'source_id': 2,
                'requires_pdf_extraction': False
            })
        
        # Strategy 4: PDF link
        if paper.pdf_link:
            strategies.append({
                'url': paper.pdf_link,
                'source': 'Direct PDF Link',
                'source_id': 2,
                'requires_pdf_extraction': False
            })
        
        # Try each strategy
        for i, strategy in enumerate(strategies):
            if self.enable_progress:
                print(f"\n📥 Attempting download {i+1}/{len(strategies)}: {strategy['source']}")
                print(f"   Paper: {paper.title[:60]}{'...' if len(paper.title) > 60 else ''}")
            
            try:
                if strategy['requires_pdf_extraction']:
                    # First, get the page content to extract PDF link
                    response = requests.get(
                        strategy['url'], 
                        headers=NetInfo.HEADERS, 
                        timeout=self.timeout
                    )
                    
                    content_type = response.headers.get('content-type', '').lower()
                    
                    if 'application/pdf' in content_type:
                        # Direct PDF response - download it
                        success = self.download_with_smartdl(
                            strategy['url'], 
                            file_path, 
                            NetInfo.HEADERS
                        )
                        if success:
                            paper.downloaded = True
                            paper.downloadedFrom = strategy['source_id']
                            return True, strategy['source'], file_path
                    else:
                        # Need to extract PDF link from HTML
                        time.sleep(random.randint(1, 3))  # Be respectful to servers
                        
                        pdf_link = getSchiHubPDF(response.text)
                        if pdf_link:
                            success = self.download_with_smartdl(
                                pdf_link, 
                                file_path, 
                                NetInfo.HEADERS
                            )
                            if success:
                                paper.downloaded = True
                                paper.downloadedFrom = strategy['source_id']
                                return True, strategy['source'], file_path
                else:
                    # Direct download
                    success = self.download_with_smartdl(
                        strategy['url'], 
                        file_path, 
                        NetInfo.HEADERS
                    )
                    if success:
                        paper.downloaded = True
                        paper.downloadedFrom = strategy['source_id']
                        return True, strategy['source'], file_path
                        
            except Exception as e:
                if self.enable_progress:
                    print(f"   ✗ Strategy failed: {e}")
                continue
        
        # All strategies failed
        if self.enable_progress:
            print(f"   ✗ All download strategies failed for: {paper.title}")
        
        return False, None, None

    def download_papers_enhanced(self, papers, download_dir, num_limit=None, 
                                 scholar_results=None, scihub_url=None):
        """
        Enhanced batch paper downloading
        
        Args:
            papers: List of Paper objects
            download_dir (str): Download directory
            num_limit (int): Maximum number of papers to download
            scholar_results (int): Total number of scholar results (for progress)
            scihub_url (str): Custom SciHub URL
            
        Returns:
            dict: Download statistics
        """
        # Ensure download directory exists
        os.makedirs(download_dir, exist_ok=True)
        
        # Initialize statistics
        stats = {
            'total_attempted': 0,
            'successful_downloads': 0,
            'failed_downloads': 0,
            'scihub_downloads': 0,
            'direct_downloads': 0,
            'downloaded_files': []
        }
        
        print(f"\n🚀 Starting enhanced paper downloading...")
        print(f"📁 Download directory: {download_dir}")
        print(f"📊 Papers to process: {len(papers)}")
        if num_limit:
            print(f"📈 Download limit: {num_limit}")
        
        paper_count = 0
        
        for paper in papers:
            if not paper.canBeDownloaded():
                continue
                
            if num_limit and stats['successful_downloads'] >= num_limit:
                break
                
            paper_count += 1
            stats['total_attempted'] += 1
            
            if self.enable_progress:
                progress_info = f"({paper_count}/{scholar_results})" if scholar_results else f"({paper_count})"
                print(f"\n{'='*60}")
                print(f"📄 Processing paper {progress_info}")
            
            success, source, file_path = self.download_paper_enhanced(
                paper, download_dir, scihub_url
            )
            
            if success:
                stats['successful_downloads'] += 1
                stats['downloaded_files'].append(file_path)
                
                if paper.downloadedFrom == 1:  # SciHub
                    stats['scihub_downloads'] += 1
                else:  # Direct download
                    stats['direct_downloads'] += 1
                    
                if self.enable_progress:
                    print(f"✅ Successfully downloaded from {source}")
            else:
                stats['failed_downloads'] += 1
        
        # Print final statistics
        print(f"\n{'='*60}")
        print("📊 DOWNLOAD SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Successful downloads: {stats['successful_downloads']}")
        print(f"❌ Failed downloads: {stats['failed_downloads']}")
        print(f"🌐 SciHub downloads: {stats['scihub_downloads']}")
        print(f"🔗 Direct downloads: {stats['direct_downloads']}")
        print(f"📁 Files saved to: {download_dir}")
        
        return stats


# Backward compatibility function
def downloadPapers(papers, dwnl_dir, num_limit, scholar_results, SciHub_URL=None):
    """
    Backward compatibility wrapper for the original downloadPapers function
    Uses the enhanced downloader with progress bars enabled
    """
    downloader = EnhancedDownloader(enable_progress=True)
    stats = downloader.download_papers_enhanced(
        papers, dwnl_dir, num_limit, scholar_results, SciHub_URL
    )
    return stats['downloaded_files']


# Legacy functions for backward compatibility
def setSciHubUrl():
    """Legacy function - now handled by EnhancedDownloader"""
    downloader = EnhancedDownloader()
    downloader.set_scihub_url()


def getSaveDir(folder, fname):
    """Legacy function for generating safe file paths"""
    downloader = EnhancedDownloader()
    return downloader.get_safe_filename(folder, fname)


def saveFile(file_name, content, paper, dwn_source):
    """Legacy function for saving files"""
    try:
        with open(file_name, 'wb') as f:
            f.write(content)
        paper.downloaded = True
        paper.downloadedFrom = dwn_source
        return file_name
    except Exception as e:
        print(f"Error saving file {file_name}: {e}")
        return None

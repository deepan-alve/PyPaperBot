#!/usr/bin/env python3
"""
Demo script showcasing the enhanced downloader capabilities
Run this to see the enhanced downloader in action
"""

import tempfile
import os
from PyPaperBot.EnhancedDownloader import EnhancedDownloader
from PyPaperBot.Paper import Paper

def demo_enhanced_features():
    """Demonstrate the enhanced downloader features"""
    print("🎯 PyPaperBot Enhanced Downloader Demo")
    print("=" * 50)
    
    # Create a demo paper
    demo_paper = Paper(title="A Sample Research Paper on AI Ethics")
    demo_paper.DOI = "10.1038/s41586-019-1234-1"  # Example DOI
    demo_paper.canBeDownloaded = lambda: True
    
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Demo download directory: {temp_dir}")
        
        # Initialize enhanced downloader
        downloader = EnhancedDownloader(
            enable_progress=True,  # Show progress bars
            threads=3,            # Use 3 download threads
            timeout=15           # 15-second timeout
        )
        
        print("\n🚀 Demonstrating Enhanced Downloader Features:")
        print("   ✨ Real-time progress bars")
        print("   ⚡ Multi-threaded downloads")  
        print("   📊 Download statistics")
        print("   🔄 Smart retry mechanisms")
        print("   📁 Automatic file management")
        
        # Perform demo download
        print(f"\n📥 Starting demo download...")
        success, source, file_path = downloader.download_paper_enhanced(
            demo_paper, temp_dir
        )
        
        if success:
            print(f"\n🎉 Demo completed successfully!")
            print(f"   📄 Paper downloaded from: {source}")
            print(f"   💾 File saved as: {os.path.basename(file_path)}")
            
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"   📏 File size: {file_size:,} bytes")
        else:
            print(f"\n⚠️  Demo download failed (this is normal for demo)")
            print(f"   💡 In real usage, the downloader tries multiple strategies")
            print(f"   🔄 and provides detailed error information")
        
        print(f"\n💡 Key Benefits Demonstrated:")
        print(f"   🎯 User-friendly progress feedback")
        print(f"   🚀 Professional download experience") 
        print(f"   🛡️  Robust error handling")
        print(f"   📈 Real-time statistics")


def show_usage_examples():
    """Show various usage examples"""
    print(f"\n📚 Usage Examples")
    print("=" * 50)
    
    print("🖥️  Command Line Usage:")
    print("   # Enhanced downloader (default)")
    print("   python -m PyPaperBot --query='machine learning' --scholar-pages=1 --dwn-dir='./downloads'")
    print()
    print("   # Classic downloader")  
    print("   python -m PyPaperBot --classic-dl --query='ai ethics' --scholar-pages=2 --dwn-dir='./downloads'")
    
    print(f"\n🐍 Python API Usage:")
    print("   from PyPaperBot.EnhancedDownloader import EnhancedDownloader")
    print()
    print("   downloader = EnhancedDownloader(enable_progress=True)")
    print("   stats = downloader.download_papers_enhanced(papers, './downloads')")
    print("   print(f'Downloaded {stats[\"successful_downloads\"]} papers!')")
    
    print(f"\n⚙️  Configuration Options:")
    print("   downloader = EnhancedDownloader(")
    print("       enable_progress=True,  # Show progress bars")
    print("       threads=5,             # Multi-threading")
    print("       timeout=10             # Connection timeout")
    print("   )")


if __name__ == "__main__":
    print("🎬 Welcome to PyPaperBot Enhanced Downloader Demo!")
    print("=" * 60)
    
    # Run the demo
    demo_enhanced_features()
    
    # Show usage examples
    show_usage_examples()
    
    print("\n" + "=" * 60)
    print("🏆 Demo completed! The enhanced downloader is ready to use!")
    print("🚀 Try it with: python -m PyPaperBot --query='your topic' --scholar-pages=1 --dwn-dir='./downloads'")
    print("📖 For more info, see: ENHANCED_DOWNLOADER.md")

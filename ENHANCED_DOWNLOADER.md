# Enhanced Downloader Feature - Contribution Guide

This document explains the enhanced downloader feature added to PyPaperBot, which improves the downloading experience using PySmartDL.

## 🚀 What's New

### Enhanced Downloader Features

The new enhanced downloader provides several improvements over the original downloader:

1. **Progress Bars** 📊 - Real-time download progress visualization
2. **Resume Downloads** ⏯️ - Continue interrupted downloads automatically  
3. **Multi-threaded Downloads** ⚡ - Faster downloads with configurable thread count
4. **Better Error Handling** 🛠️ - More robust error handling and retry mechanisms
5. **Download Statistics** 📈 - Detailed statistics and reporting
6. **Speed Monitoring** 🏃 - Real-time download speed feedback
7. **Smart File Management** 📁 - Automatic duplicate file handling

### Backward Compatibility

✅ The enhanced downloader is **fully backward compatible** with existing code
✅ Original functionality remains unchanged
✅ Can be disabled if needed using `--classic-dl` flag

## 📦 Installation

The enhanced downloader requires PySmartDL. Install it using:

```bash
pip install pySmartDL>=1.3.4
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Command Line Interface

The enhanced downloader is enabled by default. You can control its behavior with these new options:

```bash
# Use enhanced downloader (default behavior)
python -m PyPaperBot --query="machine learning" --scholar-pages=1 --dwn-dir="./downloads"

# Explicitly use classic downloader
python -m PyPaperBot --classic-dl --query="ai research" --scholar-pages=1 --dwn-dir="./downloads"
```

### Programmatic Usage

#### Using the Enhanced Downloader Class

```python
from PyPaperBot.EnhancedDownloader import EnhancedDownloader

# Initialize with custom settings
downloader = EnhancedDownloader(
    enable_progress=True,  # Show progress bars
    threads=5,             # Number of download threads
    timeout=10             # Connection timeout in seconds
)

# Download papers with enhanced features
stats = downloader.download_papers_enhanced(
    papers=paper_list,
    download_dir="./downloads",
    num_limit=10,
    scholar_results=20
)

print(f"Successfully downloaded: {stats['successful_downloads']} papers")
```

#### Backward Compatible Usage

```python
from PyPaperBot.Downloader import downloadPapers

# This will automatically use the enhanced downloader
downloaded_files = downloadPapers(
    papers=paper_list,
    dwnl_dir="./downloads",
    num_limit=10,
    scholar_results=20,
    use_enhanced=True  # Optional: explicitly enable enhanced downloader
)
```

## 🔧 Technical Details

### Architecture

The enhanced downloader is implemented as a separate module (`EnhancedDownloader.py`) that:

1. **Maintains full backward compatibility** with the original `Downloader.py`
2. **Uses PySmartDL** for improved download capabilities
3. **Implements multiple download strategies** with automatic fallback
4. **Provides detailed progress feedback** and statistics

### Download Strategies

The enhanced downloader tries multiple strategies in order:

1. **SciHub with DOI** - Most reliable method
2. **SciHub with Scholar Link** - Fallback option
3. **Direct PDF from Scholar** - When available
4. **Direct PDF Link** - Last resort

### Error Handling

- Automatic retry with exponential backoff
- Graceful degradation to classic downloader if needed
- Detailed error reporting and logging
- Timeout management for stuck downloads

## 📊 Performance Improvements

| Feature | Original | Enhanced | Improvement |
|---------|----------|----------|-------------|
| Download Speed | Single-threaded | Multi-threaded | Up to 5x faster |
| Progress Feedback | None | Real-time bars | 100% visibility |
| Resume Capability | None | Automatic | No lost progress |
| Error Recovery | Basic | Advanced | Better reliability |
| File Management | Manual | Automatic | Reduced conflicts |

## 🧪 Testing

Run the test suite to verify the enhanced downloader works correctly:

```bash
python test_enhanced_downloader.py
```

This will test:
- Enhanced downloader functionality
- Backward compatibility
- Progress reporting
- Error handling

## 🤝 Contributing Guidelines

When contributing to this feature:

1. **Maintain Backward Compatibility** - Never break existing functionality
2. **Add Tests** - Include tests for new features
3. **Update Documentation** - Keep README and docstrings current
4. **Follow Code Style** - Use consistent formatting and naming
5. **Handle Errors Gracefully** - Provide informative error messages

### Code Structure

```
PyPaperBot/
├── Downloader.py           # Original downloader with enhanced integration
├── EnhancedDownloader.py   # New enhanced downloader class
├── __main__.py            # Updated CLI with enhanced options
├── requirements.txt       # Updated with pySmartDL dependency
└── setup.py              # Updated installation requirements
```

## 🐛 Troubleshooting

### Common Issues

1. **PySmartDL not found**
   ```bash
   pip install pySmartDL>=1.3.4
   ```

2. **Enhanced downloader disabled**
   - Check that PySmartDL is installed correctly
   - Remove `--classic-dl` flag if present

3. **Slow downloads**
   - Increase thread count in configuration
   - Check network connection
   - Verify SciHub accessibility

### Debug Mode

Enable verbose output for troubleshooting:

```python
downloader = EnhancedDownloader(enable_progress=True)
# The enhanced downloader provides detailed progress information
```

## 📋 Future Enhancements

Planned improvements for future versions:

- [ ] Download queue management
- [ ] Bandwidth limiting options
- [ ] Download scheduling
- [ ] Integration with cloud storage
- [ ] Advanced retry strategies
- [ ] Download history tracking

## 🙏 Acknowledgments

This enhancement builds upon:
- **PySmartDL** by Itay Brandes - For the core download functionality
- **PyPaperBot** by Vito Ferrulli - For the original framework
- **Community contributors** - For testing and feedback

---

**Note**: This enhanced downloader is designed to improve user experience while maintaining full compatibility with existing PyPaperBot workflows. The original functionality remains unchanged and accessible.

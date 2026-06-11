# Troubleshooting Guide

This guide addresses common issues and solutions in Edge Reader.

## Playback Issues

### Play button is grayed out

**Cause:** No document is open.

**Solution:**
1. Click "Open Document" to load a file
2. The Play button will enable immediately

**Note:** You don't need to generate a bundle to play. The Play button enables as soon as you open a document, allowing live playback. If you prefer offline playback, you can generate a bundle after opening the document.

### Audio doesn't play or is silent

**Causes & Solutions:**

1. **Volume is set to 0%**
   - Check the volume slider at the bottom right
   - Adjust to desired level

2. **System volume is muted**
   - Check your system volume settings (not Edge Reader's volume slider)
   - Unmute or increase system volume

3. **No audio output device configured**
   - Ensure speakers/headphones are connected
   - Check system audio settings

4. **Audio file is corrupted**
   - Try generating a fresh bundle
   - If issue persists, try a different document or voice

### Playback skips or stutters

**Causes & Solutions:**

1. **Disk I/O bottleneck**
   - Close other applications using disk
   - Ensure files are on a fast local drive (not network share)

2. **Temporary files on slow storage**
   - Live mode audio and bundles are extracted to `/tmp` (Linux/Mac) or `%TEMP%` (Windows)
   - Verify sufficient disk space (at least 1GB free)
   - Try moving to a local SSD if using network drive

3. **Qt multimedia backend issue**
   - Try updating PySide6: `pip install --upgrade PySide6`

## Live Playback Issues

### "Could not synthesize this sentence" error

**Cause:** Internet connection dropped during live synthesis.

**Solution:**
1. Check your internet connection
2. Click "Play" to resume (starts from beginning)
3. For reliable playback without network interruptions, generate an offline bundle

### Audio stops unexpectedly during live playback

**Possible causes:**

1. **Network connectivity issue**
   - Your connection dropped while synthesizing the next sentence
   - Check your internet connection and try playing again

2. **edge-tts service issue**
   - The unofficial edge-tts service may have intermittent issues
   - Wait a moment and try again
   - Try a different voice or language to isolate the issue

3. **System resource constraints**
   - Close other applications
   - Ensure sufficient RAM and CPU available
   - Try a shorter document to test

**Workaround:** Generate an offline bundle to avoid network dependencies.

### Live playback is slow to start

**Causes & Solutions:**

1. **First sentence synthesis takes 1-2 seconds**
   - This is normal; audio is synthesized on-demand
   - Subsequent sentences play while the next one is synthesizing

2. **Network latency**
   - Slow internet connection may increase synthesis time
   - Try again on a faster network

3. **System is busy**
   - Close other applications
   - Ensure sufficient CPU available for synthesis

## Generation Issues

### "Synthesis failed" error

**What to check:**

1. **See full error details**
   - Click "Details" in the error dialog to view the complete error message and traceback
   - Common errors explained below

2. **Internet connectivity**
   - Verify you have active internet access
   - Try a ping: `ping 1.1.1.1`
   - Some networks may block TTS API calls—try a different network

3. **Microsoft edge-tts API issue**
   - The edge-tts service is unofficial and occasionally has uptime issues
   - Wait a few minutes and try again
   - Try a different voice or language

4. **Invalid document text**
   - Very long documents (>100,000 sentences) may timeout
   - Try splitting the document into smaller files
   - Check that the document loads and displays correctly

5. **Insufficient disk space**
   - Large bundles can require 500MB+ of temporary space
   - Check free disk space: `df -h /tmp`
   - Free up space and try again

### Generation hangs or times out

**Solutions:**

1. **Cancel and retry**
   - Click "Cancel Generate" button
   - Wait for graceful cancellation (may take a moment)
   - Try again

2. **Network latency**
   - If on slow/unstable internet, generation may timeout
   - Try a different network if available

3. **Very large document**
   - Documents with >10,000 sentences can take 10+ minutes
   - Monitor progress in the status bar
   - Don't cancel unless necessary

## Voice & Language Issues

### "Could not fetch voices" error

**Cause:** Network connection failed when downloading latest voice list.

**Solution:**
- Edge Reader falls back to a built-in list of common voices
- Check your internet connection
- Try clicking "Refresh Voices" again
- If persistent, you can still use the fallback voices

### Voice not available

**Causes & Solutions:**

1. **Voice was removed from service**
   - Microsoft occasionally updates voice availability
   - Try a different voice or language

2. **Language not downloaded yet**
   - Click "Refresh Voices" to download the latest list
   - Select your desired language from the dropdown

3. **Regional limitations**
   - Some voices may not be available in all regions
   - Try a different voice in the same language

### Wrong voice is selected

**Solution:**
1. Change the language dropdown to match your desired voice's language
2. The voice list will update to show only voices for that language
3. Select the voice you want
4. Your selection is saved for next time

## Document Loading Issues

### "Could not decode text file" error

**Cause:** Text encoding is not recognized.

**Solution:**
- Edge Reader tries UTF-8, Windows-1252, and Latin-1 encoding
- If document still fails, try converting it with a text editor:
  1. Open the file in a text editor (e.g., VS Code, Notepad++)
  2. Select "Save with Encoding" and try UTF-8
  3. Save and try opening in Edge Reader

### "No readable text found" error

**Cause:** Document contains no extractable text.

**Solutions:**

1. **PDF with images only**
   - PDF contains only scanned images, not text
   - OCR is not supported; try converting with specialized tools

2. **Corrupted document**
   - Try opening in another application to verify
   - Try re-downloading or re-generating the document

3. **Unsupported format**
   - Check that file extension matches actual format
   - Try converting to a supported format

### "EPUB support requires ebooklib" error

**Solution:** Install required dependency:
```bash
pip install ebooklib
```

### "PDF support requires PyMuPDF" error

**Solution:** Install required dependency:
```bash
pip install PyMuPDF
```

### "MOBI/AZW files require Calibre" error

**Solution:** Install Calibre:
1. Visit https://calibre-ebook.com/download
2. Install for your platform
3. Verify `ebook-convert` is in your PATH:
   ```bash
   which ebook-convert  # Linux/Mac
   where ebook-convert # Windows
   ```

## Performance Issues

### Application is slow to start

**Causes & Solutions:**

1. **First-time voice download**
   - On first launch, Edge Reader may fetch voices from the API
   - This can take 10-30 seconds with slow internet
   - Subsequent launches are instant (voices are cached)

2. **Large previous bundle**
   - If a very large bundle was open, cleanup may take time
   - Wait for completion; subsequent launches will be faster

3. **Slow disk**
   - Consider upgrading to SSD for better performance

### Memory usage is high

**Expected behavior:**
- Large documents in memory: 100MB+ is normal for 10+ MB documents
- Audio bundles in temp directory: Can be several hundred MB for long documents

**If genuinely excessive:**
- Close and reopen the application
- Check for temp files: `ls -lh /tmp/edge_reader_bundle_*`
- Manually delete old temp bundles if needed

## UI Issues

### Window layout is broken

**Solution:** Reset the window:
1. Close Edge Reader
2. Delete settings: See [Settings & Preferences](USER_MANUAL.md#settings--preferences)
3. Reopen Edge Reader

### Text is too small or hard to read

**Solution:**
- Edge Reader respects system font settings
- Adjust in your OS accessibility settings:
  - **Linux:** System Settings → Appearance → Font
  - **macOS:** System Preferences → Accessibility → Display
  - **Windows:** Settings → Ease of Access → Display

### Error dialog won't close

**Solution:**
1. Check if OK button is off-screen
2. Use keyboard: Press Enter or Escape to close
3. If frozen, force close the application:
   - **Linux/Mac:** `pkill -f edge.reader`
   - **Windows:** Task Manager → End Task

## Getting More Help

### Enable Debug Output

Run Edge Reader from terminal to see debug messages:

```bash
python -m edge_reader.main 2>&1 | tee debug.log
```

Attach `debug.log` when reporting issues.

### Reporting Issues

When reporting a problem, include:
1. Error message and details
2. Document type and size
3. Operating system and version
4. Python version: `python --version`
5. Edge Reader version: check Help menu
6. Steps to reproduce
7. Debug log (optional)

### Common Questions

**Q: Can I use my own voice?**
A: Not currently. Edge Reader uses Microsoft's edge-tts service. Custom voices are a planned feature.

**Q: Can I edit the document before generating audio?**
A: Not in the current version. Copy text, edit in a text editor, and generate from there.

**Q: Can I generate multiple voices for the same document?**
A: Yes. Generate once with each voice to create separate bundles.

**Q: How long does bundle generation take?**
A: Typically 30-60 seconds per 1000 words. Very large documents may take several minutes.

**Q: Can I share bundles with others?**
A: Yes! `.edgevoice.zip` files are self-contained and can be shared via email, cloud storage, etc.

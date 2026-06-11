from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Any

from PySide6.QtCore import QSettings, Qt, QUrl
from PySide6.QtGui import QAction, QTextCharFormat, QTextCursor
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QSlider,
    QSpinBox,
    QStatusBar,
    QTextBrowser,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

import tempfile

from PySide6.QtCore import Signal

from .bundle import read_bundle, unpack_bundle
from .document import DocumentLoadError, load_document
from .models import LoadedDocument, SentenceSpan, VoiceInfo
from .textseg import split_sentences
from .workers import FALLBACK_VOICES, SynthesisWorker, VoiceListWorker, LivePlaybackWorker

APP_ORG = "Monotoba"
APP_NAME = "EdgeReader"


class NavigableTextEdit(QTextEdit):
    """QTextEdit that emits a signal when user double-clicks to jump to a location."""

    jump_requested = Signal(int)  # Character position

    def mouseDoubleClickEvent(self, event):  # type: ignore[override]
        cursor = self.cursorForPosition(event.pos())
        pos = cursor.position()
        self.jump_requested.emit(pos)
        super().mouseDoubleClickEvent(event)


def _show_error_dialog(parent: QMainWindow, title: str, message: str, detail: str = "") -> None:
    """Show an error dialog with scrollable details pane."""
    dialog = QDialog(parent)
    dialog.setWindowTitle(title)
    dialog.resize(700, 500)

    layout = QVBoxLayout()

    error_label = QLabel(message)
    error_label.setWordWrap(True)
    layout.addWidget(error_label)

    if detail:
        details_label = QLabel("Error Details:")
        layout.addWidget(details_label)

        details_browser = QTextBrowser()
        details_browser.setPlainText(detail)
        details_browser.setReadOnly(True)
        layout.addWidget(details_browser, 1)

    button_layout = QHBoxLayout()
    close_btn = QPushButton("Close")
    close_btn.clicked.connect(dialog.accept)
    button_layout.addStretch()
    button_layout.addWidget(close_btn)
    layout.addLayout(button_layout)

    dialog.setLayout(layout)
    dialog.exec()


class HelpDialog(QDialog):
    """Display markdown help files in a scrollable window."""

    def __init__(self, parent: QMainWindow, title: str, content: str) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(800, 600)

        layout = QVBoxLayout()
        browser = QTextBrowser(self)
        browser.setMarkdown(content)
        layout.addWidget(browser)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)
        self.exec()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Edge Reader — PySide6 + edge-tts")
        self.resize(1100, 760)

        self.settings = QSettings(APP_ORG, APP_NAME)
        self.current_document: LoadedDocument | None = None
        self.sentences: list[SentenceSpan] = []
        self.voices: list[VoiceInfo] = FALLBACK_VOICES[:]
        self.bundle_dir: Path | None = None
        self.bundle_manifest: dict[str, Any] | None = None
        self.bundle_timings: dict[str, Any] | None = None
        self.current_sentence_index = -1
        self.is_stopping = False
        self.voice_worker: VoiceListWorker | None = None
        self.synthesis_worker: SynthesisWorker | None = None
        self.live_mode = False
        self.live_temp_dir: Path | None = None
        self.live_worker: LivePlaybackWorker | None = None
        self.word_level_highlight = False
        self.word_boundaries: dict[int, list[dict[str, Any]]] = {}

        self.text_edit = NavigableTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setLineWrapMode(QTextEdit.WidgetWidth)

        self.language_combo = QComboBox(self)
        self.voice_combo = QComboBox(self)
        self.rate_spin = QSpinBox(self)
        self.rate_spin.setRange(-90, 200)
        self.rate_spin.setSuffix(" %")
        self.rate_spin.setValue(int(self.settings.value("rate", 0)))

        self.word_highlight_checkbox = QCheckBox("Word-level Highlight", self)
        self.word_highlight_checkbox.setChecked(bool(self.settings.value("word_highlight", False)))

        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(int(self.settings.value("volume", 85)))

        self.open_button = QPushButton("Open Document", self)
        self.generate_button = QPushButton("Generate Offline Bundle", self)
        self.open_bundle_button = QPushButton("Open Bundle", self)
        self.refresh_voices_button = QPushButton("Refresh Voices", self)
        self.play_button = QPushButton("Play", self)
        self.pause_button = QPushButton("Pause", self)
        self.stop_button = QPushButton("Stop", self)
        self.cancel_button = QPushButton("Cancel Generate", self)
        self.cancel_button.setEnabled(False)

        self.progress = QProgressBar(self)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)

        self.status = QStatusBar(self)
        self.setStatusBar(self.status)

        self.audio_output = QAudioOutput(self)
        self.audio_output.setVolume(self.volume_slider.value() / 100.0)
        self.player = QMediaPlayer(self)
        self.player.setAudioOutput(self.audio_output)
        self.player.mediaStatusChanged.connect(self._on_media_status_changed)
        self.player.errorOccurred.connect(self._on_player_error)
        self.player.positionChanged.connect(self._on_position_changed)

        self._build_menu()
        self._build_layout()
        self._connect_signals()
        self._populate_voices(self.voices)
        self._restore_voice_settings()
        self._set_ready_state()
        self.status.showMessage("Open a document and choose voice settings, then click Play.")

    def _build_menu(self) -> None:
        file_menu = self.menuBar().addMenu("File")
        open_doc = QAction("Open Document…", self)
        open_doc.triggered.connect(self.open_document)
        file_menu.addAction(open_doc)

        open_bundle = QAction("Open Offline Bundle…", self)
        open_bundle.triggered.connect(self.open_bundle)
        file_menu.addAction(open_bundle)

        file_menu.addSeparator()
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        tools = self.menuBar().addMenu("Tools")
        refresh = QAction("Refresh edge-tts Voices", self)
        refresh.triggered.connect(self.refresh_voices)
        tools.addAction(refresh)

        help_menu = self.menuBar().addMenu("Help")
        getting_started = QAction("Getting Started", self)
        getting_started.triggered.connect(self._show_getting_started)
        help_menu.addAction(getting_started)

        user_manual = QAction("User Manual", self)
        user_manual.triggered.connect(self._show_user_manual)
        help_menu.addAction(user_manual)

        troubleshooting = QAction("Troubleshooting", self)
        troubleshooting.triggered.connect(self._show_troubleshooting)
        help_menu.addAction(troubleshooting)

    def _build_layout(self) -> None:
        toolbar = QToolBar("Reader", self)
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        toolbar.addWidget(self.open_button)
        toolbar.addWidget(self.open_bundle_button)
        toolbar.addSeparator()
        toolbar.addWidget(QLabel("Language:"))
        toolbar.addWidget(self.language_combo)
        toolbar.addWidget(QLabel("Voice:"))
        toolbar.addWidget(self.voice_combo)
        toolbar.addWidget(self.refresh_voices_button)
        toolbar.addSeparator()
        toolbar.addWidget(QLabel("TTS speed:"))
        toolbar.addWidget(self.rate_spin)
        toolbar.addWidget(self.word_highlight_checkbox)
        toolbar.addWidget(self.generate_button)
        toolbar.addWidget(self.cancel_button)

        playback = QHBoxLayout()
        playback.addWidget(self.play_button)
        playback.addWidget(self.pause_button)
        playback.addWidget(self.stop_button)
        playback.addSpacing(20)
        playback.addWidget(QLabel("Volume:"))
        playback.addWidget(self.volume_slider)
        playback.addSpacing(20)
        playback.addWidget(self.progress, 1)

        root = QVBoxLayout()
        root.addWidget(self.text_edit, 1)
        root.addLayout(playback)

        container = QWidget(self)
        container.setLayout(root)
        self.setCentralWidget(container)

    def _connect_signals(self) -> None:
        self.open_button.clicked.connect(self.open_document)
        self.open_bundle_button.clicked.connect(self.open_bundle)
        self.refresh_voices_button.clicked.connect(self.refresh_voices)
        self.generate_button.clicked.connect(self.generate_bundle)
        self.cancel_button.clicked.connect(self.cancel_generation)
        self.play_button.clicked.connect(self.play)
        self.pause_button.clicked.connect(self.pause)
        self.stop_button.clicked.connect(self.stop)
        self.language_combo.currentTextChanged.connect(self._filter_voices_for_language)
        self.rate_spin.valueChanged.connect(lambda value: self.settings.setValue("rate", value))
        self.volume_slider.valueChanged.connect(self._set_volume)
        self.voice_combo.currentTextChanged.connect(lambda _: self._save_voice_settings())
        self.word_highlight_checkbox.stateChanged.connect(self._on_word_highlight_toggled)
        self.text_edit.jump_requested.connect(self._on_jump_to_position)

    def _set_volume(self, value: int) -> None:
        self.audio_output.setVolume(value / 100.0)
        self.settings.setValue("volume", value)

    def _on_word_highlight_toggled(self, state: int) -> None:
        self.word_level_highlight = self.word_highlight_checkbox.isChecked()
        self.settings.setValue("word_highlight", self.word_level_highlight)

    def _on_jump_to_position(self, char_pos: int) -> None:
        """Jump to the sentence containing the clicked character position."""
        if not self.sentences:
            return

        # Find which sentence contains this character position
        sentence_index = -1
        for i, sentence in enumerate(self.sentences):
            if sentence.start <= char_pos < sentence.end:
                sentence_index = i
                break

        if sentence_index < 0:
            return

        # Check if we're playing
        is_playing = self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState

        # If playing, stop and jump to new position
        if is_playing:
            self.player.stop()

        self.current_sentence_index = sentence_index
        self.status.showMessage(f"Jumped to sentence {sentence_index + 1}. Click Play to start reading from here.")

        # Highlight the sentence
        self._highlight_sentence(sentence_index)
        self.progress.setMaximum(len(self.sentences))
        self.progress.setValue(sentence_index + 1)

    def _set_ready_state(self) -> None:
        have_doc = self.current_document is not None and bool(self.sentences)
        have_bundle = self.bundle_dir is not None and self.bundle_manifest is not None
        generating = self.synthesis_worker is not None and self.synthesis_worker.isRunning()
        live_synth_active = self.live_worker is not None and self.live_worker.isRunning()
        playback_ready = have_bundle or have_doc
        self.generate_button.setEnabled(have_doc and not generating)
        self.cancel_button.setEnabled(generating)
        self.play_button.setEnabled(playback_ready and not live_synth_active)
        self.pause_button.setEnabled(playback_ready and not live_synth_active)
        self.stop_button.setEnabled(playback_ready and not live_synth_active)

    def _save_voice_settings(self) -> None:
        self.settings.setValue("language", self.language_combo.currentText())
        voice = self.voice_combo.currentData()
        if isinstance(voice, VoiceInfo):
            self.settings.setValue("voice", voice.short_name)

    def _restore_voice_settings(self) -> None:
        lang = str(self.settings.value("language", "en-US"))
        index = self.language_combo.findText(lang)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
        self._filter_voices_for_language(self.language_combo.currentText())
        preferred_voice = str(self.settings.value("voice", "en-US-AriaNeural"))
        for i in range(self.voice_combo.count()):
            voice = self.voice_combo.itemData(i)
            if isinstance(voice, VoiceInfo) and voice.short_name == preferred_voice:
                self.voice_combo.setCurrentIndex(i)
                break

    def _populate_voices(self, voices: list[VoiceInfo]) -> None:
        self.voices = voices or FALLBACK_VOICES[:]
        current_lang = self.language_combo.currentText() or str(self.settings.value("language", "en-US"))
        self.language_combo.blockSignals(True)
        self.language_combo.clear()
        locales = sorted({v.locale for v in self.voices if v.locale})
        for locale in locales:
            self.language_combo.addItem(locale)
        self.language_combo.blockSignals(False)
        index = self.language_combo.findText(current_lang)
        if index < 0:
            index = self.language_combo.findText("en-US")
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
        self._filter_voices_for_language(self.language_combo.currentText())

    def _filter_voices_for_language(self, locale: str) -> None:
        previous_short_name = ""
        prev = self.voice_combo.currentData()
        if isinstance(prev, VoiceInfo):
            previous_short_name = prev.short_name

        self.voice_combo.blockSignals(True)
        self.voice_combo.clear()
        filtered = [v for v in self.voices if v.locale == locale] or self.voices
        for voice in filtered:
            self.voice_combo.addItem(voice.display_name, voice)
        self.voice_combo.blockSignals(False)

        target = previous_short_name or str(self.settings.value("voice", ""))
        if target:
            for i in range(self.voice_combo.count()):
                voice = self.voice_combo.itemData(i)
                if isinstance(voice, VoiceInfo) and voice.short_name == target:
                    self.voice_combo.setCurrentIndex(i)
                    break
        self._save_voice_settings()

    def refresh_voices(self) -> None:
        if self.voice_worker and self.voice_worker.isRunning():
            return
        self.status.showMessage("Fetching edge-tts voices…")
        self.refresh_voices_button.setEnabled(False)
        self.voice_worker = VoiceListWorker()
        self.voice_worker.voices_ready.connect(self._voices_ready)
        self.voice_worker.failed.connect(self._voices_failed)
        self.voice_worker.finished.connect(lambda: self.refresh_voices_button.setEnabled(True))
        self.voice_worker.start()

    def _voices_ready(self, voices: list[VoiceInfo]) -> None:
        self._populate_voices(voices)
        self._restore_voice_settings()
        self.status.showMessage(f"Loaded {len(voices)} voices.")

    def _voices_failed(self, error: str) -> None:
        _show_error_dialog(
            self,
            "Could not fetch voices",
            "Using built-in fallback voice list.",
            error,
        )
        self.status.showMessage("Voice fetch failed; using fallback voices.")

    def open_document(self) -> None:
        filters = (
            "Readable documents (*.txt *.md *.markdown *.rst *.html *.htm *.xhtml *.epub *.pdf *.docx *.rtf "
            "*.mobi *.azw *.azw3 *.fb2);;All files (*)"
        )
        filename, _ = QFileDialog.getOpenFileName(self, "Open document", "", filters)
        if not filename:
            return
        try:
            doc = load_document(filename)
            if self.live_temp_dir and self.live_temp_dir.exists():
                shutil.rmtree(self.live_temp_dir, ignore_errors=True)
            self.current_document = doc
            self.sentences = split_sentences(doc.text)
            self.text_edit.setPlainText(doc.text)
            self.bundle_dir = None
            self.bundle_manifest = None
            self.bundle_timings = None
            self.live_mode = False
            self.live_temp_dir = None
            self.live_worker = None
            self.current_sentence_index = -1
            self.progress.setValue(0)
            self.status.showMessage(f"Loaded {doc.path.name}: {len(self.sentences)} sentence/chunk(s).")
            self._set_ready_state()
        except DocumentLoadError as exc:
            QMessageBox.critical(self, "Document load failed", str(exc))
        except Exception as exc:
            QMessageBox.critical(self, "Document load failed", repr(exc))

    def generate_bundle(self) -> None:
        if not self.current_document or not self.sentences:
            QMessageBox.information(self, "No document", "Open a document first.")
            return
        voice = self.voice_combo.currentData()
        if not isinstance(voice, VoiceInfo):
            QMessageBox.warning(self, "No voice", "Choose a voice first.")
            return

        suggested = self.current_document.path.with_suffix(".edgevoice.zip")
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save offline voice bundle",
            str(suggested),
            "Edge Reader bundles (*.edgevoice.zip *.zip);;Zip files (*.zip);;All files (*)",
        )
        if not filename:
            return

        output = Path(filename)
        self.progress.setValue(0)
        self.status.showMessage("Generating audio bundle. Internet connection is required for this step.")
        self.synthesis_worker = SynthesisWorker(
            document_text=self.current_document.text,
            title=self.current_document.title,
            source_name=self.current_document.path.name,
            sentences=self.sentences,
            voice=voice.short_name,
            locale=voice.locale,
            rate_percent=self.rate_spin.value(),
            output_bundle=output,
        )
        self.synthesis_worker.progress.connect(self._synthesis_progress)
        self.synthesis_worker.finished_ok.connect(self._synthesis_finished)
        self.synthesis_worker.failed.connect(self._synthesis_failed)
        self.synthesis_worker.finished.connect(self._synthesis_thread_done)
        self._set_ready_state()
        self.synthesis_worker.start()

    def _synthesis_progress(self, done: int, total: int, preview: str) -> None:
        self.progress.setMaximum(total)
        self.progress.setValue(done)
        self.status.showMessage(f"Generating {done}/{total}: {preview}")

    def _synthesis_finished(self, bundle_path: str) -> None:
        self.status.showMessage(f"Generated offline bundle: {bundle_path}")
        self._load_bundle_path(Path(bundle_path))

    def _synthesis_failed(self, error: str) -> None:
        _show_error_dialog(self, "Synthesis failed", "Could not generate audio bundle.", error)
        self.status.showMessage("Synthesis failed.")

    def _synthesis_thread_done(self) -> None:
        self.synthesis_worker = None
        self._set_ready_state()

    def cancel_generation(self) -> None:
        if self.synthesis_worker:
            self.synthesis_worker.cancel()
            self.status.showMessage("Cancellation requested; waiting for current sentence to finish…")

    def open_bundle(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open offline voice bundle",
            "",
            "Edge Reader bundles (*.edgevoice.zip *.zip);;All files (*)",
        )
        if filename:
            self._load_bundle_path(Path(filename))

    def _load_bundle_path(self, path: Path) -> None:
        try:
            old_bundle = self.bundle_dir
            workdir = unpack_bundle(path)
            manifest, timings, text = read_bundle(workdir)
            if old_bundle and old_bundle.exists():
                shutil.rmtree(old_bundle, ignore_errors=True)
            self.bundle_dir = workdir
            self.bundle_manifest = manifest
            self.bundle_timings = timings
            self._parse_word_boundaries(timings)
            self.current_document = LoadedDocument(path=path, title=str(manifest.get("title") or path.stem), text=text)
            self.sentences = [
                SentenceSpan(
                    int(item["index"]),
                    int(item["start"]),
                    int(item["end"]),
                    str(item["text"]),
                )
                for item in manifest.get("sentences", [])
            ]
            self.text_edit.setPlainText(text)
            self.current_sentence_index = -1
            self.progress.setRange(0, max(1, len(self.sentences)))
            self.progress.setValue(0)
            self._clear_highlight()
            self._set_ready_state()
            self.status.showMessage(f"Opened bundle: {path.name} ({len(self.sentences)} sentence/chunk(s)).")
        except Exception as exc:
            QMessageBox.critical(self, "Could not open bundle", str(exc))

    def play(self) -> None:
        if not self.current_document or not self.sentences:
            QMessageBox.information(self, "No document", "Open a document first.")
            return

        if self.bundle_dir and self.bundle_manifest:
            if self.current_sentence_index < 0:
                self.current_sentence_index = 0
                self._play_current_sentence()
            else:
                self.player.play()
        else:
            if self.current_sentence_index < 0:
                self.current_sentence_index = 0
                self._start_live_playback()
            else:
                self.player.play()

    def pause(self) -> None:
        self.player.pause()

    def stop(self) -> None:
        self.is_stopping = True
        self.player.stop()
        if self.live_worker and self.live_worker.isRunning():
            self.live_worker.wait()
        self.current_sentence_index = -1
        self.progress.setValue(0)
        self._clear_highlight()
        if self.live_mode and self.live_temp_dir and self.live_temp_dir.exists():
            shutil.rmtree(self.live_temp_dir, ignore_errors=True)
        self.live_mode = False
        self.live_temp_dir = None
        self.live_worker = None
        self.status.showMessage("Stopped.")
        self.is_stopping = False
        self._set_ready_state()

    def _start_live_playback(self) -> None:
        if self.live_mode or self.live_temp_dir is None:
            self.live_mode = True
            self.live_temp_dir = Path(tempfile.mkdtemp(prefix="edge_reader_live_"))
            self.status.showMessage("Starting live playback (internet required)…")
        self._synthesize_and_play_sentence()

    def _synthesize_and_play_sentence(self) -> None:
        if not self.live_temp_dir or self.current_sentence_index < 0:
            return
        if self.current_sentence_index >= len(self.sentences):
            self.stop()
            self.status.showMessage("Finished.")
            return

        sentence = self.sentences[self.current_sentence_index]
        voice = self.voice_combo.currentData()
        if not isinstance(voice, VoiceInfo):
            QMessageBox.warning(self, "No voice", "Choose a voice first.")
            return

        self._highlight_sentence(self.current_sentence_index)
        self.progress.setMaximum(len(self.sentences))
        self.progress.setValue(self.current_sentence_index + 1)

        self.live_worker = LivePlaybackWorker(
            sentence=sentence,
            voice=voice.short_name,
            rate_percent=self.rate_spin.value(),
            audio_dir=self.live_temp_dir,
        )
        self.live_worker.finished_ok.connect(self._live_synthesis_finished)
        self.live_worker.failed.connect(self._live_synthesis_failed)
        self.live_worker.finished.connect(self._live_synthesis_thread_done)
        self._set_ready_state()
        self.status.showMessage(
            f"Synthesizing {self.current_sentence_index + 1}/{len(self.sentences)}…"
        )
        self.live_worker.start()

    def _live_synthesis_finished(self, audio_path: str) -> None:
        if not self.is_stopping:
            self._play_current_sentence()

    def _live_synthesis_failed(self, error: str) -> None:
        _show_error_dialog(
            self,
            "Synthesis failed",
            "Could not synthesize this sentence. Check your internet connection.",
            error,
        )
        self.stop()
        self.status.showMessage("Live playback failed.")

    def _live_synthesis_thread_done(self) -> None:
        self.live_worker = None
        self._set_ready_state()

    def _play_current_sentence(self) -> None:
        if self.current_sentence_index < 0 or self.current_sentence_index >= len(self.sentences):
            self.stop()
            self.status.showMessage("Finished.")
            return

        if self.live_mode:
            audio_path = self.live_temp_dir / f"{self.current_sentence_index:06d}.mp3"
        else:
            if not self.bundle_dir or not self.bundle_manifest:
                return
            sentences = self.bundle_manifest.get("sentences", [])
            if self.current_sentence_index >= len(sentences):
                self.stop()
                self.status.showMessage("Finished.")
                return
            item = sentences[self.current_sentence_index]
            audio_path = self.bundle_dir / item["audio"]

        if not audio_path.exists():
            QMessageBox.critical(self, "Missing audio", f"Missing audio segment: {audio_path}")
            self.stop()
            return

        self._highlight_sentence(self.current_sentence_index)
        self.progress.setMaximum(len(self.sentences))
        self.progress.setValue(self.current_sentence_index + 1)
        self.player.setSource(QUrl.fromLocalFile(str(audio_path)))
        self.player.play()
        mode_indicator = " (offline)" if not self.live_mode else " (live)"
        self.status.showMessage(
            f"Reading {self.current_sentence_index + 1}/{len(self.sentences)}{mode_indicator}"
        )

    def _on_media_status_changed(self, status: QMediaPlayer.MediaStatus) -> None:
        if status == QMediaPlayer.MediaStatus.EndOfMedia and not self.is_stopping:
            self.current_sentence_index += 1
            if self.live_mode:
                self._synthesize_and_play_sentence()
            else:
                self._play_current_sentence()

    def _on_position_changed(self, pos: int) -> None:
        # Highlight words based on playback position if word-level highlighting is enabled
        if not self.word_level_highlight or self.current_sentence_index < 0:
            return
        self._highlight_word_at_position(pos)

    def _on_player_error(self, error: QMediaPlayer.Error, error_string: str) -> None:
        if error != QMediaPlayer.Error.NoError:
            QMessageBox.warning(self, "Playback error", error_string or str(error))

    def _clear_highlight(self) -> None:
        self.text_edit.setExtraSelections([])

    def _highlight_sentence(self, index: int) -> None:
        if index < 0 or index >= len(self.sentences):
            self._clear_highlight()
            return
        span = self.sentences[index]
        cursor = self.text_edit.textCursor()
        cursor.setPosition(span.start)
        cursor.setPosition(span.end, QTextCursor.KeepAnchor)

        fmt = QTextCharFormat()
        fmt.setBackground(Qt.GlobalColor.yellow)
        selection = QTextEdit.ExtraSelection()
        selection.cursor = cursor
        selection.format = fmt
        self.text_edit.setExtraSelections([selection])
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()

    def _highlight_word_at_position(self, pos_ms: int) -> None:
        if self.current_sentence_index not in self.word_boundaries:
            return

        boundaries = self.word_boundaries[self.current_sentence_index]
        current_word = None

        for boundary in boundaries:
            start = boundary.get("offset_ms", 0)
            duration = boundary.get("duration_ms", 0)
            end = start + duration

            if start <= pos_ms < end:
                current_word = boundary
                break

        if current_word is None:
            return

        sentence_span = self.sentences[self.current_sentence_index]
        word_text = current_word.get("text", "")

        # Find word position in the sentence text
        sentence_text = sentence_span.text
        word_start = sentence_text.find(word_text)

        if word_start == -1:
            return

        word_end = word_start + len(word_text)

        # Convert to document-level positions
        doc_word_start = sentence_span.start + word_start
        doc_word_end = sentence_span.start + word_end

        cursor = self.text_edit.textCursor()
        cursor.setPosition(doc_word_start)
        cursor.setPosition(doc_word_end, QTextCursor.KeepAnchor)

        fmt = QTextCharFormat()
        fmt.setBackground(Qt.GlobalColor.cyan)
        fmt.setFontWeight(700)  # Bold

        selection = QTextEdit.ExtraSelection()
        selection.cursor = cursor
        selection.format = fmt
        self.text_edit.setExtraSelections([selection])
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()

    def _parse_word_boundaries(self, timings: dict[str, Any]) -> None:
        self.word_boundaries = {}
        segments = timings.get("segments", [])

        for segment in segments:
            sentence_index = segment.get("sentence_index", -1)
            if sentence_index < 0:
                continue

            words = [
                event for event in segment.get("events", [])
                if event.get("type") == "WordBoundary"
            ]

            if words:
                self.word_boundaries[sentence_index] = words

    def _load_help_file(self, filename: str) -> str:
        """Load a help markdown file from the help directory."""
        help_dir = Path(__file__).parent.parent.parent / "help"
        help_file = help_dir / filename
        if help_file.exists():
            return help_file.read_text(encoding="utf-8")
        return f"# Help\n\nCould not find help file: {filename}"

    def _show_getting_started(self) -> None:
        content = self._load_help_file("GETTING_STARTED.md")
        HelpDialog(self, "Getting Started", content)

    def _show_user_manual(self) -> None:
        content = self._load_help_file("USER_MANUAL.md")
        HelpDialog(self, "User Manual", content)

    def _show_troubleshooting(self) -> None:
        content = self._load_help_file("TROUBLESHOOTING.md")
        HelpDialog(self, "Troubleshooting", content)

    def closeEvent(self, event) -> None:  # type: ignore[override]
        self.stop()
        if self.bundle_dir and self.bundle_dir.exists():
            shutil.rmtree(self.bundle_dir, ignore_errors=True)
        if self.live_temp_dir and self.live_temp_dir.exists():
            shutil.rmtree(self.live_temp_dir, ignore_errors=True)
        super().closeEvent(event)


def main() -> int:
    app = QApplication(sys.argv)
    app.setOrganizationName(APP_ORG)
    app.setApplicationName(APP_NAME)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

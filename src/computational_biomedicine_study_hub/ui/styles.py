"""Application-level stylesheet."""

APPLICATION_STYLESHEET = """
QMainWindow { background: #f4f6f8; }
QWidget { color: #1f2933; font-family: \"Segoe UI\", \"Inter\", sans-serif; font-size: 14px; }
QWidget#navigationSidebar { background: #17212b; }
QLabel#productName { color: #ffffff; font-size: 19px; font-weight: 700; padding: 4px 8px 18px 8px; }
QLabel#navigationSection { color: #8fa1b3; font-size: 11px; font-weight: 700; padding: 16px 8px 4px 8px; }
QPushButton#navigationButton { background: transparent; color: #dbe4ec; border: none; border-radius: 7px; padding: 10px 12px; text-align: left; }
QPushButton#navigationButton:hover { background: #243443; }
QPushButton#navigationButton:checked { background: #2f80ed; color: #ffffff; font-weight: 600; }
QLabel#pageTitle { font-size: 26px; font-weight: 700; }
QLabel#pageSubtitle { color: #66727f; }
QLabel#homeMessage, QLabel#placeholderMessage { color: #52606d; font-size: 16px; padding: 32px; }
"""

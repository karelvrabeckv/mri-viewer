from asyncio import get_event_loop
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

def watchdog(self):
    """Monitor files and update user interface on file save."""

    try:
        current_event_loop = get_event_loop()

        def update_ui():
            with self.server.state:
                self.build_ui()

        class UpdateUIOnChange(FileSystemEventHandler):
            def on_modified(self, _):
                current_event_loop.call_soon_threadsafe(update_ui)
                print("WATCHDOG: Updated")

        observer = Observer()
        observer.schedule(
            UpdateUIOnChange(), str(Path(__file__).parent.absolute()), recursive=True
        )
        observer.start()
        
        print("WATCHDOG: Starting auto monitoring")
    except:
        print("WATCHDOG: Package not found")
        print("WATCHDOG: Skipping auto monitoring")

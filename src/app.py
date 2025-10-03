from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication

from src.core.global_timer import GlobalTimer
from src.lua.manager import LuaManager
from src.resource.loader import Loader


class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        # Load resources and initialize LuaManager
        self.resources = Loader().scan()
        self.lua_manager = LuaManager(self.resources)

        # Initialize GlobalTimer
        self.global_timer = GlobalTimer()

        # Setup tray icon
        self.tray_icon = QSystemTrayIcon(self)
        # Replace with actual icon path if available, or use a default Qt icon
        self.tray_icon.setIcon(QIcon.fromTheme("applications-system"))  # Fallback to a system icon
        self.tray_menu = QMenu()

        self.pause_action = QAction("Pause", self)
        self.pause_action.triggered.connect(self.toggle_pause)
        self.tray_menu.addAction(self.pause_action)

        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.exit_app)
        self.tray_menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        self.is_paused = False

        # Call on_startup for all scripts if exists
        self.lua_manager.execute_all("on_startup")

        # Subscribe to GlobalTimer for on_update
        GlobalTimer.subscribe(self)

    def global_update(self, delta_time: float):
        if not self.is_paused:
            self.lua_manager.execute_all("on_update", delta_time)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_action.setText("Resume")
            GlobalTimer.stop()
        else:
            self.pause_action.setText("Pause")
            GlobalTimer.start()

    def exit_app(self):
        # Call on_exit for all scripts if exists
        self.lua_manager.execute_all("on_exit")
        self.quit()
from PyQt6.QtCore import QRunnable, QThreadPool, QTimer

class PairingTask(QRunnable):
    def __init__(self, device_manager, address, callback):
        super().__init__()
        self.device_manager = device_manager
        self.address = address
        self.callback = callback

    def run(self):
        success = self.device_manager.pair(self.address)
        QTimer.singleShot(0, lambda: self.callback(success, self.address))


if action == 'pair':
    self.log.info(f"Attempting to pair with {device_address}")
    if self.bluetooth_device_manager.is_device_paired(device_address):
        QMessageBox.information(self, "Already Paired", f"{device_address} is already paired.")
        self.add_paired_device_to_list(device_address)
        return

    def on_pairing_complete(success, address):
        if success:
            QMessageBox.information(self, "Pairing Successful", f"{address} was paired.")
            self.add_paired_device_to_list(address)
        else:
            QMessageBox.critical(self, "Pairing Failed", f"Pairing with {address} failed.")

    task = PairingTask(self.bluetooth_device_manager, device_address, on_pairing_complete)

def handle_pairing_request(self, request_type, device, uuid=None, passkey=None):
    self.log.info(f"Handling pairing request: {request_type} for {device}")
    device_address = device.split("dev_")[-1].replace("_", ":")

    def show_info(title, message):
        dialog = QMessageBox(self)
        dialog.setWindowTitle(title)
        dialog.setText(message)
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.show()

    def show_warning(title, message):
        dialog = QMessageBox(self)
        dialog.setWindowTitle(title)
        dialog.setText(message)
        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.show()

    def show_question(title, message, callback):
        dialog = QMessageBox(self)
        dialog.setWindowTitle(title)
        dialog.setText(message)
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dialog.setIcon(QMessageBox.Icon.Question)
        dialog.buttonClicked.connect(callback)
        dialog.show()

    def show_input(title, label, callback, is_int=False):
        if is_int:
            value, ok = QInputDialog.getInt(self, title, label)
        else:
            value, ok = QInputDialog.getText(self, title, label)
        if ok and value:
            callback(value)

    if self.selected_capability == "NoInputNoOutput":
        QTimer.singleShot(0, lambda: (
            show_info("Pairing Successful", f"{device_address} was paired"),
            self.add_paired_device_to_list(device_address)
            if self.bluetooth_device_manager.is_device_paired(device_address)
            else show_warning("Pairing Failed", f"Pairing with {device_address} failed")
        ))
        return

    if request_type == "pin":
        QTimer.singleShot(0, lambda: show_input("Pairing Request", f"Enter PIN for device {device_address}:", lambda pin: pin))
    elif request_type == "passkey":
        QTimer.singleShot(0, lambda: show_input("Pairing Request", f"Enter passkey for device {device_address}:", lambda pk: (
            show_info("Pairing Successful", f"{device_address} was paired"),
            self.add_paired_device_to_list(device_address),
            pk
        ), is_int=True))
    elif request_type == "confirm":
        QTimer.singleShot(0, lambda: show_question("Confirm Pairing", f"Device {device_address} requests to pair with passkey: {uuid}\nAccept?",
            lambda btn: (
                show_info("Pairing Successful", f"{device_address} was paired"),
                self.add_paired_device_to_list(device_address)
            ) if btn.text() == "&Yes" else (
                show_info("Pairing Failed", f"Pairing with {device_address} failed"),
                self.log.info("User rejected pairing confirmation request")
            )
        ))
    elif request_type == "authorize":
        QTimer.singleShot(0, lambda: show_question("Authorize Service", f"Device {device_address} wants to use service {uuid}\nAllow?",
            lambda btn: (
                show_info("Connection Successful", f"{device_address} was connected")
            ) if btn.text() == "&Yes" else (
                self.log.warning("User denied service authorization for device %s", device_address),
                self.bluetooth_device_manager.disconnect(device_address)
            )
        ))
    elif request_type == "display_pin":
        if uuid is not None:
            QTimer.singleShot(0, lambda: show_info("Display PIN", f"Enter this PIN on {device_address}: {uuid}"))
            QTimer.singleShot(5000, lambda: (
                self.add_paired_device_to_list(device_address)
                if self.bluetooth_device_manager.is_device_paired(device_address)
                else show_warning("Pairing Failed", f"Pairing with {device_address} did not complete.")
            ))
        else:
            self.log.warning("DisplayPinCode called, but no PIN provided.")
    elif request_type == "display_passkey":
        if passkey is not None:
            QTimer.singleShot(0, lambda: show_info("Display Passkey", f"Enter this passkey on {device_address}: {passkey}"))
            QTimer.singleShot(5000, lambda: (
                self.add_paired_device_to_list(device_address)
                if self.bluetooth_device_manager.is_device_paired(device_address)
                else show_warning("Pairing Failed", f"Pairing with {device_address} did not complete.")
            ))
    elif request_type == "cancel":
        QTimer.singleShot(0, lambda: show_warning("Pairing Cancelled", f"Pairing with {device_address} was cancelled."))

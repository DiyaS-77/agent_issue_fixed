import dbus
import dbus.service


class Agent(dbus.service.Object):
    def __init__(self, bus, path, ui_callback, log):
        super().__init__(bus, path)
        self.ui_callback = ui_callback
        self.log = log

    @dbus.service.method("org.bluez.Agent1", in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
        self.log.info("RequestPinCode called for %s ", device)
        pin = self.ui_callback("pin", device)
        self.log.info("RequestPinCode reply=%s ", pin)
        return pin

    @dbus.service.method("org.bluez.Agent1", in_signature="o", out_signature="u")
    def RequestPasskey(self, device):
        self.log.info("RequestPasskey called for %s ", device)
        passkey = self.ui_callback("passkey", device)
        self.log.info("RequestPasskey reply=%s", passkey)
        return dbus.UInt32(passkey)

    @dbus.service.method("org.bluez.Agent1", in_signature="ou", out_signature="")
    def RequestConfirmation(self, device, passkey):
        self.log.info("RequestConfirmation called for %s, passkey=%s ", device, passkey)
        response = self.ui_callback("confirm", device, passkey)
        self.log.info("RequestConfirmation response=%s", response)
        if not response:
            raise Exception("User rejected confirmation")
        return

    @dbus.service.method("org.bluez.Agent1", in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        self.log.info("RequestAuthorization called for %s", device)
        response = self.ui_callback("authorize_device", device)
        self.log.info("RequestAuthorization response=%s", response)
        if not response:
            raise Exception("Connection not authorized by user")
        return

    @dbus.service.method("org.bluez.Agent1", in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):
        self.log.info("AuthorizeService called for %s uuid=%s", device, uuid)
        response = self.ui_callback("authorize", device, uuid)
        self.log.info("AuthorizeService response=%s", response)
        if not response:
            raise Exception("Service not authorized")
        return

    @dbus.service.method("org.bluez.Agent1", in_signature="o", out_signature="")
    def Cancel(self, device):
        self.log.info("[Agent] Cancel called for %s", device)

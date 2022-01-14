from DesktopClient.MixnetClient import MixnetClient


app = MixnetClient()
app.send(app.key_manager.pk, "Hi mark!")

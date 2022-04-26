import dbus
import logging
import pykka

from mopidy import core


ROOT_URI = 'cd:/'

logger = logging.getLogger(__name__)

class CdFrontend(pykka.ThreadingActor, core.CoreListener):
    BUS_NAME = 'org.freedesktop.UDisks2'

    def __init__(self, config, core):
        super().__init__()
        self._core = core
        self._bus = dbus.SystemBus()
        self._cd_drive_path = self._get_cd_drive_dbus_path()

        if self._cd_drive_path is None:
            logger.error('CD Rom drive not fount. CD Frontend will not work')

        iface  = 'org.freedesktop.DBus.Properties'
        signal = 'PropertiesChanged'
        self._bus.add_signal_receiver(self._callback_function, signal, iface, self.BUS_NAME, self._cd_drive_path)

    def _get_cd_drive_dbus_path(self):
        manager = self._bus.get_object(self.BUS_NAME, '/org/freedesktop/UDisks2')
        objects = manager.GetManagedObjects(dbus_interface='org.freedesktop.DBus.ObjectManager')
        for path, ifaces in objects.items():
            if 'org.freedesktop.UDisks2.Drive' in ifaces:
                drive = ifaces['org.freedesktop.UDisks2.Drive']
                optical = drive['Optical']
                if optical:
                    return path

    def _callback_function(self, sender, properties, _signature):
        if 'MediaAvailable' not in properties:
            return
        if not properties['MediaAvailable']:
            logger.info('CD Removed')
            tl_tracks = self._core.tracklist.get_tl_tracks().get()
            cd_tl_tracks = filter(lambda tl_track: tl_track.track.uri.startswith(ROOT_URI), tl_tracks)
            self._core.tracklist.remove({'tlid': [tl_track.tlid for tl_track in cd_tl_tracks]})
            return
        logger.info('CD Inserted')
        cd_tracks = self._core.library.browse(uri=ROOT_URI).get()
        self._core.tracklist.clear().get()
        tl_tracks = self._core.tracklist.add(uris=[track.uri for track in cd_tracks]).get()
        if tl_tracks:
            self._core.playback.play(tl_tracks[0]).get()

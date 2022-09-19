import pyudev
import logging
import pykka

from mopidy import core


ROOT_URI = 'cd://'

logger = logging.getLogger(__name__)

class CdFrontend(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super().__init__()
        self._core = core
        self._context = pyudev.Context()
        self._monitor = pyudev.Monitor.from_netlink(self._context)
        self._monitor.filter_by('block')
        self._observer = pyudev.MonitorObserver(self._monitor, self._callback_function)
        self._cd_drive_path = self._get_cd_drive_path()

        if self._cd_drive_path is None:
            logger.error('CD Rom drive not fount. CD Frontend will not work')
            return
        else:
            logger.info('CD Rom found [%s]', self._cd_drive_path)
            self._available = self._get_cd_available()
            if self._available:
                logger.info('Disk present in CD Rom')
            else:
                logger.info('Disk missing in CD Rom')

        self._observer.start()

    def _get_cd_drive_path(self):
        for device in self._context.list_devices(subsystem='block', DEVTYPE='disk'):
            try:
                if device['ID_CDROM_CD'] == '1':
                    return device['DEVNAME']
            except KeyError:
                pass

    def _get_cd_available(self):
        for device in self._context.list_devices(subsystem='block', DEVTYPE='disk'):
            try:
                if device['ID_CDROM_MEDIA_CD'] == '1':
                    return True
            except KeyError:
                pass
        return False

    def _callback_function(self, action, device):
        if action != 'change':
            return
        try:
            if device['DEVNAME'] != self._cd_drive_path:
                return
        except KeyError:
            return

        available = False
        try:
            if device['ID_CDROM_MEDIA_CD'] == '1':
                available = True
        except KeyError:
            pass

        if available == self._available:
            return
        self._available = available
        if not self._available:
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

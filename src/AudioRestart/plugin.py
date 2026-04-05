from Components.config import config, ConfigSubsection, ConfigInteger, ConfigSelection
from Components.SystemInfo import SystemInfo
from enigma import eTimer
from Plugins.Plugin import PluginDescriptor
from Screens import Standby
from Screens.Setup import Setup
from .__init__ import _
import NavigationInstance


config.plugins.AudioRestart = ConfigSubsection()
config.plugins.AudioRestart.restartSelection = ConfigSelection(default="disabled", choices=[("disabled", _("disabled")), ("restart", _("after restart")), ("standby", _("after standby")), ("both", _("after restart/standby"))])
config.plugins.AudioRestart.restartDelay = ConfigInteger(default=5, limits=(0, 30))

PLUGIN_BASE = "AudioRestart"
PLUGIN_VERSION = "0.1"


class AudioRestart:
    def __init__(self):
        self.activate_timer = eTimer()
        self.activate_timer.callback.append(self.restartAudio)
        if config.plugins.AudioRestart.restartSelection.value in ["standby", "both"]:
            config.misc.standbyCounter.addNotifier(self.enterStandby, initial_call=False)
        if config.plugins.AudioRestart.restartSelection.value in ["restart", "both"]:
            self.startTimer()

    def enterStandby(self, configElement):
        Standby.inStandby.onClose.append(self.endStandby)

    def endStandby(self):
        self.startTimer()

    def startTimer(self):
        self.intDelay = config.plugins.AudioRestart.restartDelay.value * 1000
        print("[AudioSync] audio restart in ", self.intDelay)
        self.activate_timer.start(self.intDelay, True)

    def restartAudio(self):
        self.activate_timer.stop()
        if self.audioIsAC3() and SystemInfo["CanDownmixAC3"] and (config.av.downmix_ac3.value is False):
            config.av.downmix_ac3.value = True
            config.av.downmix_ac3.save()
            config.av.downmix_ac3.value = False
            config.av.downmix_ac3.save()
            print("[AudioSync] audio restarted")

    def audioIsAC3(self):
        service = NavigationInstance.instance.getCurrentService()
        audio_tracks = service and service.audioTracks()
        result = False
        if audio_tracks is not None:
            n = audio_tracks and audio_tracks.getNumberOfTracks() or 0
            if n >= 0:
                selected_audio_index = audio_tracks.getCurrentTrack()
                if selected_audio_index <= n:
                    track_info = audio_tracks.getTrackInfo(selected_audio_index)
                    description = track_info.getDescription()
                    if (description.find("AC3") != -1 or description.find("AC-3") != -1) or description.find("DTS") != -1:
                        result = True
        return result


class AudioRestartSetup(Setup):
    def __init__(self, session):
        Setup.__init__(self, session, "audiorestart", plugin="Extensions/AudioRestart", PluginLanguageDomain="AudioRestart")


def sessionstart(reason, **kwargs):
    if reason == 0:
        AudioRestart()


def setup(session, **kwargs):
    session.open(AudioRestartSetup)


def Plugins(path, **kwargs):
    global plugin_path
    plugin_path = path
    plugin_list = [PluginDescriptor(name=_("Audio restart Setup"), description=_("Setup for the AudioRestart Plugin"), icon="AudioRestart.png", where=PluginDescriptor.WHERE_PLUGINMENU, fnc=setup)]
    if config.plugins.AudioRestart.restartSelection.value != "disabled":
        plugin_list.append(PluginDescriptor(name="Audio restart", description=_("Restart audio"), where=PluginDescriptor.WHERE_SESSIONSTART, fnc=sessionstart))
    return plugin_list

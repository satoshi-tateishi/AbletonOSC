from typing import Tuple, Any, Callable, Optional
import re
import math
from .handler import AbletonOSCHandler


class TrackHandler(AbletonOSCHandler):
    def __init__(self, manager):
        super().__init__(manager)
        self.class_identifier = "track"

    def init_api(self):
        def create_track_callback(func: Callable,
                                  *args,
                                  include_track_id: bool = False):
            def track_callback(params: Tuple[Any]):
                track_id = params[0]
                tracks = []

                try:
                    if isinstance(track_id, int):
                        # 数値(整数)の場合はインデックスとして処理
                        tracks = [self.song.tracks[track_id]]
                    else:
                        # 文字列の場合の処理
                        track_id_str = str(track_id)
                        if track_id_str == "*":
                            tracks = list(self.song.tracks)
                        elif track_id_str == "master":
                            tracks = [self.song.master_track]
                        elif re.match(r"^return .+$", track_id_str):
                            val = track_id_str.split(" ")[1]
                            if val.isdigit():
                                idx = int(val)
                            elif len(val) == 1 and val.isalpha():
                                idx = ord(val.upper()) - 65
                            else:
                                self.logger.error("Invalid return track ID: %s" % val)
                                return
                            tracks = [self.song.return_tracks[idx]]
                        else:
                            # トラック名として検索
                            found_track = None
                            for t in self.song.tracks:
                                if t.name == track_id_str:
                                    found_track = t
                                    break
                            
                            if found_track:
                                tracks = [found_track]
                            else:
                                self.logger.error("Track Name Error: Could not find track named '%s'" % track_id_str)
                                return
                except Exception as e:
                    self.logger.error("Track ID Error (%s): %s" % (track_id, str(e)))
                    return

                for track in tracks:
                    if include_track_id:
                        # 元の引数の型を尊重するため params[0] を使う
                        rv = func(track, *args, tuple([params[0]] + list(params[1:])))
                    else:
                        rv = func(track, *args, tuple(params[1:]))
                
                if rv is not None:
                    return (params[0], *rv)

            return track_callback

        methods = [
            "delete_device",
            "stop_all_clips"
        ]
        properties_r = [
            "can_be_armed",
            "fired_slot_index",
            "has_audio_input",
            "has_audio_output",
            "has_midi_input",
            "has_midi_output",
            "is_foldable",
            "is_grouped",
            "is_visible",
            "output_meter_level",
            "output_meter_left",
            "output_meter_right",
            "playing_slot_index",
        ]
        properties_rw = [
            "arm",
            "color",
            "color_index",
            "current_monitoring_state",
            "fold_state",
            "mute",
            "solo",
            "name"
        ]

        for method in methods:
            self.osc_server.add_handler("/live/track/%s" % method,
                                        create_track_callback(self._call_method, method))

        for prop in properties_r + properties_rw:
            self.osc_server.add_handler("/live/track/get/%s" % prop,
                                        create_track_callback(self._get_property, prop))
            self.osc_server.add_handler("/live/track/start_listen/%s" % prop,
                                        create_track_callback(self._start_listen, prop, include_track_id=True))
            self.osc_server.add_handler("/live/track/stop_listen/%s" % prop,
                                        create_track_callback(self._stop_listen, prop, include_track_id=True))
        for prop in properties_rw:
            self.osc_server.add_handler("/live/track/set/%s" % prop,
                                        create_track_callback(self._set_property, prop))

        #--------------------------------------------------------------------------------
        # Calibration points: (dB, Internal Value 0.0-1.0)
        # Measured by user on 2026-02-09
        #--------------------------------------------------------------------------------
        VOLUME_CALIBRATION = [
            (6.0, 1.0),
            (0.0, 0.85),
            (-1.0, 0.8249424),
            (-2.0, 0.8),
            (-3.0, 0.77494246),
            (-4.0, 0.75),
            (-5.0, 0.72494245),
            (-6.0, 0.7),
            (-7.0, 0.6749425),
            (-8.0, 0.65),
            (-9.0, 0.6249424),
            (-10.0, 0.5999999),
            (-11.0, 0.5749423),
            (-12.0, 0.5499998),
            (-13.0, 0.52494216),
            (-14.0, 0.4999997),
            (-15.0, 0.47494212),
            (-16.0, 0.44999963),
            (-17.0, 0.4249421),
            (-18.0, 0.39999965),
            (-19.0, 0.378422),
            (-20.0, 0.35999975),
            (-21.0, 0.3436637),
            (-22.0, 0.3288473),
            (-23.0, 0.3151538),
            (-24.0, 0.3024141),
            (-25.0, 0.29045436),
            (-26.0, 0.27908748),
            (-27.0, 0.26825535),
            (-28.0, 0.25790662),
            (-29.0, 0.24798255),
            (-30.0, 0.23843874),
            (-31.0, 0.22924192),
            (-32.0, 0.22033513),
            (-33.0, 0.21163003),
            (-34.0, 0.20318082),
            (-35.0, 0.1949828),
            (-36.0, 0.18703678),
            (-37.0, 0.17934948),
            (-38.0, 0.17170678),
            (-39.0, 0.16421922),
            (-40.0, 0.15697643),
            (-41.0, 0.14999975),
            (-42.0, 0.14288141),
            (-43.0, 0.13601433),
            (-44.0, 0.1294287),
            (-45.0, 0.122716844),
            (-46.0, 0.116201736),
            (-47.0, 0.10999971),
            (-48.0, 0.10353564),
            (-49.0, 0.097383834),
            (-50.0, 0.09134783),
            (-55.0, 0.062097773),
            (-60.0, 0.034623146),
            (-65.0, 0.014195016),
            (-67.0, 0.008032522),
            (-68.0, 0.0050417474),
            (-69.0, 0.0023759215),
            (-69.6, 0.0009176678),
            (-70.0, 0.0)
        ]

        def interpolate(val, point_a, point_b, index_val_idx, index_res_idx):
            val_a, val_b = point_a[index_val_idx], point_b[index_val_idx]
            res_a, res_b = point_a[index_res_idx], point_b[index_res_idx]
            if val_a == val_b: return res_a
            return res_a + (val - val_a) / (val_b - val_a) * (res_b - res_a)

        def db_to_float(db):
            if db >= 6.0: return 1.0
            if db <= -70.0: return 0.0
            for i in range(len(VOLUME_CALIBRATION) - 1):
                upper, lower = VOLUME_CALIBRATION[i], VOLUME_CALIBRATION[i+1]
                if db <= upper[0] and db >= lower[0]:
                    return interpolate(db, lower, upper, 0, 1)
            return 0.0

        def float_to_db(val):
            if val >= 1.0: return 6.0
            if val <= 0.0: return -70.0
            for i in range(len(VOLUME_CALIBRATION) - 1):
                upper, lower = VOLUME_CALIBRATION[i], VOLUME_CALIBRATION[i+1]
                if val <= upper[1] and val >= lower[1]:
                    return interpolate(val, lower, upper, 1, 0)
            return -70.0

        #--------------------------------------------------------------------------------
        # Volume Handlers
        #--------------------------------------------------------------------------------
        def track_set_volume(track, params: Tuple[Any] = ()):
            track.mixer_device.volume.value = db_to_float(float(params[0]))

        def track_get_volume(track, params: Tuple[Any] = ()):
            return float_to_db(track.mixer_device.volume.value),

        def track_start_listen_volume(track, params: Tuple[Any] = ()):
            def callback():
                self.osc_server.send("/live/track/get/volume", (*params, float_to_db(track.mixer_device.volume.value),))
            listener_key = ("volume", tuple(params))
            if listener_key in self.listener_functions: self._stop_mixer_listen(track, "volume", params)
            track.mixer_device.volume.add_value_listener(callback)
            self.listener_functions[listener_key] = callback
            callback()

        self.osc_server.add_handler("/live/track/get/volume", create_track_callback(track_get_volume))
        self.osc_server.add_handler("/live/track/set/volume", create_track_callback(track_set_volume))
        self.osc_server.add_handler("/live/track/start_listen/volume", create_track_callback(track_start_listen_volume, include_track_id=True))

        #--------------------------------------------------------------------------------
        # Panning Handlers (-50 to +50)
        #--------------------------------------------------------------------------------
        def track_set_panning(track, params: Tuple[Any] = ()):
            track.mixer_device.panning.value = max(-1.0, min(1.0, float(params[0]) / 50.0))

        def track_get_panning(track, params: Tuple[Any] = ()):
            return track.mixer_device.panning.value * 50.0,

        def track_start_listen_panning(track, params: Tuple[Any] = ()):
            def callback():
                self.osc_server.send("/live/track/get/panning", (*params, track.mixer_device.panning.value * 50.0,))
            listener_key = ("panning", tuple(params))
            if listener_key in self.listener_functions: self._stop_mixer_listen(track, "panning", params)
            track.mixer_device.panning.add_value_listener(callback)
            self.listener_functions[listener_key] = callback
            callback()

        self.osc_server.add_handler("/live/track/set/panning", create_track_callback(track_set_panning))
        self.osc_server.add_handler("/live/track/get/panning", create_track_callback(track_get_panning))
        self.osc_server.add_handler("/live/track/start_listen/panning", create_track_callback(track_start_listen_panning, include_track_id=True))

        #--------------------------------------------------------------------------------
        # Send Volume: -70.0dB to 0.0dB.
        # Uses dedicated calibration data for maximum accuracy.
        #--------------------------------------------------------------------------------
        SEND_CALIBRATION = [
            (0.0, 1.0),
            (-1.0, 0.97494245),
            (-2.0, 0.95),
            (-3.0, 0.92494243),
            (-4.0, 0.9),
            (-5.0, 0.8749424),
            (-6.0, 0.85),
            (-7.0, 0.82494247),
            (-8.0, 0.8),
            (-9.0, 0.7749424),
            (-10.0, 0.75),
            (-11.0, 0.72494245),
            (-12.0, 0.7),
            (-13.0, 0.67494243),
            (-14.0, 0.65),
            (-15.0, 0.6249424),
            (-16.0, 0.6),
            (-17.0, 0.57494247),
            (-18.0, 0.55),
            (-19.0, 0.5249424),
            (-20.0, 0.5),
            (-21.0, 0.4749424),
            (-22.0, 0.44999987),
            (-23.0, 0.4249423),
            (-24.0, 0.39999983),
            (-25.0, 0.37842214),
            (-26.0, 0.35999984),
            (-27.0, 0.3436638),
            (-28.0, 0.32884738),
            (-29.0, 0.31515393),
            (-30.0, 0.3024142),
            (-31.0, 0.29045448),
            (-32.0, 0.2790877),
            (-33.0, 0.26825556),
            (-34.0, 0.25790676),
            (-35.0, 0.2479827),
            (-36.0, 0.23843881),
            (-37.0, 0.22924209),
            (-38.0, 0.2203353),
            (-39.0, 0.21163017),
            (-40.0, 0.20318097),
            (-41.0, 0.19498289),
            (-42.0, 0.18703692),
            (-43.0, 0.17934962),
            (-44.0, 0.17170687),
            (-45.0, 0.16421928),
            (-46.0, 0.15697636),
            (-47.0, 0.14999978),
            (-48.0, 0.14288142),
            (-49.0, 0.13601431),
            (-50.0, 0.12942863),
            (-51.0, 0.122716784),
            (-52.0, 0.11620167),
            (-53.0, 0.109999634),
            (-54.0, 0.10353558),
            (-55.0, 0.097383775),
            (-56.0, 0.09134778),
            (-57.0, 0.085235655),
            (-58.0, 0.079489216),
            (-59.0, 0.073491305),
            (-60.0, 0.06778603),
            (-61.0, 0.062097725),
            (-62.0, 0.056433436),
            (-63.0, 0.051011093),
            (-64.0, 0.045390394),
            (-65.0, 0.04019515),
            (-66.0, 0.034623135),
            (-67.0, 0.02940422),
            (-68.0, 0.022410715),
            (-69.0, 0.013755304),
            (-69.7, 0.004913827),
            (-70.0, 0.0)
        ]

        def send_db_to_float(db):
            if db >= 0.0: return 1.0
            if db <= -70.0: return 0.0
            for i in range(len(SEND_CALIBRATION) - 1):
                upper, lower = SEND_CALIBRATION[i], SEND_CALIBRATION[i+1]
                if db <= upper[0] and db >= lower[0]:
                    return interpolate(db, lower, upper, 0, 1)
            return 0.0

        def send_float_to_db(val):
            if val >= 1.0: return 0.0
            if val <= 0.0: return -70.0
            for i in range(len(SEND_CALIBRATION) - 1):
                upper, lower = SEND_CALIBRATION[i], SEND_CALIBRATION[i+1]
                if val <= upper[1] and val >= lower[1]:
                    return interpolate(val, lower, upper, 1, 0)
            return -70.0

        def track_get_send(track, params: Tuple[Any] = ()):
            send_id = params[0]
            if isinstance(send_id, str):
                send_id = ord(send_id.upper()) - 65
            return send_id, send_float_to_db(track.mixer_device.sends[send_id].value)

        def track_set_send(track, params: Tuple[Any] = ()):
            send_id, db = params
            if isinstance(send_id, str):
                send_id = ord(send_id.upper()) - 65
            track.mixer_device.sends[send_id].value = send_db_to_float(float(db))

        self.osc_server.add_handler("/live/track/get/send", create_track_callback(track_get_send))
        self.osc_server.add_handler("/live/track/set/send", create_track_callback(track_set_send))

        #--------------------------------------------------------------------------------
        # Other Track Methods
        #--------------------------------------------------------------------------------
        def track_delete_clip(track, params: Tuple[Any]):
            track.clip_slots[params[0]].delete_clip()
        self.osc_server.add_handler("/live/track/delete_clip", create_track_callback(track_delete_clip))

        def track_get_clip_names(track, _): return tuple(slot.clip.name if slot.clip else None for slot in track.clip_slots)
        def track_get_clip_lengths(track, _): return tuple(slot.clip.length if slot.clip else None for slot in track.clip_slots)
        def track_get_clip_colors(track, _): return tuple(slot.clip.color if slot.clip else None for slot in track.clip_slots)
        self.osc_server.add_handler("/live/track/get/clips/name", create_track_callback(track_get_clip_names))
        self.osc_server.add_handler("/live/track/get/clips/length", create_track_callback(track_get_clip_lengths))
        self.osc_server.add_handler("/live/track/get/clips/color", create_track_callback(track_get_clip_colors))

        def track_get_num_devices(track, _): return len(track.devices),
        def track_get_device_names(track, _): return tuple(d.name for d in track.devices)
        self.osc_server.add_handler("/live/track/get/num_devices", create_track_callback(track_get_num_devices))
        self.osc_server.add_handler("/live/track/get/devices/name", create_track_callback(track_get_device_names))

        # Output/Input routing (Minimal implementation for brevity, can be expanded)
        def track_get_output_routing_type(track, _): return track.output_routing_type.display_name,
        self.osc_server.add_handler("/live/track/get/output_routing_type", create_track_callback(track_get_output_routing_type))

    def _set_mixer_property(self, target, prop, params: Tuple) -> None:
        getattr(target.mixer_device, prop).value = params[0]

    def _get_mixer_property(self, target, prop, params: Optional[Tuple] = ()) -> Tuple[Any]:
        return getattr(target.mixer_device, prop).value,

    def _start_mixer_listen(self, target, prop, params: Optional[Tuple] = ()) -> None:
        obj = getattr(target.mixer_device, prop)
        def cb(): self.osc_server.send("/live/%s/get/%s" % (self.class_identifier, prop), (*params, obj.value,))
        key = (prop, tuple(params))
        if key in self.listener_functions: self._stop_mixer_listen(target, prop, params)
        obj.add_value_listener(cb)
        self.listener_functions[key] = cb
        cb()

    def _stop_mixer_listen(self, target, prop, params: Optional[Tuple[Any]] = ()) -> None:
        key = (prop, tuple(params))
        if key in self.listener_functions:
            getattr(target.mixer_device, prop).remove_value_listener(self.listener_functions[key])
            del self.listener_functions[key]
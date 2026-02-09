from .handler import AbletonOSCHandler
from functools import partial
from typing import Tuple, Any

class SceneHandler(AbletonOSCHandler):
    def __init__(self, manager):
        super().__init__(manager)
        self.class_identifier = "scene"

    def init_api(self):
        # TODO: Needs unit tests

        def create_scene_callback(func, *args, include_ids: bool = False):
            def scene_callback(params: Tuple[Any]):
                try:
                    if isinstance(params[0], int):
                        scene_index = params[0]
                        scene = self.song.scenes[scene_index]
                    else:
                        scene_name = str(params[0])
                        found = False
                        for idx, s in enumerate(self.song.scenes):
                            if s.name == scene_name:
                                scene_index = idx
                                scene = s
                                found = True
                                break
                        if not found:
                            self.logger.error("Scene Name Error: Could not find scene named '%s'" % scene_name)
                            return
                except IndexError as e:
                    self.logger.error("Scene ID Error: %s" % str(e))
                    return

                callback_params = params[0:] if include_ids else params[1:]
                rv = func(scene, *args, callback_params)

                if rv is not None:
                    return (scene_index, *rv)

            return scene_callback

        methods = [
            "fire",
            "fire_as_selected",
        ]
        properties_r = [
            "is_empty",
            "is_triggered",
        ]
        properties_rw = [
            "color",
            "color_index",
            "name",
            "tempo",
            "tempo_enabled",
            "time_signature_numerator",
            "time_signature_denominator",
            "time_signature_enabled",
        ]

        for method in methods:
            self.osc_server.add_handler("/live/scene/%s" % method, create_scene_callback(self._call_method, method))

        for prop in properties_r + properties_rw:
            self.osc_server.add_handler("/live/scene/get/%s" % prop,
                                        create_scene_callback(self._get_property, prop))
            self.osc_server.add_handler("/live/scene/start_listen/%s" % prop,
                                        create_scene_callback(self._start_listen, prop, include_ids=True))
            self.osc_server.add_handler("/live/scene/stop_listen/%s" % prop,
                                        create_scene_callback(self._stop_listen, prop, include_ids=True))
        for prop in properties_rw:
            self.osc_server.add_handler("/live/scene/set/%s" % prop,
                                        create_track_callback(self._set_property, prop) if hasattr(self, "create_track_callback") else create_scene_callback(self._set_property, prop))

        # Fix for potential previous typo: create_scene_callback should be used
        for prop in properties_rw:
            self.osc_server.add_handler("/live/scene/set/%s" % prop,
                                        create_scene_callback(self._set_property, prop))
        
        #------------------------------------------------------------------------------------------------
        # The Live API does not have a `fire_selected` Scene method (or class method accessible from Python).
        # This block adds a `fire_selected` method that calls `fire_as_selected` on the selected scene.
        #------------------------------------------------------------------------------------------------
        def scene_fire_selected(params: Tuple[Any] = ()):
            selected_scene = self.song.view.selected_scene
            if selected_scene:
                selected_scene.fire_as_selected()

        self.osc_server.add_handler("/live/scene/fire_selected", scene_fire_selected)

        #--------------------------------------------------------------------------------
        # Selected scene: Get index or name
        #--------------------------------------------------------------------------------
        def scene_get_selected_scene_index(params: Tuple[Any] = ()):
            selected_scene = self.song.view.selected_scene
            for index, scene in enumerate(self.song.scenes):
                if scene == selected_scene:
                    return index,

        def scene_get_selected_scene_name(params: Tuple[Any] = ()):
            selected_scene = self.song.view.selected_scene
            if selected_scene:
                return selected_scene.name,

        self.osc_server.add_handler("/live/scene/get/selected_index", scene_get_selected_scene_index)
        self.osc_server.add_handler("/live/scene/get/selected_name", scene_get_selected_scene_name)
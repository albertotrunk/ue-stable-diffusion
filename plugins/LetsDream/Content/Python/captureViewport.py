import unreal
class capture():
  def __init__(self):
    unreal.EditorLevelLibrary.editor_set_game_view(True)
    self.actors = (actor for actor in unreal.EditorLevelLibrary.get_selected_level_actors())
    self.on_pre_tick = unreal.register_slate_pre_tick_callback(self.__pretick__)

  def __pretick__(self, deltatime):
    try:
      actor = next(self.preactors)
      shot_name = actor.get_name()
      unreal.EditorLevelLibrary.pilot_level_actor(actor)
      unreal.AutomationLibrary.take_high_res_screenshot(512,512, 'dream.png')
      unreal.EditorLevelLibrary.eject_pilot_level_actor()
    except Exception as error:
      print(error)
      unreal.unregister_slate_pre_tick_callback(self.on_pre_tick)

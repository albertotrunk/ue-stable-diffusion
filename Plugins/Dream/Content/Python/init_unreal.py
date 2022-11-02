#import unreal
#unreal.EditorUtilitySubsystem().spawn_and_register_tab(unreal.EditorAssetLibrary.load_asset("Game/Plugins/Dream/Content/tabdream.tabdream"))

#asset  = unreal.EditorAssetLibrary.load_asset(f'{unreal.Paths.project_plugins_dir()}Dream/Content/Python/tabdream.tabdream')
#eus = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
#tab = eus.spawn_and_register_tab(asset)

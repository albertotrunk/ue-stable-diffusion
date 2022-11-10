
import unreal
"""
def main():
    unreal.log("Creating Menus!")
    menus = unreal.ToolMenus.get()

    # Find the 'Main' menu, this should not fail,
    # but if we're looking for a menu we're unsure about 'if not'
    # works as nullptr check,
    main_menu = menus.find_menu("LevelEditor.MainMenu")
    if not main_menu:
        print("Failed to find the 'Main' menu. Something is wrong in the force!")

    entry = unreal.ToolMenuEntry(
                                name="Python.Tools",
                                # If you pass a type that is not supported Unreal will let you know,
                                type=unreal.MultiBlockType.MENU_ENTRY,
                                # this will tell unreal to insert this entry into the First spot of the menu
                                insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.FIRST)
    )
    entry.set_label("YourMenuItemName")
    # this is what gets executed on click
    entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, string=("from foo import bar;bar.main()"))
    # add a new menu called PyTools to the MainMenu bar. You should probably rename the last 3 properties here to useful things for you
    script_menu = main_menu.add_sub_menu(main_menu.get_name(), "PythonTools", "Tools", "PyTools")
    # add our new entry to the new menu
    script_menu.add_menu_entry("Scripts",entry)
    # refresh the UI
    menus.refresh_all_widgets()


if __name__ == '__main__':
  main()
"""

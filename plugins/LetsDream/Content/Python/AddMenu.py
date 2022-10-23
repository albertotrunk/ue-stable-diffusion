"""

    Example of extending a menu in Unreal using Python

"""

import unreal

def dream():
    if unreal.AutomationLibrary.take_high_res_screenshot(512,512, 'dream'):
        if unreal.EditorDialog.show_message("Let's dream!", "Do you want to dream?", unreal.AppMsgType.OK_CANCEL):
            unreal.PythonScriptLibrary.execute_python_command_ex('UE5Dream.py', unreal.PythonCommandExecutionMode.EXECUTE_FILE, unreal.PythonFileExecutionScope.PRIVATE)
"""
python_command (str): The command to run. This may be literal Python code, or a file (with optional arguments) that you want to run.
execution_mode (PythonCommandExecutionMode): Controls the mode used to execute the command.
file_execution_scope (PythonFileExecutionScope): Controls the scope used when executing Python files.

Returns:
tuple or None: true if the command ran successfully, false if there were errors.

command_result (str): The result of running the command. On success, for EvaluateStatement mode this will be the actual result of running the command, and will be None in all other cases. On failure, this will be the error information (typically a Python exception trace).

log_output (Array(PythonLogOutputEntry)): The log output captured while running the command.
"""
def main():

    menus = unreal.ToolMenus.get()

    # Find the 'edit' menu, this should not fail,
    # but if we're looking for a menu we're unsure about 'if not'
    # works as nullptr check,
    main_menu = menus.find_menu("LevelEditor.MainMenu")


    e = unreal.ToolMenuEntry(
        name = "Dream",
        type = unreal.MultiBlockType.MENU_ENTRY, # If you pass a type that is not supported Unreal will let you know,
    )
    e.set_label("Dream")
    e.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, '', dream())

    main_menu.add_menu_entry(main_menu.get_name(), e)

    b = unreal.ToolMenuEntry(
        name = "About",
        type = unreal.MultiBlockType.EDITABLE_TEXT, # If you pass a type that is not supported Unreal will let you know
    )
    b.set_label("A Dream of...")

    main_menu.add_menu_entry(main_menu.get_name(), b)

    menus.refresh_all_widgets()

if __name__ == '__main__':
    main()

import pkg_resources

font_files = {}

for entry_point in pkg_resources.iter_entry_points('fonts_ttf'):
    font_files.update(entry_point.load())

for font in font_files:
    globals()[font] = font_files[font]

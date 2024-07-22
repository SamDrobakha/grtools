import pkgutil

# checks dependancies
bidi_loader = pkgutil.find_loader("bidi")
if bidi_loader is not None:
    print(f"'bidi' is installed at: {bidi_loader.get_filename()}")
else:
    print("'bidi' is not installed.")

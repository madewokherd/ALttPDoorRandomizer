import os

from OverworldShuffle import __version__
OWR_VERSION = __version__

def write_appversion():
  APP_VERSION = OWR_VERSION
  if "-" in APP_VERSION:
    APP_VERSION = APP_VERSION[:APP_VERSION.find("-")]
  APP_VERSION_FILE = os.path.join(".","resources","app","meta","manifests","app_version.txt")
  with open(APP_VERSION_FILE,"w") as f:
    f.seek(0)
    f.truncate()
    f.write(APP_VERSION)

if __name__ == "__main__":
    write_appversion()

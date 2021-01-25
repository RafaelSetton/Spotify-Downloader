import cx_Freeze

executables = [cx_Freeze.Executable("main.py", base="Win32GUI", target_name="Spotify Downloader.exe",
                                    icon="icon.png", shortcut_name="Spotify Downloader.lnk")]
cx_Freeze.setup(name="Spotify Downloader",
                options={"build_exe": {'include_files': ['spotify_playlist.py', 'yt_downloader.py', 'cache.pickle']}},
                executables=executables
                )

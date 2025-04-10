import os, data

def makeconfig(filename: str = None, AlbumInfo: data.Album = None):
    with open((filename), "w") as cfg:

        cfg.writelines(
f'''name: "{AlbumInfo.name}"
year: "{AlbumInfo.year}"
author: "{AlbumInfo.author}"
albumartist: "{AlbumInfo.albumartist}"
picture: "{AlbumInfo.picture}"'''
        )
    
    cfg.close()
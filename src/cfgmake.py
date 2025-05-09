import data

class config:
    """
    A class to create a configuration file for the program.
    """
    
    def makeconfig(filename: str = None, AlbumInfo: data.Album = None) -> None:
        """
        Creates a configuration file for the program.
        Args:
            filename (str): The name of the configuration file.
            AlbumInfo (data.Album): An instance of the Album class containing album information.
            program_version (str): The version of the program.
        """
        with open((filename), "w") as cfg:
            if AlbumInfo.picture == None:
                AlbumInfo.picture = "not_exists"
            cfg.writelines(
f'''
name: "{AlbumInfo.name}"
year: "{AlbumInfo.year}"
author: "{AlbumInfo.author}"
picture: "{AlbumInfo.picture}"''')
            
            
        cfg.close()
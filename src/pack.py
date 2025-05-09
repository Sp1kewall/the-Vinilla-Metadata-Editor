import os, zipfile
import data
from tkinter import messagebox
import eyed3

# This module is responsible for packing and unpacking albums into a zip file.
def FileExtension(filename: str) -> str | None:
    """
    Returns the file extension of a given filename.
    Args:
        filename (str): The name of the file.
    Returns:
        The file extension if it exists, otherwise None.
    """

    tmp = os.path.splitext(filename)

    if len(tmp) < 2:
        return None
    
    else:
         return tmp[-1]

def pack(Album: str = None, Output: str = None, ConfigPath: str = None) -> bool:
        """
        Packs an album into a zip file.
        Args:
            Album (str): The path to the album to be packed.
            Output (str): The path where the packed album will be saved.
            ConfigPath (str): The path to the configuration file.
        Returns:
            bool: True if the packing was successful, False otherwise.
        """

        if Album == None:
            print("Album import path not specified")
            return False

        elif Output == None:
            print("Album export path is not specified")
            return False

        elif ConfigPath == None:
            print("Album config file is not specified")
            return False

        info = data.Album.GetInfo(ConfigPath)

        os.chdir(Output)

        with zipfile.ZipFile(f"{info.name}.album", "w", zipfile.ZIP_DEFLATED) as AlbumArchive:
            ErrorFiles = []
            for root, dirs, files in os.walk(Album):
                for file in files:
                    if FileExtension(file).lower() in data.Album.AudioExtensions:

                        audiofile = eyed3.load(f"{root}{os.sep}{file}")

                        try:
                            if audiofile.tag is None:
                                ErrorFiles.append(file)

                            audiofile.tag.album = info.name
                            audiofile.tag.album_artist = info.author
                            audiofile.tag.title = os.path.splitext(file)[0]
                            
                            if info.picture != None:
                                audiofile.tag.images.set(3, open(info.picture, 'rb').read(), 'image/jpeg')

                            audiofile.tag.save()

                        except AttributeError:
                            ErrorFiles.append(file)
                            continue



                        AlbumArchive.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(Album)))
            
            AlbumArchive.close()

        if ErrorFiles == []:
            messagebox.showinfo(title="Success", message="Album file is created")

        else:
            messagebox.showwarning(title="Success, but...", message=f"Album file is created, but {len(ErrorFiles)} files wasnt added to Album, because its corruped")
        return True

def unpack(AlbumPath: str = None, OutputPath = None):
    with zipfile.ZipFile(AlbumPath, "r") as zip:
        zip.extractall(path=OutputPath)

        messagebox.showinfo(title="Success", message="Album was extracted")

    zip.close()
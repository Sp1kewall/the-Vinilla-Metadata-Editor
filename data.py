import yaml

class Album:
    AudioExtensions = [
    ".mp3",  # MPEG Audio Layer III
    ".wav",  # Waveform Audio File Format
    ".aac",  # Advanced Audio Coding
    ".ogg",  # Ogg Vorbis
    ".flac", # Free Lossless Audio Codec
    ".m4a",  # MPEG-4 Audio
    ".wma",  # Windows Media Audio
    ".aiff", # Audio Interchange File Format
    ".alac", # Apple Lossless Audio Codec
    ".amr",  # Adaptive Multi-Rate audio codec
    ".ape",  # Monkey's Audio
    ".opus", # Opus audio codec
    ".mid",  # MIDI file
    ".midi", # MIDI file
    ".ac3",  # Audio Codec 3
    ".dts",  # Digital Theater Systems
    ".ra",   # RealAudio
    ".rm",   # RealMedia
    ".mp2",  # MPEG Audio Layer II
    ".mpa",  # MPEG Audio Layer I/II
    ".webm", # WebM audio
    ".3ga",  # 3GPP audio file
    ".8svx", # 8SVX audio file
    ".cda",  # CD Audio Track
    ".ivs",  # IVS audio file
    ".mka",  # Matroska Audio
    ".pcm",  # Pulse-code modulation
    ".snd",  # SND audio file
    ".voc",  # Creative Voice File
    ".weba", # Web Audio
]




    def __init__(self, name: str = None, year: int = None, author: str = None, picture: str = None, albumartist: str = None):
        self.name = name
        self.year = year
        self.picture = picture
        self.albumartist = albumartist

        if author is None:
            self.author = ""
        else:
            self.author = author




    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name}, year={self.year}, \
                  author={self.author}, picture={self.picture}, albumartist={self.albumartist}'




    def GetInfo(Path):

        with open(Path, "r") as Data:
            print(Path)

            work = yaml.load(Data, Loader=yaml.FullLoader)

            name = work.get("name")
            year = work.get("year")
            author = work.get("author")
            picture = work.get("picture")
            albumartist = work.get("albumartist")

            return Album(name, year, author, picture, albumartist)
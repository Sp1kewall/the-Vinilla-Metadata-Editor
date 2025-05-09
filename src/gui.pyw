from tkinter import *
from tkinter import Listbox, END, messagebox
from tkinter import filedialog
from customtkinter import CTkButton, CTkLabel, CTk, CTkEntry

import cfgmake, data, pack, updates
import os, eyed3, sys, webbrowser, requests

cfgpath = None
albumpath = None
AlbumData = None

class File:
    """File operations for the Vinylla Metadata Editor."""

    def OpenConfig():
        global cfgpath
        tmp = filedialog.askopenfile(title="Load config", filetypes=[("YAML Config files", ".yaml")])

        if tmp == "" or tmp == None:
            messagebox.showwarning(title="Config", message="Configuration file is not selected")
        
        else:
            if (tmp.name).split(".")[-1].lower() != "yaml":
                messagebox.showwarning(title="Config", message="Configuration file is not selected")
            else:
                cfgpath = tmp.name
                messagebox.showinfo(title="Config", message="Config file is loaded")

    def OpenAlbumPath():
        global albumpath
        tmp = filedialog.askdirectory(title="Album source")

        if tmp == "" or tmp == None:
            messagebox.showwarning(title="Album source", message="Album source directory is not selected")
        
        else:
            albumpath = tmp
            messagebox.showinfo(title="Album source", message="Album source directory is loaded")
            
    def EnhancedChangeMusicNumbering():
        window = CTk()
        window.configure(fg_color=BackgroundColor)

        window.title("Audio Numbering")
        window.resizable(False, False)

        if sys.platform.lower() == "nt":
            window.iconbitmap(default="resources/icon.ico")

        CTkLabel(window, text="Audio Numbering", font=("Open Sans", 16, 'bold'), text_color=MinorColor).pack(pady=10)

        frame = Frame(window, bg=BackgroundColor)
        frame.pack(pady=10)

        listbox = Listbox(
            frame,
            selectmode="single",
            width=50,
            height=15,
            font=("Open Sans", 12),
            selectbackground=AccentColor,
            selectforeground="white",
            activestyle="none"
        )
        listbox.grid(row=0, column=0, rowspan=4, padx=10)

        scrollbar = Scrollbar(frame, orient="vertical", command=listbox.yview)
        scrollbar.grid(row=0, column=1, rowspan=4, sticky="ns")
        listbox.config(yscrollcommand=scrollbar.set)

        audio_files = []

        def load_album_path():
            nonlocal audio_files
            listbox.delete(0, END)
            audio_files.clear()

            if not albumpath:
                messagebox.showerror("Error", "Album path is not set. Please load an album folder first.")
                return

            for file_name in sorted(os.listdir(albumpath)):
                file_path = os.path.join(albumpath, file_name)
                if os.path.isfile(file_path) and os.path.splitext(file_name)[1].lower() in data.Album.AudioExtensions:
                    audio_files.append(file_path)
                    listbox.insert(END, file_name)

        def move_item(direction):
            selected = listbox.curselection()
            if not selected:
                return
            index = selected[0]
            new_index = index + direction
            if 0 <= new_index < listbox.size():
                audio_files[index], audio_files[new_index] = audio_files[new_index], audio_files[index]
                listbox.delete(index)
                listbox.insert(new_index, os.path.basename(audio_files[new_index]))
                listbox.select_set(new_index)

        def move_cursor(direction):
            selected = listbox.curselection()
            if not selected:
                return
            index = selected[0]
            new_index = index + direction
            if 0 <= new_index < listbox.size():
                listbox.select_clear(index)
                listbox.select_set(new_index)

        def save_order():
            for idx, file_path in enumerate(audio_files, start=1):
                audiofile = eyed3.load(file_path)
                if audiofile.tag is None:
                    audiofile.initTag()
                audiofile.tag.track_num = idx
                audiofile.tag.save()

            messagebox.showinfo("Success", "Track numbers have been updated successfully!")
            window.destroy()

        button_frame = Frame(window, bg=BackgroundColor)
        button_frame.pack(pady=10)

        CTkButton(button_frame, text="Move Up", command=lambda: move_item(-1), font=("Open Sans", 12, 'bold'),
                  fg_color=AccentColor, hover_color=hover_global, corner_radius=32).grid(row=0, column=0, padx=10, pady=5)

        CTkButton(button_frame, text="Move Down", command=lambda: move_item(1), font=("Open Sans", 12, 'bold'),
                  fg_color=AccentColor, hover_color=hover_global, corner_radius=32).grid(row=0, column=1, padx=10, pady=5)

        CTkButton(button_frame, text="Save Order", command=save_order, font=("Open Sans", 12, 'bold'),
                  fg_color=AccentColor, hover_color=hover_global, corner_radius=32).grid(row=0, column=2, padx=10, pady=5)

        # Bind keyboard events
        window.bind("<Up>", lambda event: move_item(-1))
        window.bind("<Down>", lambda event: move_item(1))
        window.bind("<Left>", lambda event: move_cursor(-1))
        window.bind("<Right>", lambda event: move_cursor(1))

        load_album_path()
        window.mainloop()

    def ExtractAlbum():
        AlbumPathOpen = filedialog.askopenfilename(title="Album file", filetypes=[("ALBUM Archive", ".album")])

        if AlbumPathOpen == "" or AlbumPathOpen == None:
            return

        AlbumPathOut = filedialog.askdirectory(title="Album file")

        if AlbumPathOut == "" or AlbumPathOut == None:
            return

        pack.unpack(AlbumPathOpen, AlbumPathOut)


class Make:
    """Make operations for the Vinylla Metadata Editor."""
    
    def CreateAlbumConfig():
        CfgWindow = CTk()

        CfgWindow.configure(fg_color=BackgroundColor)

        if sys.platform.lower() != "nt":
            pass
        else:
            CfgWindow.iconbitmap(default="resources/icon.ico")
        
        CfgWindow.title("Album Configuration")
        CfgWindow.resizable(False, False)

        def select_output():
            output = filedialog.asksaveasfilename(
                title="Output path",
                filetypes=[("YAML Config files", ".yaml")]
            )
            if output:
                output_entry.delete(0, "end")
                output_entry.insert(0, output)

        def select_cover():
            cover_path = filedialog.askopenfilename(
                title="Select Cover Image",
                filetypes=[("Image files", "*.jpg *.jpeg *.png")]
            )
            if cover_path:
                cover_path_entry.delete(0, "end")
                cover_path_entry.insert(0, cover_path)

        def save_to_list():
            title = title_entry.get()
            year = year_entry.get()
            author = author_entry.get()
            cover_path = cover_path_entry.get()
            output = output_entry.get()


            if not title or not year or not author or not output:
                messagebox.showwarning("Error", "All fields except Cover Path are required!")
                return

            cfgmake.config.makeconfig(output, data.Album(title, year, author, cover_path))
            messagebox.showinfo("Success", "Config file created successfully!")

            CfgWindow.destroy()

        CTkLabel(CfgWindow, text="Album Author:", text_color=MinorColor, font=("Open Sans", 12, "bold"),).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        author_entry = CTkEntry(CfgWindow, width=150)
        author_entry.grid(row=1, column=1, padx=10, pady=5)

        CTkLabel(CfgWindow, text="Title:", text_color=MinorColor, font=("Open Sans", 12, "bold"),).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        title_entry = CTkEntry(CfgWindow, width=150)
        title_entry.grid(row=2, column=1, padx=10, pady=5)

        CTkLabel(CfgWindow, text="Year:", text_color=MinorColor, font=("Open Sans", 12, "bold"),).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        year_entry = CTkEntry(CfgWindow, width=150)
        year_entry.grid(row=3, column=1, padx=10, pady=5)

        CTkLabel(CfgWindow, text="Cover Path:", text_color=MinorColor, font=("Open Sans", 12, "bold"),).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        cover_path_entry = CTkEntry(CfgWindow, width=150)
        cover_path_entry.grid(row=4, column=1, padx=10, pady=5)
        CTkButton(CfgWindow, border_width=2, text="Browse", command=select_cover, fg_color=AccentColor, hover_color=hover_global, corner_radius=32, height=25, border_color=MinorColor).grid(row=4, column=2, padx=10, pady=5)

        CTkLabel(CfgWindow, text="Output Path:", text_color=MinorColor, font=("Open Sans", 12, "bold"),).grid(row=5, column=0, padx=10, pady=5, sticky="e")
        output_entry = CTkEntry(CfgWindow, width=150)
        output_entry.grid(row=5, column=1, padx=10, pady=5)
        CTkButton(CfgWindow, border_width=2, text="Browse", command=select_output, fg_color=AccentColor, hover_color=hover_global, corner_radius=32, height=25, border_color=MinorColor).grid(row=5, column=2, padx=10, pady=5)

        CTkButton(CfgWindow, border_width=2, text="Make Config", command=save_to_list, fg_color=AccentColor, hover_color=hover_global, corner_radius=32, height=25, border_color=MinorColor).grid(row=6, column=1, pady=10)

        CTkButton(CfgWindow, border_width=2, text="Close", command=CfgWindow.destroy, fg_color=AccentColor, hover_color=hover_global, corner_radius=32, height=25, border_color=MinorColor).grid(row=7, column=1, pady=10)

        CfgWindow.mainloop()

    def BuildAlbum():
        try:
            if albumpath == None or os.path.exists(albumpath) == False:
                messagebox.showerror(title="Error", message="You have not selected the path to the album")
                return

            if cfgpath == None or os.path.exists(cfgpath) == False:
                messagebox.showerror(title="Error", message="You have not selected the path to the config file")
                return
            
            output = filedialog.askdirectory(title="Output directory")

            sure = messagebox.askyesno(title="Are you sure?", message=f"Are you sure you want to change audio file metadata? This action cannot be undone\nAlbum - {albumpath}\nConfig - {cfgpath}")
            if sure == False:
                return
            
            pack.pack(albumpath, output, cfgpath)

            return
        
        except Exception as e:
            messagebox.showerror(title="Error", message=f"We got error: {e}")
            exit()

def create_main_window():
    root = CTk()
    root.configure(fg_color=BackgroundColor)

    def on_closing():
        exit()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.title("Vinylla Metadata Editor")
    root.geometry("600x510")

    if sys.platform.lower() == "nt":
        root.iconbitmap(default="resources/icon.ico")

    root.resizable(False, False)

    # Header
    header_label = CTkLabel(
        root,
        text="Welcome to Vinylla Metadata Editor",
        font=("Open Sans", 18, "bold"),
        text_color=MinorColor,
        anchor="center"
    )
    header_label.pack(pady=20)

    # Instructions
    instructions_frame = Frame(root, bg=BackgroundColor)
    instructions_frame.pack(pady=10)

    steps = [
        "1. Open album folder",
        "2. Open or create a config file",
        "3. Optionally, change music numbering",
        "4. Build the album!",
    ]

    for step in steps:
        step_label = CTkLabel(
        instructions_frame,
        text=step,
        font=("Open Sans", 14, "bold"),
        text_color=MinorColor,
        anchor="w"
        )
        step_label.pack(fill="x", padx=20, pady=5)

    # Buttons
    button_frame = Frame(root, bg=BackgroundColor)
    button_frame.pack(pady=20)

    CTkButton(
        button_frame,
        text="Load Album Folder",
        command=File.OpenAlbumPath,
        font=("Open Sans", 12, "bold"),
        fg_color=AccentColor,
        text_color=MinorColor,
        hover_color=hover_global,
        corner_radius=32,
        width=200
    ).grid(row=0, column=0, padx=10, pady=10)

    CTkButton(
        button_frame,
        text="Load Config File",
        command=File.OpenConfig,
        font=("Open Sans", 12, "bold"),
        fg_color=AccentColor,
        text_color=MinorColor,
        hover_color=hover_global,
        corner_radius=32,
        width=200
    ).grid(row=0, column=1, padx=10, pady=10)

    CTkButton(
        button_frame,
        text="Change Music Numbering",
        command=File.EnhancedChangeMusicNumbering,
        font=("Open Sans", 12, "bold"),
        fg_color=AccentColor,
        text_color=MinorColor,
        hover_color=hover_global,
        corner_radius=32,
        width=200
    ).grid(row=1, column=0, padx=10, pady=10)

    CTkButton(
        button_frame,
        text="Create Config File",
        command=Make.CreateAlbumConfig,
        font=("Open Sans", 12, "bold"),
        fg_color=AccentColor,
        text_color=MinorColor,
        hover_color=hover_global,
        corner_radius=32,
        width=200
    ).grid(row=1, column=1, padx=10, pady=10)

    CTkButton(
        button_frame,
        text="Build Album",
        command=Make.BuildAlbum,
        font=("Open Sans", 12, "bold"),
        fg_color=AccentColor,
        text_color=MinorColor,
        hover_color=hover_global,
        corner_radius=32,
        width=200
    ).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    CTkButton(
        button_frame,
        text="Extract Album",
        command=File.ExtractAlbum,
        font=("Open Sans", 12, "bold"),
        fg_color=AccentColor,
        text_color=MinorColor,
        hover_color=hover_global,
        corner_radius=32,
        width=200
    ).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Footer
    footer_label = CTkLabel(
        root,
        text=f"the Vinylla Metadata Editor (VME) Version {version} {VersionType}",
        font=("Open Sans", 10, "italic"),
        text_color=MinorColor,
        anchor="center"
    )
    footer_label.pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":

    # Theme vars
    MinorColor = "#CDA47B"
    BackgroundColor = "#382020"
    AccentColor = "#9F4125"
    hover_global = "#292929"

    # Version info
    version = "0.2"
    VersionType = "beta"

    # Check for updates
    try:
        response = requests.get("https://www.google.com", timeout=5)
        response.raise_for_status()
    except (requests.ConnectionError, requests.Timeout):
        create_main_window()
    
    updater = updates.Update("https://api.github.com/repos/Sp1kewall/the-Vinylla-Metadata-Editor/releases", os.getcwd())
    latest_version, assets = updater.check_for_updates()

    if latest_version and float(latest_version) > float(version):
        with open("versionignore", "r") as f:
            versions = f.read().splitlines()

            if latest_version not in versions:
                if messagebox.askyesno("Update Available", f"Version {latest_version} is available. Do you want to download it?"):
                    webbrowser.open(assets["browser_download_url"])
                    exit()
                else:
                    with open("versionignore", "w") as f:
                        f.write(f"{latest_version}\n")
                        f.close()
    create_main_window()
from tkinter import *
from tkinter import Tk, Listbox, Button, Label, END, messagebox, font
from tkinter import filedialog

import cfgmake, data, pack

import os, eyed3

cfgpath = None
albumpath = None
AlbumData = None



class File:
    def OpenConfig():
        global cfgpath
        tmp = filedialog.askopenfile(title="Load config", filetypes=[("YAML Config files", ".yaml")])

        if tmp == "" or tmp == None:
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




    def ChangeMusicNumbering():
        window = Tk()
        window.title("Audio numbering")

        custom_font = font.Font(size=12)

        label = Label(window, text="Select a folder with audio files:", font=custom_font)
        label.pack(pady=10)

        listbox = Listbox(
            window,
            selectmode="single",
            width=50,
            height=15,
            font=custom_font,
            selectbackground="blue",
            selectforeground="white",
            activestyle="none"
        )
        listbox.pack(pady=10)

        audio_files = []
        order_dict = {}
        folder_path = None

        def select_folder():
            nonlocal folder_path, audio_files
            listbox.delete(0, END)
            audio_files.clear()

            if albumpath == None or albumpath == "":
                folder_path = filedialog.askdirectory()
                if not folder_path:
                    return
            
            else:
                folder_path = albumpath

            files_with_track_num = []
            files_without_track_num = []

            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path) and os.path.splitext(file_name)[1].lower() in data.Album.AudioExtensions:
                    audiofile = eyed3.load(file_path)

                    try:
                        track_num = audiofile.tag.track_num[0] if audiofile.tag and audiofile.tag.track_num else None
                    except AttributeError:
                        continue

                    if track_num is not None:
                        files_with_track_num.append((track_num, file_name))
                    else:
                        files_without_track_num.append(file_name)

            files_with_track_num.sort(key=lambda x: x[0])
            files_without_track_num.sort()

            sorted_files = [file_name for _, file_name in files_with_track_num] + files_without_track_num

            for file_name in sorted_files:
                audio_files.append(os.path.join(folder_path, file_name))
                listbox.insert(END, file_name)

        def move_up():
            selected = listbox.curselection()
            if not selected:
                return
            index = selected[0]
            if index == 0:
                return
            audio_files[index], audio_files[index - 1] = audio_files[index - 1], audio_files[index]
            listbox.insert(index - 1, listbox.get(index))
            listbox.delete(index + 1)
            listbox.select_set(index - 1)

        def move_down():
            selected = listbox.curselection()
            if not selected:
                return
            index = selected[0]
            if index == listbox.size() - 1:
                return
            audio_files[index], audio_files[index + 1] = audio_files[index + 1], audio_files[index]
            listbox.insert(index + 2, listbox.get(index))
            listbox.delete(index)
            listbox.select_set(index + 1)

        def select_previous():
            selected = listbox.curselection()
            if not selected:
                return
            index = selected[0]
            if index > 0:
                listbox.select_clear(index)
                listbox.select_set(index - 1)

        def select_next():
            selected = listbox.curselection()
            if not selected:
                return
            index = selected[0]
            if index < listbox.size() - 1:
                listbox.select_clear(index)
                listbox.select_set(index + 1)

        def save_order():
            nonlocal order_dict
            order_dict.clear()
            for idx in range(listbox.size()):
                file_name = listbox.get(idx)
                order_dict[file_name] = idx + 1

            for file_name, track_num in order_dict.items():
                file_path = os.path.join(folder_path, file_name)
                audiofile = eyed3.load(file_path)
                if audiofile.tag is None:
                    audiofile.initTag()
                audiofile.tag.track_num = track_num
                audiofile.tag.save()

            messagebox.showinfo("Order Saved", "Track numbers have been successfully written to the metadata!")

        select_button = Button(window, text="Select Folder", command=select_folder, font=custom_font)
        select_button.pack(pady=10)

        save_button = Button(window, text="Save Order", command=save_order, font=custom_font)
        save_button.pack(pady=10)

        window.bind("<Up>", lambda event: move_up())
        window.bind("<Down>", lambda event: move_down())
        window.bind("<Left>", lambda event: select_previous())
        window.bind("<Right>", lambda event: select_next())

        select_folder()
        window.mainloop()




    def ExtractAlbum():
        AlbumPathOpen = filedialog.askopenfilename(title="Album file", filetypes=[("ALBUM Archive", ".album")])

        while AlbumPathOpen == "" or AlbumPathOpen == None:
            ask = messagebox.askyesno(title="Album File", message="You have not selected an album file. Do you want to select it again?")

            if ask == False:
                return
            
            AlbumPathOpen = filedialog.askopenfilename(title="Album file", filetypes=[("ALBUM Archive", ".album")])

        AlbumPathOut = filedialog.askdirectory(title="Album file")

        while AlbumPathOut == "" or AlbumPathOut == None:
            ask = messagebox.askyesno(title="Album File", message="You have not selected an album extracting directory. Do you want to select it again?")

            if ask == False:
                return
            
            AlbumPathOut = filedialog.askdirectory(title="Album file")

        pack.unpack(AlbumPathOpen, AlbumPathOut)


class Make:

    def CreateAlbumConfig():
        CfgWindow = Tk()
        CfgWindow.title("Album Configuration")
        CfgWindow.resizable(False, False)

        album_data = []

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
            artist = artist_entry.get()
            output = output_entry.get()

            print(title, year, author, cover_path, artist, output)

            if not title or not year or not author or not artist:
                messagebox.showwarning("Error", "All fields except Cover Path are required!")
                return

            album_data.append(title)
            album_data.append(year)
            album_data.append(author)
            album_data.append(cover_path)
            album_data.append(artist)

            cfgmake.makeconfig(output, data.Album(album_data[0], album_data[1], album_data[2], album_data[3], album_data[4]))
            messagebox.showinfo("Success", "Config is ready")

            CfgWindow.destroy()


        Label(CfgWindow, text="Artist:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        artist_entry = Entry(CfgWindow, width=40)
        artist_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(CfgWindow, text="Author:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        author_entry = Entry(CfgWindow, width=40)
        author_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(CfgWindow, text="Title:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        title_entry = Entry(CfgWindow, width=40)
        title_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(CfgWindow, text="Year:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        year_entry = Entry(CfgWindow, width=40)
        year_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(CfgWindow, text="Cover Path:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        cover_path_entry = Entry(CfgWindow, width=40)
        cover_path_entry.grid(row=4, column=1, padx=10, pady=5)
        Button(CfgWindow, text="Browse", command=select_cover).grid(row=4, column=2, padx=10, pady=5)

        Label(CfgWindow, text="Output Path:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        output_entry = Entry(CfgWindow, width=40)
        output_entry.grid(row=5, column=1, padx=10, pady=5)
        Button(CfgWindow, text="Browse", command=select_output).grid(row=5, column=2, padx=10, pady=5)

        Button(CfgWindow, text="Make Config", command=save_to_list).grid(row=6, column=1, pady=10)

        Button(CfgWindow, text="Close", command=CfgWindow.destroy).grid(row=7, column=1, pady=10)

        CfgWindow.mainloop()




    def BuildAlbum():
        if albumpath == None:
            messagebox.showerror(title="Error", message="You have not selected the path to the album")
            return

        if cfgpath == None:
            messagebox.showerror(title="Error", message="You have not selected the path to the config file")
            return
        
        output = filedialog.askdirectory(title="Output directory")

        sure = messagebox.askyesno(title="Are you shure?", message=f"Are you sure you want to change audio file metadata? This action cannot be undone\nAlbum - {albumpath}\nConfig - {cfgpath}")

        if sure == False:
            return
        
        pack.pack(albumpath, output, cfgpath)

        return




def main():
    root = Tk()

    root.title("Vinylla")
    root.geometry("450x300")
    root.resizable(False, False)

    file_menu = Menu(tearoff=0)
    file_menu.add_command(label="Load config", command=File.OpenConfig)
    file_menu.add_command(label="Load Album", command=File.OpenAlbumPath)
    file_menu.add_command(label="Change music numbering", command=File.ChangeMusicNumbering)
    file_menu.add_command(label="Extract Album", command=File.ExtractAlbum)

    make_menu = Menu(tearoff=0)
    make_menu.add_command(label="Create Config", command=Make.CreateAlbumConfig)
    make_menu.add_command(label="Build Album", command=Make.BuildAlbum)

    main_menu = Menu(tearoff=0)
    main_menu.add_cascade(label="File...", menu=file_menu)
    main_menu.add_cascade(label="Make...", menu=make_menu)


    root.config(menu=main_menu)

    label1 = Label(
        root, 
        text="1. Open album folder", 
        font=('Lexend', 14, 'bold'),
        anchor='w',
        padx=20
    )
    label1.pack(fill='x', pady=10)

    label2 = Label(
        root, 
        text="2. Open config file (create if doesn't exist)", 
        font=('Lexend', 14, 'bold'),
        anchor='w',
        padx=20
    )
    label2.pack(fill='x', pady=10)

    label3 = Label(
        root, 
        text="3. Build the album!", 
        font=('Lexend', 14, 'bold'),
        anchor='w',
        padx=20
    )
    label3.pack(fill='x', pady=10)

    footer_label = Label(
        root,
        text=f"the Vinylla Metadata Editor (VME) Version {version} {VersionType}",
        font=('Lexend', 8, 'italic'),
        fg='gray',
        anchor='center',
        pady=10
    )
    footer_label.pack(side='bottom', fill='x')

    root.mainloop()




if __name__ == "__main__":
    version = "0.1"
    VersionType = "beta"

    main()
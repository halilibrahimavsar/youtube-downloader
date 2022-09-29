"""
    YOUTUBE DOWNLOADER

Author : Halil ibrahim AVSAR
"""

from os import system, getcwd, name, path
from sys import executable
from time import sleep
from colorama import init, Fore


init(autoreset=True)
red = Fore.RED
rst = Fore.RESET
green = Fore.GREEN
blue = Fore.BLUE
yellv = Fore.YELLOW


def shell_clear():
    system("clear" if name != "nt" else "cls")

def byte_to_mb(byte_size):
    return round(((byte_size / 1024) / 1024), 2)

def progress_function(stream, chunk, byte_remaining):
    perc = 100
    finished = False
    remain = round((byte_remaining/stream.filesize)*perc)
    remain = str(abs(remain - 100))
    sym1 = ">"*(int(remain)//4)
    sym2 = "<"*(int(remain)//4)
    total_mb = byte_to_mb(stream.filesize)
    remain_mb = round(abs(byte_to_mb(byte_remaining) - total_mb), 2)
    shell_clear()
    green
    print(blue + "|{:<25}TARGET{:>25}| {}%  [{}/{} Mb]         ".format(sym1,sym2, remain, remain_mb, total_mb),flush=True, end="\r")
    perc += 1
    if remain == "100":
        finished = True

    if finished:
        shell_clear()
        for i in range(46): #finish effect
            print(green + "»{:>23}DOWNLOADED{:<23}«".format("<"*(i//2), ">"*(i//2)), end="\r")
            sleep(0.0005)
        print()


def progress_finished(stream, file_path):
    print("-"*40)
    try:
        print(f"Downloaded : {stream.title[:24]}...", f"Resolution : {stream.resolution}",\
             f"Fps : {stream.fps}", f"Type : {stream.type}", f"VIDEO-AUDIO codecs : {stream.codecs}", f"Path of File : {getcwd()}", sep="\n")
    except AttributeError:
        print("Some of attributes not found...")
    print("-"*40)

def single_video(url, path="."):
    shell_clear()
    yt_obj = YouTube(url, on_progress_callback=progress_function, on_complete_callback=progress_finished)
    print("Checking Details  » [' {:^30} ']".format(yt_obj.title))

    yt_streams = {}

    for i, j in enumerate(yt_obj.streams):
        if j.resolution:
            yt_streams[i] = [j.itag, j.resolution, j.type]
        else:
            yt_streams[i] = [j.itag, j.abr, j.type]
    
    for num, res in yt_streams.items():
        print("    [{:^2}] : Resolution > [{:^8}]    Type > [{}]".format(num, res[1], res[2]))
    while True:
        selected_res = int(input("Resolution num :"))
        if selected_res not in yt_streams.keys():
            print("Wrong number selected!")
            continue
        else:
            print("Connecting Stream...")   
            fltr = yt_obj.streams.get_by_itag(yt_streams.get(selected_res)[0])
            fltr.download(output_path=path)
            break

def playlist_as_mp3(playlist_url="", path="."):
    playlst = Playlist(playlist_url)
    for i in playlst:
        single_video(i)


def launch():
    msg = """
       [1] : Single video url
       [2] : Playlist url
    """

    while True:
        shell_clear()
        print(msg)
        choice = input("Select which you want to [Default 1] :")
        if choice not in ["1", "2", ""]:

            print("Ooops, something wrong typed ! [type 1 or 2]")
            continue
        
        path_of_vid = input("Path : [Default is current directory] : ") 
        while (not path.exists(path_of_vid) and path_of_vid != ""):
            print("Path is not exists, Try again !")
            path_of_vid = input("Path : [Default is current directory] : ")


        if choice == "1" or choice == "":
            single_video(input("Just copy video url link into here : "), path=path_of_vid)

        elif choice == "2":
            playlist_as_mp3(playlist_url=input("Just copy playlist link into here :"), path=path_of_vid)


        while True:
            new_loop = input("\nDo you wanna continue the new download ? [Y/N] : ")
            if new_loop.lower() == "y":
                break
            elif new_loop.lower() == "n":
                exit()
            else:
                print("What do you mean with '{}'? :) ".format(new_loop))
                continue
            

if __name__ == "__main__":
    launch() #launch the program






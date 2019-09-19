# Imports
from eyed3 import id3
import os


def get_mp3_files(directory):
    return [os.path.join(directory,x) for x in os.listdir(directory) if '.mp3' in x and os.path.isfile(os.path.join(directory,x))]

def sort_songs_by_title(direcotry):
    mp3_files = get_mp3_files(direcotry)
    mp3_tuples = []

    for mp3 in mp3_files:
        tag = id3.Tag()
        tag.parse(mp3)
        mp3_tuples.append((mp3, tag.title))
    
    sorted_mp3_tuples = sorted(mp3_tuples, key = lambda x: x[1].lower())
    counter = 1
    for mp3_path, mp3_title in sorted_mp3_tuples:
        tag = id3.Tag()
        tag.parse(mp3_path)
        tag.track_num = counter
        tag.save()
        counter += 1

def main():
    directory = r'D:\Music\Soundtrack\Assorted Anime Songs'
    sort_songs_by_title(direcotry)
    

if __name__ == "__main__":
    main()
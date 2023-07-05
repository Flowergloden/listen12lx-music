import sqlite3
import json
import sys
import fnmatch

# listen1 to lx-music
num_id = 0000000000000
order = 0
source_dict = {
    'kuwo': 'kw',
    'kugou': 'kg',
    'qq': 'tx',
    'netease': 'wy',
    'migu': 'mg',
}
record_file = open('unknownSongsList.txt', 'w', encoding='utf-8')

def create_new_list(name):
    global num_id
    global order

    full_id = 'userlist_' + str(num_id)
    c.execute('INSERT INTO my_list (id, name, position) VALUES (?, ?, ?)', (full_id, name, order))
    num_id += 1
    order += 1

    print('create list ' + name)

    return full_id


def record_unknown_songs(item):
    global record_file

    try:
        song_name = item.get('title', 'unknown')
        singer = item.get('artist', 'unknown')
        album_name = item.get('album', 'unknown')
    except KeyError:
        return

    print('    unknown song ' + song_name)
    record_file.write(song_name + ' - ' + singer + ' - ' + album_name + '\n')

def insert_song(item, list_id):
    global c

    try:
        source = source_dict[item['source']]
        song_id = item['id'].split('_')[1]
        item_id = source + '_' + song_id
        song_name = item['title']
        singer = item['artist']
        album_name = item['album']
        album_id = item['album_id'].split('_')[1]
        pic_url = item['img_url']
    except KeyError:
        record_unknown_songs(item)
        return

    meta = json.dumps({"songId": song_id, "albumName": album_name, "picUrl": pic_url, "albumId": album_id})
    c.execute('INSERT INTO my_list_music_info (id, listId, name, singer, source, meta) VALUES (?, ?, ?, ?, ?, ?)',
              (item_id, list_id, song_name, singer, source, meta))
    print('    insert song ' + song_name)


def listen1_to_lxmusic():
    global data
    global c

    for listName, lst in data.items():
        if 'myplaylist' not in listName:
            continue
        list_title = lst['info']['title']
        list_id = create_new_list(list_title)
        for item in lst['tracks']:
            insert_song(item, list_id)


# lx-music to listen1
def lxmusic_to_listen1():
    pass


# Check direction
origin = sys.argv[1]
target = sys.argv[2]
pattern_listen1 = '*.json'
pattern_lx_music = '*.db'

if fnmatch.fnmatch(origin, pattern_listen1):
    print('listen1 to lx-music')
    file = open(origin, encoding='utf-8')
    data = json.load(file)
    db = sqlite3.connect(target)
    c = db.cursor()
    listen1_to_lxmusic(origin)
    db.commit()
    db.close()
    file.close()
elif fnmatch.fnmatch(origin, pattern_lx_music):
    print('lx-music to listen1')
    lxmusic_to_listen1(origin)
else:
    print('Unknown file type')

record_file.close()

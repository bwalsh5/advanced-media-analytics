
import lyricsgenius as lg
from lyricsgenius import Genius

genius = lg.Genius('KMvkiE6_Ypzv3N8opyenQ_PAybeSiw1363k00mAUTZyxw-SElfibYpNbC6jCob7G', skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
genius.timeout = 20

fiftySecond = genius.search_album("52nd Street", "Billy Joel")

fiftySecond.save_lyrics(filename='fiftySecond.json')

import sys
import music_tag
from os import listdir
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Main(QMainWindow):
    def __init__(self):
        self.folder = ""
        self.comment = "redactor_ID3fromIly"
        self.filenames = ""
        self.album_image = ''
        super().__init__()
        uic.loadUi('front.ui', self)
        self.start_process_button.clicked.connect(self.master_traks)
        self.folder_link.clicked.connect(self.get_folder)
        self.album_image_link.clicked.connect(self.get_image_for_album)
        self.clear_button.clicked.connect(self.clear)
    
    def get_folder(self):
        self.folder = QFileDialog.getExistingDirectory(self,"Select folder",".")
        self.messege.setText("<br>you have selected a folder: <b>{}</b>".format(self.folder))
    
    def get_names(self):
        if self.folder == "":
            self.messege.setText("select a folder")
        else:
            self.filenames = listdir(self.folder)
            return self.filenames
    
    def get_image_for_album(self):
        self.album_image = QFileDialog.getOpenFileName(self, "Select image", ".")
        self.messege.setText("<br>you have selected an image: <b>{}</b>".format(self.album_image))
        print(self.album_image)
        pixmap = QPixmap(self.album_image[0])
        self.image_of_album.setPixmap(pixmap)
    
    def function_tag(self, track):
        f = music_tag.load_file(self.folder + "/" + track)
        print(f)
        
        if self.album_image != '':
            with open('file_of_image', 'rb') as img_in:
                f['artwork'] = img_in.read()
                
        f.remove_tag('album')
        f.remove_tag('artist')
        f.remove_tag('genre')
        f.remove_tag('comment')
        f['album'] = self.album
        f['artist'] = self.artist
        f['genre'] = self.genre
        f['comment'] = self.comment
                
        f.save()
    
    def master_traks(self):
        self.album = self.input_album.text()
        self.artist = self.input_artist.text()
        self.genre = self.input_genre.text()
        self.get_names()
        for name_of_track in self.filenames:
            self.function_tag(name_of_track)
            
    def clear(self):
        self.folder = ""
        self.filenames = ""
        self.album_image = ''
        self.input_album.setText("")
        self.input_artist.setText("")
        self.input_genre.setText("")
        self.album = ""
        self.artist = ""
        self.genre = ""
        self.messege.setText("messege")
        self.image_of_album.setText("image")
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
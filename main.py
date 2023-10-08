from os import listdir
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, music_tag, mutagen



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
        self.check_artist.clicked.connect(self.checkbox_return)
        self.check_album.clicked.connect(self.checkbox_return)
        self.check_genre.clicked.connect(self.checkbox_return)
        self.check_image.clicked.connect(self.checkbox_return)
    
    def checkbox_return(self):
        if self.check_artist.isChecked():
            self.label_artist.setEnabled(True)
            self.input_artist.setEnabled(True)
        else:
            self.label_artist.setDisabled(True)
            self.input_artist.setDisabled(True)
        
        if self.check_album.isChecked():
            self.label_album.setEnabled(True)
            self.input_album.setEnabled(True)
        else:
            self.label_album.setDisabled(True)
            self.input_album.setDisabled(True)
        
        if self.check_genre.isChecked():
            self.label_genre.setEnabled(True)
            self.input_genre.setEnabled(True)
        else:
            self.label_genre.setDisabled(True)
            self.input_genre.setDisabled(True)
        
        if self.check_image.isChecked():
            self.image_of_album.setEnabled(True)
            self.album_image_link.setEnabled(True)
        else:
            self.image_of_album.setDisabled(True)
            self.album_image_link.setDisabled(True)
            
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
        
        if self.check_artist.isChecked():
            f.remove_tag('artist')
            f['artist'] = self.artist

        
        if self.check_album.isChecked():
            f.remove_tag('album')
            f['album'] = self.album

        
        if self.check_genre.isChecked():
            f.remove_tag('genre')
            f['genre'] = self.genre

        
        if self.check_image.isChecked():
            if self.album_image != '':
                with open(self.album_image[0], 'rb') as img_in:
                    f['artwork'] = img_in.read()
        
        f.remove_tag('comment')
        f['comment'] = "redactor_ID3fromIly"

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

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
        self.trash = ''
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
        self.check_find.clicked.connect(self.find_trash)
    
    def find_trash(self):
        if self.check_find.isChecked():
            self.label_find.setEnabled(True)
            self.input_find.setEnabled(True)
            
            self.check_artist.setChecked(False)
            self.check_album.setChecked(False)
            self.check_genre.setChecked(False)
            self.check_image.setChecked(False)
            
            self.check_artist.setDisabled(True)
            self.check_album.setDisabled(True)
            self.check_genre.setDisabled(True)
            self.check_image.setDisabled(True)

        else:
            self.label_find.setDisabled(True)
            self.input_find.setDisabled(True)
            
            self.check_artist.setChecked(True)
            self.check_album.setChecked(True)
            self.check_genre.setChecked(True)
            self.check_image.setChecked(True)
            
            self.check_artist.setDisabled(False)
            self.check_album.setDisabled(False)
            self.check_genre.setDisabled(False)
            self.check_image.setDisabled(False)
        
        self.checkbox_return()
        
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
            print(self.filenames)
            return self.filenames
    
    def get_image_for_album(self):
        self.album_image = QFileDialog.getOpenFileName(self, "Select image", ".")
        self.messege.setText("<br>you have selected an image: <b>{}</b>".format(self.album_image))
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
            
        
        if self.check_find.isChecked():
            
            art = str(f['artist'])
            alb = str(f['artist'])
            gen = str(f['genre'])
            
            if self.trash in art:
                art = art.replace(self.trash, '')
                f.remove_tag('artist')
                f['artist'] = art
                
            if self.trash in alb:
                alb = alb.replace(self.trash, '')
                f.remove_tag('album')
                f['album'] = alb
            
            if self.trash in gen:
                gen = gen.replace(self.trash, '')
                f.remove_tag('genre')
                f['genre'] = gen

        if self.check_image.isChecked():
            if self.album_image != '':
                img = self.album_image[0]
                with open(img, 'rb') as img_in:
                    f.remove_tag('artwork')
                    f['artwork'] = img_in.read()
        
        f.remove_tag('comment')
        f['comment'] = "redactor_ID3fromIly"

        f.save()
    
    def master_traks(self):
        self.album = self.input_album.text()
        self.artist = self.input_artist.text()
        self.genre = self.input_genre.text()
        self.trash = self.input_find.text()
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
        self.trash = ''
        self.input_find.setText("")
        self.messege.setText("messege")
        self.image_of_album.setText("image")
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())

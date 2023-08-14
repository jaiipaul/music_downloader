import sys
from PySide6 import QtCore, QtWidgets
import pytube


class Downloader:
    def __init__(self) -> None:
        self.widget = DownloaderWidget()
        self._init_connections()

    def _init_connections(self):
        self.widget.download_button.clicked.connect(self.download)

    @property
    def url(self):
        return self.widget.url.text()

    @url.setter
    def url(self, url):
        self.widget.url.setText(url)

    @property
    def output_path(self):
        return self.widget.filepath.text()

    def download(self):
        try:
            yt = pytube.YouTube(self.url)
            yt.register_on_complete_callback(self.download_done) 
            audio_stream = sorted(
                yt.streams.filter(only_audio=True, file_extension='mp4'),
                key=lambda x: x.bitrate, reverse=True)
            tag = audio_stream[0].itag
            yt.streams.get_by_itag(tag).download(output_path=self.output_path)
        except pytube.exceptions.RegexMatchError:
            print('not a valid url')

    def download_done(self, stream, filepath):
        self.widget.url.clear()
        print('done')

class DownloaderWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.url = QtWidgets.QLineEdit(self)
        self.filepath = QtWidgets.QLineEdit(self)
        self.browse_button = QtWidgets.QPushButton(self)
        self.download_button = QtWidgets.QPushButton(self)
        self.layout = QtWidgets.QGridLayout(self)
        self._init_connections()
        self._setup()

    def _setup(self):
        self.resize(400, 400)
        url_label = QtWidgets.QLabel("Track URL", self)
        filepath_label = QtWidgets.QLabel("Output Path", self) 
        self.download_button.setText("DOWNLOAD")
        self.browse_button.setText("Browse")
        self.layout.addWidget(url_label, 0, 1, 1, 2, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.url, 1, 0, 1, 4)
        self.layout.addWidget(filepath_label, 2, 1, 1, 2, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.filepath, 3, 0, 1, 3)
        self.layout.addWidget(self.browse_button, 3, 3, 1, 1)
        self.layout.addWidget(self.download_button, 4, 1, 1, 2)

    def _init_connections(self):
        self.browse_button.clicked.connect(self._browse_filepath)

    def _browse_filepath(self):
        output_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Choose output path",
            options=QtWidgets.QFileDialog.ShowDirsOnly |QtWidgets.QFileDialog.DontResolveSymlinks)
        self.filepath.setText(output_path)



if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    with open("./styles/dark.qss") as f:
        style = f.read()
        app.setStyleSheet(style)
    
    main = QtWidgets.QMainWindow()
    main.setWindowTitle("Youtube Downloader")
    main.setFixedSize(400, 200)
    downloader = Downloader()
    main.setCentralWidget(downloader.widget)
    main.show()

    sys.exit(app.exec())
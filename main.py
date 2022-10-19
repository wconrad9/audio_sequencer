import datetime
import multiprocessing
import os
from pathlib import Path
from random import sample
import sys
import threading
from turtle import width

from playsound import playsound
import pydub
from pydub.playback import play
from PySide6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QWidget

from helpers import infinite_bpm_sequence


class Sequencer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.brand_image = QtGui.QPixmap('./static/brand.png')
        self.brand_image = self.brand_image.scaledToHeight(75)
        self.brand_label = QtWidgets.QLabel()
        self.brand_label.setPixmap(self.brand_image)

        self.sample_paths = self.load_samples()

        self.bpm = 120.0

        # Sequencer Control Elements
        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.setFixedWidth(100)
        self.start_button.setStyleSheet("background-color: green")

        self.stop_button = QtWidgets.QPushButton("Stop")
        self.stop_button.setFixedWidth(100)
        self.stop_button.setStyleSheet("background-color: red")

        self.bpm_input = QtWidgets.QLineEdit("120.0")
        self.bpm_input.setFixedWidth(75)

        self.sample_library = QtWidgets.QPushButton("Samp")
        self.sample_library.setFixedWidth(100)

        self.file = QtWidgets.QLabel("Filename", alignment=QtCore.Qt.AlignCenter)
        
        self.filepath = "/Users/walt/Desktop/turnmills.mp3"


        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.brand_label)

        self.control_layout = QtWidgets.QHBoxLayout(self)
        self.control_layout.addWidget(self.start_button)
        self.control_layout.addWidget(self.stop_button)
        self.control_layout.addWidget(self.bpm_input)
        self.control_layout.addWidget(self.sample_library)

        self.main_layout.addLayout(self.control_layout)

        self.sample_slots: SampleSlot = []
        self.sample_slots_layout = QtWidgets.QHBoxLayout(self)

        for i in range(16):
            sample_slot = SampleSlot(i+1, QtWidgets.QComboBox())
            sample_slot.dropdown.addItems(["None"] + [path.__str__()[5:-4] for path in self.sample_paths])
            sample_slot.dropdown.setFixedWidth(75)
            self.sample_slots_layout.addWidget(sample_slot.dropdown)

            self.sample_slots.append(sample_slot)

        self.main_layout.addLayout(self.sample_slots_layout)

        self.start_button.clicked.connect(self.start_clock)
        self.stop_button.clicked.connect(self.stop_clock)
        self.bpm_input.returnPressed.connect(self.parse_bpm)


    @QtCore.Slot()
    def load_sample(self, index):

        print(self.sample_slots[index].dropdown.currentText())


    @QtCore.Slot()
    def start_clock(self):
        """Start the audio stream in the background."""

        def startAudioEngine(self):

            now = datetime.datetime.now()

            # create a generator to progressively generate BPM time values
            bpm_gen = infinite_bpm_sequence(self.bpm)
        
            count = 0
            while self.started:
                next_sixteenth = datetime.timedelta(seconds=next(bpm_gen))

                while datetime.datetime.now() - now < next_sixteenth:
                    continue
                
                self.sample_slots[count % 16].activate_slot()
                count += 1
            
            return
        

        self.started = True

        audio_context = threading.Thread(target=startAudioEngine, args=(self,))
        audio_context.start()

    
    @QtCore.Slot()
    def stop_clock(self):
        """Stop the audio stream."""
    
        self.started = False


    @QtCore.Slot()
    def parse_bpm(self):
        """Take user input BPM and use it to set the beat grid."""
        self.bpm = float(self.bpm_input.text())
        print(float(self.bpm_input.text()))


    @QtCore.Slot()
    def play_file(self):
        # pydub play implementation

        self.file.setText(self.filepath)
        audio = pydub.AudioSegment.from_file(file=self.filepath, duration=5)

        # starts a new thread for each click of the playfile button
        t = threading.Thread(target=play, args=(audio,))
        t.start()

        # playsound play implementation
        """
        :args
            sound: str (path to sound file)
            Block: bool (whether or not to run as blocking)
        playsound(self.filepath, False)
        """

    def load_samples(self):
        """
        Load built-in samples into audio sequencer.
        returns: a list of built-in sample file paths
        """

        sample_dir = Path('./samp')
        
        return list(sample_dir.glob("*.wav"))


class SampleSlot:

    def __init__(self, id: int, dropdown: QtWidgets.QComboBox):
        self.id = id
        self.dropdown = dropdown
        self.loaded = False
        self.sample = None

        self.dropdown.currentTextChanged.connect(self.load_sample)
        
    # connect to signal of QtComboBox selection
    @QtCore.Slot()
    def load_sample(self):
        """Load sample file into a pydub AudioSegment."""

        if self.dropdown.currentText() != "None":
            self.sample = pydub.AudioSegment.from_file(f'./samp/{self.dropdown.currentText()}.wav')
            self.loaded = True

        else:
            self.loaded = False
        
        return        


    @QtCore.Slot()
    def activate_slot(self):
        """Play the loaded sample in a separate thread."""

        if self.loaded:
            t = threading.Thread(target=(play), args=(self.sample,))
            t.start()
        else:
            return


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Sequencer()
    widget.resize(1200, 400)
    widget.setStyleSheet("background-color: #2e79db")
    widget.show()

    sys.exit(app.exec())
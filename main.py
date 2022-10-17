import sys
import threading
import multiprocessing
import datetime

from PySide6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QWidget
from playsound import playsound
import pydub
from pydub.playback import play


class Sequencer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

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

        # Sample Slots
        # TODO: 16 sample slot elements...

        self.file = QtWidgets.QLabel("Filename", alignment=QtCore.Qt.AlignCenter)
        
        self.filepath = "/Users/walt/Desktop/turnmills.mp3"
        """
        self.vlayout = QtWidgets.QVBoxLayout(self)

        # vertical layout creation
        self.vlayout.addWidget(self.file)
        """
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.control_layout = QtWidgets.QHBoxLayout(self)
        self.control_layout.addWidget(self.start_button)
        self.control_layout.addWidget(self.stop_button)
        self.control_layout.addWidget(self.bpm_input)
        self.control_layout.addWidget(self.sample_library)

        self.main_layout.addLayout(self.control_layout)

        sample_slots = []
        self.sample_slots_layout = QtWidgets.QHBoxLayout(self)

        for i in range(16):
            current_slot = QtWidgets.QComboBox()
            current_slot.setFixedWidth(75)
            self.sample_slots_layout.addWidget(current_slot)
            sample_slots.append(current_slot)

        self.main_layout.addLayout(self.sample_slots_layout)

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.bpm_input.returnPressed.connect(self.parse_bpm)


    def infinite_bpm_sequence(self):
        """Generate an infinite series of BPM time values."""

        beat_time = 60/self.bpm
        current_time = 0

        while True:
            current_time = current_time + beat_time
            yield current_time


    @QtCore.Slot()
    def start(self):
        """Start the audio stream in the background."""

        def startAudioEngine(self):

            now = datetime.datetime.now()

            # create a generator to progressively generate BPM time values
            bpm_gen = self.infinite_bpm_sequence()
        
            while self.started:
                next_beat = datetime.timedelta(seconds=next(bpm_gen))

                while datetime.datetime.now() - now < next_beat:
                    continue

                print(next_beat)
            
            return
        

        self.started = True

        audio_context = threading.Thread(target=startAudioEngine, args=(self,))
        audio_context.start()

    
    @QtCore.Slot()
    def stop(self):
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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Sequencer()
    widget.resize(1200, 400)
    widget.show()

    sys.exit(app.exec())
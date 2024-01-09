import numpy as np
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QLabel, QPushButton, QLineEdit, \
    QTextEdit
from PySide6.QtGui import QIcon, QPalette, QColor, QFont
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QApplication
import pyqtgraph as pg
import serial
import re



serial_port = 'COM9'
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate, timeout=1)

class SerialThread(QThread):
    received = Signal(int)

    def __init__(self, serial_instance):
        QThread.__init__(self)
        self.serial_instance = serial_instance

    def run(self):
        ser.flushInput()

        while True:
            bytes_read = ser.readline()

            if len(bytes_read) == 6:
                digits_str = bytes_read.decode('ascii').strip('\r\n')
                cleaned_str = re.sub(r'[^\d]', '', digits_str)
                if(cleaned_str == ''):
                    number= 0
                number = int(cleaned_str)
                self.received.emit(number)
            elif bytes_read == b'':
                pass

            else:
                # Handle the case where fewer than 6 bytes were received
                print(f"Cleaning buffer, please wait...",bytes_read)



class MainWindow(QMainWindow):
    promotie: str = "2023-2024"
    team: list[str] = [
        "Niță Claudiu",
        "Băluți Cristian",
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Proiect Microprocesoare {self.promotie}")
        self.setWindowIcon(QIcon("./icon.png"))
        self.setMinimumSize(1000, 600)
        primary_layout = QVBoxLayout()
        secondary_layout = QHBoxLayout()
        tertiary_layout = QVBoxLayout()

        team_box = QGroupBox("Membrii echipei")
        bold_font = QFont()
        bold_font.setBold(True)
        team_box.setFont(bold_font)

        # Initialize SerialThread with the serial instance
        self.serial_thread = SerialThread(ser)
        self.serial_thread.received.connect(self.update_plot)
        self.serial_thread.start()

        first_member = QLabel(f"Membru 1: {self.team[0]}")
        second_member = QLabel(f"Membru 2: {self.team[1]}")
        team_box_layout = QVBoxLayout()
        team_box_layout.addWidget(first_member, 1)
        team_box_layout.addWidget(second_member, 1)
        team_box.setLayout(team_box_layout)

        control_panel_box = QGroupBox("Control Panel")
        control_panel_box.setFont(bold_font)

        button1 = QPushButton("Reverse")
        button2 = QPushButton("Shutdown")
        button1.setFixedHeight(40)
        button2.setFixedHeight(40)
        #button3 = QPushButton("Send")
        # button1.clicked.connect(self.connect_serial)
        button1.clicked.connect(self.reverse)
        button2.clicked.connect(self.shutdown)
       # button3.clicked.connect(self.send_input)

        self.line_edit = QLineEdit()
        self.line_edit.setAlignment(Qt.AlignmentFlag.AlignBottom)
        line_edit_label = QLabel("Input:", parent=self.line_edit)
        control_panel_box_layout = QVBoxLayout()
        control_panel_box_layout.setSpacing(5)
        control_panel_box_layout.addWidget(button1, 1)
        control_panel_box_layout.addWidget(button2, 1)

        # control_panel_box_layout.addStretch()
        # control_panel_box_layout.addWidget(line_edit_label)
        # control_panel_box_layout.addWidget(self.line_edit, 1)
        # control_panel_box_layout.addWidget(button3, 1)

        control_panel_box.setLayout(control_panel_box_layout)

        tertiary_layout.addWidget(team_box, 1)
        tertiary_layout.addWidget(control_panel_box, 5)

        self.plot_widget = pg.PlotWidget(self)
        #self.setCentralWidget(self.plot_widget)

        # Initial data
        self.hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12]
        self.sound = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45, 50, 55]
        self.plot_widget.setYRange(0, 2000)       # Plot the initial data
        #self.curve = self.plot_widget.plot(self.hour, self.sound, pen='y')
        bar_graph = pg.BarGraphItem(x=self.hour, height=self.sound, width=0.5, brush='y')
        self.plot_widget.addItem(bar_graph)

        secondary_layout.addWidget(self.plot_widget, 3)
        secondary_layout.addLayout(tertiary_layout, 1)

        primary_layout.addLayout(secondary_layout, 4)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        # debug_box = QGroupBox("Debug")
        # debug_box_layout = QVBoxLayout()
        # debug_box_layout.addWidget(self.text_edit, 1)
        # debug_box.setLayout(debug_box_layout)
        #
        # primary_layout.addWidget(debug_box, 1)

        widget = QWidget()
        widget.setLayout(primary_layout)
        # ... [Set up SerialThread and connect signals] ...
        self.serial_thread = SerialThread(ser)  # You would pass your actual serial port instance
        self.serial_thread.received.connect(self.update_plot)
        self.serial_thread.start()



        self.setCentralWidget(widget)

    def append_to_debug(self, data):
        self.text_edit.insertPlainText(f"RECEIVED: {data}\n")

    def update_plot(self, value):
        self.sound.append(value)
        if len(self.sound) > 5000:
            self.sound = self.sound[-1000:]
        if len(self.sound) % 20 == 0:
            self.hour.append(self.hour[-1] + 1)
            last_n_entries = self.sound[-20:]  # Get the last 10 entries
            average_sound = np.mean(last_n_entries)
           # self.curve.setData(self.hour, self.sound)  # Update the data.
           # self.plot_widget.clear()
            if average_sound < 250:
                color = 'g'
            elif average_sound < 1000:
                color = 'y'
            else:
                color = 'r'

            new_bar_graph = pg.BarGraphItem(x=self.hour[-1], height=average_sound,
                                        width=0.6, brush=color)

            self.plot_widget.addItem(new_bar_graph)
            window_size = 20

            if len(self.hour) > window_size:
                self.plot_widget.setXRange(self.hour[-window_size], self.hour[-1])
            if len(self.plot_widget.plotItem.items) > window_size:
                self.plot_widget.plotItem.removeItem(self.plot_widget.plotItem.items[0])

    def send_input(self):
        input_text = self.line_edit.text()
        ser.write(input_text.encode())  # Send the input text over the serial port
        self.line_edit.clear()
        self.text_edit.insertPlainText(f"SENT: {input_text}\n")


    def shutdown(self):
        ser.close()
        self.serial_thread.terminate()
        self.serial_thread.wait()

        self.close()
        QApplication.quit()

    def reverse(self):
        ser.write(b'1')
        self.text_edit.insertPlainText(f"SENT: Reverse signal\n")
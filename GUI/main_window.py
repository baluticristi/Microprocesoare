from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QLabel, QPushButton, QLineEdit, \
    QTextEdit
from PySide6.QtGui import QIcon, QPalette, QColor, QFont
from PySide6.QtCore import Qt, QThread, Signal
import pyqtgraph as pg
import serial




serial_port = 'COM9'
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate, timeout=1)

class SerialThread(QThread):
    received = Signal(int)

    def __init__(self, serial_instance):
        QThread.__init__(self)
        self.serial_instance = serial_instance

    def run(self):
        while True:
            if self.serial_instance.in_waiting > 0:
                raw_data = self.serial_instance.readline()

                try:
                    # Decode and strip carriage returns, new lines, null bytes, and spaces
                    reading = raw_data.decode(errors='ignore').rstrip('\r\n\x00 ')

                    # Filter out non-digit characters before attempting to convert to an integer
                    clean_reading = ''.join(filter(str.isdigit, reading))

                    if clean_reading:  # Ensure it's not empty after cleaning
                        digits = int(clean_reading)
                        self.received.emit(digits)
                    else:
                        print(f"Received non-numeric data: {reading}")

                except ValueError as e:
                    print(f"Error converting '{reading}' to an integer: {e}")



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

        button1 = QPushButton("write")
        button2 = QPushButton("Control 2")
        button3 = QPushButton("Send")
        # button1.clicked.connect(self.connect_serial)
        button3.clicked.connect(self.send_input)
        self.line_edit = QLineEdit()
        self.line_edit.setAlignment(Qt.AlignmentFlag.AlignBottom)
        line_edit_label = QLabel("Input:", parent=self.line_edit)
        control_panel_box_layout = QVBoxLayout()
        control_panel_box_layout.setSpacing(5)
        control_panel_box_layout.addWidget(button1, 1)
        control_panel_box_layout.addWidget(button2, 1)

        control_panel_box_layout.addStretch()
        control_panel_box_layout.addWidget(line_edit_label)
        control_panel_box_layout.addWidget(self.line_edit, 1)
        control_panel_box_layout.addWidget(button3, 1)

        control_panel_box.setLayout(control_panel_box_layout)

        tertiary_layout.addWidget(team_box, 1)
        tertiary_layout.addWidget(control_panel_box, 5)

        self.plot_widget = pg.PlotWidget(self)
        #self.setCentralWidget(self.plot_widget)

        # Initial data
        self.hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        self.plot_widget.setYRange(0, 4000)       # Plot the initial data
        self.curve = self.plot_widget.plot(self.hour, self.temperature, pen='y')

        secondary_layout.addWidget(self.plot_widget, 3)
        secondary_layout.addLayout(tertiary_layout, 1)

        primary_layout.addLayout(secondary_layout, 4)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        debug_box = QGroupBox("Debug")
        debug_box_layout = QVBoxLayout()
        debug_box_layout.addWidget(self.text_edit, 1)
        debug_box.setLayout(debug_box_layout)

        primary_layout.addWidget(debug_box, 1)

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
        self.hour.append(self.hour[-1] + 1)  # Increment the last hour value
        self.temperature.append(value)

        # Update the plot with the new data
        self.curve.setData(self.hour, self.temperature)  # Update the data.

        # Optionally, if you want to limit the number of displayed points:
        window_size = 10
        print(self.hour)
        if len(self.hour) > window_size:
            self.plot_widget.setXRange(self.hour[-window_size], self.hour[-1])

    def send_input(self):
        input_text = self.line_edit.text()
        ser.write(input_text.encode())  # Send the input text over the serial port
        self.line_edit.clear()
        self.text_edit.insertPlainText(f"SENT: {input_text}\n")

    def closeEvent(self, event):
        # Close the serial port and stop the thread
        ser.close()
        self.serial_thread.terminate()
        self.serial_thread.wait()
        event.accept()

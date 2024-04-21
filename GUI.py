import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QMessageBox
import pandas as pd

class FileSelectorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Data Convertor')
        
        self.setMinimumSize(400, 200)
        self.setMaximumSize(600, 400)
        
        self.setGeometry(100, 100, 300, 200)

        self.setStyleSheet("background-image: url(background.png);")
        
        layout = QVBoxLayout()

        input_file_label = QLabel('將.dat文件轉換爲.csv文件 (冇header同異常值！)\n\nConvert .dat file to .csv file (without headers and outliers!)')
        layout.addWidget(input_file_label)
        
        
        self.select_input_file_btn = QPushButton('Select Input File')
        self.select_output_folder_btn = QPushButton('Select Output Folder')
        
        self.select_input_file_btn.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                background-color: #b28f94;
                border: 2px solid #b28f94;
                padding: 15px; /*增加内边距*/
                font-size: 16px; /*字体大小，根据需要调整*/
                color: white; /*字体颜色，根据需要调整*/
            }
            QPushButton:hover {
                background-color: #b28f94;
            }
        """)

        self.select_output_folder_btn.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                background-color: #b28f94;
                border: 2px solid #b28f94;
                padding: 15px; /*增加内边距*/
                font-size: 16px; /*字体大小，根据需要调整*/
                color: white; /*字体颜色，根据需要调整*/
            }
            QPushButton:hover {
                background-color: #b28f94;
            }
        """)
  
        self.select_input_file_btn.clicked.connect(self.select_input_file)
        self.select_output_folder_btn.clicked.connect(self.select_output_folder)


        layout.addWidget(self.select_input_file_btn)
        layout.addWidget(self.select_output_folder_btn)


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    def select_input_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        input_file_name, _ = QFileDialog.getOpenFileName(self, "选择输入.dat文件",
                                                        "", "Dat Files (*.dat);;All Files (*)", options=options)
        if input_file_name:
            self.input_dat_file_path = input_file_name
            print(f"选择的输入文件: {input_file_name}")

    def select_output_folder(self):
        output_folder_name = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if output_folder_name:
            self.output_directory_path = output_folder_name
            print(f"选择的输出文件夹: {output_folder_name}")
            self.convert_dat_to_output()

    def convert_dat_to_output(self):
        if self.input_dat_file_path and self.output_directory_path:
            output_file_path = f"{self.output_directory_path}/converted_output.csv"
            data_started = False
            data_lines = []

            try:
                with open(self.input_dat_file_path, 'r') as file:
                    for line in file:
                        if data_started:
                            data_lines.append(line)
                        elif '[Data]' in line:
                            data_started = True
            except FileNotFoundError:
                print("唔揾到文件,请确保文件路径正确. ")  
            
            try:
                with open(output_file_path, 'w') as file:
                    file.writelines(data_lines)
                QMessageBox.information(self, 'Success', f'Successfully converted and save to \n{output_file_path}', QMessageBox.Ok, QMessageBox.Ok)
                print("资料处理完成,已经摆到指定嘅输出文件.")
            except Exception as e:
                print("保存输出文件时发生错误：", str(e))             
   
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = FileSelectorApp()
    mainWin.show()
    sys.exit(app.exec_())
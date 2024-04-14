import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import cartopy
import cartopy.crs as ccrs
from geopy.geocoders import Nominatim

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 700, 450)

        self.create_map()
        self.create_city_input()

    def create_map(self):
        self.fig = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.fig)
        self.setCentralWidget(self.canvas)

        self.ax = self.fig.add_subplot(111, projection=ccrs.PlateCarree())
        self.ax.set_global()

        self.ax.add_feature(cartopy.feature.LAND, edgecolor='black', facecolor='#7e8c3e')
        self.ax.add_feature(cartopy.feature.OCEAN, facecolor='#1b4c89') 

        self.canvas.draw()

    def create_city_input(self):
        self.label = QLabel("Type country...", self)
        self.label.setGeometry(20, 30, 100, 30)

        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(150, 30, 400, 30)
        self.textbox.setStyleSheet("background-color: white; color: black")
        
        self.button = QPushButton("Select", self)
        self.button.setGeometry(500, 30, 100, 30)
        self.button.setStyleSheet("background-color: darkgray")
        self.button.clicked.connect(self.show_map)

    def show_map(self):
        city = self.textbox.text()
        if city:
            self.update_map(city)

    def update_map(self, city):
        geolocator = Nominatim(user_agent="weather_app")
        # Get location (inpit city))
        location = geolocator.geocode(city)
        if location:
            latitude, longitude = location.latitude, location.longitude
            self.ax.clear()

            # Create a map
            self.ax.set_global()
            self.ax.add_feature(cartopy.feature.LAND, edgecolor='black', facecolor='#7e8c3e') 
            self.ax.add_feature(cartopy.feature.OCEAN, facecolor='#1b4c89') 
            self.ax.add_feature(cartopy.feature.BORDERS, linestyle='-', edgecolor='black') 

            self.ax.set_extent([longitude - 5, longitude + 5, latitude - 5, latitude + 5])

            # marker
            self.ax.plot(longitude, latitude, marker='+', color='red', markersize=10, transform=ccrs.PlateCarree())

            self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

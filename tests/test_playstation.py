import os
import time
from pathlib import Path
from src.driver.hdmi.hdmi_driver import HDMIDriver
from src.driver.device_capabilities import DeviceCapabilities
from src.driver.by import By
from src.driver.element import Element
from src.exceptions.no_such_element_exception import NoSuchElementException
from src.driver.screen_size import ScreenSize

class Test_PlaystationTests:

    SERVER_URL = "http://localhost:7777"

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    PLAYSTATION_IMAGES_DIR = ROOT_DIR + os.path.sep + "resources" + os.path.sep + "playstationimages" + os.path.sep

    hdmi_driver = None
    capabilities = None

    def teardown_method(self):
        if not self.hdmi_driver is None:
            self.hdmi_driver.stop()
        
    def setup_method(self):
        self.capabilities = DeviceCapabilities()
        self.capabilities.add_capability("Platform", "HDMI")
        self.capabilities.add_capability("DeviceName", "Playstation4")
        self.capabilities.add_capability("HomeHubIPAddress", "192.168.1.41")
        home = str(Path.home())
        self.capabilities.add_capability("OCRType", "GoogleVision")
        self.capabilities.add_capability("GoogleCredentials", home + os.path.sep + "Service.json")
        self.capabilities.add_capability("VideoCaptureInput", "FHD Webcamera")
        self.capabilities.add_capability("AudioCaptureInput", "FHD Webcamera")
    
    def test_find_element_from_text_with_google_vision(self):
        self.hdmi_driver = HDMIDriver(self.SERVER_URL, self.capabilities)
        self.hdmi_driver.options().set_element_timeout(15000)
        element = self.hdmi_driver.finder().find_element(By().text("Sign in"))
        
        print("element x: " + str(element.get_x()))
        assert element.get_x() > 760 and element.get_x() < 780

        print("element y: " + str(element.get_y()))
        assert element.get_y() > 790 and element.get_y() < 800

        print("element width: " + str(element.get_width()))
        assert element.get_width() > 75 and element.get_width() < 90

        print("element height: " + str(element.get_height()))
        assert element.get_height() > 25 and element.get_height() < 35

        print("element text: " + str(element.get_text()))
        assert element.get_text() == "Sign in"

        print("element id: " + str(element.get_element_id()))
        
        print("element session id: " + str(element.get_session_id()))
        assert element.get_session_id() == self.hdmi_driver.get_session_id()

    def test_find_element_from_image(self):
        self.hdmi_driver = HDMIDriver(self.SERVER_URL, self.capabilities)
        self.hdmi_driver.options().set_element_timeout(15000)

        for by in { By().image(self.PLAYSTATION_IMAGES_DIR + "playplus.png"), By().image("https://dl.dropboxusercontent.com/s/3bzhadgvuuko94j/playplus.png") }:
            element = self.hdmi_driver.finder().find_element(by)
        
            print("element x: " + str(element.get_x()))
            assert element.get_x() > 90 and element.get_x() < 100

            print("element y: " + str(element.get_y()))
            assert element.get_y() > 70 and element.get_y() < 90

            print("element width: " + str(element.get_width()))
            assert element.get_width() > 50 and element.get_width() < 60

            print("element height: " + str(element.get_height()))
            assert element.get_height() > 45 and element.get_height() < 60

            print("element confidence: " + str(element.get_confidence()))
            assert element.get_confidence() > 0.90

            print("element id: " + str(element.get_element_id()))
        
            print("element session id: " + str(element.get_session_id()))
            assert element.get_session_id() == self.hdmi_driver.get_session_id()

    def test_find_element_in_sub_screen(self):
        self.hdmi_driver = HDMIDriver(self.SERVER_URL, self.capabilities)
        self.hdmi_driver.options().set_element_timeout(5000)

        by = By().image(self.PLAYSTATION_IMAGES_DIR + "playplus.png")
        element = self.hdmi_driver.finder().find_element_sub_screen(by, 1, 1, 300, 300)
    
        success = False
        try:
            self.hdmi_driver.finder().find_element_sub_screen(by, 800, 800, 100, 100)
        except NoSuchElementException as e:
            success = str(e).__contains__("Failed to find")
        
        assert success

    def test_remote_control(self):
        self.hdmi_driver = HDMIDriver(self.SERVER_URL, self.capabilities)
        self.hdmi_driver.options().set_element_timeout(15000)

        self.hdmi_driver.finder().find_element(By().text("Sign in"))
        button_options = self.hdmi_driver.remote().get_button_options()
        print(button_options)
        assert "Circle" in button_options

        self.hdmi_driver.remote().press_button("DirectionUp")
        self.hdmi_driver.finder().find_element(By().text("Notifications"))
        self.hdmi_driver.remote().press_button("Circle")
        self.hdmi_driver.finder().find_element(By().text("Sign in"))
        
    def test_get_screen_text_google_vision(self):
        self.hdmi_driver = HDMIDriver(self.SERVER_URL, self.capabilities)
        self.hdmi_driver.options().set_element_timeout(15000)
        self.hdmi_driver.finder().find_element(By().text("playstation store"))
        screen_texts = self.hdmi_driver.screen().get_text()
        match_found = False
        for screen_text in screen_texts:
            if screen_text.get_text() == "PlayStation":
                match_found = True
                x = screen_text.get_x()
                y = screen_text.get_y()
                width = screen_text.get_width()
                height = screen_text.get_height()
                confidence = screen_text.get_confidence()

                assert x > 640 and x < 650
                assert y > 550 and y < 560
                assert width > 285 and width < 295
                assert height > 50 and height < 60
                break
        assert match_found

        screen_texts = self.hdmi_driver.screen().get_text_sub_screen(1, 1, 500, 500)
        assert len(screen_texts) > 1

    def test_get_screen_size(self):
        self.hdmi_driver = HDMIDriver(self.SERVER_URL, self.capabilities)
        screen_size = self.hdmi_driver.screen().get_screen_size()
        assert screen_size.get_width() > 1900 and screen_size.get_width() < 1930
        assert screen_size.get_height() > 1000 and screen_size.get_height() < 1090

    def test_get_screen_artifacts(self):
        self.hdmi_driver = HDMIDriver(self.SERVER_URL, self.capabilities)

        screen_image = self.hdmi_driver.screen().get_image()
        print(screen_image)
        assert os.path.exists(screen_image)

        screen_sub_image = self.hdmi_driver.screen().get_image_sub_screen(1, 1, 300, 300)
        print(screen_sub_image)
        assert os.path.exists(screen_sub_image)

        screen_recording = self.hdmi_driver.screen().get_recording()
        print(screen_recording)
        assert os.path.exists(screen_recording)

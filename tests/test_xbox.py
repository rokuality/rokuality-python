import os
import time
from pathlib import Path
from src.driver.xbox.xbox_driver import XBoxDriver
from src.driver.device_capabilities import DeviceCapabilities
from src.driver.by import By
from src.driver.element import Element
from src.exceptions.no_such_element_exception import NoSuchElementException
from src.enums.xbox_button import XBoxButton
from src.driver.xbox.xbox_device_info import XBoxDeviceInfo
from src.driver.screen_size import ScreenSize

class Test_XBoxTests:

    SERVER_URL = "http://localhost:7777"

    DEMO_APP_URL = "https://rokualitypublic.s3.amazonaws.com/XBoxDebug.appxbundle"
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    XBOX_IMAGES_DIR = ROOT_DIR + os.path.sep + "resources" + os.path.sep + "xboximages" + os.path.sep

    xbox_driver = None
    capabilities = None

    def teardown_method(self):
        if not self.xbox_driver is None:
            self.xbox_driver.stop()
        
    def setup_method(self):
        self.capabilities = DeviceCapabilities()
        self.capabilities.add_capability("Platform", "XBox")
        self.capabilities.add_capability("AppPackage", self.DEMO_APP_URL)
        self.capabilities.add_capability("DeviceIPAddress", "192.168.1.36")
        self.capabilities.add_capability("DeviceName", "XboxOne")
        self.capabilities.add_capability("HomeHubIPAddress", "192.168.1.41")
        self.capabilities.add_capability("AppPackage", self.DEMO_APP_URL)
        self.capabilities.add_capability("App", "MTV")
        home = str(Path.home())
        self.capabilities.add_capability("OCRType", "GoogleVision")
        self.capabilities.add_capability("GoogleCredentials", home + os.path.sep + "Service.json")
    
    def test_install_from_url(self):
        self.capabilities.add_capability("AppPackage", self.DEMO_APP_URL)
        
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)
        self.xbox_driver.options().set_element_timeout(15000)
        self.xbox_driver.finder().find_element(By().text("featured"))

    def test_install_from_local_file(self):
        self.capabilities.add_capability("AppPackage", self.__get_demo_app())
        
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)
        self.xbox_driver.options().set_element_timeout(15000)
        self.xbox_driver.finder().find_element(By().text("featured"))

    def test_launch_already_installed_app(self):
        '''NOTE - this assumes you already have your app installed on the device'''
        self.capabilities.remove_capability("AppPackage")
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)

        self.xbox_driver.options().set_element_timeout(15000)
        self.xbox_driver.finder().find_element(By().text("featured"))

    def test_find_element_from_text_with_google_vision(self):
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)
        self.xbox_driver.options().set_element_timeout(15000)
        element = self.xbox_driver.finder().find_element(By().text("featured"))
        
        print("element x: " + str(element.get_x()))
        assert element.get_x() > 90 and element.get_x() < 100

        print("element y: " + str(element.get_y()))
        assert element.get_y() > 450 and element.get_y() < 460

        print("element width: " + str(element.get_width()))
        assert element.get_width() > 130 and element.get_width() < 145

        print("element height: " + str(element.get_height()))
        assert element.get_height() > 20 and element.get_height() < 30

        print("element text: " + str(element.get_text()))
        assert element.get_text() == "Featured"

        '''only relevant for tesseract'''
        print("element confidence: " + str(element.get_confidence()))
        assert element.get_confidence() == 0.0 

        print("element id: " + str(element.get_element_id()))
        
        print("element session id: " + str(element.get_session_id()))
        assert element.get_session_id() == self.xbox_driver.get_session_id()

    def test_find_element_from_image(self):
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)
        self.xbox_driver.options().set_element_timeout(15000)

        for by in { By().image(self.XBOX_IMAGES_DIR + "featured.png"), By().image("https://dl.dropboxusercontent.com/s/36upxsx1cbhh3tp/featured.png") }:
            element = self.xbox_driver.finder().find_element(by)
        
            print("element x: " + str(element.get_x()))
            assert element.get_x() > 90 and element.get_x() < 110

            print("element y: " + str(element.get_y()))
            assert element.get_y() > 445 and element.get_y() < 460

            print("element width: " + str(element.get_width()))
            assert element.get_width() > 140 and element.get_width() < 150

            print("element height: " + str(element.get_height()))
            assert element.get_height() > 25 and element.get_height() < 35

            print("element confidence: " + str(element.get_confidence()))
            assert element.get_confidence() > 0.90

            print("element id: " + str(element.get_element_id()))
        
            print("element session id: " + str(element.get_session_id()))
            assert element.get_session_id() == self.xbox_driver.get_session_id()

    def test_element_not_found_in_text_tesseract(self):
        self.capabilities.add_capability("OCRType", "Tesseract")
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)
        
        success = False
        try:
            self.xbox_driver.finder().find_element(By().text("not found"))
        except NoSuchElementException as e:
            print(str(e))
            success = str(e).__contains__("Failed to find text element on the device screen")
        
        assert success

    def test_element_not_found_in_text_google_vision(self):
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)
        
        success = False
        try:
            self.xbox_driver.finder().find_element(By().text("not found"))
        except NoSuchElementException as e:
            print(str(e))
            success = str(e).__contains__("Failed to find text element on the device screen")
        
        assert success

    def test_element_not_found_in_image(self):
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)
        
        success = False
        try:
            self.xbox_driver.finder().find_element(By().image(self.XBOX_IMAGES_DIR + "helloworld.png"))
        except NoSuchElementException as e:
            print(str(e))
            success = str(e).__contains__("Failed to find image element on the device screen")
        
        assert success

    def test_element_set_timeout(self):
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)
        
        self.xbox_driver.options().set_element_timeout(5000)
        self.xbox_driver.options().set_element_poll_interval(500)
        start_time = time.time()
        success = False
        try:
            self.xbox_driver.finder().find_element(By().text("not here"))
        except NoSuchElementException as e:
            print(str(e))
            success = str(e).__contains__("Failed to find text element on the device screen")
        
        assert success
        end_time = time.time()
        time_dif_seconds = end_time - start_time
        print("time difference in seconds " + str(time_dif_seconds))
        success = time_dif_seconds >= 5 and time_dif_seconds <= 9
        assert success

    def test_find_element_in_sub_screen(self):
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)
        self.xbox_driver.options().set_element_timeout(5000)

        for by in { By().image(self.XBOX_IMAGES_DIR + "featured.png"), By().text("featured") }:
            element = self.xbox_driver.finder().find_element_sub_screen(by, 75, 410, 230, 90)
    
        success = False
        try:
            self.xbox_driver.finder().find_element_sub_screen(by, 500, 500, 100, 100)
        except NoSuchElementException as e:
            success = str(e).__contains__("Failed to find")
        
        assert success

    def test_remote_control(self):
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)
        self.xbox_driver.options().set_element_timeout(15000)

        self.xbox_driver.finder().find_element(By().text("featured"))
        self.xbox_driver.remote().press_button(XBoxButton.UP_ARROW)
        self.xbox_driver.remote().press_button(XBoxButton.RIGHT_ARROW)
        self.xbox_driver.remote().press_button(XBoxButton.RIGHT_ARROW)
        self.xbox_driver.remote().press_button(XBoxButton.RIGHT_ARROW)
        self.xbox_driver.remote().press_button(XBoxButton.A)
        self.xbox_driver.finder().find_element(By().text("Watch with Your TV Provider"))
        
        self.xbox_driver.remote().press_button(XBoxButton.B)
        self.xbox_driver.remote().press_button(XBoxButton.B)
        self.xbox_driver.finder().find_element(By().text("featured"))
        
    def test_device_info(self):
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)
        xbox_device_info = self.xbox_driver.info().get_device_info()
        assert xbox_device_info.get_console_type() == "Xbox One"
    
    def test_get_screen_text_google_vision(self):
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)
        self.xbox_driver.options().set_element_timeout(15000)
        self.xbox_driver.finder().find_element(By().text("featured"))
        screen_texts = self.xbox_driver.screen().get_text()
        match_found = False
        for screen_text in screen_texts:
            if screen_text.get_text() == "Featured":
                match_found = True
                x = screen_text.get_x()
                y = screen_text.get_y()
                width = screen_text.get_width()
                height = screen_text.get_height()
                confidence = screen_text.get_confidence()

                assert x > 90 and x < 110
                assert y > 440 and y < 460
                assert width > 130 and width < 140
                assert height > 20 and height < 30
                break
        assert match_found

        screen_texts = self.xbox_driver.screen().get_text_sub_screen(1, 1, 500, 500)
        assert len(screen_texts) > 1

    def test_get_screen_size(self):
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)
        screen_size = self.xbox_driver.screen().get_screen_size()
        assert screen_size.get_width() > 1900 and screen_size.get_width() < 1930
        assert screen_size.get_height() > 1000 and screen_size.get_height() < 1090

    def test_get_screen_artifacts(self):
        self.xbox_driver = XBoxDriver(self.SERVER_URL, self.capabilities)

        screen_image = self.xbox_driver.screen().get_image()
        print(screen_image)
        assert os.path.exists(screen_image)

        screen_sub_image = self.xbox_driver.screen().get_image_sub_screen(1, 1, 300, 300)
        print(screen_sub_image)
        assert os.path.exists(screen_sub_image)

        screen_recording = self.xbox_driver.screen().get_recording()
        print(screen_recording)
        assert os.path.exists(screen_recording)

    def __get_demo_app(self):
        home = str(Path.home())
        return home + os.path.sep + "XBoxDebug.appxbundle"

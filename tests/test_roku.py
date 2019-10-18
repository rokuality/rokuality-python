import os
import time
from pathlib import Path
from src.driver.roku.roku_driver import RokuDriver
from src.driver.device_capabilities import DeviceCapabilities
from src.driver.by import By
from src.driver.element import Element
from src.exceptions.no_such_element_exception import NoSuchElementException
from src.enums.roku_button import RokuButton
from src.driver.roku.roku_device_info import RokuDeviceInfo
from src.driver.screen_size import ScreenSize

class Test_RokuTests:

    DEMO_APP_URL = "https://rokualitypublic.s3.amazonaws.com/RokualityDemoApp.zip"
    SERVER_URL = "http://localhost:7777"

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    ROKU_IMAGES_DIR = ROOT_DIR + os.path.sep + "resources" + os.path.sep + "rokuimages" + os.path.sep
    HELLOW_WORLD_ZIP = ROOT_DIR + os.path.sep + "resources" + os.path.sep + "helloworld.zip"

    roku_driver = None
    capabilities = None

    def teardown_method(self):
        if not self.roku_driver is None:
            self.roku_driver.stop()
        
    def setup_method(self):
        self.capabilities = DeviceCapabilities()
        self.capabilities.add_capability("Platform", "Roku")
        self.capabilities.add_capability("AppPackage", self.DEMO_APP_URL)
        self.capabilities.add_capability("DeviceIPAddress", "192.168.1.38")
        self.capabilities.add_capability("DeviceUsername", "rokudev")
        self.capabilities.add_capability("DevicePassword", "1234")
        self.capabilities.add_capability("OCRType", "Tesseract")
    
    def test_install_from_url(self):
        self.capabilities.add_capability("AppPackage", self.DEMO_APP_URL)
        
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        self.roku_driver.options().set_element_timeout(5000)
        self.roku_driver.finder().find_element(By().text("SHOWS"))

    def test_install_from_local_file(self):
        self.capabilities.add_capability("AppPackage", self.HELLOW_WORLD_ZIP)
        
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        self.roku_driver.options().set_element_timeout(5000)
        self.roku_driver.finder().find_element(By().text("Hello World!"))

    def test_launch_already_installed_app(self):
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        self.roku_driver.stop()

        self.capabilities.remove_capability("AppPackage")
        '''NOTE - only use this cap if you have a package that is already sideloaded on the device under test '''
        self.capabilities.add_capability("App", "dev")

        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        self.roku_driver.options().set_element_timeout(5000)
        self.roku_driver.finder().find_element(By().text("SHOWS"))

    def test_find_element_from_text_with_tesseract(self):
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        self.roku_driver.options().set_element_timeout(5000)
        element = self.roku_driver.finder().find_element(By().text("SHOWS"))
        
        print("element x: " + str(element.get_x()))
        assert element.get_x() > 100 and element.get_x() < 120

        print("element y: " + str(element.get_y()))
        assert element.get_y() > 575 and element.get_y() < 590

        print("element width: " + str(element.get_width()))
        assert element.get_width() > 90 and element.get_width() < 105

        print("element height: " + str(element.get_height()))
        assert element.get_height() > 15 and element.get_height() < 25

        print("element text: " + str(element.get_text()))
        assert element.get_text() == "SHOWS"

        print("element confidence: " + str(element.get_confidence()))
        assert element.get_confidence() > 85.0

        print("element id: " + str(element.get_element_id()))
        
        print("element session id: " + str(element.get_session_id()))
        assert element.get_session_id() == self.roku_driver.get_session_id()

    def test_find_element_from_text_with_google_vision(self):
        home = str(Path.home())
        self.capabilities.add_capability("OCRType", "GoogleVision")
        self.capabilities.add_capability("GoogleCredentials", home + os.path.sep + "Service.json")
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        self.roku_driver.options().set_element_timeout(5000)
        element = self.roku_driver.finder().find_element(By().text("SHOWS"))
        
        print("element x: " + str(element.get_x()))
        assert element.get_x() > 100 and element.get_x() < 120

        print("element y: " + str(element.get_y()))
        assert element.get_y() > 575 and element.get_y() < 590

        print("element width: " + str(element.get_width()))
        assert element.get_width() > 90 and element.get_width() < 105

        print("element height: " + str(element.get_height()))
        assert element.get_height() > 15 and element.get_height() < 25

        print("element text: " + str(element.get_text()))
        assert element.get_text() == "SHOWS"

        '''only relevant for tesseract'''
        print("element confidence: " + str(element.get_confidence()))
        assert element.get_confidence() == 0.0 

        print("element id: " + str(element.get_element_id()))
        
        print("element session id: " + str(element.get_session_id()))
        assert element.get_session_id() == self.roku_driver.get_session_id()

    def test_find_element_from_image(self):
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        self.roku_driver.options().set_element_timeout(5000)

        for by in { By().image(self.ROKU_IMAGES_DIR + "shows.png"), By().image("https://dl.dropboxusercontent.com/s/jfywmqqnsndgki8/shows.png") }:
            element = self.roku_driver.finder().find_element(by)
        
            print("element x: " + str(element.get_x()))
            assert element.get_x() > 100 and element.get_x() < 120

            print("element y: " + str(element.get_y()))
            assert element.get_y() > 560 and element.get_y() < 580

            print("element width: " + str(element.get_width()))
            assert element.get_width() > 100 and element.get_width() < 120

            print("element height: " + str(element.get_height()))
            assert element.get_height() > 30 and element.get_height() < 50

            print("element confidence: " + str(element.get_confidence()))
            assert element.get_confidence() > 0.90

            print("element id: " + str(element.get_element_id()))
        
            print("element session id: " + str(element.get_session_id()))
            assert element.get_session_id() == self.roku_driver.get_session_id()

    def test_element_not_found_in_text_tesseract(self):
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        
        success = False
        try:
            self.roku_driver.finder().find_element(By().text("not found"))
        except NoSuchElementException as e:
            print(str(e))
            success = str(e).__contains__("Failed to find text element on the device screen")
        
        assert success

    def test_element_not_found_in_text_google_vision(self):
        home = str(Path.home())
        self.capabilities.add_capability("OCRType", "GoogleVision")
        self.capabilities.add_capability("GoogleCredentials", home + os.path.sep + "Service.json")
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        
        success = False
        try:
            self.roku_driver.finder().find_element(By().text("not found"))
        except NoSuchElementException as e:
            print(str(e))
            success = str(e).__contains__("Failed to find text element on the device screen")
        
        assert success

    def test_element_not_found_in_image(self):
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        
        success = False
        try:
            self.roku_driver.finder().find_element(By().image(self.ROKU_IMAGES_DIR + "helloworld.png"))
        except NoSuchElementException as e:
            print(str(e))
            success = str(e).__contains__("Failed to find image element on the device screen")
        
        assert success

    def test_element_set_timeout(self):
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        
        self.roku_driver.options().set_element_timeout(5000)
        self.roku_driver.options().set_element_poll_interval(500)
        start_time = time.time()
        success = False
        try:
            self.roku_driver.finder().find_element(By().text("not here"))
        except NoSuchElementException as e:
            print(str(e))
            success = str(e).__contains__("Failed to find text element on the device screen")
        
        assert success
        end_time = time.time()
        time_dif_seconds = end_time - start_time
        print("time difference in seconds " + str(time_dif_seconds))
        success = time_dif_seconds >= 5 and time_dif_seconds <=10
        assert success

    def test_element_set_image_match_similarity(self):
        self.capabilities.add_capability("AppPackage", self.HELLOW_WORLD_ZIP)
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        
        self.roku_driver.options().set_image_match_similarity(0.10)
        self.roku_driver.finder().find_element(By().image(self.ROKU_IMAGES_DIR + "shows.png"))

        self.roku_driver.options().set_image_match_similarity(0.99)
        success = False
        try:
            self.roku_driver.finder().find_element(By().image(self.ROKU_IMAGES_DIR + "shows.png"))
        except NoSuchElementException as e:
            success = str(e).__contains__("Failed to find image element on the device screen")
        
        assert success

    def test_find_element_in_sub_screen(self):
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        self.roku_driver.options().set_element_timeout(5000)

        for by in { By().image(self.ROKU_IMAGES_DIR + "shows.png"), By().text("SHOWS") }:
            element = self.roku_driver.finder().find_element_sub_screen(by, 100, 500, 300, 200)
    
        success = False
        try:
            self.roku_driver.finder().find_element_sub_screen(by, 1, 1, 100, 500)
        except NoSuchElementException as e:
            success = str(e).__contains__("Failed to find")
        
        assert success

    def test_remote_control(self):
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        self.roku_driver.options().set_element_timeout(5000)

        self.roku_driver.finder().find_element(By().text("SHOWS"))
        self.roku_driver.remote().press_button(RokuButton.BACK)
        self.roku_driver.finder().find_element(By().text("EXIT"))
        self.roku_driver.remote().press_button(RokuButton.SELECT)
        self.roku_driver.finder().find_element(By().text("SHOWS"))
        self.roku_driver.remote().press_button(RokuButton.OPTION)
        self.roku_driver.finder().find_element(By().text("LEGAL"))

    def test_device_info(self):
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        roku_device_info = self.roku_driver.info().get_device_info()
        assert roku_device_info.get_vendor_name() == "Roku"
    
    def test_get_screen_text_tesseract(self):
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        self.roku_driver.options().set_element_timeout(5000)
        self.roku_driver.finder().find_element(By().text("SHOWS"))
        screen_texts = self.roku_driver.screen().get_text()
        match_found = False
        for screen_text in screen_texts:
            if screen_text.get_text() == "SHOWS":
                match_found = True
                x = screen_text.get_x()
                y = screen_text.get_y()
                width = screen_text.get_width()
                height = screen_text.get_height()
                confidence = screen_text.get_confidence()

                assert x > 100 and x < 120
                assert y > 575 and y < 590
                assert width > 90 and width < 105
                assert height > 15 and height < 25
                assert confidence > 89
                break
        assert match_found

        screen_texts = self.roku_driver.screen().get_text_sub_screen(1, 1, 500, 500)
        assert len(screen_texts) > 1
        
        text_as_string_sub_screen = self.roku_driver.screen().get_text_as_string_sub_screen(1, 1, 500, 500)
        assert not "SHOWS" in text_as_string_sub_screen

        text_as_string = self.roku_driver.screen().get_text_as_string()
        print("screen text as string :" + text_as_string)
        assert "SHOWS" in text_as_string

    def test_get_screen_text_google_vision(self):
        home = str(Path.home())
        self.capabilities.add_capability("OCRType", "GoogleVision")
        self.capabilities.add_capability("GoogleCredentials", home + os.path.sep + "Service.json")
        
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        self.roku_driver.options().set_element_timeout(5000)
        self.roku_driver.finder().find_element(By().text("SHOWS"))
        screen_texts = self.roku_driver.screen().get_text()
        match_found = False
        for screen_text in screen_texts:
            if screen_text.get_text() == "SHOWS":
                match_found = True
                x = screen_text.get_x()
                y = screen_text.get_y()
                width = screen_text.get_width()
                height = screen_text.get_height()
                confidence = screen_text.get_confidence()

                assert x > 100 and x < 120
                assert y > 575 and y < 590
                assert width > 90 and width < 105
                assert height > 15 and height < 25
                break
        assert match_found

        screen_texts = self.roku_driver.screen().get_text_sub_screen(1, 1, 500, 500)
        assert len(screen_texts) > 1

    def test_get_screen_size(self):
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)
        screen_size = self.roku_driver.screen().get_screen_size()
        assert screen_size.get_width() > 1900 and screen_size.get_width() < 1930
        assert screen_size.get_height() > 1000 and screen_size.get_height() < 1090

    def test_get_screen_artifacts(self):
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)

        screen_image = self.roku_driver.screen().get_image()
        print(screen_image)
        assert os.path.exists(screen_image)

        screen_sub_image = self.roku_driver.screen().get_image_sub_screen(1, 1, 300, 300)
        print(screen_sub_image)
        assert os.path.exists(screen_sub_image)

        screen_recording = self.roku_driver.screen().get_recording()
        print(screen_recording)
        assert os.path.exists(screen_recording)

    def test_send_keys(self):
        home = str(Path.home())
        self.capabilities.add_capability("OCRType", "GoogleVision")
        self.capabilities.add_capability("GoogleCredentials", home + os.path.sep + "Service.json")
        
        self.roku_driver = RokuDriver(self.SERVER_URL, self.capabilities)

        self.roku_driver.options().set_element_timeout(5000)
        self.roku_driver.finder().find_element(By().text("SHOWS"))
        self.roku_driver.remote().press_button(RokuButton.OPTION)
        self.roku_driver.finder().find_element(By().text("LEGAL"))
        self.roku_driver.remote().press_button(RokuButton.SELECT)
        self.roku_driver.finder().find_element(By().text("123"))
        
        self.roku_driver.remote().send_keys("search for something")
        self.roku_driver.finder().find_element(By().text("search for something"))

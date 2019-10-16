# Rokuality Python - End to End Automation for Roku and XBox!

The Rokuality platform allows you to distribute Roku and XBox end to end tests across multiple devices on your network. (Playstation and other devices coming soon!) The project goal is to provide a no cost/low cost open source solution for various video streaming platforms that otherwise don't offer an easily automatable solution! Clone and start the [Rokuality Server](https://github.com/rokuality/rokuality-server), and start writing tests!

### Getting started: Get the Server
Clone/Download and start the [Rokuality Server](https://github.com/rokuality/rokuality-server) which acts as a lightweight web server proxy for your test traffic. The server does all the 'heavy lifting' on the backend.

### Getting started: Add the bindings to your Project
To use Rokuality in your tests or application, install the `rokuality-python` dependency:
```xml
    pip install rokuality-python
```

### Getting started: Roku
See the [Getting Started: Roku](https://github.com/rokuality/rokuality-server) section for details about preparing your Roku device for test.

### Getting started: XBox
See the [Getting Started: XBox](https://github.com/rokuality/rokuality-server) section for details about preparing your XBox device for test.


### The Basics:
The Rokuality bindings operate via Image Based Object Recognition and OCR techniques to identify 'elements' on the device screen and return them to your test scripts as Objects for verification and interaction. The project is modeled after the Selenium/Appium structure so if you've used those toolsets for browsers/mobile devices previously - this framework will look and feel very comfortable to you. See the [Roku example tests](https://github.com/rokuality/rokuality-python/blob/master/tests/test_roku.py)  or the [XBox example tests](https://github.com/rokuality/rokuality-python/blob/master/tests/test_xbox.py) for a full list of samples.

#### Declare a driver to connect to the server:
```python
    '''Roku'''
    driver = RokuDriver("http://yourserverurl:yourrunningserverport", self.capabilities)

    '''XBox'''
    driver = XBoxDriver("http://yourserverurl:yourrunningserverport", self.capabilities)
```
This will take care of installing/launching your device app package, ensure the device is available and ready for test, and start a dedicated session on your device as indicated via your DeviceCapabilities object. See [Device Capabilities](#device-capabilities-explained) for an explanation of what capabilities are available for your driver startup.

#### Finding elements:
There are two primary ways of finding elements on your device:

1) TEXT
```python
    driver.finder().find_element(By().text("text to find on screen"))
```
In this example, the Rokuality server will capture the image from your device screen, and then perform an evaluation against the found text within that image and match it against your locator. If your locator text is NOT found, then a NoSuchElementException will be thrown. Tesseract is the default OCR engine used to perform textual evaluations. But you can optionally indicate that you want to use GoogleVision's OCR engine which requires you have a valid VisionUI service account setup with Google. See [Using Google Vision](#using-google-vision-ocr) for those details. But for most use cases, using the default tesseract engine is enough.

2) IMAGE - local image snippet file
```python
    driver.finder().find_element(By().image("/path/to/your/image/snippet.png"))
```
In this example, you can provide the path to an image snippet that you expect to be contained within your device screen. The server will then ship this image snippet to itself, capture the device screen, and evaluate if it exists on the device.

OR

3) IMAGE - url to to an image snippet file
```python
    driver.finder().find_element(By().image("http://urltoyourimagesnippet.png"))
```
In this example, you can provide a url to your locator image snippet and the server will download that image and evaluate it against the device screen. Useful for those more dynamic testing situations where you may want to query your application feeds to get the dynamic app images for evaluation, or if you want to keep your image based locators in a remote repository.

#### Elements as objects:
A found element can be stored to an object and additional details about it can be retrieved:
```python
    element = self.roku_driver.finder().find_element(By().text("Hello World!"))
    print("element x: " + str(element.get_x()))
    print("element y: " + str(element.get_y()))
    print("element width: " + str(element.get_width()))
    print("element height: " + str(element.get_height()))
    print("element confidence: " + str(element.get_confidence()))
    print("element text: " + element.get_text())
```
The element details include the elements location and size details as found on the device, the text contained within the match (relevent if an image snippet locator was provided), and the confidence score of the match with higher values indicating the confidence in your find:
```xml
    368
    319
    45
    19
    91.33713
    Hello World!
```

#### Sending remote control commands to the device:
To send remote button presses to the device you can do the following:
```python
    '''roku'''
    driver.remote().press_button(RokuButton.SELECT)
    
    '''xbox'''
    driver.remote().press_button(XBoxButton.A)
```
All remote commands are available. See [roku remote command](https://github.com/rokuality/rokuality-python/blob/master/src/enums/roku_button.py) or [xbox remote command](https://github.com/rokuality/rokuality-python/blob/master/src/enums/xbox_button.py) for all available remote buttons. Also you can send literal characters to the device if you need to interact with a Roku search selector (coming soon for XBox as well):
```python
    roku_driver.remote().send_keys("typing out hello world on a search screen")
```

#### Getting screen artifacts:
Various methods exist for getting screen artifacts such as the screen image, sub screen image, screen recording during test, and screen text:

```python
    '''get screen size'''
    driver.screen().get_screen_size()

    '''get screen image'''
    driver.screen().get_image()

    '''get the screen sub image from starting x,y with width/height'''
    driver.screen().get_image_sub_screen(1, 1, 300, 300)

    """get the screen recording of the test session from start to now
       note that the screen recordings are created by stitching the collected device screenshots
       together and video quality won't be the best"""
    driver.screen().get_recording()
```

#### Getting screen text:
Screen text of the device is returned as a collection of ScreenText objects as found on the screen. Each ScreenText item will be an object containing details about the found device text such as location, height, and width of the word as found on the device screen:
```python
    screen_texts = roku_driver.screen().get_text()
    for screen_text in screen_texts:
        x = screen_text.get_x()
        y = screen_text.get_y()
        width = screen_text.get_width()
        height = screen_text.get_height()
        confidence = screen_text.get_confidence()
```

Alternatively you can get the entire device screen as a full string via `driver.screen().get_text_as_string()`

#### Device Capabilities explained:
Various capabilities and values can be provided and passed to your driver instance at startup. Some of them are required and others are optional. The following are the minimum capabilities **required** to start a driver session.

#### Roku
```python
    '''init a capability object'''
    capabilities = DeviceCapabilities()

    '''indicates you want a Roku test'''
    capabilities.add_capability("Platform", "Roku")

    '''set the path or url to your sideloadable .zip'''
    capabilities.add_capability("AppPackage", "path/or/url/to/your/apppackage")

    '''set your roku ip address'''
    capabilities.add_capability("DeviceIPAddress", "yourdeviceipaddress")

    '''set your device username and password'''
    capabilities.add_capability("DeviceUsername", "yourdeviceusername")
    capabilities.add_capability("DevicePassword", "yourdevicepassword")

    '''set your OCR module - options are "Tesseract" or "GoogleVision"'''
    capabilities.add_capability("OCRType", "Tesseract")
    
    '''pass the capabilities and start your driver'''
    driver = RokuDriver("http://yourserverurl:yourrunningserverport", capabilities)
```

#### Xbox
```python
    '''init a capability object'''
    capabilities = DeviceCapabilities()

    '''indicates you want a XBox test'''
    capabilities.add_capability("Platform", "XBox")

    '''set the path or url to your .appxbundle package to install'''
    capabilities.add_capability("AppPackage", "path/or/url/to/your/apppackage")

    '''the app id - will be the friendly app name of your appxbundle'''
    capabilities.add_capability("App", "appid")

    '''set your xbox ip address'''
    capabilities.add_capability("DeviceIPAddress", "yourdeviceipaddress")

    '''set your logitech harmony info. see the why harmony and harmony setups section of the main server page for details'''
    capabilities.add_capability("HomeHubIPAddress", "yourharmonyipaddress")
    capabilities.add_capability("DeviceName", "devicenameassavedinharmony")

    '''set your OCR module - options are "Tesseract" or "GoogleVision"'''
    capabilities.add_capability("OCRType", "Tesseract")
    
    '''pass the capabilities and start your driver'''
    driver = XBoxDriver("http://yourserverurl:yourrunningserverport", capabilities)
```

| Capability  | Description | Required Or Optional | Notes |
| ------------- | ------------- | ------------- | ------------- |
| Platform | Indicates the target platform for the tests. Currently only 'Roku' and 'XBox' are supported but Playstation and other devices coming soon.  | Required | String |
| AppPackage | The sideloadable zip to be installed (Roku), or the .appxbundle (XBox). Must be a valid file path OR a valid url.  | Required | String |
| DeviceIPAddress | The ip address of your Roku or XBox  | Required | Your device MUST be reachable from the machine running the Rokuality server. |
| DeviceUsername | The dev console username created when you enabled developer mode on your device  | Required - Roku Only | String |
| DevicePassword | The dev console password created when you enabled developer mode on your device   | Required - Roku Only | String |
| ImageMatchSimilarity | An optional image match similarity default used during Image locator evaluations. A lower value will allow for greater tolerance of image disimilarities between the image locator and the screen, BUT will also increase the possibility of a false positive.  | Optional | Double. Defaults to .90 |
| ScreenSizeOverride | An optional 'WIDTHxHEIGHT' cap that all screen image captures will be resized to prior to match evaluation. Useful if you want to enforce test consistence across multiple device types and multiple developer machines or ci environments.  | Optional | String - I.e. a value of '1800x1200' will ensure that all image captures are resized to those specs before the locator evaluation happens no matter what the actual device screen size is.  |
| OCRType | The OCR type - Options are 'Tesseract' OR 'GoogleVision'. In most cases Tesseract is more than enough but if you find that your textual evalutions are lacking reliability you can provide 'GoogleVision' as a more powerful alternative. BUT if the capability is set to 'GoogleVision' you MUST have a valid Google Vision account setup and provide the 'GoogleCredentials' capability with a valid file path to the oath2 .json file with valid credentials for the Google Vision service.  | Required | String 
| GoogleCredentials | The path to a valid .json Google Auth key service file. | Optional but Required if the 'OCRType' capability is set to 'GoogleVision' | The .json service key must exist on the machine triggering the tests. See [Using Google Vision](#using-google-vision-ocr) for additional details.  |
| HomeHubIPAddress | The ip address of your logitech harmony hub. | Required for those devices that indicate it during their setup requirement, i.e. XBox | String - See the [why harmony](https://github.com/rokuality/rokuality-server) and [configuring your harmony](https://github.com/rokuality/rokuality-server) sections of the server page for details. |
| DeviceName | The name of your device as saved in your Harmony hub i.e. 'MyXBoxOne'. | Required for those devices that indicate it during their setup requirement, i.e. XBox | String |

#### Element Timeouts and Polling:
There are two main options when it comes to element timeouts and polling

Timeouts - By default the element timeout is set to 0 milliseconds, meaning if the driver fails to find an element immediately, it will throw a NoSuchElement exception. But a better practice is to set a implicit wait timeout so the driver will poll for a duration, trying to find the element before it fails and throws the NoSuchElementException:

```python
    '''will fail immediately'''
    driver.finder().find_element(By().text("no such test"))
```
vs
```python
    '''will fail after 5 seconds'''
    driver.options().set_element_timeout(5000)
    driver.finder().find_element(By().text("no such test"))
```
It is generally recommended to set respective timeouts to reduce test flake, but setting the values too high can increase test duration.

Additionally you can set the interval of how often the element search polling will happen. In this example, the same timeout is applied but the element polling will happen every second. If the polling interval is ommited the default is 250 milliseconds.
```python
    '''will fail after 5 seconds polling every second'''
    driver.options().set_element_timeout(5000)
    driver.options().set_element_poll_interval(1000)
    driver.finder().find_element(By().text("no such test"))
```

#### Using Google Vision OCR:
As mentioned previously, Tesseract is the default OCR engine used when you provide a text based locator. And the Rokuality server ships the relevant trained data files so the more you use it during test, the better it will get at finding the provided text based locators. But if you find that's not as reliable as needed for your testing purposes you can use Google Vision as an alternative provided you have a valid [Google Vision](https://cloud.google.com/vision/docs/before-you-begin) account setup. You must also set the path to your .json service file containing your service key in your DeviceCapabilities prior to driver start.

```python
    capabilities = DeviceCapabilities()
    capabilities.add_capability("OCRType", "GoogleVision")
    capabilities.add_capability("GoogleCredentials", "/path/to/your/vision/authkey.json")
```

#### Failing to find elements? :
Image Based Locators `By().image("pathorurltoyoourimagesnippet.png")`
1. Make sure your locator image snippet is in a valid image format. Most tests use .png format so for best results please use locators of this type.
2. Make sure that your image snippets are in good quality and you are doing an apples to apples comparison of the image snippet you wish to find within the screen image. Some image snipping tools are better than others, so if capturing static image snippets for later locator use be wary of the tools you're using. Alternatively, you can get a subscreen section from the device during test and save it as a static locator for later use.
`locator_to_use_later = driver.screen().get_image_sub_screen(40, 80, 160, 220)`
3. You can optionally set the "ImageMatchSimilarity" DeviceCapability at driver startup which will set a tolerance for image comparisons. Lower values will mean a greater likelihood of getting a match, but too low of a value will introduce a false positive.
`capabilities.add_capability("ImageMatchSimilarity", .85)`

Text Based Locators `By().text("text to search for")`
1. Check that your string isn't too complicated, i.e. a locator of `By().text("hello world")` is much more likely to be found than a locator of `By().text("he!!O W@rLd!#!")`. Also, single world locators are better than multiple world locators but we continue to work on the server back end to improve the reliability.
2. As mentioned previously, Tesseract is the default OCR engine but if you're finding that the results aren't as reliable as you'd like, consider using [Google Vision](#using-google-vision-ocr) as an alternative.
3. You can access the entire decoded device screen text by `driver.screen().get_text_as_string()`. If your locator is present in the string but not found during test, please log a bug on the [issues](https://github.com/rokuality/rokuality-java/issues) page and we'll investigate.
4. By default the OCR evaluations happen against the entire device screen but sometimes it's better to narrow the scope of the find to a smaller region of the screen to get better results. This can be done with `driver.finder().find_element_sub_screen(by, 100, 500, 300, 200)` which will limit the scope of the find to that subset of the screen and likely return better results.

#### Server timeouts and orphaned sessions:
At the end of every driver session, you should close the driver and cleanup all session data by calling the stop method:
```python
    '''stop the driver and clean up all resources'''
    driver.stop()
```
But if you don't a safety exists to eventually clean up those assets. The server session will listen for new commands and will timeout if no commands for the session have been received for a specified duration. The default command timeout is set to 60 seconds - meaning if a session is started and no commands are sent to it for 60 seconds, then the session will automatically be terminated and released. You can increase/decrease this time by setting the 'commandtimeout' option when you launch the server. See the [Server Command Options](https://github.com/rokuality/rokuality-server) section of the server for details.
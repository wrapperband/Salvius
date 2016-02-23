import zorg
import time


def work(salvius):
    from serial import SerialException

    using_emic = True

    try:
        salvius.speech_synthesis.start()
        salvius.speech_synthesis.set_voice(1)
    except SerialException:
        using_emic = False

    salvius.speech_recognition.start()

    while True:
        try:
            recognized_speech = salvius.speech_recognition.get_words()

            if recognized_speech:

                print(recognized_speech)
                salvius.communication.get_response(recognized_speech)

                if using_emic:
                    salvius.speech_synthesis.speak()
                else:
                    # TODO: use espeak if emic is not available
                    pass

            time.sleep(1)
        except (KeyboardInterrupt, EOFError, SystemExit):
            break


def main():
    robot = zorg.robot({
        "name": "Salvius",
        "connections": {
            "camera": {
                "adaptor": "zorg_network_camera.Camera",
                "url": "http://192.168.1.6/image.jpg"
            },
            "chatterbot": {
                "adaptor": "salvius.communication.Conversation",
                "io_adapter": "chatterbot.adapters.io.JsonAdapter"
            },
            "serial": {
                "adaptor": "zorg_emic.Serial",
                "port": "/dev/ttyAMA0",
            },
            "sphinx": {
                "adaptor": "salvius.speech.SpeechRecognition",
                "recognizer_function": "recognize_sphinx"
            },
            "analytics": {
                "adaptor": "iot_analytics.apps.zorg.GoogleAnalytics",
                "property_id": "UA-12573345-12",
                "client_id": "salvius",
            },
        },
        "devices": {
            "camera_one": {
                "connection": "camera",
                "driver": "zorg_network_camera.Feed"
            },
            "camera_ocr": {
                "connection": "camera",
                "driver": "zorg_network_camera.OCR"
            },
            "communication": {
                "connection": "chatterbot",
                "driver": "salvius.communication.ApiDriver"
            },
            "speech_synthesis": {
                "connection": "serial",
                "driver": "zorg_emic.Emic2",
            },
            "speech_recognition": {
                "connection": "sphinx",
                "driver": "salvius.speech.ApiDriver",
            },
            "touch_sensor": {
                "connection": "analytics",
                "driver": "iot_analytics.apps.zorg.drivers.Event",
            }
        },
        "work": work,
    })

    api = zorg.api("zorg.api.Http", {})

    try:
        robot.start()
        api.start()
    except (KeyboardInterrupt, EOFError, SystemExit):
        pass


if __name__ == "__main__":
    main()
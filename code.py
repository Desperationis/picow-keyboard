import socketpool
import wifi
import usb_hid
from adafruit_httpserver import Server, Request, Response, GET, POST
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)


wifi.radio.start_ap(ssid="picow-keyboard", password="picow-keyboard")
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)

key_translate = {
    "enter": Keycode.ENTER,
    "escape": Keycode.ESCAPE,
    "backspace": Keycode.BACKSPACE,
    "delete": Keycode.DELETE,
    "l_shift": Keycode.LEFT_SHIFT,
    "l_control": Keycode.LEFT_CONTROL,
    "l_alt": Keycode.LEFT_ALT,
    "l_shift": Keycode.RIGHT_SHIFT,
    "l_control": Keycode.RIGHT_CONTROL,
    "l_alt": Keycode.RIGHT_ALT,
    "f1": Keycode.F1,
    "f2": Keycode.F2,
    "f3": Keycode.F3,
    "f4": Keycode.F4,
    "f5": Keycode.F5,
    "f6": Keycode.F6,
    "f7": Keycode.F7,
    "f8": Keycode.F8,
    "f9": Keycode.F9,
    "f10": Keycode.F10,
    "f11": Keycode.F11,
    "f12": Keycode.F12,
    "windows": Keycode.WINDOWS,
    "tab": Keycode.TAB
}

FORM_HTML_TEMPLATE = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multiline Input Form</title>
</head>
<body>
    <h1>Web interface for pico-keyboard</h1>
    <form action="/" method="post" enctype="text/plain">
        <label for="keyboard_data">Enter your text:</label><br>
        <input type="text" name="data" placeholder="Type something..."><br>
        <label for="press_enter">Press ENTER?</label>
        <input type="checkbox" id="press_enter" name="press_enter"><br>

        <label for="special_1">Special Key 1 (Overrides text)</label>
        <select id="special_1" name="special_1">
            <option value="none">N/A</option>
            <option value="enter">ENTER</option>
            <option value="escape">ESC</option>
            <option value="backspace">BACKSPACE</option>
            <option value="delete">DEL</option>
            <option value="l_shift">LSHIFT</option>
            <option value="l_control">LCTRL</option>
            <option value="l_alt">LALT</option>
            <option value="r_shift">RSHIFT</option>
            <option value="r_control">RCONTROL</option>
            <option value="r_alt">RALT</option>
            <option value="f1">F1</option>
            <option value="f2">F2</option>
            <option value="f3">F3</option>
            <option value="f4">F4</option>
            <option value="f5">F5</option>
            <option value="f6">F6</option>
            <option value="f7">F7</option>
            <option value="f8">F8</option>
            <option value="f9">F9</option>
            <option value="f10">F10</option>
            <option value="f11">F11</option>
            <option value="f12">F12</option>
            <option value="windows">WINDOWS</option>
            <option value="tab">TAB</option>
        </select>

        <br>
        <label for="special_2">Special Key 2 (Overrides text)</label>
        <select id="special_2" name="special_2">
            <option value="none">N/A</option>
            <option value="enter">ENTER</option>
            <option value="escape">ESC</option>
            <option value="backspace">BACKSPACE</option>
            <option value="delete">DEL</option>
            <option value="l_shift">LSHIFT</option>
            <option value="l_control">LCTRL</option>
            <option value="l_alt">LALT</option>
            <option value="r_shift">RSHIFT</option>
            <option value="r_control">RCONTROL</option>
            <option value="r_alt">RALT</option>
            <option value="f1">F1</option>
            <option value="f2">F2</option>
            <option value="f3">F3</option>
            <option value="f4">F4</option>
            <option value="f5">F5</option>
            <option value="f6">F6</option>
            <option value="f7">F7</option>
            <option value="f8">F8</option>
            <option value="f9">F9</option>
            <option value="f10">F10</option>
            <option value="f11">F11</option>
            <option value="f12">F12</option>
            <option value="windows">WINDOWS</option>
            <option value="tab">TAB</option>
        </select>
        <br>
        <label for="shortcut_char">Char to use shortcut with: (lowercase)</label>
        <input type="text" id="shortcut_char" name="shortcut_char" maxlength="1">
        <br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

@server.route("/", [GET, POST])
def form(request: Request):
    """
    Serve a form with the given enctype, and display back the submitted value.
    """
    enctype = "text/plain"

    if request.method == POST:
        text_sent = request.form_data["data"]
        key1 = request.form_data["special_1"]
        key2 = request.form_data["special_2"]
        shortcut_char = request.form_data["shortcut_char"]
        enter = "press_enter" in request.form_data

        print(request.form_data)
        if key1 == "none" and key2 == "none":
            data = request.form_data.get("data")

            print("Decoded:")
            print(data)

            if enter:
                data += "\n"

            layout.write(data)

        else:
            # Shortcut mode
            keycodes = []

            if key1 != "none":
                keycodes.append(key_translate[key1])

            if key2 != "none":
                keycodes.append(key_translate[key2])

            if len(shortcut_char) > 0:
                keycodes.extend(layout.keycodes(shortcut_char))


            print(f"Sending {keycodes}")
            kbd.send(*keycodes)

    return Response(
        request,
        FORM_HTML_TEMPLATE,
        content_type="text/html",
    )


server.serve_forever("0.0.0.0", 80)

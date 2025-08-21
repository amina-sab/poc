from pipeline.sanitizer import sanitize_input

def test_unicode_fix():
    assert sanitize_input("caf\xe9") == "café"

def test_base64_decode():
    assert "hello" in sanitize_input("aGVsbG8=")

def test_control_chars():
    assert "\x00" not in sanitize_input("test\x00test")

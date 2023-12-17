def test_filter_invalid_char():
    origin_str = ": 'Hello, world! This is a test string.'"
    expected_result = "Hello, world! This is a test string."
    result = filter_invalid_char(None, origin_str)
    assert result == expected_result, f"Expected: {expected_result}, but got: {result}"

    origin_str = '"Another test string with special characters: @#$\"'
    expected_result = 'Another test string with special characters: @#$"'
    result = filter_invalid_char(None, origin_str)
    assert result == expected_result, f"Expected: {expected_result}, but got: {result}"

    origin_str = "No special characters in this string"
    expected_result = "No special characters in this string"
    result = filter_invalid_char(None, origin_str)
    assert result == expected_result, f"Expected: {expected_result}, but got: {result}"

    print("All test cases passed!")
def filter_invalid_char(self, origin_str):
        s = origin_str.replace(": ", ":")
        while len(s) > 0 and (s[0] == "'" or s[0] == '"'):
            s=s[1:]
        return s
test_filter_invalid_char()
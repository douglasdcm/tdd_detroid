def test_taxonomy():
    funcs = []
    for func in funcs:
        report_result(func)


def report_result(func):
    print(f"{func.__name__}")
    try:
        print(f"RESULT: {func()}")
    except Exception as e:
        print(str(e))

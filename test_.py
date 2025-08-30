def test_modules():
    from main import import_modules

    assert import_modules() == "Modules imported"
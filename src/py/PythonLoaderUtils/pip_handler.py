import sys, os, subprocess


def check_for_pip() -> bool:
    try:
        import pip

        print("Pip Found!")
        return True
    except ImportError as e:
        print("Pip Not Found!")
        return False


def install_pip() -> bool:
    from measure_host import MeasureHost

    inst = MeasureHost.get_instance()

    print("Hello")

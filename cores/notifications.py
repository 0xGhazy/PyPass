# By: Hossam Hamdy
# all notifications functions in PyPass project

from win10toast import ToastNotifier

def copy_notification() -> None:
    toaster = ToastNotifier()
    toaster.show_toast("[+] PyPass Application",
        "The password has been moved to the clipboard successfully!",
        duration = 5)


def add_notification() -> None:
    toaster = ToastNotifier()
    toaster.show_toast("[+] PyPass Application",
        "A new account has been added to database",
        duration = 5)


def del_notification() -> None:
    toaster = ToastNotifier()
    toaster.show_toast("[+] PyPass Application",
        "The account has been removed successfully!",
        duration = 5)


def edit_notification() -> None:
    toaster = ToastNotifier()
    toaster.show_toast("[+] PyPass Application",
        "The account has been updated successfully!",
        duration = 5)

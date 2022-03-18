import os
import getpass
from datetime import datetime


class LogSystem:
    f"""
    DESCRIPTION:

        class for handling all logging system process for application.


    DATA:
        cwd = currant working directory.
        log_file = Logs.txt
        user_name = {getpass.getuser()}
        time-now = {str(datetime.now())}
        currant_directories = a list of all directories and files in the same directory.


    FUNCTIONS:

        create_log_file() -> None
            creating a new log.txt file to use in case of we need to add any event to logs.

        write_into_log() -> None
            Function to write into Log.txt file to add an event to logs


    Example:
        >>> write_into_log("!" , "Application has closed.")
            [!] User: MyPC --- Time: 2021-11-10 21:04:25.515886 --- Event: Application has closed.

    """

    def __init__(self) -> None:
        self_cwd = os.chdir(os.path.dirname(__file__))
        self.log_file = "Logs.txt"
        self.user_name = getpass.getuser()
        self.time_now = str(datetime.now())
        self.currant_directories = os.listdir(self_cwd)
        self.create_log_file()


    def create_log_file(self: "LogSystem") -> None:
        """ Function to create a log file if it doesn't exist. """
        # check if the Log.txt file was exist
        if os.path.isfile(self.log_file):
            pass
        else:
            # creating Log.txt file in the same directory.
            with open(self.log_file, "a") as log_file_obj:
                log_file_obj.write(self.write_into_log("+", "Log file was created"))


    def write_into_log(self: "LogSystem", status: str, message: str) -> str:
        """ Function to write into Log.txt file to add an event to logs

        Args:
            self (LogSystem): [LogSystem object]
            status (str): [(!) -> Warning,
                           (-) -> Error,
                           (+) -> info]
            message (str): [event message]
        """
        with open(self.log_file, 'a') as log_file_obj:
            # write the statement to the log file
            log_file_obj.write(f"[{status}] User: {self.user_name} --- Time: {self.time_now} --- Event: {message}\n")

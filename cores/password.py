import random
import string

class Password:
    """
        Password class takes care of:
        - Checks for password stregth.
        - Generates strong random password that contains lower/upper/numbers,
          random password legth 16 bits.
    """

    def __init__(self):
        self._password_strength = 0
        self._max_strength = 4           # Covers all cases/constraints
        self._random_password = ""


    def check_length(self: "Password", password: str) -> None:
        if len(password) >= 8:
            self._password_strength += 1

    def check_lower(self: "Password", password: str) -> None:
        for letter in password:
            if letter in string.ascii_lowercase:
                self._password_strength += 1
                break

    def check_upper(self: "Password", password: str) -> None:
        for letter in password:
            if letter in string.ascii_uppercase:
                self._password_strength += 1
                break

    def check_symbols(self: "Password", password: str) -> None:
        symbols = string.punctuation
        for letter in password:
            if letter in symbols:
                self._password_strength += 1
                break

    def check_numbers(self: "Password", password: str) -> None:
        for letter in password:
            if letter.isdigit():
                self._password_strength += 1
                break


    ## Get password strength score (x of 5)
    def check_strength(self: "Password", password: str) -> int:
        self.check_length(password)
        self.check_lower(password)
        self.check_numbers(password)
        self.check_symbols(password)
        self.check_upper(password)
        return self._password_strength


    def generate_password(self: "Password") -> str:
        self._random_password = ""
        for _ in range(0, 16):
            self._random_password += random.choice(
            string.ascii_uppercase + 
            string.ascii_lowercase +
            string.digits)
        return self._random_password


if __name__ == '__main__':
    x = Password()
    print("[+] Generate random password")
    x.generate_password()
    print("Random password: ", x._random_password)

    print("\n\n[+] Check password strength")
    x.check_strength("Hello_World 2022")
    print(x._password_strength)

import os
from cryptography.fernet import Fernet
import getpass

class Security:
    f"""
    DESCRIPTION:

        Class for handling all encryption process in the application.

    DATA:

        currant_username = {getpass.getuser()}
        log_obj = log_system class object


    FUNCTIONS:

        generate_key() -> None
            creates an encryption key for encryption process.

        load_encryption_key() -> Bytes
            reading encryption key content and return it.

        encrypt(plain_text) -> str
            encrypting plain text with loaded encryption key from the same path.

        decrypt(encrypted_text) -> str
            decrypt encrypted message with the same encryption key in the same path.

            
    EXAMPLE:
    
        >>> import Security
        >>> x  = Security()
        >>> message = "Hello"
        >>> encrypted_message = x.encrypt(message)
        >>> print(str(encrypted_message.decode()))
            gAAAAABhjTcFEm4vpY6RCxoPvicsaxIrnQoe274H-iEcuUYWFIiLCKte1DL5Rc6rM9_rWGd5n52wp4QqiFV965zTABkbqFDsqw==
        >>> print(x.decrypt(encrypted_message))
            Hello
    """


    def __init__(self: "Security") -> None:
        # change working directory to __file__ direnamee
        os.chdir(os.path.dirname(__file__))
        self.currant_username = getpass.getuser()
        if "security_key.key" in os.listdir():
            pass
        else:
            self.generate_key()
        

    def generate_key(self: str) -> None:
        """Function to generate encryption key at first time of running the application."""
        self.key = Fernet.generate_key()
        with open("security_key.key", "wb") as key_obj:
            key_obj.write(self.key)
        print("[+] It's important to take a copy of encryption key :)")

    
    def load_encryption_key(self: "Security") -> bin:
        """Function to read encryption key (security_key.key) from the same directory"""
        try:
            with open("security_key.key", "rb") as key_obj:
                return key_obj.read()
        except Exception as error_message:
            print(f"[-] {str(error_message)}")


    def encrypt(self: "Security", message: str) -> str:
        """Function to encrypt message/data using encryption key"""
        # reading the encryption key
        key = self.load_encryption_key()
        encoded_message = message.encode()
        f = Fernet(key)
        # return the encrypted message
        encrypted_message = f.encrypt(encoded_message)
        return encrypted_message.decode()


    def decrypt(self: "Security", encrypted_message: bytes) -> str:
        """Decrypts an encrypted message"""
        key = self.load_encryption_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message)
        return decrypted_message.decode()


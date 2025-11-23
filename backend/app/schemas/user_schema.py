class UserLoginSchema:
    """
    Data transfer object for login.
    """

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class UserRegisterCustomerSchema:
    """
    Data for creating a customer with a user login.
    """

    def __init__(
        self,
        username: str,
        password: str,
        name: str,
        email: str,
        phone: str,
        license_number: str,
    ):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.phone = phone
        self.license_number = license_number

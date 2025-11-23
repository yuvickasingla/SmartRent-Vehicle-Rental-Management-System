from typing import Optional
from ..models import User, Customer
from ..schemas import UserLoginSchema, UserRegisterCustomerSchema
from ..utils import UserRole


class AuthManager:
    """
    Handles registration and login logic.
    """

    def register_customer(self, schema: UserRegisterCustomerSchema) -> User:
        """
        Create a Customer and a linked User with role 'customer'.
        """
        # Create customer profile first
        customer = Customer(
            name=schema.name,
            email=schema.email,
            phone=schema.phone,
            license_number=schema.license_number,
        ).save()

        # Create user record
        user = User(
            username=schema.username,
            password=schema.password,  # plain text as requested
            role=UserRole.CUSTOMER.value,
            customer_id=customer.id,
        ).save()

        return user

    def authenticate(self, schema: UserLoginSchema) -> Optional[User]:
        """
        Validate username + password.
        Returns User if valid, else None.
        """
        user = User.find_by_username(schema.username)
        if user is None:
            return None
        if user.password != schema.password:
            return None
        return user

    def list_customers(self) -> list[Customer]:
        """
        Admin helper: get all customers.
        """
        return Customer.get_all()

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        return Customer.get_by_id(customer_id)

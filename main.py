from src.core.factory.factory import Factory


def create_factory() -> Factory:
    return Factory()


def main():
    factory = create_factory()
    validator = factory.get_validator_repository()
    return validator.return_language()


if __name__ == "__main__":
    main()

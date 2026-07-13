import yaml


def print_yaml(result):

    print(
        yaml.safe_dump(
            result,
            sort_keys=False
        )
    )
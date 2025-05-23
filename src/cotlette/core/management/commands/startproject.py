from cotlette.core.management.templates import TemplateCommand
from cotlette.core.management.utils import get_random_secret_key



SECRET_KEY_INSECURE_PREFIX = "insecure-"


class Command(TemplateCommand):
    help = (
        "Creates a Cotlette project directory structure for the given project "
        "name in the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide a project name."

    def handle(self, **options):
        project_name = options.pop("name")
        target = options.pop("directory")

        # Create a random SECRET_KEY to put it in the main settings.
        options["secret_key"] = SECRET_KEY_INSECURE_PREFIX + get_random_secret_key()

        super().handle("project", project_name, target, **options)

from cotlette.core import migrations

class Migration:
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='GroupModel',
            table='groups_groupmodel',
            fields=[
                ("id", "INTEGER", {'autoincrement': True, 'primary_key': True}),
                ("name", "VARCHAR(100)", {'unique': True}),
                ("description", "VARCHAR(100)")
            ],
        )
    ]

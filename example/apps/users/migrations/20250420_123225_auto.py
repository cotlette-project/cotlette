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
        ),

        migrations.CreateModel(
            name='UserModel',
            table='users_usermodel',
            fields=[
                ("id", "INTEGER", {'autoincrement': True, 'primary_key': True}),
                ("name", "VARCHAR(50)"),
                ("age", "INTEGER"),
                ("email", "VARCHAR(100)"),
                ("password_hash", "VARCHAR(255)"),
                ("group", "INTEGER"),
                ("organization", "VARCHAR(100)")
            ],
        )
    ]

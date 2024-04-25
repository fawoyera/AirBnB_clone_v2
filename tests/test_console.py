#!/usr/bin/env python3
"""
    Test module for the Airbnb console
"""
import unittest
import cmd
from console import HBNBCommand
from io import StringIO
from models.__init__ import storage
from models.base_model import BaseModel
from models.user import User
import sys
from unittest.mock import patch


class TestHBNBCommand(unittest.TestCase):
    """Test class for the console"""
    def test_class_attr(self):
        """Test if class is subclass of cmd.Cmd and class attributes exist"""
        self.assertTrue(issubclass(HBNBCommand, cmd.Cmd))

    def test_help(self):
        """Test if console print help text on typing commannd help"""
        with patch('sys.stdout', new=StringIO()) as f:

            # Test the output of command help show
            HBNBCommand().onecmd("help show")
            self.assertIn("[Usage]: show <className> <objectId>", f.getvalue())

    def test_create(self):
        """Test the method create which creates new instance of a class"""
        with patch('sys.stdout', new=StringIO()) as f:

            # Test output when no class name is entered
            HBNBCommand().onecmd("create")
            self.assertEqual(f.getvalue().strip('\n'),
                             "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:

            # Test when class name is not a recognised class
            HBNBCommand().onecmd("create MyModel")
            self.assertEqual(f.getvalue().strip('\n'),
                             "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:

            # Test if new instance of specified class is created and saved
            # Only when command usage is correct: create <class name>
            HBNBCommand().onecmd("create BaseModel")
            i_id = f.getvalue().strip('\n')  # save the instance_id
            self.assertEqual(type(i_id).__name__, "str")  # test if string
            self.assertEqual(len(i_id), 36)  # test if instance id has 36 char
            self.assertIn(f"BaseModel.{i_id}", storage.all())

            # Test if instance is reloaded from file correctly on reload
            storage.reload()
            self.assertIn(f"BaseModel.{i_id}", storage.all())

        with patch('sys.stdout', new=StringIO()) as f:

            # Test if new instance of specified class is created and saved
            # Only when command usage is correct:
            # create <class name> <param 1> <param 2> <param 3>...
            HBNBCommand().onecmd('create State name="Ethiopia"')
            i_id = f.getvalue().strip('\n')  # save the instance_id
            self.assertEqual(type(i_id).__name__, "str")  # test if string
            self.assertEqual(len(i_id), 36)  # test if instance id has 36 char
            self.assertIn(f"State.{i_id}", storage.all())
            self.assertEqual(storage.all()[f"State.{i_id}"].name, "Ethiopia")

            # Test if instance is reloaded from file correctly on reload
            storage.reload()
            self.assertIn(f"State.{i_id}", storage.all())

    def test_show(self):
        """Test the command show of the console.

        This prints the string representation of an instance
        """
        with patch('sys.stdout', new=StringIO()) as f:

            # Test output when no class name is entered
            HBNBCommand().onecmd("show")
            self.assertEqual(f.getvalue().strip('\n'),
                             "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:

            # Test when class name is not a recognised class
            HBNBCommand().onecmd("show MyModel")
            self.assertEqual(f.getvalue().strip('\n'),
                             "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:

            # Test output when no id is entered
            HBNBCommand().onecmd("show BaseModel")
            self.assertEqual(f.getvalue().strip('\n'),
                             "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:

            # Test output when given class instance with id is not found
            HBNBCommand().onecmd("show BaseModel 121212")
            self.assertEqual(f.getvalue().strip('\n'),
                             "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            # Create an instance and get the id
            base1 = BaseModel()
            base1.save()

            # Test output when given class instance with id is found in file
            # Only when command usage is correct: show <class name> <id>
            HBNBCommand().onecmd(f"show BaseModel {base1.id}")
            output = f.getvalue().strip('\n')  # save the output
            self.assertTrue(output.startswith(f"[BaseModel] ({base1.id})"))

    def test_destroy(self):
        """Test the destroy command

        Usage: destroy <class name> <id>
        """
        with patch('sys.stdout', new=StringIO()) as f:

            # Test output when no class name is entered
            HBNBCommand().onecmd("destroy")
            self.assertEqual(f.getvalue().strip('\n'),
                             "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:

            # Test when class name is not a recognised class
            HBNBCommand().onecmd("destroy MyModel")
            self.assertEqual(f.getvalue().strip('\n'),
                             "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:

            # Test output when no id is entered
            HBNBCommand().onecmd("destroy User")
            self.assertEqual(f.getvalue().strip('\n'),
                             "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:

            # Test output when given class instance with id is not found
            HBNBCommand().onecmd("destroy User 121212")
            self.assertEqual(f.getvalue().strip('\n'),
                             "** no instance found **")

        # Test output when given class instance with id is found in file
        # Only when command usage is correct: destroy <class name> <id>

        # Create an instance of User
        user1 = User()
        user1.save()

        with patch('sys.stdout', new=StringIO()) as f:

            # Confirm instance is saved to file
            HBNBCommand().onecmd(f"show User {user1.id}")
            output = f.getvalue().strip('\n')  # save the output
            self.assertTrue(output.startswith(f"[User] ({user1.id})"))

            # Destroy the instance
            HBNBCommand().onecmd(f"destroy User {user1.id}")

        with patch('sys.stdout', new=StringIO()) as f:
            # Confirm instance is no longer in file
            HBNBCommand().onecmd(f"show User {user1.id}")
            output = f.getvalue().strip('\n')  # save the output
            self.assertEqual(output, "** no instance found **")

    def test_all(self):
        """Test the command all of the console"""
        pass

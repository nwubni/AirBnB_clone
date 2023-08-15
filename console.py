#!/usr/bin/python3
"""
entry point of the command interpreter
"""
import cmd

from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    class HBNBCommand inherits from cmd.Cmd
    """
    prompt = "(hbnb) "
    __model_list = ["BaseModel", "User",
                    "State", "City", "Amenity",
                    "Place", "Review"]

    def do_create(self, line):
        """
        creates an instance of BaseModel
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__model_list:
            print("** class doesn't exist **")
        # elif len(args) == 1:
            # print("** instance id missing **")
        else:
            new_instance = eval(args[0])(*args[1:])
            new_instance.save()
            print(new_instance.id)

    def do_show(self, line):
        """
        prints the string representation of an instance
        based on the class name and id
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__model_list:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in storage.all():
            print("** no instance found **")

    def do_destroy(self, line):
        """
        deletes an instance based on the class name and id
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__model_list:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in storage.all():
            print("** no instance found **")
        else:
            del storage.all()[args[0] + "." + args[1]]
            storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances"""
        args = line.split()
        args_len = len(args)
        output = []
        if args_len > 0 and args[0] not in HBNBCommand.__model_list:
            print("** class doesn't exist **")
            return
        elif args_len > 0 and args[0] in HBNBCommand.__model_list:
            for key, value in storage.all().items():
                if key.startswith(args[0]):
                    output.append(str(value))
        else:
            for obj in storage.all().values():
                output.append(str(obj))

        print(output)

    @staticmethod
    def build_str(arg):
        """
        Builds a string from values found in
        quotations from the given argument

        Parameters
        arg : string
            The argument contains characters
            to build the string

        Return
            The string found between a pair of
            quotations
        """
        temp = []
        increment = 3
        value = ""

        temp = arg.split()
        while increment < len(temp):
            value += temp[increment]
            if temp[increment].endswith("\""):
                break
            value += " "
            increment += 1

        return value[1:-1]

    def do_update(self, line):
        """
        updates an instance based on the class name and
        id by adding or updating attribute
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__model_list:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in storage.all():
            print("** no instance found **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if len(args) == 2:
                print("** attribute name missing **")
            elif len(args) == 3:
                print("** value missing **")
            else:
                if args[3].isdigit():
                    setattr(storage.all()[key], args[2], int(args[3]))
                elif "." in args[3]:
                    setattr(storage.all()[key], args[2], float(args[3]))
                else:
                    args[3] = HBNBCommand.build_str(line)
                    setattr(storage.all()[key], args[2], args[3])

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """ handles Ctrl + D pressed"""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()

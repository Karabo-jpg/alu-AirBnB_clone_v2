#!/usr/bin/python3
"""Console module for AirBnB clone."""
import cmd
import sys
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter for AirBnB clone."""
    prompt = "(hbnb) "
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program."""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty line."""
        pass

    def do_create(self, arg):
        """Create a new instance of a class."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        new_instance = self.__classes[class_name]()
        # Set attributes if provided
        for param in args[1:]:
            if '=' in param:
                key, value = param.split('=', 1)
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('_', ' ')
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                setattr(new_instance, key, value)
        storage.new(new_instance)
        storage.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Show the string representation of an instance."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = f"{class_name}.{obj_id}"
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
            return
        print(obj)

    def do_destroy(self, arg):
        """Delete an instance based on class name and id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = f"{class_name}.{obj_id}"
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
            return
        storage.delete(obj)
        storage.save()

    def do_all(self, arg):
        """Print all instances of a class or all instances."""
        args = arg.split()
        objects = storage.all()
        if not args:
            print([str(obj) for obj in objects.values()])
            return
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        print([str(obj) for obj in objects.values()
               if obj.__class__.__name__ == class_name])

    def do_update(self, arg):
        """Update an instance based on class name and id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = f"{class_name}.{obj_id}"
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attr_name = args[2]
        attr_value = args[3]
        if attr_value.startswith('"') and attr_value.endswith('"'):
            attr_value = attr_value[1:-1].replace('_', ' ')
        elif '.' in attr_value:
            try:
                attr_value = float(attr_value)
            except ValueError:
                pass
        else:
            try:
                attr_value = int(attr_value)
            except ValueError:
                pass
        if attr_name in ["id", "created_at", "updated_at"]:
            return
        setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()

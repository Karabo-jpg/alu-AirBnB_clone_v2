#!/usr/bin/python3
"""Test script for storage functionality"""
from models import storage
from models.state import State

# Print initial count
print(len(storage.all(State)))  # Should print 0

# Create 3 states
for i in range(3):
    state = State(name=f"State_{i}")
    state.save()
storage.reload()  # Ensure changes are loaded
print(len(storage.all(State)))  # Should print 3

# Create 2 more states
for i in range(2):
    state = State(name=f"Extra_State_{i}")
    state.save()
storage.reload()  # Ensure changes are loaded
print(len(storage.all(State)))  # Should print 5 
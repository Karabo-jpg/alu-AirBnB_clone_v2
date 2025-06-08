#!/usr/bin/python3
"""Test script for states_list route"""
from models import storage
from models.state import State


def test_states():
    """Test different scenarios for states_list route"""
    # Clear all states
    states = storage.all(State)
    for state in states.values():
        storage.delete(state)
    storage.save()

    # Test with 0 states
    print("Testing with 0 states...")
    print(len(storage.all(State)))

    # Add 5 states
    for i in range(5):
        state = State(name=f"State_{i}")
        state.save()
    print("\nTesting with 5 states...")
    print(len(storage.all(State)))

    # Add one more state
    state = State(name="Extra_State")
    state.save()
    print("\nTesting with 6 states...")
    print(len(storage.all(State)))

    # Add more states (total 100)
    for i in range(94):
        state = State(name=f"State_{i+6}")
        state.save()
    print("\nTesting with 100 states...")
    print(len(storage.all(State))) 
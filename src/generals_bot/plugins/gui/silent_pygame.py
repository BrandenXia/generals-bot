from os import environ


def silent_pygame():
    """Import pygame and hide the support prompt"""
    environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    import pygame

    return pygame

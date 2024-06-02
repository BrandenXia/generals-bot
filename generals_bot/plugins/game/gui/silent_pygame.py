from os import environ


def silent_pygame():
    environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    import pygame

    return pygame

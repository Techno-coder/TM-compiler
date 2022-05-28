"""
Generates a Turing Machine that checks if 
the binary string is a palindrome or not.

Strategy: We check whether the symbols at either ends of the
current string are equal or not. If they are, then we remove them
and repeat.
"""

from tm_compiler import compile

# Flags are individual bits of state that persist across
# TM state transitions. In other words, they represent bits of "memory".
# 
# We achieve this by having concrete TM states for every possible 
# flag combination for every possible label. This means, that the number of
# concrete states is proportional to 2^F where F is the number of flags.
flags = [
    # Set if the current bit is a 1.
    "isOne",
]

compile(flags, {
    # Each label has a list of associated transitions.
    # A label here is analogous to labels in assembly or C.
    # They represent a particular position in the "program" (concretely, a TM state).
    "storeBit": [
        (
            [],     # The flags that must be set or unset for this transition to be activated.
            "0",    # The current symbol under the head for this transition to match. ("*")
            "_",    # The replacement symbol. ("*" or "_")
            "r",    # The next direction to move the head to. ("l" or "r" or "*")
            (
                "moveToRight",  # The next label to transition to.
                []              # Any flags that will be set or unset. ("flag" or "!flag")
            )
        ),
        ([], "1", "_", "r", ("moveToRight", ["isOne"])),
        # If the current symbol is blank, then there are no more pairs
        # of symbols to check, and so we know the string is a palindrome.
        ([], "_", "*", "*", "halt-accept"),
    ],
    # Move to the rightmost symbol, then transition to "checkMatches".
    "moveToRight": [
        ([], "_", "*", "l", ("checkMatches", [])),
        ([], "*", "*", "r", ("moveToRight", [])),
    ],
    # Check the current symbol matches a 1 if "isOne" is set.
    "checkMatches": [
        # If the current symbol is blank, then there is no pairing
        # symbol and so we know the string is a palindrome. That is,
        # the current string has a length of 1.
        ([], "_", "*", "*", "halt-accept"),
        # We also reset the flag "isOne" after we have checked that it matches
        # so that on the next iteration, we start from a blank state.
        (["isOne"], "1", "_", "l", ("moveToLeft", ["!isOne"])),
        (["!isOne"], "0", "_", "l", ("moveToLeft", [])),
        ([], "*", "*", "*", "halt-reject"),
    ],
    # Move to the leftmost symbol and return to the start.
    "moveToLeft": [
        ([], "_", "*", "r", ("storeBit", [])),
        ([], "*", "*", "l", ("moveToLeft", [])),
    ],
}, "storeBit") # The initial state.


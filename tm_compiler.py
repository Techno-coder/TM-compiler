import itertools

SPECIAL_TARGETS = ["halt-accept", "halt-reject"]


def compile(all_flags, blocks, start_block):
    """
    Compiles a program to the format usable in:

        <http://morphett.info/turing/turing.html>

    ## Arguments

    `all_flags` - A list of strings representing all the global flags for this machine
    `blocks` - A dictionary of labels to a list of transitions
    `start_block` - The label of the starting block

    ## What is a transition?
    
    A transition takes the form:

        `(required_flags, symbol, new_symbol, direction, (new_label, new_flags))`

    A flag can be either a name ("flag") or the negation of the name ("!flag").
    A transition is executed if all the flags in `required_flags` match. Upon
    execution, the existing flags are *overwritten* by `new_flags` if they are
    referenced. If they are not referenced, the previous flag's state is kept.

    If `new_label` is `None`, the same label is kept for convenience. The tuple
    may also take the special values `"halt-accept"` and `"halt-reject"` which
    terminates execution.
    """
    if start_block not in blocks:
        raise ValueError(f"undefined starting block `{start_block}`")

    # Print flags.
    print("; == Flags ==")
    for flag in all_flags:
        print(f"; {flag}")
    print()

    # Print labels.
    print("; == Labels ==")
    for label in blocks:
        print(f"; {label}")
    print()

    # Set starting transition.
    print(f"; == Transitions ==")
    print(f"0 * * * {start_block}0")

    # Generate and normalize combinations of flags.
    flag_states = []
    for flag_state in power_set(all_flags):
        flag_states.append(sorted(flag_state))

    # Generate transitions for each label.
    for label, transitions in blocks.items():
        visited = set()
        for flag_state in flag_states:
            # Generate transitions.
            state_a = f"{label}{flag_states.index(flag_state)}"
            for (required, symbol, new_symbol, lr, target) in transitions:
                key = (state_a, symbol)
                if key in visited:
                    continue

                if not flag_requirements_fulfilled(flag_state, required):
                    continue

                # Generate target label.
                if target not in SPECIAL_TARGETS:
                    new_label, new_flags = target
                    new_flag_state = overwrite_flag_state(flag_state, new_flags)
                    if new_label is None:
                        new_label = label

                    # Verify label.
                    if new_label not in blocks:
                        raise ValueError(f"invalid block `{new_label}`")

                    # Verify flag names.
                    for flag in new_flag_state:
                        if flag not in all_flags:
                            raise ValueError(f"invalid flag `{flag}`")

                    state_b = f"{new_label}{flag_states.index(new_flag_state)}"
                else:
                    state_b = target

                # Print transition.
                print(f"{state_a} {symbol} {new_symbol} {lr} {state_b}")
                visited.add(key)


def power_set(l):
    for r in range(0, len(l) + 1):
        for combination in itertools.combinations(l, r):
            yield list(combination)


def overwrite_flag_state(flag_state, new_flags):
    flag_state = flag_state.copy()
    for flag in new_flags:
        (is_true, name) = parse_flag(flag)
        if is_true:
            if name not in flag_state:
                flag_state.append(name)
        else:
            if name in flag_state:
                flag_state.remove(name)

    flag_state.sort()
    return flag_state


def flag_requirements_fulfilled(flag_state, required):
    for flag in required:
        (is_true, name) = parse_flag(flag)
        is_present = name in flag_state
        if is_true != is_present:
            return False
    return True


def parse_flag(flag):
    if flag[0] == "!": return (False, flag[1:])
    return (True, flag)


# To run: "python tests/examples/Example_print_current_branch.py"

from external_resources.executables import GitExecutable, executable_type_defs


# TODO - add manager to handle initial checks?
GIT = GitExecutable()
GIT.throw_if_unavailable()


def get_current_branch() -> str:
    r = GIT.use(executable_type_defs.ExecutableUseArgs(args=["branch"]))
    assert r.return_code == 0
    lines = r.stdout.split("\n")
    for line in lines:
        if "*" not in line:
            continue
        return line.split("*")[1].strip()
    raise ValueError(f"Could not find current branch in stdout: {r.stdout}")


print("Current branch is:", get_current_branch())

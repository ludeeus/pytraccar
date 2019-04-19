workflow "Release" {
  on = "release"
  resolves = ["Publish to PyPi"]
}

action "Publish to PyPi" {
  uses = "mariamrf/py-package-publish-action@v0.0.2"
  secrets = ["TWINE_USERNAME", "TWINE_PASSWORD"]
}

workflow "Push" {
  on = "push"
  resolves = [
    "Black Code Formatter",
    "Pytest",
  ]
}

action "Black Code Formatter" {
  uses = "lgeiger/black-action@v1.0.1"
  args = ". --check"
}

action "Pytest" {
  uses = "cclauss/GitHub-Action-for-pytest@0.0.2"
  args = "python3 -m pip install -e .; python3 setup.py test"
}

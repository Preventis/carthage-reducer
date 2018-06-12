# carthage-reducer

# Problem

We are using a monorepo and one big workspace to handle different apps and frameworks.

First pain point is the need to fetch for each framework all dependencies und add them to the final app. One possibility to overcome this issue is to use umbrella frameworks, which is in several ways very ugly.

Secondly, some repos on GitHub contain broken binaries of their frameworks, or you broke them by yourself (for instance using Xcode 10 to try one thing out or another).

At third, Carthage is able to cache builds, but you need to specify `--cache-builds` everytime you invoke Carthage.

# Solution

This small script collects all the dependency information from all specified framework projects, writes one final Cartfile for the project / monospace as a whole, and invokes Carthage with your desired `CarthageConfig.json`.

This is still WIP.

# Usage

Very simple, just invoke `python3 carthage.py`.

Some options can be specified in `CarthageConfig.json`.

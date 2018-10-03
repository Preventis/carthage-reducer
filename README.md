# carthage-reducer

Small Carthage helper script which helps in overcoming some pain points while working with monorepos.

# Problem

We are using a monorepo and one big workspace to handle different apps and frameworks.

- First pain point is the need to fetch all dependencies for each framework und add them to the final app. One possibility to overcome this issue is to use umbrella frameworks, which is in several ways very ugly.
- Secondly some repos on GitHub contain broken binaries of their frameworks, or you broke them by yourself (for instance using Xcode 10 to try one thing out or another). Thus we use of the `--no-use-binaries` argument can help.
- At third Carthage is able to cache builds, but you need to specify `--cache-builds` everytime you invoke Carthage.

# Solution

This small script collects all the dependency information from all specified framework projects, writes one final Cartfile for the project / monospace as a whole, and invokes Carthage with your desired `CarthageConfig.json`.

# Usage

Very simple, just invoke `python3 carthage.py`.

Some options can be specified in `CarthageConfig.json`.

## Hint

In order to overcome the pain with adding each framework, which is used, to the base apps, we use `carthage-copy-frameworks`. [lvillani](https://github.com/lvillani) did an awesome job, [lvillani/carthage-copy-frameworks](https://github.com/lvillani/carthage-copy-frameworks).

## Related

We wrote an article on how we achieved a collection of modular components as building blocks for different mobile apps. With this small helper script we found a way to reduce our spent time on Carthage (cloning, building, waiting) significantly.

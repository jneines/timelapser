# timelapser


Python based timelapsing service for IP cams

The timelapser allows to (quite) easily create a timelapse video based on snapshots taken from a suitable IP camera based on rules defined in a program description.

Currently all IP cameras offering a webservice endpoint to deliver a jpeg based image are supported.

This piece of software has been developed for use with a raspberry pi based setup to act as an IP camera by using the awesome [camera-streamer](https://github.com/ayufan/camera-streamer) project.

To configure the software a combination of a config file with at least listing the cameras name, its snapshot url and a program name, as well as the program description itself is required.
The latter at least holds an identifier for the type of the program, which currently is one of either `base`, `fuzzy` or `solar`, and usually an `start_ts`, `end_ts` and `every` setting.

Some examples for these config and program files are given in the related directories in this repository.

After installing this package, and creating the necessary set of configuration files, the app can be started using `timelapser -c <config_name>`, with `config_name` being the name of the json encoded `config_file`.

This application makes use of pyythons platformdirs package to locate the correct paths for the config and data dirs used in this package.
On Linux based systems for example config files have to go in the ${HOME}/.config/timelapser directory, whereas programs have to be stored in the ${HOME}/.local/share/timelapser/programs directory.

Aside from the usual requirements listed in the requirements.txt, the `video_processor` component currently expects an `ffmpeg` binary to be found at `/usr/bin/ffmpeg` in order to operate.


* Free software: MIT license
* Documentation: https://timelapser.readthedocs.io.


### Credits

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

[Cookiecutter](https://github.com/audreyr/cookiecutter)
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)

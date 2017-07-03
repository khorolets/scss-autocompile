import sublime
import sublime_plugin

import os
import re
import subprocess
import json


BOOLEAN_MAP = {'true': True, 'false': False, '1': True, '0': False}

class ExampleCommand(sublime_plugin.EventListener):
    """
    Plugin for controlled scss autocompilation

    Usage:
        In your main scss file you simple add:
        // out: <filepath>
        // sourcemap: <true | false>
        // compress: <true | false>

        <filepath> may be relative

        In the including files you need to simply add:
        // main: ../path/to/main.scss
        This would trigger that file every time you'd be saving the including one
    """

    @staticmethod
    def _parse_parameter_value(value):
        """
        Checks if value in available data of boolean representation
        """
        if value in BOOLEAN_MAP:
            return BOOLEAN_MAP[value]
        return value

    def on_post_save(self, view):
        if view.file_name().split('.')[-1].lower() == 'scss':
            regions_of_keywords = view.find_all(
                    r"(out|sourcemap|compress|main):\s(.+css|.+scss|true|false)", sublime.IGNORECASE
                )
            parameters = {}
            for region in regions_of_keywords:
                text = view.substr(region)
                parameters.update(
                        {text.split(':')[0].strip(): self._parse_parameter_value(text.split(':')[1].strip())}
                    )
            print(parameters)
            if parameters:
                main_file = None
                if 'main' in parameters:
                    main_file = os.path.join(
                            os.path.dirname(view.file_name()), parameters['main']
                        )

                    parameters = self._get_parameters_from_main_file(
                            file_name=os.path.join(
                                    os.path.dirname(view.file_name()),
                                    parameters['main']
                                )
                        )
                self._compile(
                        main_file or view.file_name(), **parameters
                    )

    def _get_parameters_from_main_file(self, file_name):
        """
        Reads the main file to parse parameters from there

        Args:
            file_name: absolute path to main file
        Returns:
            parameter dict
        """
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                main_file_content = f.read()

                match = re.findall(
                        r"(out|sourcemap|compress|main):\s(.+css|.+less|true|false)",
                        main_file_content
                    )
                if match:
                    return dict(
                            zip(
                                    [m[0] for m in match],
                                    [self._parse_parameter_value(m[1]) for m in match]
                                )
                        )
        return {}


    def _compile(self, file_name, out, compress=False, sourcemap=False):
        """
        SCSS compilation itself. It calls system `node-sass-chokidar` command that should be
        available after `npm install -g node-sass-chokidar` and the it should be added to the path
        """
        print('compile scss')
        destination = os.path.join(
                os.path.dirname(file_name),
                out
            )

        env = os.environ.copy()
        if sublime.platform() == 'osx':
            env['PATH'] += ':/usr/local/bin'
        elif sublime.platform() == 'windows':
            env['PATH'] += ';%s\AppData\Roaming\\npm' % os.path.expanduser("~")
        else:
            env['PATH'] += ':/usr/bin'

        compile_command = [
            "node-sass-chokidar",
            '--output-style=compressed' if compress else '',
            '--source-map=true' if sourcemap else '',
            str(file_name),
            str(destination),
        ]
        print(
            " ".join(compile_command)
        )
        proc = subprocess.Popen(
            compile_command,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True if sublime.platform() == 'windows' else False
        )
        out, err = proc.communicate()
        if err:
            error = err.decode('utf-8')
            error = json.loads(error)
            formatted = re.sub("(\[\d+m)","", error['formatted'])
            sublime.error_message(formatted)

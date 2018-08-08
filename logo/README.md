# Codestar Logo Generator

Use this tool for generating PNGs of the Codestar logo at various sizes and options.

For guidelines about which color versions to use, refer to the parent directory in this repository.

For convenience, PNG images are always generated with a `@2x` "retina" variant.

## Running

You will need Python 3 (`brew install python3`).

Installing the dependencies:

```bash
brew install cairo
pip3 install -r requirements.txt
```

Then, you can use the tool either by calling it directly: `./logo.py [OPTIONS]` or by invoking it through python: `python3 logo.py [OPTIONS]`

## Usage

```bash
$ ./logo.py --help
Usage: logo.py [OPTIONS]

Options:
  -c, --color [standard|light|dark|monochrome|all]  Color of the logo to generate (Repeatable).
  -o, --option [tagline]                            Additional feature to add to the logo (Repeatable, all apply at
                                                    once).
  -f, --format [png|svg]                            Desired image file format (Repeatable).  [required]
  -H, --height INTEGER                              Desired logo height, only for non-vector formats (Repeatable).
  -W, --width INTEGER                               Desired logo width, only for non-vector formats (Repeatable).
  -nz, --no-zip                                     Don't package output in an archive.
  -h, --help                                        Show this message and exit.
```

Examples:

- Generating all color variants in SVG, with tagline, in a zip file:
    ```bash
    ./logo.py -c all -f svg -o tagline
    ```

- Generating monochrome logos with no taglines at various widths, in a local directory:
    ```bash
    ./logo.py -c monochrome -f png -W 128 -W 256 -W 512 -nz
    ```

- Generating light and dark theme logos at a fixed height:
    ```bash
    ./logo.py -c light -c dark -H 200
    ```

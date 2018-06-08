#!/usr/bin/env python3

import os
import copy
import click
import shutil
import tempfile
import cairosvg
from lxml import etree

click.utils.make_default_short_help.__defaults__ = (100,)
click.formatting.HelpFormatter.write_dl.__defaults__ = (100, 2)

colors_choices = ["standard", "light", "dark", "monochrome"]
options_choices = ["tagline"]
formats_choices = ["png", "svg"]

with open("logo.svg") as f:
    original_logo = etree.parse(f).getroot()


def generate_style(left_color="#f08300", right_color="#ffffff", right_opacity="0.45"):
    return """
        .st0{{fill:{left_color};}}
        .st1{{fill:{right_color};opacity:{right_opacity};}}
        .st3{{fill:{right_color};opacity:{right_opacity};}}
    """.format(left_color=left_color, right_color=right_color, right_opacity=right_opacity)


def generate_filename(destination, color, options, format, width=None, height=None, retina=False):
    name = "codestar_logo_%s" % color
    if options:
        name += "_(%s)" % "_".join(options)
    if width:
        name += "_[width=%d]" % width
    if height:
        name += "_[height=%d]" % height
    if retina:
        name += "@2x"
    name += ".%s" % format

    return os.path.join(destination, name)


@click.command(context_settings = {
    "help_option_names": ["-h", "--help"],
    "max_content_width": 120
})
@click.option("-c", "--color", "colors",
              type=click.Choice(colors_choices + ["all"]), multiple=True,
              help="Color of the logo to generate (Repeatable).")
@click.option("-o", "--option", "options",
              type=click.Choice(options_choices), multiple=True,
              help="Additional feature to add to the logo (Repeatable, all apply at once).")
@click.option("-f", "--format", "formats",
              type=click.Choice(formats_choices), multiple=True, required=True,
              help="Desired image file format (Repeatable).")
@click.option("-H", "--height", "heights",
              type=int, multiple=True,
              help="Desired logo height, only for non-vector formats (Repeatable).")
@click.option("-W", "--width", "widths",
              type=int, multiple=True,
              help="Desired logo width, only for non-vector formats (Repeatable).")
@click.option("-nz", "--no-zip", is_flag=True, default=False,
              help="Package all files in a zip archive.")
def logo(colors, options, formats, heights, widths, no_zip):
    ratio = 2102 / 558
    if "tagline" not in options:
        ratio = 2102 / 421
        for root in original_logo.xpath("/*"):
            x, y, w, h = [float(elem) for elem in root.attrib["viewBox"].split()]
            h = w * (1 / ratio)
            root.attrib["viewBox"] = "%g %g %g %g" % (x, y, w, h)
        for tagline in original_logo.xpath("/*[local-name() = 'svg']/*[local-name() = 'g']/*[local-name() = 'g'][2]"):
            tagline.getparent().remove(tagline)

    if "all" in colors:
        colors = colors_choices

    with tempfile.TemporaryDirectory() as temp_dir:
        for color in colors:
            logo = copy.deepcopy(original_logo)

            if color == "standard":
                style = generate_style()
            elif color == "light":
                style = generate_style(right_color="#000000", right_opacity="1.00")
            elif color == "dark":
                style = generate_style(right_opacity="1.00")
            elif color == "monochrome":
                style = generate_style(left_color="#000000", right_color="#000000", right_opacity="1.00")

            logo[0].text = style

            if "svg" in formats:
                # Save SVG in tempdir
                with open(generate_filename(temp_dir, color, options, "svg", retina=False), "w") as f:
                    f.write(etree.tostring(logo).decode("utf-8"))

            if "png" in formats:
                def make_png(width=None, height=None, retina=False):
                    factor = 2 if retina else 1

                    if width:
                        kwargs = {
                            "parent_width": width * factor,
                            "parent_height": width * factor * (1 / ratio)
                        }
                    elif height:
                        kwargs = {
                            "parent_width": height * factor * ratio,
                            "parent_height": height * factor
                        }

                    cairosvg.svg2png(
                        bytestring=etree.tostring(logo),
                        write_to=generate_filename(temp_dir, color, options, "png", width=width, height=height, retina=retina),
                        **kwargs
                    )

                for height in heights:
                    make_png(height=height)
                    make_png(height=height, retina=True)
                for width in widths:
                    make_png(width=width)
                    make_png(width=width, retina=True)

        destination = "./codestar_logos"
        if no_zip:
            if os.path.exists(destination):
                shutil.rmtree(destination)
            shutil.copytree(temp_dir, destination)
        else:
            shutil.make_archive(destination, "zip", temp_dir)


if __name__ == "__main__":
    logo()

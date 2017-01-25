"""Classes for validating user-controlled values."""

# This file WAS part of PASTA, which is forked from SATe
# It has been edited heavily since being copied from PASTA
#
# PASTA, like SATe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Jiaye Yu and Mark Holder, University of Kansas

import ConfigParser
import os
# import glob

# import pdb


def _underscores_to_dashes(s):
    return '-'.join(s.split('_'))

def open_with_intermediates(filepath, mode):
    """Opens a `filepath` in the `mode`, but will create intermediate directories if they are absent."""
    d = os.path.dirname(filepath)
    if d:
        if not os.path.exists(d):
            os.makedirs(d)
        elif not os.path.isdir(d):
            raise IOError('The file "%s" cannot be created because "%s" exists but is not a directory' % (filepath, d))
    return open(filepath, mode)

class UserSetting(object):
    def __init__(self, name, default, **kwargs):
        self.name = name
        self.default = default
        self.short_name = kwargs.get('short_name')
        self.subcategory = kwargs.get('subcategory')
        self.must_be_valid = kwargs.get('must_be_valid')
        if self.subcategory is None:
            self.subcategory = ''
        self.help = kwargs.get('help')
        self._value = self.default
    def is_valid(self):
        return self.value is not None

    def get_value(self):
        return self._value
    def set_value(self, v):
        self._value = v
    value = property(get_value, set_value)
    def as_config_parsable(self):
        v = self.value
        if v is None:
            return None
        return str(v)
    def _get_optparse_option_args_dict(self):
        kwargs = {'dest' : self.name,
                    'default' : None
                    }
        if self.help is not None:
            kwargs['help'] = self.help
        return kwargs

    def add_to_optparser(self, parser):
        kwargs = self._get_optparse_option_args_dict()
        long_name = '--%s' % _underscores_to_dashes(self.name)
        if self.short_name and len(self.short_name) == 1:
            parser.add_option('-%s' % self.short_name, long_name, **kwargs)
        else:
            parser.add_option(long_name, **kwargs)


class StringUserSetting(UserSetting):
    pass

class ChoiceUserSetting(UserSetting):
    def __init__(self, name, default, choices, multiple_choices=False, **kwargs):
        UserSetting.__init__(self, name, default, **kwargs)
        self.multiple_choices = multiple_choices
        self.choices = [i.lower() for i in choices]
        self.value = default
    def get_value(self):
        return self._value
    def set_value(self, v):
        if v is None:
            self._value = None
            return
        if self.multiple_choices:
            o = v.strip()
            if o.startswith('[') and o.endswith(']'):
                quoted_toks = [i.strip() for i in o[1:-1].split()]
                sq = "'"
                dq = '"'
                x = []
                if (i.startswith(sq) and i.endswith(sq)) or (i.startswith(dq) and i.endswith(dq)):
                    x.append(i[1:-1].lower())
            else:
                x = [i.lower() for i in o.split()]
            for el in x:
                if el not in self.choices:
                    raise ValueError("%s is not a valid setting for %s. Exepcting one of %s" % (el, self.name, str(self.choices)))
            self._value = x
        else:
            el = v.lower()
            if el not in self.choices:
                raise ValueError("%s is not a valid setting for %s" % (el, self.name))
            self._value = el
    value = property(get_value, set_value)
    def as_config_parsable(self):
        v = self.value
        if v is None:
            return None
        if self.multiple_choices:
            return ' '.join(v)
        return str(v)

class NumberUserSetting(UserSetting):
    def __init__(self, name, default, min=None, max=None, **kwargs):
        UserSetting.__init__(self, name, default, **kwargs)
        self.max = max
        self.min = min
    def get_value(self):
        return self._value
    def set_value(self, v):
        v = self.conv_type(v)
        if (self.max is not None) and v > self.max:
            raise ValueError("%s must be <= %s" % (self.name, str(self.max)))
        if (self.min is not None) and v < self.min:
            raise ValueError("%s must be >= %s" % (self.name, str(self.min)))
        self._value = v
    value = property(get_value, set_value)

class BoolUserSetting(UserSetting):
    def __init__(self, name, default, min=None, max=None, **kwargs):
        UserSetting.__init__(self, name, default, **kwargs)
        self.value = default
        self.default = self.value
    def get_value(self):
        return self._value
    def set_value(self, v):
        if isinstance(v, str):
            l = v.lower()
            self._value = l in ['1', 'true']
        elif isinstance(v, int):
            self._value = (v != 0)
        elif isinstance(v, bool):
            self._value = v
        else:
            raise TypeError("Expecting a boolean for %s" % self.name)
    value = property(get_value, set_value)

    def add_to_optparser(self, parser):
        kwargs = UserSetting._get_optparse_option_args_dict(self)
        if bool(self.default):
            kwargs['action'] = 'store_false'
            long_name = '--no-%s' % _underscores_to_dashes(self.name)
        else:
            kwargs['action'] = 'store_true'
            long_name = '--%s' % _underscores_to_dashes(self.name)
        if self.short_name and len(self.short_name) == 1:
            parser.add_option('-%s' % self.short_name, long_name, **kwargs)
        else:
            parser.add_option(long_name, **kwargs)

class FloatUserSetting(NumberUserSetting):
    def __init__(self, name, default, min=None, max=None, **kwargs):
        self.conv_type = float
        NumberUserSetting.__init__(self, name, default, min=min, max=max, **kwargs)
        self.value = default
    def _get_optparse_option_args_dict(self):
        kwargs = UserSetting._get_optparse_option_args_dict(self)
        kwargs['type'] = 'float'
        kwargs['metavar'] = '#.#'
        return kwargs

class IntUserSetting(NumberUserSetting):
    def __init__(self, name, default, min=None, max=None, **kwargs):
        self.conv_type = int
        NumberUserSetting.__init__(self, name, default, min=min, max=max, **kwargs)
        self.value = default
    def _get_optparse_option_args_dict(self):
        kwargs = UserSetting._get_optparse_option_args_dict(self)
        kwargs['type'] = 'int'
        kwargs['metavar'] = '#'
        return kwargs

class UserSettingGroup(object):
    def __init__(self, name):
        self.name = name
        self.options = {}

    def add_option(self, k, o):
        self.options[k] = o

    def remove_option(self, o):
        del self.options[o]

    def dict(self):
        d = {}
        for k, v in self.options.iteritems():
            d[k] = v.value
        return d

    def keys(self):
        return self.dict().keys()

    def __getattr__(self, att_name):
        try:
            return self.__dict__['options'][att_name].value
        except:
            raise AttributeError("Attribute %s not found" % att_name)
    def __setattr__(self, att_name, value):
        if att_name in ['name', 'options']:
            self.__dict__[att_name] = value
        else:
            o = self.options.get(att_name)
            if o is None:
                raise AttributeError("Attribute %s not found" % att_name)
            o.value = value
    def set_config_parser_fields(self, p):
        if not p.has_section(self.name):
            p.add_section(self.name)
        for opt in self.all_options():
            v = opt.as_config_parsable()
            if v is not None:
                p.set(self.name, opt.name, v)

    def read_config_parser_fields(self, parsed):
        try:
            items = parsed.items(self.name)
        except ConfigParser.NoSectionError:
            return
        for p in items:
            k, v = p
            opt = self.options.get(k)
            if opt is not None:
                opt.value = v
            else:
                print 'Unknown option "%s" in section "%s" skipped!' % (k, self.name)
                # _LOG.warn('Unknown option "%s" in section "%s" skipped!' % (k, self.name))

    def all_options(self):
        key_opt_list =[i for i in self.options.iteritems()]
        key_opt_list.sort()
        return [i[1] for i in key_opt_list]

    def subcategories(self):
        s = set()
        for opt in self.all_options():
            s.add(opt.subcategory)
        l = list(s)
        l.sort()
        return l

    def add_to_optparser(self, parser):
        from optparse import OptionGroup
        s_list = self.subcategories()
        for s in s_list:
            n = self.name
            if n == 'sate': # how is this  for a hack
                n = 'SATe'
            if s:
                g = OptionGroup(parser, '%s %s options' % (n, s))
            else:
                g = OptionGroup(parser, '%s options' % n)
            parser.add_option_group(g)
            for opt in self.all_options():
                if opt.subcategory == s:
                    opt.add_to_optparser(g)

    def set_values_from_dict(self, d):
        """Walks through the keys of `d` and sets any matching UserSetting.name
        to the value in `d` ONLY IF the value in `d` is not None.
        """
        for o in self.all_options():
            v = d.get(o.name)
            if v is not None:
                o.value = v

class UserSettingsContainer(object):

    def __init__(self):
        self._categories = []
        self._config_parser = ConfigParser.RawConfigParser()

    def read_config_filepath(self, filepath):
        self._config_parser.read(filepath)
        for gn in self._categories:
            g = getattr(self, gn)
            g.read_config_parser_fields(self._config_parser)

    def save_to_filepath(self, filepath):
        if filepath is None:
            filepath = os.path.expanduser(os.path.join( 'work', 'settings.cfg'))
        # f = open_with_intermediates(filepath, 'wb')
        f = open_with_intermediates(filepath, 'wb')
        for g in self.get_categories():
            g.set_config_parser_fields(self._config_parser)
        self._config_parser.write(f)
        f.close()

    def get(self, category):
        "Returns a UserSettingGroup based on name or None"
        i = self.__dict__.get(category)
        if isinstance(i, UserSettingGroup):
            return i
        return None

    def get_categories(self):
        c = [i for i in self.__dict__.iteritems() if isinstance(i[1], UserSettingGroup)]
        c.sort()
        return [i[1] for i in c]

    def set_values_from_dict(self, d):
        """Walks through the keys of `d` and sets any matching UserSetting.name
        to the value in `d` ONLY IF the value in `d` is not None.
        """
        for c in self.get_categories():
            c.set_values_from_dict(d)
    def dicts(self):
        d = {}
        for  c in self.get_categories():
            d[c.name] = c.dict()
        return d

class PhylostratorUserSettings(UserSettingsContainer):
    def __init__(self):
        UserSettingsContainer.__init__(self)
        self.starting_file_paths = UserSettingGroup('starting_file_paths')
        self._categories.append('starting_file_paths')
        self.cairo = UserSettingGroup('cairo')
        self._categories.append('cairo')
        self.spread = UserSettingGroup('spread')
        self._categories.append('spread')
        self.placement = UserSettingGroup('placement')
        self._categories.append('placement')

        self.starting_file_paths.add_option('init_tree_path',UserSetting(name='init_tree_path', default='', short_name=None, help='Path to tree file to be opened on startup', subcategory=None))
        self.starting_file_paths.add_option('init_annotation_path',UserSetting(name='init_annotation_path', default='', short_name=None,help='Path to annotation file to be opened on startup',subcategory=None))
        self.starting_file_paths.add_option('temp_subtree_path',UserSetting(name='temp_subtree_path', default='', short_name=None,help='Path to tree file to be opened on startup',subcategory=None))
        self.starting_file_paths.add_option('init_working_folder',UserSetting(name='init_working_folder', default='', short_name=None,help='Folder to be used to save images, etc...',subcategory=None))
        self.starting_file_paths.add_option('sepp_placement_path',UserSetting(name='sepp_placement_path', default='', short_name=None,help='Path to the SEPP placement JSON file...',subcategory=None))
        self.starting_file_paths.add_option('sepp_annotation_path',UserSetting(name='sepp_annotation_path', default='', short_name=None,help='Path to the SEPP annotation file...',subcategory=None))
        self.cairo.add_option('jitter_radius',IntUserSetting(name='jitter_radius', default=3, min=0, max=None, short_name=None, help='The radius to jitter circles by randomly when they are not placed on the leaves of the tree [default: 3]', subcategory=None))
        self.cairo.add_option('sepp_alphas',FloatUserSetting(name='sepp_alphas', default=0.55, min=0.0, max=1.0,short_name=None,help='Alpha values for cirlces at ends of tree placements.',subcategory=None))
        self.cairo.add_option('node_alphas',FloatUserSetting(name='node_alphas', default=0.75, min=0.0, max=1.0, short_name=None,help='Alpha values for circles at nodes.', subcategory=None))
        self.cairo.add_option('tree_line_width',FloatUserSetting(name='tree_line_width', default=0.01, min=0.0, max=None, short_name=None,help='Width of the lines used to draw the tree.', subcategory=None))
        self.cairo.add_option('image_width',IntUserSetting(name='image_width', default=1500, min=0, max=None, short_name=None,help='Width of the png image.',subcategory=None))
        self.cairo.add_option('image_height',IntUserSetting(name='image_height', default=900, min=0, max=None, short_name=None,help='Height of the png image.', subcategory=None))
        self.cairo.add_option('legend_block_size',IntUserSetting(name='legend_block_size', default=20, min=0, max=None, short_name=None,help='Height of the blocks for the legend.', subcategory=None))
        self.cairo.add_option('legend_spacing',IntUserSetting(name='legend_spacing', default=3, min=0, max=None, short_name=None,help='Vertical spacing between legend entries', subcategory=None))
        self.cairo.add_option('tree_line_color_rgb',UserSetting(name='tree_line_color_rgb', default='240,240,240', short_name=None,help='Color of the branches of the tree.', subcategory=None))
        self.placement.add_option('show_all_seven_placements',BoolUserSetting(name='show_all_seven_placements', default=False, short_name=None,help='True if we want to show all the placements in the tree with non-zero probability. If False, only shows the most probable', subcategory=None))
        self.spread.add_option('max_angle',FloatUserSetting(name='max_angle', default=0.34, min=0.0, max=None, short_name=None,help='Maximum change to an edge angle in a single iteration.', subcategory=None))


        # print self.starting_file_paths.

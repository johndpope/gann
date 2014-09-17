#
# 3-party libraries
#
from django.utils import timezone


#
# project libraries
#
from history.models import Taiex, Tx


#
# module classes
#
class ProductGroup():
    """Sub-group commands handler for product information."""

    symbols = ['TAIEX', 'TX']
    actions = ['list', 'info']

    def complete_command(self, text, line, begin_index, end_index):
        if self.has_complete_action(line):
            return []
        elif not text:
            return self.actions
        else:
            completions = []
            for act in self.actions:
                if act.startswith(text):
                    completions.append(act)
            return completions

    def has_complete_action(self, line):
        for act in self.actions:
            if act in line:
                return True
        return False

    def perform(self, arg):
        if arg['list']:
            self.show_symbols()
        elif arg['info']:
            self.show_product_info(arg['<symbol>'])
        else:
            print "*** not supported"

    def show_symbols(self):
        for index, name in enumerate(self.symbols):
            print "%d. %s" % (index+1, name)

    def show_product_info(self, symbol):
        if symbol not in self.symbols:
            print "*** unknown symbol: %s" % symbol
        # calculate info title length for printing
        info_title = dict(
            symbol='Symbol',
            name='Name',
            size='Contract size',
            begin='Begin time',
            end='End time',
            )
        item_len = [len(v) for v in info_title.values()]
        min_width = max(item_len)
        # print info
        if symbol == 'TAIEX':
            print "{symbol:>{width}}: {value}".format(value=symbol,
                                                      width=min_width,
                                                      **info_title)
            full_name = "Taiwan Stock Exchange " + \
                        "Capitalization Weighted Stock Index"
            print "{name:>{width}}: {value}".format(value=full_name,
                                                    width=min_width,
                                                    **info_title)
            print "{size:>{width}}: {value}".format(value=None,
                                                    width=min_width,
                                                    **info_title)
            self._print_time_range(Taiex, info_title, min_width)
        elif symbol == 'TX':
            print "{symbol:>{width}}: {value}".format(value=symbol,
                                                      width=min_width,
                                                      **info_title)
            full_name = "TAIEX Futures"
            print "{name:>{width}}: {value}".format(value=full_name,
                                                    width=min_width,
                                                    **info_title)
            print "{size:>{width}}: {value}".format(value='200 NTD',
                                                    width=min_width,
                                                    **info_title)
            self._print_time_range(Tx, info_title, min_width)

    def _print_time_range(self, product, title_dict, title_width):
        data = product.objects.all().order_by('time')
        count = data.count()
        begin = data[0].time
        end = data[count-1].time
        self._print_time(title_dict['begin'], begin, title_width)
        self._print_time(title_dict['end'], end, title_width)

    def _print_time(self, title, value, title_width):
        curr_tz = timezone.get_current_timezone()
        value = value.astimezone(curr_tz)
        time_format = "%Y-%m-%d %H:%M:%S"
        print "{title:>{width}}: {value:{format}}".format(
            title=title,
            width=title_width,
            value=value,
            format=time_format)

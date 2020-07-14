# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from thetaetl.domain.amount_transfer import ThetaAmountTransfer
from thetaetl.mappers.amount_mapper import ThetaAmountMapper

class ThetaAmountTransferMapper(object):
    def __init__(self, amount_mapper=None):
        if amount_mapper is None:
            self.amount_mapper = ThetaAmountMapper()
        else:
            self.amount_mapper = amount_mapper

    def json_dict_to_amount_transfer(self, json_dict):
        amount_transfer = ThetaAmountTransfer()
        amount_transfer.address = json_dict.get('address')
        amount_transfer.sequence = json_dict.get('sequence')
        amount_transfer.signature = json_dict.get('signature')

        amount_transfer.coins = self.amount_mapper.json_dict_to_amount(json_dict.get('coins'))

        return amount_transfer

    def amount_transfer_to_dict(self, amount_transfer):
        if amount_transfer.coins is not None:
            coins = self.amount_mapper.amount_to_dict(amount_transfer.coins)
        return {
            'type': 'amount_transfer',
            'address': amount_transfer.address,
            'coins': coins,
            'sequence': amount_transfer.sequence,
            'signature': amount_transfer.signature
        }

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
#    Copyright (C) 2017 Chuan Ji <jichu4n@gmail.com>                          #
#                                                                             #
#    Licensed under the Apache License, Version 2.0 (the "License");          #
#    you may not use this file except in compliance with the License.         #
#    You may obtain a copy of the License at                                  #
#                                                                             #
#     http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                             #
#    Unless required by applicable law or agreed to in writing, software      #
#    distributed under the License is distributed on an "AS IS" BASIS,        #
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
#    See the License for the specific language governing permissions and      #
#    limitations under the License.                                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Tests for srslib."""

import re
import srslib

# Default instance for testing.
_srs = srslib.SRS(b'12345678')


def test_forward_1st_hop():
  addr = _srs.forward('alice@example.com', '1st.com')
  print(addr)
  assert re.fullmatch(
      r'SRS0=[A-Za-z+/]{4}=[A-Z2-7]{2}=example[.]com=alice@1st[.]com',
      addr)


def test_forward_2nd_hop():
  addr = _srs.forward(
      'SRS0-ASd+=11=example.com=alice@1st.com',
      '2nd.com')
  print(addr)
  assert re.fullmatch(
      r'SRS1=[A-Za-z+/]{4}=1st[.]com=-ASd[+]=11=example[.]com=alice@2nd[.]com',
      addr)


def test_forward_3nd_hop():
  addr = _srs.forward(
      'SRS1+ASd+=1st.com=-QwEr=11=example.com=alice@2nd.com',
      '3rd.com')
  print(addr)
  assert re.fullmatch(
      r'SRS1=[A-Za-z+/]{4}=1st[.]com=-QwEr=11=example[.]com=alice@3rd[.]com',
      addr)


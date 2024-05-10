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
import pytest
import srslib
import time

# Default instance for testing.
_srs = srslib.SRS(b'12345678')


def test_forward_1st_hop():
  srs0_addr = _srs.forward('alice@example.com', '1st.com')
  assert re.match(
      r'SRS0=[A-Za-z0-9+/]{4}=[A-Z2-7]{2}=example[.]com=alice@1st[.]com$',
      srs0_addr)


def test_forward_2nd_hop():
  srs1_addr = _srs.forward(
      'SRS0-ASd+=11=example.com=alice@1st.com',
      '2nd.com')
  assert re.match(
      r'SRS1=[A-Za-z0-9+/]{4}=1st[.]com=-ASd[+]=11=example[.]com=alice@2nd[.]com$',
      srs1_addr)


def test_forward_3nd_hop():
  srs1_addr = _srs.forward(
      'SRS1+ASd+=1st.com=-QwEr=11=example.com=alice@2nd.com',
      '3rd.com')
  assert re.match(
      r'SRS1=[A-Za-z0-9+/]{4}=1st[.]com=-QwEr=11=example[.]com=alice@3rd[.]com$',
      srs1_addr)


def test_reverse_3rd_hop():
  orig_addr = 'alice@example.com'
  srs0_addr = _srs.forward(orig_addr, '1st.com')
  rev_addr = _srs.reverse(srs0_addr)
  assert rev_addr == orig_addr
  addr = srs0_addr
  for i in range(2, 11):
    addr = _srs.forward(addr, '%d.com' % i)
    rev_addr = _srs.reverse(addr)
    assert rev_addr == srs0_addr


def test_reverse_prev_secrets():
  orig_addr = 'alice@example.com'
  new_srs = srslib.SRS(b'new secret', prev_secrets=[_srs._secret])
  ctl_srs = srslib.SRS(b'new secret')
  srs0_addr = _srs.forward(orig_addr, '1st.com')
  assert new_srs.reverse(srs0_addr) == orig_addr
  with pytest.raises(srslib.InvalidHashError):
    ctl_srs.reverse(srs0_addr)
  addr = srs0_addr
  for i in range(2, 11):
    addr = _srs.forward(addr, '%d.com' % i)
    rev_addr = new_srs.reverse(addr)
    assert rev_addr == srs0_addr
    with pytest.raises(srslib.InvalidHashError):
      ctl_srs.reverse(rev_addr)


def test_check_timestamp():
  past_srs = srslib.SRS(_srs._secret)
  now_srs = srslib.SRS(_srs._secret, validity_days=10)
  now = time.time()
  now_srs._time_fn = lambda: now
  i = 0
  while True:
    past_srs._time_fn = lambda: now - i * srslib.SRS._SECONDS_IN_DAY
    if i > 0 and past_srs.generate_ts() == now_srs.generate_ts():
      break
    srs0_addr = past_srs.forward('alice@example.com', '1st.com')
    if i < now_srs._validity_days:
      now_srs.reverse(srs0_addr)
    else:
      with pytest.raises(srslib.InvalidTimestampError):
        now_srs.reverse(srs0_addr)
    i += 1

def test_is_srs_address():
  assert not srslib.SRS.is_srs_address('foo@example.com')
  assert not srslib.SRS.is_srs_address('"foo@bar"@example.com')
  assert not srslib.SRS.is_srs_address('SRS0@example.com')
  assert not srslib.SRS.is_srs_address('SRS0+@example.com')
  assert not srslib.SRS.is_srs_address('SRS0=@example.com')
  assert srslib.SRS.is_srs_address('SRS0=1@example.com', strict=False)
  assert not srslib.SRS.is_srs_address('SRS0=1@example.com', strict=True)
  srs0_addr = _srs.forward('foo@example.com', '1st.com')
  assert srslib.SRS.is_srs_address(srs0_addr, strict=True)
  assert srslib.SRS.is_srs_address(srs0_addr, strict=False)
  srs1_addr = _srs.forward(srs0_addr, '2nd.com')
  assert srslib.SRS.is_srs_address(srs1_addr, strict=True)
  assert srslib.SRS.is_srs_address(srs1_addr, strict=False)


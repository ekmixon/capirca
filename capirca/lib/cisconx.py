# Copyright 2021 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""CiscoNX generator."""

from capirca.lib import cisco


class Error(Exception):
  """Base error class."""


class UnsupportedNXosAccessListError(Error):
  """When a filter type is not supported in an NXOS policy target."""


class CiscoNX(cisco.Cisco):
  """An CiscoNX policy object.

  CiscoNX devices differ slightly from Cisco, omitting the extended argument to
  ACLs for example.
  """

  _PLATFORM = 'cisconx'
  SUFFIX = '.nxacl'
  # Protocols should be emitted as they were in the policy (names).
  _PROTO_INT = False

  # CiscoNX omits the "extended" access-list argument.
  def _AppendTargetByFilterType(self, filter_name, filter_type):
    """Takes in the filter name and type and appends headers.

    Args:
      filter_name: Name of the current filter
      filter_type: Type of current filter

    Returns:
      list of strings

    Raises:
      UnsupportedNXosAccessListError: When unknown filter type is used.
    """
    target = []
    if filter_type in ['extended', 'object-group']:
      target.extend((f'no ip access-list {filter_name}',
                     f'ip access-list {filter_name}'))
    elif filter_type == 'inet6':
      target.extend((
          f'no ipv6 access-list {filter_name}',
          f'ipv6 access-list {filter_name}',
      ))
    else:
      raise UnsupportedNXosAccessListError(
          f'access list type {filter_type} not supported by {self._PLATFORM}')
    return target

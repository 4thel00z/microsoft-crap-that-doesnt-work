# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from .recovery_point import RecoveryPoint


class GenericRecoveryPoint(RecoveryPoint):
    """Generic backup copy.

    :param object_type: Polymorphic Discriminator
    :type object_type: str
    :param friendly_name: Friendly name of the backup copy.
    :type friendly_name: str
    :param recovery_point_type: Type of the backup copy.
    :type recovery_point_type: str
    :param recovery_point_time: Time at which this backup copy was created.
    :type recovery_point_time: datetime
    :param recovery_point_additional_info: Additional information associated
     with this backup copy.
    :type recovery_point_additional_info: str
    """

    _validation = {
        'object_type': {'required': True},
    }

    _attribute_map = {
        'object_type': {'key': 'objectType', 'type': 'str'},
        'friendly_name': {'key': 'friendlyName', 'type': 'str'},
        'recovery_point_type': {'key': 'recoveryPointType', 'type': 'str'},
        'recovery_point_time': {'key': 'recoveryPointTime', 'type': 'iso-8601'},
        'recovery_point_additional_info': {'key': 'recoveryPointAdditionalInfo', 'type': 'str'},
    }

    def __init__(self, friendly_name=None, recovery_point_type=None, recovery_point_time=None, recovery_point_additional_info=None):
        super(GenericRecoveryPoint, self).__init__()
        self.friendly_name = friendly_name
        self.recovery_point_type = recovery_point_type
        self.recovery_point_time = recovery_point_time
        self.recovery_point_additional_info = recovery_point_additional_info
        self.object_type = 'GenericRecoveryPoint'

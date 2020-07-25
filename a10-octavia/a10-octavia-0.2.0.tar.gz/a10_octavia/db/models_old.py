#    Copyright 2019, A10 Networks
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import sqlalchemy as sa

from a10_octavia.db import model_base


class VThunder(model_base.A10BaseMixin, model_base.A10Base):
    __tablename__ = 'vthunders'

    id = sa.Column(sa.Integer(), primary_key=True)
    amphora_id = sa.Column(sa.String(36), nullable=True)
    device_name = sa.Column(sa.String(1024), nullable=False)
    ip_address = sa.Column('ip_address', sa.String(64), nullable=False)
    username = sa.Column(sa.String(1024), nullable=False)
    password = sa.Column(sa.String(50), nullable=False)
    axapi_version = sa.Column(sa.Integer, default=30, nullable=False)
    undercloud = sa.Column(sa.Boolean(), default=False, nullable=False)
    loadbalancer_id = sa.Column(sa.String(36))

    @classmethod
    def find_by_loadbalancer_id(cls, loadbalancer_id, db_session=None):
        return cls.find_by_attribute('loadbalancer_id', loadbalancer_id, db_session)

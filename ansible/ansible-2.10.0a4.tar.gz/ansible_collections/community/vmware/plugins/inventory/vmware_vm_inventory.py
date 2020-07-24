#
# Copyright: (c) 2018, Ansible Project
# Copyright: (c) 2018, Abhijeet Kasurde <akasurde@redhat.com>
# Copyright: (c) 2020, dacrystal
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
    name: vmware_vm_inventory
    plugin_type: inventory
    short_description: VMware Guest inventory source
    author:
      - Abhijeet Kasurde (@Akasurde)
    description:
        - Get virtual machines as inventory hosts from VMware environment.
        - Uses any file which ends with vmware.yml, vmware.yaml, vmware_vm_inventory.yml, or vmware_vm_inventory.yaml as a YAML configuration file.
    extends_documentation_fragment:
      - inventory_cache
      - constructed
    requirements:
      - "Python >= 2.7"
      - "PyVmomi"
      - "requests >= 2.3"
      - "vSphere Automation SDK - For tag feature"
      - "vCloud Suite SDK - For tag feature"
    options:
        hostname:
            description: Name of vCenter or ESXi server.
            required: True
            env:
              - name: VMWARE_HOST
              - name: VMWARE_SERVER
        username:
            description: Name of vSphere user.
            required: True
            env:
              - name: VMWARE_USER
              - name: VMWARE_USERNAME
        password:
            description: Password of vSphere user.
            required: True
            env:
              - name: VMWARE_PASSWORD
        port:
            description: Port number used to connect to vCenter or ESXi Server.
            default: 443
            env:
              - name: VMWARE_PORT
        validate_certs:
            description:
            - Allows connection when SSL certificates are not valid.
            - Set to C(false) when certificates are not trusted.
            default: True
            type: bool
            env:
              - name: VMWARE_VALIDATE_CERTS
        with_tags:
            description:
            - Include tags and associated virtual machines.
            - Requires 'vSphere Automation SDK' library to be installed on the given controller machine.
            - Please refer following URLs for installation steps
            - U(https://code.vmware.com/web/sdk/7.0/vsphere-automation-python)
            default: False
            type: bool
        hostnames:
            description:
            - A list of templates in order of precedence to compose inventory_hostname.
            - Ignores template if resulted in an empty string or None value.
            - You can use property specified in I(properties) as variables in the template.
            type: list
            default: ['config.name + "_" + config.uuid']
        properties:
            description:
            - Specify the list of VMware schema properties associated with the VM.
            - These properties will be populated in hostvars of the given VM.
            - Each value in the list can be a path to a specific property in VM object or a path to a collection of VM objects.
            - C(config.name), C(config.uuid) are required properties if C(hostnames) is set to default.
            - C(config.guestId), C(summary.runtime.powerState) are required if C(keyed_groups) is set to default.
            - Please make sure that all the properties that are used in other parameters are included in this options.
            - In addition to VM properties, the following are special values
            - Use C(customValue) to populate virtual machine's custom attributes. C(customValue) is only supported by vCenter and not by ESXi.
            - Use C(all) to populate all the properties of the virtual machine.
              The value C(all) is time consuming operation, do not use unless required absolutely.
            - Please refer more VMware guest attributes which can be used as properties
              U(https://github.com/ansible/ansible/blob/devel/docs/docsite/rst/scenario_guides/vmware_scenarios/vmware_inventory_vm_attributes.rst)
            type: list
            default: [ 'name', 'config.cpuHotAddEnabled', 'config.cpuHotRemoveEnabled',
                       'config.instanceUuid', 'config.hardware.numCPU', 'config.template',
                       'config.name', 'config.uuid', 'guest.hostName', 'guest.ipAddress',
                       'guest.guestId', 'guest.guestState', 'runtime.maxMemoryUsage',
                       'customValue', 'summary.runtime.powerState', 'config.guestId',
                       ]
        with_nested_properties:
            description:
            - This option transform flatten properties name to nested dictionary.
            type: bool
            default: False
        keyed_groups:
            description:
            - Add hosts to group based on the values of a variable.
            type: list
            default: [
                {key: 'config.guestId', separator: ''},
                {key: 'summary.runtime.powerState', separator: ''},
            ]
        filters:
            description:
            - This option allows client-side filtering hosts with jinja templating.
            - When server-side filtering is introduced, it should be preferred over this.
            type: list
            elements: str
            default: []
'''

EXAMPLES = r'''
# Sample configuration file for VMware Guest dynamic inventory
    plugin: community.vmware.vmware_vm_inventory
    strict: False
    hostname: 10.65.223.31
    username: administrator@vsphere.local
    password: Esxi@123$%
    validate_certs: False
    with_tags: True

# Gather minimum set of properties for VMware guest
    plugin: community.vmware.vmware_vm_inventory
    strict: False
    hostname: 10.65.223.31
    username: administrator@vsphere.local
    password: Esxi@123$%
    validate_certs: False
    properties:
    - 'name'
    - 'guest.ipAddress'

# Create Groups based upon VMware Tools status
    plugin: community.vmware.vmware_vm_inventory
    strict: False
    hostname: 10.65.223.31
    username: administrator@vsphere.local
    password: Esxi@123$%
    validate_certs: False
    with_tags: False
    properties:
    - 'name'
    - 'config.name'
    - 'guest.toolsStatus'
    - 'guest.toolsRunningStatus'
    hostnames:
    - config.name
    keyed_groups:
    - key: guest.toolsStatus
      separator: ''
    - key: guest.toolsRunningStatus
      separator: ''

# Filter VMs based upon condition
    plugin: community.vmware.vmware_vm_inventory
    strict: False
    hostname: 10.65.223.31
    username: administrator@vsphere.local
    password: Esxi@123$%
    validate_certs: False
    properties:
    - runtime.powerState
    - config.name
    filters:
    - runtime.powerState == "poweredOn"
    hostnames:
    - config.name

# Using compose and groups
    plugin: community.vmware.vmware_vm_inventory
    strict: False
    hostname: 10.65.223.31
    username: administrator@vsphere.local
    password: Esxi@123$%
    validate_certs: False
    with_tags: False
    properties:
    - 'name'
    - 'config.name'
    - 'guest.ipAddress'
    compose:
      # This will populate the IP address of virtual machine if available
      # and will be used while communicating to the given virtual machine
      ansible_host: 'guest.ipAddress'
      composed_var: 'config.name'
    groups:
      VMs: True
    hostnames:
    - config.name
'''

import ssl
import atexit
import base64
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils._text import to_text, to_native
from ansible.module_utils.common.dict_transformations import dict_merge
from ansible.module_utils.common.dict_transformations import _snake_to_camel
from ansible.utils.display import Display

display = Display()

try:
    # requests is required for exception handling of the ConnectionError
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from pyVim import connect
    from pyVmomi import vim, vmodl
    from pyVmomi.VmomiSupport import DataObject
    from pyVmomi import Iso8601
    HAS_PYVMOMI = True
except ImportError:
    HAS_PYVMOMI = False

try:
    from com.vmware.vapi.std_client import DynamicID
    from vmware.vapi.vsphere.client import create_vsphere_client
    HAS_VSPHERE = True
except ImportError:
    HAS_VSPHERE = False


from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable
from ansible.parsing.yaml.objects import AnsibleVaultEncryptedUnicode


class BaseVMwareInventory:
    def __init__(self, hostname, username, password, port, validate_certs, with_tags):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.with_tags = with_tags
        self.validate_certs = validate_certs
        self.content = None
        self.rest_content = None

    def do_login(self):
        """
        Check requirements and do login
        """
        self.check_requirements()
        self.si, self.content = self._login()
        if self.with_tags:
            self.rest_content = self._login_vapi()

    def _login_vapi(self):
        """
        Login to vCenter API using REST call
        Returns: connection object

        """
        session = requests.Session()
        session.verify = self.validate_certs
        if not self.validate_certs:
            # Disable warning shown at stdout
            requests.packages.urllib3.disable_warnings()

        server = self.hostname
        if self.port:
            server += ":" + str(self.port)

        client, err = None, None
        try:
            client = create_vsphere_client(server=server,
                                           username=self.username,
                                           password=self.password,
                                           session=session)
        except Exception as err:
            err = err

        if client is None:
            msg = "Failed to login to %s using %s" % (server, self.username)
            if err:
                msg += " due to : %s" % to_native(err)
            raise AnsibleError(msg)
        return client

    def _login(self):
        """
        Login to vCenter or ESXi server
        Returns: connection object

        """
        if self.validate_certs and not hasattr(ssl, 'SSLContext'):
            raise AnsibleError('pyVim does not support changing verification mode with python < 2.7.9. Either update '
                               'python or set validate_certs to false in configuration YAML file.')

        ssl_context = None
        if not self.validate_certs and hasattr(ssl, 'SSLContext'):
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            ssl_context.verify_mode = ssl.CERT_NONE

        service_instance = None
        try:
            service_instance = connect.SmartConnect(host=self.hostname, user=self.username,
                                                    pwd=self.password, sslContext=ssl_context,
                                                    port=self.port)
        except vim.fault.InvalidLogin as e:
            raise AnsibleParserError("Unable to log on to vCenter or ESXi API at %s:%s as %s: %s" % (self.hostname, self.port, self.username, e.msg))
        except vim.fault.NoPermission as e:
            raise AnsibleParserError("User %s does not have required permission"
                                     " to log on to vCenter or ESXi API at %s:%s : %s" % (self.username, self.hostname, self.port, e.msg))
        except (requests.ConnectionError, ssl.SSLError) as e:
            raise AnsibleParserError("Unable to connect to vCenter or ESXi API at %s on TCP/%s: %s" % (self.hostname, self.port, e))
        except vmodl.fault.InvalidRequest as e:
            # Request is malformed
            raise AnsibleParserError("Failed to get a response from server %s:%s as "
                                     "request is malformed: %s" % (self.hostname, self.port, e.msg))
        except Exception as e:
            raise AnsibleParserError("Unknown error while connecting to vCenter or ESXi API at %s:%s : %s" % (self.hostname, self.port, e))

        if service_instance is None:
            raise AnsibleParserError("Unknown error while connecting to vCenter or ESXi API at %s:%s" % (self.hostname, self.port))

        atexit.register(connect.Disconnect, service_instance)
        return service_instance, service_instance.RetrieveContent()

    def check_requirements(self):
        """ Check all requirements for this inventory are satisfied"""
        if not HAS_REQUESTS:
            raise AnsibleParserError('Please install "requests" Python module as this is required'
                                     ' for VMware Guest dynamic inventory plugin.')
        elif not HAS_PYVMOMI:
            raise AnsibleParserError('Please install "PyVmomi" Python module as this is required'
                                     ' for VMware Guest dynamic inventory plugin.')
        if HAS_REQUESTS:
            # Pyvmomi 5.5 and onwards requires requests 2.3
            # https://github.com/vmware/pyvmomi/blob/master/requirements.txt
            required_version = (2, 3)
            requests_version = requests.__version__.split(".")[:2]
            try:
                requests_major_minor = tuple(map(int, requests_version))
            except ValueError:
                raise AnsibleParserError("Failed to parse 'requests' library version.")

            if requests_major_minor < required_version:
                raise AnsibleParserError("'requests' library version should"
                                         " be >= %s, found: %s." % (".".join([str(w) for w in required_version]),
                                                                    requests.__version__))

        if not HAS_VSPHERE and self.with_tags:
            raise AnsibleError("Unable to find 'vSphere Automation SDK' Python library which is required."
                               " Please refer this URL for installation steps"
                               " - https://code.vmware.com/web/sdk/7.0/vsphere-automation-python")

        if not all([self.hostname, self.username, self.password]):
            raise AnsibleError("Missing one of the following : hostname, username, password. Please read "
                               "the documentation for more information.")

    def get_managed_objects_properties(self, vim_type, properties=None, resources=None, strict=False):
        """
        Look up a Managed Object Reference in vCenter / ESXi Environment
        :param vim_type: Type of vim object e.g, for datacenter - vim.Datacenter
        :param properties: List of properties related to vim object e.g. Name
        :param resources: List of resources to limit search scope
        :param strict: Dictates if plugin raises error or just warns
        :return: local content object
        """
        TraversalSpec = vmodl.query.PropertyCollector.TraversalSpec
        FilterSpec = vmodl.query.PropertyCollector.FilterSpec
        ObjectSpec = vmodl.query.PropertyCollector.ObjectSpec
        PropertySpec = vmodl.query.PropertyCollector.PropertySpec

        resource_filters = resources or []
        type_to_name_map = {}

        def _handle_error(message):
            if strict:
                raise AnsibleError(message)
            else:
                display.warning(message)

        def get_contents(container, vim_types):
            return self.content.propertyCollector.RetrieveContents([
                FilterSpec(
                    objectSet=[
                        ObjectSpec(
                            obj=self.content.viewManager.CreateContainerView(
                                container, vim_types, True),
                            skip=False,
                            selectSet=[TraversalSpec(
                                type=vim.view.ContainerView, path='view', skip=False)]
                        )],
                    propSet=[PropertySpec(type=t, all=False, pathSet=['name']) for t in vim_types],
                )
            ])

        def filter_containers(containers, typ, filter_list):
            if len(filter_list) > 0:
                objs = []
                results = []
                found_filters = {}

                for container in containers:
                    results.extend(get_contents(container, [typ]))

                for res in results:
                    if res.propSet[0].val in filter_list:
                        objs.append(res.obj)
                        found_filters[res.propSet[0].val] = True

                for fil in filter_list:
                    if fil not in found_filters:
                        _handle_error("Unable to find %s %s" % (type_to_name_map[typ], fil))

                return objs
            return containers

        def build_containers(containers, vim_type, names, filters):
            filters = filters or []
            if vim_type:
                containers = filter_containers(containers, vim_type, names)

            new_containers = []
            for fil in filters:
                new_filters = None
                for k, v in fil.items():
                    if k == "resources":
                        new_filters = v
                    else:
                        vim_type = getattr(vim, _snake_to_camel(k, True))
                        names = v
                        type_to_name_map[vim_type] = k.replace("_", " ")

                new_containers.extend(build_containers(containers, vim_type, names, new_filters))

            if len(filters) > 0:
                return new_containers
            return containers

        containers = build_containers([self.content.rootFolder], None, None, resource_filters)
        if len(containers) == 0:
            return []

        objs_list = [ObjectSpec(
            obj=self.content.viewManager.CreateContainerView(r, [vim_type], True),
            selectSet=[TraversalSpec(path='view', skip=False, type=vim.view.ContainerView)]) for r in containers]

        is_all = False if properties else True

        # Create Property Spec
        property_spec = PropertySpec(
            type=vim_type,  # Type of object to retrieved
            all=is_all,
            pathSet=properties
        )

        # Create Filter Spec
        filter_spec = FilterSpec(
            objectSet=objs_list,
            propSet=[property_spec],
            reportMissingObjectsInResults=False
        )

        try:
            return self.content.propertyCollector.RetrieveContents([filter_spec])
        except vmodl.query.InvalidProperty as err:
            _handle_error("Invalid property name: %s" % err.name)
        except Exception as err:  # pylint: disable=broad-except
            _handle_error("Couldn't retrieve contents from host: %s" % to_native(err))
        return []


def to_nested_dict(vm_properties):
    """
    Parse properties from dot notation to dict

    """

    host_properties = {}

    for vm_prop_name, vm_prop_val in vm_properties.items():
        prop_parents = reversed(vm_prop_name.split("."))
        prop_dict = parse_vim_property(vm_prop_val)

        for k in prop_parents:
            prop_dict = {k: prop_dict}
        host_properties = dict_merge(host_properties, prop_dict)

    return host_properties


def to_flatten_dict(d, parent_key='', sep='.'):
    """
    Parse properties dict to dot notation

    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if v and isinstance(v, dict):
            items.extend(to_flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def parse_vim_property(vim_prop):
    """
    Helper method to parse VIM properties of virtual machine
    """
    prop_type = type(vim_prop).__name__
    if prop_type.startswith("vim") or prop_type.startswith("vmodl"):
        if isinstance(vim_prop, DataObject):
            r = {}
            for prop in vim_prop._GetPropertyList():  # pylint: disable=protected-access
                if prop.name not in ['dynamicProperty', 'dynamicType', 'managedObjectType']:
                    sub_prop = getattr(vim_prop, prop.name)
                    r[prop.name] = parse_vim_property(sub_prop)
            return r

        elif isinstance(vim_prop, list):
            r = []
            for prop in vim_prop:
                r.append(parse_vim_property(prop))
            return r
        return vim_prop.__str__()

    elif prop_type == "datetime":
        return Iso8601.ISO8601Format(vim_prop)

    elif prop_type == "long":
        return int(vim_prop)
    elif prop_type == "long[]":
        return [int(x) for x in vim_prop]

    elif isinstance(vim_prop, list):
        return [parse_vim_property(x) for x in vim_prop]

    elif prop_type in ['bool', 'int', 'NoneType']:
        return vim_prop

    elif prop_type in ['binary']:
        return to_text(base64.b64encode(vim_prop))

    return to_text(vim_prop)


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

    NAME = 'community.vmware.vmware_vm_inventory'

    def verify_file(self, path):
        """
        Verify plugin configuration file and mark this plugin active
        Args:
            path: Path of configuration YAML file
        Returns: True if everything is correct, else False
        """
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('vmware.yaml', 'vmware.yml', 'vmware_vm_inventory.yaml', 'vmware_vm_inventory.yml')):
                valid = True

        return valid

    def parse(self, inventory, loader, path, cache=True):
        """
        Parses the inventory file
        """
        super(InventoryModule, self).parse(inventory, loader, path, cache=cache)

        cache_key = self.get_cache_key(path)

        config_data = self._read_config_data(path)

        # set _options from config data
        self._consume_options(config_data)

        password = self.get_option('password')

        if isinstance(password, AnsibleVaultEncryptedUnicode):
            password = password.data

        self.pyv = BaseVMwareInventory(
            hostname=self.get_option('hostname'),
            username=self.get_option('username'),
            password=password,
            port=self.get_option('port'),
            with_tags=self.get_option('with_tags'),
            validate_certs=self.get_option('validate_certs')
        )

        self.pyv.do_login()

        if cache:
            cache = self.get_option('cache')

        update_cache = False
        if cache:
            try:
                cacheable_results = self._cache[cache_key]
            except KeyError:
                update_cache = True

        if cache and not update_cache:
            self._populate_from_cache(cacheable_results)
        else:
            cacheable_results = self._populate_from_source()

        if update_cache or (not cache and self.get_option('cache')):
            self._cache[cache_key] = cacheable_results

    def _populate_from_cache(self, cache_data):
        """
        Populate cache using source data

        """
        for host, host_properties in cache_data.items():
            self._populate_host_properties(host_properties, host)

    def _populate_from_source(self):
        """
        Populate inventory data from direct source

        """
        hostvars = {}
        strict = self.get_option('strict')

        vm_properties = self.get_option('properties')
        if not isinstance(vm_properties, list):
            vm_properties = [vm_properties]

        if len(vm_properties) == 0:
            vm_properties = ['name']

        if 'all' in vm_properties:
            query_props = None
            vm_properties.remove('all')
        else:
            query_props = [x for x in vm_properties if x != "customValue"]

        objects = self.pyv.get_managed_objects_properties(
            vim_type=vim.VirtualMachine,
            properties=query_props,
            # resources=self.get_option('resources'),
            strict=strict,
        )

        tags_info = dict()
        if self.pyv.with_tags:
            tag_svc = self.pyv.rest_content.tagging.Tag
            tag_association = self.pyv.rest_content.tagging.TagAssociation

            tags = tag_svc.list()
            for tag in tags:
                tag_obj = tag_svc.get(tag)
                tags_info[tag_obj.id] = tag_obj.name

        hostnames = self.get_option('hostnames')

        for vm_obj in objects:
            if not vm_obj.obj.config:
                # Sometime orphaned VMs return no configurations
                continue

            properties = dict()
            for vm_obj_property in vm_obj.propSet:
                properties[vm_obj_property.name] = vm_obj_property.val

            # Custom values
            if 'customValue' in vm_properties:
                field_mgr = []
                if self.pyv.content.customFieldsManager:  # not an ESXi
                    field_mgr = self.pyv.content.customFieldsManager.field
                for cust_value in vm_obj.obj.customValue:
                    properties[[y.name for y in field_mgr if y.key == cust_value.key][0]] = cust_value.value

            # Tags
            if tags_info:
                # Add virtual machine to appropriate tag group
                vm_mo_id = vm_obj.obj._GetMoId()  # pylint: disable=protected-access
                vm_dynamic_id = DynamicID(type='VirtualMachine', id=vm_mo_id)
                attached_tags = [tags_info[tag_id] for tag_id in tag_association.list_attached_tags(vm_dynamic_id)]
                properties['tags'] = attached_tags

            host_properties = to_nested_dict(properties)

            host = self._get_hostname(host_properties, hostnames, strict=strict)

            host_filters = self.get_option('filters')

            if host not in hostvars and self._can_add_host(host_filters, host_properties, host, strict=strict):
                hostvars[host] = host_properties
                self._populate_host_properties(host_properties, host)

        return hostvars

    def _get_hostname(self, properties, hostnames, strict=False):
        hostname = None
        errors = []

        for preference in hostnames:
            try:
                hostname = self._compose(preference, properties)
            except Exception as e:  # pylint: disable=broad-except
                if strict:
                    raise AnsibleError("Could not compose %s as hostnames - %s" % (preference, to_native(e)))
                else:
                    errors.append(
                        (preference, str(e))
                    )
            if hostname:
                return to_text(hostname)

        raise AnsibleError(
            'Could not template any hostname for host, errors for each preference: %s' % (
                ', '.join(['%s: %s' % (pref, err) for pref, err in errors])
            )
        )

    def _can_add_host(self, host_filters, host_properties, host, strict=False):
        can_add_host = True
        for host_filter in host_filters:
            try:
                can_add_host = self._compose(host_filter, host_properties)
            except Exception as e:  # pylint: disable=broad-except
                if strict:
                    raise AnsibleError("Could not evaluate %s as host filters - %s" % (host_filter, to_native(e)))

            if not can_add_host:
                return False
        return True

    def _populate_host_properties(self, host_properties, host):
        # Load VM properties in host_vars
        self.inventory.add_host(host)

        # Use constructed if applicable
        strict = self.get_option('strict')

        # Composed variables
        compose = self.get_option('compose')
        if not compose:
            compose['ansible_host'] = 'guest.ipAddress'

        if not compose.get('ansible_host', None):
            raise AnsibleError('"ansible_host" not found in "compose". '
                               'Without this inventory will be useless.')
        self._set_composite_vars(compose, host_properties, host, strict=strict)
        # Complex groups based on jinja2 conditionals, hosts that meet the conditional are added to group
        self._add_host_to_composed_groups(self.get_option('groups'), host_properties, host, strict=strict)
        # Create groups based on variable values and add the corresponding hosts to it
        self._add_host_to_keyed_groups(self.get_option('keyed_groups'), host_properties, host, strict=strict)

        with_nested_properties = self.get_option('with_nested_properties')
        if with_nested_properties:
            for k, v in host_properties.items():
                self.inventory.set_variable(host, k, v)

        # For backward compatability
        host_properties = to_flatten_dict(host_properties)
        for k, v in host_properties.items():
            self.inventory.set_variable(host, k, v)

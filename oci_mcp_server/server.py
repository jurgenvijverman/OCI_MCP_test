# FastAPI REST API server for OCI MCP
from fastapi import FastAPI
import oci
import os

app = FastAPI()

# Reads OCI config from ~/.oci/config
OCI_CONFIG_PATH = os.path.expanduser("~/.oci/config")
OCI_PROFILE = os.getenv("OCI_PROFILE", "DEFAULT")
# COMPARTMENT_OCID = os.getenv("OCI_COMPARTMENT_OCID")

COMPARTMENT_OCID = "ocid1.compartment.oc1..aaaaaaaauhgedaw4ieu4fdnuud5tpnrbv32qsp7ipvboqxkhklkk3xmhg23a"

def get_oci_clients():
    config = oci.config.from_file(OCI_CONFIG_PATH, OCI_PROFILE)
    vcn_client = oci.core.VirtualNetworkClient(config)
    identity_client = oci.identity.IdentityClient(config)
    return vcn_client, identity_client, config

@app.get("/network/config")
def get_network_config():
    if not COMPARTMENT_OCID:
        return {"error": "OCI_COMPARTMENT_OCID environment variable not set"}
    vcn_client, identity_client, config = get_oci_clients()
    # List VCNs
    vcns = vcn_client.list_vcns(COMPARTMENT_OCID).data
    # List Subnets
    subnets = vcn_client.list_subnets(COMPARTMENT_OCID).data
    # List Security Lists
    sec_lists = vcn_client.list_security_lists(COMPARTMENT_OCID).data
    # List Service Gateways
    svc_gws = vcn_client.list_service_gateways(COMPARTMENT_OCID).data
    # List Local Peering Gateways
    lpgs = vcn_client.list_local_peering_gateways(COMPARTMENT_OCID).data
    # List Dynamic Routing Gateways
    drgs = vcn_client.list_drgs(COMPARTMENT_OCID).data

    # List Internet Gateways
    igws = vcn_client.list_internet_gateways(COMPARTMENT_OCID).data
    # List NAT Gateways
    nat_gws = vcn_client.list_nat_gateways(COMPARTMENT_OCID).data
    # List Route Tables
    route_tables = vcn_client.list_route_tables(COMPARTMENT_OCID).data

    return {
        "vcns": [dict(id=v.id, display_name=v.display_name, cidr_block=v.cidr_block) for v in vcns],
        "subnets": [dict(id=s.id, display_name=s.display_name, cidr_block=s.cidr_block, vcn_id=s.vcn_id, route_table_id=s.route_table_id, dhcp_options_id=s.dhcp_options_id) for s in subnets],
        "security_lists": [dict(id=sl.id, display_name=sl.display_name, vcn_id=sl.vcn_id) for sl in sec_lists],
        "internet_gateways": [dict(id=g.id, display_name=g.display_name, vcn_id=g.vcn_id, is_enabled=g.is_enabled) for g in igws],
        "nat_gateways": [dict(id=n.id, display_name=n.display_name, vcn_id=n.vcn_id, nat_ip=n.nat_ip) for n in nat_gws],
        "route_tables": [dict(id=rt.id, display_name=rt.display_name, vcn_id=rt.vcn_id, route_rules=[dict(network_entity_id=rr.network_entity_id, destination=rr.destination, destination_type=rr.destination_type) for rr in rt.route_rules]) for rt in route_tables],
        "service_gateways": [dict(id=sg.id, display_name=sg.display_name, vcn_id=sg.vcn_id, services=[dict(service_id=s.service_id, service_name=s.service_name) for s in sg.services]) for sg in svc_gws],
        "local_peering_gateways": [dict(id=lpg.id, display_name=lpg.display_name, vcn_id=lpg.vcn_id, peering_status=lpg.peering_status) for lpg in lpgs],
        "dynamic_routing_gateways": [dict(id=drg.id, display_name=drg.display_name) for drg in drgs]
    }

@app.get("/compartments")
def list_compartments():
    _, identity_client, config = get_oci_clients()
    tenancy_id = config["tenancy"]
    compartments = identity_client.list_compartments(
        tenancy_id,
        compartment_id_in_subtree=True,
        access_level="ACCESSIBLE"
    ).data
    return [
        dict(id=c.id, name=c.name, description=c.description, lifecycle_state=c.lifecycle_state)
        for c in compartments
    ]

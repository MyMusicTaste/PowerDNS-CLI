# inpydns

inpydns allows you to manage a [PowerDNS](https://www.powerdns.com/) server trought the [REST API](https://doc.powerdns.com/md/httpapi/README/).

This script is inspired by the [job](https://github.com/mrlesmithjr/python-powerdns-management) of [Larry Smith Jr.](http://everythingshouldbevirtual.com/),
and [this](https://github.com/pbertera/PowerDNS-CLI) of [Pietro Bertera](https://github.com/pbertera/PowerDNS-CLI).

Main changes to the original script:
    
* removed all the CSV stuff
* moved output to the logging module
* updated to the API V1 (https://doc.powerdns.com/md/httpapi/api_spec/)
* --debug switch
* Python 3
* installable using pip

## Usage:

### Installation

```
cd /path/to/inpydns
pip install -e .
```

### Config:

```
export PDNS_API_KEY=<the API key get from the PDNS's /etc/powerdns/pdns.conf>
export PDNS_WEB_HOST=<PDNS server's API host address>
export PDNS_WEB_PORT=<PDNS server's API port>
```

### Help:

```
# inpydns -h
usage: inpydns [-h] [--apikey APIKEY] [--apihost APIHOST] [--apiport APIPORT]
               [--content CONTENT] [--disabled]
               [--masters MASTERS] [--name NAME] [--nameserver NAMESERVER]
               [--priority PRIORITY]
               [--recordType {A,AAAA,CNAME,MX,NS,PTR,SOA,SRV,TXT,NAPTR}]
               [--setPTR] [--ttl TTL] [--zone ZONE]
               [--zoneType {MASTER,NATIVE,SLAVE}] [--debug]
               {add_records,add_zones,delete_records,delete_zones,query_config,query_stats,query_zones}

PDNS Controls...

positional arguments:
  {add_record,add_zone,delete_record,delete_zone,query_config,query_stats,query_zone}
                        Define action to take

optional arguments:
  -h, --help            show this help message and exit
  --apikey APIKEY       PDNS API Key, default getting from os env's PDNS_API_KEY
  --apihost APIHOST     PDNS API Host
  --apiport APIPORT     PDNS API Port
  --content CONTENT     DNS Record content
  --disabled            Define if Record is disabled
  --master MASTER       DNS zone master, can be specified multiple times
  --name NAME           DNS record name
  --nameserver NAMESERVER
                        DNS nameserver for zone, can be specified multiple times
  --priority PRIORITY   Define priority
  --recordType {A,AAAA,CNAME,MX,NS,PTR,SOA,SRV,TXT,NAPTR}
                        DNS record type
  --setPTR              Define if PTR record is created
  --ttl TTL             Define TTL
  --zone ZONE           DNS zone
  --zoneType {MASTER,NATIVE,SLAVE}
                        DNS Zone Type
  --debug               Enable debug
```

## Adding a DNS zone

The following commands adds the new MASTER zone `example.com`the PowerDNS API Key is `MyAPIKey` the nameserver is `ns.example.com`

```
inpydns  --apikey MyAPIKey --apihost 127.0.0.1 --apiport 80 --zone example.com. --zoneType MASTER --nameserver ns.example.com. --debug add_zone
2016-09-05 23:55:15,591 pdns         DEBUG    sending GET request to http://127.0.0.1:80/api/v1/servers/localhost/zones/example.com.
2016-09-05 23:55:15,615 pdns         DEBUG    returned 422 {"error": "Could not find domain 'example.com.'"}
2016-09-05 23:55:15,616 pdns         DEBUG    sending POST request to http://127.0.0.1:80/api/v1/servers/localhost/zones
2016-09-05 23:55:15,616 pdns         DEBUG    POST data: {"name": "example.com.", "masters": [], "kind": "MASTER", "soa_edit_api": "INCEPTION-INCREMENT", "nameservers": ["ns.example.com."]}
2016-09-05 23:55:15,696 pdns         DEBUG    returned 201 {"account": "", "dnssec": false, "id": "example.com.", "kind": "Master", "last_check": 0, "masters": [], "name": "example.com.", "notified_serial": 0, "rrsets": [{"comments": [], "name": "example.com.", "records": [{"content": "a.misconfigured.powerdns.server. hostmaster.example.com. 2016090501 10800 3600 604800 3600", "disabled": false}], "ttl": 3600, "type": "SOA"}, {"comments": [], "name": "example.com.", "records": [{"content": "ns.example.com.", "disabled": false}], "ttl": 3600, "type": "NS"}], "serial": 2016090501, "soa_edit": "", "soa_edit_api": "INCEPTION-INCREMENT", "url": "api/v1/servers/localhost/zones/example.com."}
2016-09-05 23:55:15,696 pdns         INFO     DNS Zone 'example.com.' Successfully Added...
```

### Adding a zone with multiple NS

```
inpydns  --apikey MyAPIKey --apihost 127.0.0.1 --apiport 80 --zone example.com. --zoneType MASTER --nameserver ns1.example.com.,ns2.example.com. --debug add_zone
2016-09-06 00:00:55,286 pdns         DEBUG    sending GET request to http://127.0.0.1:80/api/v1/servers/localhost/zones/example.com.
2016-09-06 00:00:55,379 pdns         DEBUG    returned 422 {"error": "Could not find domain 'example.com.'"}
2016-09-06 00:00:55,379 pdns         DEBUG    sending POST request to http://127.0.0.1:80/api/v1/servers/localhost/zones
2016-09-06 00:00:55,380 pdns         DEBUG    POST data: {"name": "example.com.", "kind": "MASTER", "nameservers": ["ns1.example.com.", "ns2.example.com."], "soa_edit_api": "INCEPTION-INCREMENT", "masters": []}
2016-09-06 00:00:55,560 pdns         DEBUG    returned 201 {"account": "", "dnssec": false, "id": "example.com.", "kind": "Master", "last_check": 0, "masters": [], "name": "example.com.", "notified_serial": 0, "rrsets": [{"comments": [], "name": "example.com.", "records": [{"content": "a.misconfigured.powerdns.server. hostmaster.example.com. 2016090601 10800 3600 604800 3600", "disabled": false}], "ttl": 3600, "type": "SOA"}, {"comments": [], "name": "example.com.", "records": [{"content": "ns1.example.com.", "disabled": false}, {"content": "ns2.example.com.", "disabled": false}], "ttl": 3600, "type": "NS"}], "serial": 2016090601, "soa_edit": "", "soa_edit_api": "INCEPTION-INCREMENT", "url": "api/v1/servers/localhost/zones/example.com."}
2016-09-06 00:00:55,561 pdns         INFO     DNS Zone 'example.com.' Successfully Added...
```

## Managing zone records

### Adding an A record

The following command adds the A record for the zone NS: `ns1.example.com` with IP `172.16.18.15`:

```
inpydns  --apikey MyAPIKey --apihost 127.0.0.1 --apiport 80 --zone example.com. --recordType A --name ns1.example.com. --content 172.16.18.15 add_record
2016-09-05 23:58:05,652 pdns         INFO     DNS Record 'ns1.example.com.' Successfully Added/Updated
```

### Adding a CNAME record

`www.example.com`is a `CNAME` pointing to `host.example.com.`:

```
inpydns  --apikey MyAPIKey --apihost 127.0.0.1 --apiport 80 --zone example.com. --recordType CNAME --name www.example.com. --content host.example.com. add_record
2016-09-06 00:05:30,753 pdns         INFO     DNS Record 'www.example.com.' Successfully Added/Update
```

### Adding a NAPTR record

Adding a `NAPTR` record with value `10 10 "S" "SIP+D2U" "" _sip._udp.example.com.`: 

```
inpydns  --apikey MyAPIKey --apihost 127.0.0.1 --apiport 80 --zone example.com. --content "10 10 \"S\" \"SIP+D2U\" \"\" _sip._udp.example.com." --name "example.com." --recordType NAPTR  add_record 
2016-09-06 00:10:30,137 pdns         INFO     DNS Record 'example.com.' Successfully Added/Updated
```

### Adding multiple NAPTR record

Adding 3 `NAPTR`records:

* `10 10 "S" "SIPS+D2T" "" _sips._tcp.wonderland.com.`
* `20 10 "S" "SIP+D2T" "" _sip._tcp.wonderland.com.`
* `30 10 "S" "SIP+D2U" "" _sip._udp.wonderland.com.`

```
inpydns --zone wonderland.com. --content "10 10 \"S\" \"SIPS+D2T\" \"\" _sips._tcp.wonderland.com." --content "20 10 \"S\" \"SIP+D2T\" \"\" _sip._tcp.wonderland.com." --content "30 10 \"S\" \"SIP+D2U\" \"\" _sip._udp.wonderland.com." --name wonderland.com. --recordType=NAPTR add_record
2016-11-09 07:30:32,386 pdns         INFO     DNS Record 'wonderland.com.' Successfully Added/Updated
```

### Adding an SRV record

Adding an `SRV` record with value 20 50 5060 pbx2.example.com.` for the name `_sip._udp.example.com.` *Please note that if you don't add the trailing dot (.) the zone name will be concatenated to the --name parameter*

```
inpydns  --apikey MyAPIKey --apihost 127.0.0.1 --apiport 80 --zone example.com. --content "20 50 5060 pbx2.example.com." --name _sip._udp --recordType SRV  add_record
2016-09-06 00:15:24,356 pdns         INFO     DNS Record '_sip._udp.example.com.' Successfully Added/Updated
```

## Maintainer

Jin Nguyen <dangtrinhnt@mymusictaste.com>

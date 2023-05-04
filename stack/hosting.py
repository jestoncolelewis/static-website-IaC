from constructs import Construct
from aws_cdk import (
    aws_route53 as r53,
    aws_route53_targets as targets
)
from .static_website_stack import StaticWebsiteIaCStack, name

class Hosting(Construct):
    @property
    def zone(self):
        return self._zone

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Hosting
        zone = r53.HostedZone(
            self, 'HostedZone',
            zone_name=name
        )

        bucket = StaticWebsiteIaCStack(self, 'Buckets')

        main_record = r53.RecordSet(
            self, 'MainRecord',
            record_type=r53.RecordType.A,
            target=r53.RecordTarget.from_alias(targets.BucketWebsiteTarget(bucket._main_bucket)),
            zone=zone,
            record_name=name
        )

        www_record = r53.RecordSet(
            self, 'wwwRecord',
            record_type=r53.RecordType.A,
            target=r53.RecordTarget.from_alias(targets.BucketWebsiteTarget(bucket._www_bucket)),
            zone=zone,
            record_name='www.' + name
        )

        self._zone = zone
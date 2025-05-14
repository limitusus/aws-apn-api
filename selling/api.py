import time
from selling.opportunity import Opportunity


class SellingApi:
    def __init__(self, client):
        self._client = client

    CATALOG = "AWS"
    ALIVE_OPPORTUNITY_STATUSES = [
        "Prospect",
        "Qualified",
        "Technical Validation",
        "Business Validation",
        "Committed",
        # 'Launched',
        # 'Closed Lost',
    ]
    API_INTERVAL = 1
    MAX_RESULTS = 5

    def list_alive_opportunities(
        self,
    ):
        opps = []
        paginator = self._client.get_paginator("list_opportunities")
        response_iterator = paginator.paginate(
            Catalog=self.CATALOG,
            LifeCycleStage=self.ALIVE_OPPORTUNITY_STATUSES,
            PaginationConfig={
                "PageSize": self.MAX_RESULTS,
            },
        )
        for result in response_iterator:
            opps += result["OpportunitySummaries"]
        rv = []
        for opp in opps:
            op = Opportunity()
            op.Id = opp["Id"]
            op.Arn = opp["Arn"]
            op.Stage = opp["LifeCycle"]["Stage"]
            op.ClientName = opp["Customer"]["Account"]["CompanyName"]
            op.TargetCloseDate = opp["LifeCycle"]["TargetCloseDate"]
            op.Title = self.get_opportunity(op.Id)["Project"]["Title"]
            rv.append(op)
        return sorted(rv, key=lambda r: r.TargetCloseDate)

    def get_opportunity(self, o_id):
        r = self._client.get_opportunity(
            Catalog=self.CATALOG,
            Identifier=o_id,
        )
        return r

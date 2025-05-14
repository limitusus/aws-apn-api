from collections import UserDict


class Opportunity(UserDict):
    def __repr__(self):
        return f"<Title:{self.Title} Stage:{self.Stage} Client:{self.ClientName} TargetCloseDate:{self.TargetCloseDate}>"

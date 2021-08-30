from libqtile import qtile
from libqtile.widget import base
from libqtile.widget.generic_poll_text import GenPollUrl
from libqtile.log_utils import logger

class SolarEdge(GenPollUrl):
    defaults = [
            ('apiKey', "", 'Soloar Edge ApiKey'),
            ('siteID', "", 'Soloar Edge Site ID'),
            ('positiveColour', "00ff00", 'Display colour when energy is delivered to grid'),
            ('negativeColour', "ff0000", 'Display colour when energy is drawn from grid'),
    ]

    @property
    def url(self):
        return "https://monitoringapi.solaredge.com/site/{siteid}/currentPowerFlow?api_key={apikey}".format(siteid=self.siteID, apikey=self.apiKey)

    def __init__(self, **config):
        GenPollUrl.__init__(self, **config)
        self.add_defaults(SolarEdge.defaults)

    def parse(self, body):
        myData = body['siteCurrentPowerFlow']
        Load = myData['LOAD']['currentPower']
        Grid = myData['GRID']['currentPower']
        PV = myData['PV']['currentPower']
        Overall = PV - Load
        if Overall < 0:
           self.layout.colour = self.negativeColour
        else:
            self.layout.colour = self.positiveColou

        return "PV:{pv} Load:{load} Grid:{grid} Overall:{overall}".format(pv=PV, load=Load, grid=Grid, overall=PV-Load)